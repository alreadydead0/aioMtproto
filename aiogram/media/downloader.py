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
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any, BinaryIO

from aiogram.errors.mtproto import (
    AuthKeyNotFound,
    AuthKeyUnregistered,
    FileMigrate,
    FileReferenceExpired,
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
        workers: int = 4,
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

        dc_client = self.client
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
        active_client = dc_client or self.client
        offsets = list(range(0, file_size, self.chunk_size))

        chunks_map: dict[int, bytes] = {}
        downloaded_bytes = 0
        progress_lock = asyncio.Lock()
        semaphore = asyncio.Semaphore(self.workers)

        current_location: TLObject = location
        refreshed_count = 0
        refresh_lock = asyncio.Lock()

        file_handle: BinaryIO | None = None
        if isinstance(destination, str):
            parent_dir = os.path.dirname(destination)
            if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)
            file_handle = open(destination, "wb")  # noqa: SIM115
        elif destination is not None:
            file_handle = destination

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

        async def _fetch_chunk(offset: int) -> None:
            nonlocal downloaded_bytes
            async with semaphore:
                chunk_client = active_client
                chunk_data = b""
                attempt = 0
                while attempt < self.max_retries:
                    loc = current_location
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
                        target_dc = getattr(e, "new_dc", getattr(e, "dc_id", 2))
                        chunk_client = await self.client.get_media_client(target_dc)
                        attempt += 1
                        continue
                    except (AuthKeyUnregistered, AuthKeyNotFound):
                        if hasattr(chunk_client, "dc_id"):
                            chunk_client = await self.client.get_media_client(chunk_client.dc_id)
                        attempt += 1
                        continue
                    except Exception:
                        attempt += 1
                        if attempt >= self.max_retries:
                            raise
                        await asyncio.sleep(min(0.5 * attempt, 3.0))

                async with progress_lock:
                    if file_handle:
                        file_handle.seek(offset)
                        file_handle.write(chunk_data)
                    else:
                        chunks_map[offset] = chunk_data
                    downloaded_bytes += len(chunk_data)
                    if progress:
                        with contextlib.suppress(Exception):
                            progress(downloaded_bytes, file_size)

        try:
            await asyncio.gather(*(_fetch_chunk(off) for off in offsets))
        finally:
            if file_handle and isinstance(destination, str):
                file_handle.close()

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

        file_handle: BinaryIO | None = None
        if isinstance(destination, str):
            parent_dir = os.path.dirname(destination)
            if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)
            file_handle = open(destination, "wb")  # noqa: SIM115
        elif destination is not None:
            file_handle = destination

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
                    except Exception:
                        attempt += 1
                        if attempt >= self.max_retries:
                            raise
                        await asyncio.sleep(min(0.5 * attempt, 3.0))

                if not chunk_data:
                    break

                if file_handle:
                    file_handle.write(chunk_data)
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
            if file_handle and isinstance(destination, str):
                file_handle.close()

        if isinstance(destination, str):
            return destination
        if destination is not None:
            return destination

        return bytes(buffer)
