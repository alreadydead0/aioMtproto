"""
High-Speed Parallel MTProto File Downloader.

Design:
- Uses DC-specific media clients so parallel chunk workers never block each other.
- upload.GetFile returns an upload.File TL object; _extract_bytes pulls .bytes.
- Supports coordinated location refresh on FILE_REFERENCE_EXPIRED.
- Falls back to sequential mode for small/unknown-size files.
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
import os
import re
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any, BinaryIO

import aiofiles

from aiogram.errors.mtproto import (
    AuthKeyNotFound,
    AuthKeyUnregistered,
    FileMigrate,
    FileReferenceExpired,
    FloodWait,
)
from aiogram.raw import functions as raw_funcs
from aiogram.raw.core.primitives import TLObject

if TYPE_CHECKING:
    from aiogram.client.mtproto import MTProtoClient

logger = logging.getLogger("aiogram.media.downloader")

ProgressCallback = Callable[[int, int], None]
RefreshCallback = Callable[[Any], Awaitable[Any] | Any]

# Telegram's practical maximum for a single GetFile call is 512 KiB.
MAX_CHUNK_SIZE = 512 * 1024


def _extract_bytes(chunk: Any) -> bytes:
    """
    upload.GetFile returns an upload.File TL object with a .bytes attribute.
    Handle both the TL object and a raw bytes fallback.
    """
    if isinstance(chunk, bytes):
        return chunk
    raw = getattr(chunk, "bytes", None)
    if raw is not None and isinstance(raw, bytes):
        return raw
    return b""


class FileDownloader:
    """
    High-performance MTProto file downloader with parallel chunk workers.
    """

    def __init__(
        self,
        client: MTProtoClient,
        chunk_size: int = MAX_CHUNK_SIZE,
        workers: int = 8,
        max_retries: int = 5,
        max_file_reference_refreshes: int = 1,
    ) -> None:
        self.client = client
        self.chunk_size = min(chunk_size, MAX_CHUNK_SIZE)
        self.workers = max(1, workers)
        self.max_retries = max_retries
        self.max_file_reference_refreshes = max_file_reference_refreshes

    async def download(
        self,
        location: Any,
        file_size: int | None = None,
        destination: str | BinaryIO | None = None,
        progress: ProgressCallback | None = None,
        refresh_location: RefreshCallback | None = None,
    ) -> bytes | str | BinaryIO:
        """
        Download a file from Telegram.

        :param location: InputFileLocation TLObject or Bot-API file_id string/object.
        :param file_size: Total bytes (enables parallel mode when > chunk_size).
        :param destination: File path or open BinaryIO to stream into; None returns bytes.
        :param progress: Callback (downloaded_bytes, total_bytes) after each chunk.
        :param refresh_location: Async/sync callback to obtain fresh location.
        :return: bytes if destination is None, else destination path/object.
        """
        target_dc_id = self.client.dc_id

        # Resolve Bot-API file_id → InputFileLocation
        if not isinstance(location, TLObject):
            from aiogram.media.file_id import decode_file_id, file_id_to_input_location

            file_id_str = getattr(location, "file_id", str(location))
            decoded = decode_file_id(file_id_str)
            if decoded and decoded.dc_id:
                target_dc_id = decoded.dc_id
            location = file_id_to_input_location(location)

        dc_client: Any = self.client
        if hasattr(self.client, "get_media_client"):
            res = self.client.get_media_client(target_dc_id)
            if asyncio.iscoroutine(res) or hasattr(res, "__await__"):
                dc_client = await res
            elif res is not None:
                dc_client = res

        if file_size and file_size > self.chunk_size:
            return await self._download_parallel(
                location=location,
                file_size=file_size,
                destination=destination,
                progress=progress,
                dc_client=dc_client,
                refresh_location=refresh_location,
            )

        return await self._download_sequential(
            location=location,
            file_size=file_size,
            destination=destination,
            progress=progress,
            dc_client=dc_client,
            refresh_location=refresh_location,
        )

    # ------------------------------------------------------------------
    # Parallel download (large files with known size)
    # ------------------------------------------------------------------

    async def _download_parallel(
        self,
        location: TLObject,
        file_size: int,
        destination: str | BinaryIO | None = None,
        progress: ProgressCallback | None = None,
        dc_client: Any = None,
        refresh_location: RefreshCallback | None = None,
    ) -> bytes | str | BinaryIO:
        import inspect
        import time

        active_client = dc_client or self.client
        offsets = list(range(0, file_size, self.chunk_size))

        chunks_map: dict[int, bytes] = {}
        downloaded_bytes = 0
        file_lock = asyncio.Lock()
        state_lock = asyncio.Lock()

        current_location: TLObject = location
        refreshed_count = 0
        refresh_lock = asyncio.Lock()

        last_progress_time = 0.0
        progress_task: asyncio.Task[Any] | None = None

        def _dispatch_progress(curr: int, total: int) -> None:
            nonlocal last_progress_time, progress_task
            if not progress:
                return
            now = time.monotonic()
            if now - last_progress_time >= 1.0 or curr >= total:
                last_progress_time = now
                if progress_task is None or progress_task.done():

                    async def _run_cb() -> None:
                        try:
                            res = progress(curr, total)
                            if inspect.isawaitable(res):
                                await res
                        except Exception:
                            pass

                    progress_task = asyncio.create_task(_run_cb())

        sync_file: BinaryIO | None = None
        owns_file = False
        if isinstance(destination, str):
            parent_dir = os.path.dirname(destination)
            base_name = os.path.basename(destination)
            base_name = re.sub(r'[\r\n\t\x00-\x1f*?:"<>|]', " ", base_name).strip()
            destination = os.path.join(parent_dir, base_name) if parent_dir else base_name
            if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)
            sync_file = open(destination, "wb")
            owns_file = True
        elif destination is not None:
            sync_file = destination

        async def _handle_file_reference_expired(expired_loc: TLObject) -> TLObject:
            nonlocal current_location, refreshed_count
            if refresh_location is None:
                raise FileReferenceExpired(400, "FILE_REFERENCE_EXPIRED")

            async with refresh_lock:
                # If another worker already refreshed the location, reuse it immediately
                if current_location is not expired_loc and current_location != expired_loc:
                    return current_location

                if refreshed_count >= self.max_file_reference_refreshes:
                    logger.warning("Max file reference refreshes exceeded (%d)", refreshed_count)
                    raise FileReferenceExpired(400, "FILE_REFERENCE_EXPIRED")

                logger.info("File reference expired. Calling refresh_location callback...")
                try:
                    res = refresh_location(current_location)
                    if asyncio.iscoroutine(res) or hasattr(res, "__await__"):
                        new_loc = await res
                    else:
                        new_loc = res
                except Exception as exc:
                    logger.error("refresh_location callback failed: %s", exc)
                    raise

                if not isinstance(new_loc, TLObject):
                    from aiogram.media.file_id import file_id_to_input_location

                    new_loc = file_id_to_input_location(new_loc)

                current_location = new_loc
                refreshed_count += 1
                logger.info("Media location successfully refreshed (count=%d)", refreshed_count)
                return current_location

        async def _resolve_media_client(target_dc: int, worker_id: int) -> Any:
            if hasattr(self.client, "get_media_client"):
                res = self.client.get_media_client(
                    target_dc, worker_idx=worker_id, pool_size=self.workers
                )
                if asyncio.iscoroutine(res) or hasattr(res, "__await__"):
                    resolved = await res
                    if resolved is not None:
                        return resolved
                elif res is not None:
                    return res
            return active_client

        offsets_queue: asyncio.Queue[int | None] = asyncio.Queue()
        for off in offsets:
            offsets_queue.put_nowait(off)

        dc_flood_until: dict[int, float] = {}
        dc_flood_lock = asyncio.Lock()

        async def _worker(worker_id: int) -> None:
            nonlocal downloaded_bytes
            target_dc = getattr(active_client, "dc_id", 2)
            chunk_client = await _resolve_media_client(target_dc, worker_id)

            while True:
                offset = await offsets_queue.get()
                if offset is None:
                    offsets_queue.task_done()
                    break

                try:
                    chunk_data = b""
                    attempt = 0
                    while attempt < self.max_retries:
                        loc = current_location
                        cur_dc = getattr(chunk_client, "dc_id", target_dc)

                        # Check if this DC is currently cooling down from a FloodWait
                        now = time.monotonic()
                        if cur_dc in dc_flood_until and now < dc_flood_until[cur_dc]:
                            pause = dc_flood_until[cur_dc] - now
                            if pause > 0:
                                await asyncio.sleep(pause)

                        try:
                            result = await chunk_client.invoke(
                                raw_funcs.upload.GetFile(
                                    location=loc,
                                    offset=offset,
                                    limit=self.chunk_size,
                                )
                            )
                            chunk_data = _extract_bytes(result)
                            break
                        except FileReferenceExpired:
                            if refresh_location is None:
                                raise
                            # Coordinate refresh across parallel workers
                            await _handle_file_reference_expired(loc)
                            continue
                        except FileMigrate as e:
                            new_dc = getattr(e, "new_dc", getattr(e, "dc_id", 2))
                            chunk_client = await _resolve_media_client(new_dc, worker_id)
                            attempt += 1
                            continue
                        except (AuthKeyUnregistered, AuthKeyNotFound):
                            cur_dc = getattr(chunk_client, "dc_id", target_dc)
                            chunk_client = await _resolve_media_client(cur_dc, worker_id)
                            attempt += 1
                            continue
                        except FloodWait as e:
                            wait_time = float(max(e.value, 1)) + 0.2
                            async with dc_flood_lock:
                                dc_flood_until[cur_dc] = max(
                                    dc_flood_until.get(cur_dc, 0.0), time.monotonic() + wait_time
                                )
                            logger.debug(
                                "FloodWait received on DC %d. Coordinated pause for %.1fs...",
                                cur_dc,
                                wait_time,
                            )
                            await asyncio.sleep(wait_time)
                            continue
                        except Exception as e:
                            attempt += 1
                            if attempt >= self.max_retries:
                                logger.error(
                                    "Chunk offset %d failed after %d attempts: %s",
                                    offset,
                                    attempt,
                                    e,
                                )
                                raise
                            await asyncio.sleep(0.05)

                    if sync_file is not None:
                        async with file_lock:
                            sync_file.seek(offset)
                            sync_file.write(chunk_data)
                    else:
                        async with file_lock:
                            chunks_map[offset] = chunk_data

                    async with state_lock:
                        downloaded_bytes += len(chunk_data)
                        _dispatch_progress(downloaded_bytes, file_size)

                    # Smooth micro-pacing per worker
                    await asyncio.sleep(0.02)
                finally:
                    offsets_queue.task_done()

        worker_tasks = [asyncio.create_task(_worker(w_id)) for w_id in range(self.workers)]

        try:
            await offsets_queue.join()
        finally:
            for _ in range(self.workers):
                await offsets_queue.put(None)
            await asyncio.gather(*worker_tasks, return_exceptions=True)
            if sync_file is not None and owns_file:
                sync_file.close()
            if progress_task and not progress_task.done():
                with contextlib.suppress(Exception):
                    await progress_task

        if isinstance(destination, str):
            return destination
        if destination is not None:
            return destination

        return b"".join(chunks_map[off] for off in sorted(chunks_map))

    # ------------------------------------------------------------------
    # Sequential download (small / unknown-size files)
    # ------------------------------------------------------------------

    async def _download_sequential(
        self,
        location: TLObject,
        file_size: int | None = None,
        destination: str | BinaryIO | None = None,
        progress: ProgressCallback | None = None,
        dc_client: Any = None,
        refresh_location: RefreshCallback | None = None,
    ) -> bytes | str | BinaryIO:
        active_client = dc_client or self.client
        buffer = bytearray()
        downloaded_bytes = 0
        offset = 0

        current_location: TLObject = location
        refreshed_count = 0

        sync_file: BinaryIO | None = None
        owns_file = False
        if isinstance(destination, str):
            parent_dir = os.path.dirname(destination)
            base_name = os.path.basename(destination)
            base_name = re.sub(r'[\r\n\t\x00-\x1f*?:"<>|]', " ", base_name).strip()
            destination = os.path.join(parent_dir, base_name) if parent_dir else base_name
            if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)
            sync_file = open(destination, "wb")
            owns_file = True
        elif destination is not None:
            sync_file = destination

        async def _handle_file_reference_expired(expired_loc: TLObject) -> TLObject:
            nonlocal current_location, refreshed_count
            if refresh_location is None:
                raise FileReferenceExpired(400, "FILE_REFERENCE_EXPIRED")

            if refreshed_count >= self.max_file_reference_refreshes:
                logger.warning("Max file reference refreshes exceeded (%d)", refreshed_count)
                raise FileReferenceExpired(400, "FILE_REFERENCE_EXPIRED")

            logger.info("File reference expired. Calling refresh_location callback...")
            try:
                res = refresh_location(current_location)
                if asyncio.iscoroutine(res) or hasattr(res, "__await__"):
                    new_loc = await res
                else:
                    new_loc = res
            except Exception as exc:
                logger.error("refresh_location callback failed: %s", exc)
                raise

            if not isinstance(new_loc, TLObject):
                from aiogram.media.file_id import file_id_to_input_location

                new_loc = file_id_to_input_location(new_loc)

            current_location = new_loc
            refreshed_count += 1
            logger.info("Media location successfully refreshed (count=%d)", refreshed_count)
            return current_location

        try:
            while True:
                chunk_data = b""
                attempt = 0
                while attempt < self.max_retries:
                    loc = current_location
                    try:
                        result = await active_client.invoke(
                            raw_funcs.upload.GetFile(
                                location=loc,
                                offset=offset,
                                limit=self.chunk_size,
                            )
                        )
                        chunk_data = _extract_bytes(result)
                        break
                    except FileReferenceExpired:
                        if refresh_location is None:
                            raise
                        await _handle_file_reference_expired(loc)
                        continue
                    except FileMigrate as e:
                        target_dc = getattr(e, "new_dc", getattr(e, "dc_id", 2))
                        active_client = await self.client.get_media_client(target_dc)
                        attempt += 1
                        continue
                    except (AuthKeyUnregistered, AuthKeyNotFound):
                        if hasattr(active_client, "dc_id"):
                            active_client = await self.client.get_media_client(active_client.dc_id)
                        attempt += 1
                        continue
                    except FloodWait as e:
                        wait_time = float(max(e.value, 1)) + 0.2
                        logger.debug(
                            "FloodWait received for chunk offset %d. Waiting %.1f seconds...",
                            offset,
                            wait_time,
                        )
                        await asyncio.sleep(wait_time)
                        continue
                    except Exception:
                        attempt += 1
                        if attempt >= self.max_retries:
                            raise
                        await asyncio.sleep(0.05)

                if not chunk_data:
                    break

                if sync_file is not None:
                    sync_file.write(chunk_data)
                else:
                    buffer.extend(chunk_data)

                downloaded_bytes += len(chunk_data)
                offset += len(chunk_data)

                if progress and file_size:
                    with contextlib.suppress(Exception):
                        progress(downloaded_bytes, file_size)

                if len(chunk_data) < self.chunk_size:
                    # Last partial chunk → transfer complete
                    break
        finally:
            if sync_file is not None and owns_file:
                sync_file.close()

        if isinstance(destination, str):
            return destination
        if destination is not None:
            return destination

        return bytes(buffer)
