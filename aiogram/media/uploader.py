"""
High-Speed Parallel MTProto File Uploader with chunk retries, bounded memory,
and progress tracking.
"""

from __future__ import annotations

import asyncio
import contextlib
import inspect
import math
import os
import random
from collections.abc import Callable, Generator
from typing import TYPE_CHECKING, Any, BinaryIO

import aiofiles

from aiogram.media.chunker import (
    BIG_FILE_THRESHOLD,
    get_chunk_size,
)
from aiogram.raw import functions as raw_funcs
from aiogram.raw import types as raw_types

if TYPE_CHECKING:
    from aiogram.client.mtproto import MTProtoClient

ProgressCallback = Callable[[int, int], None]

# Telegram's practical maximum per SaveFilePart / SaveBigFilePart call is 512 KiB.
MAX_PART_SIZE = 512 * 1024


async def _stream_file_chunks(
    source: str | bytes | BinaryIO,
    chunk_size: int,
    queue: asyncio.Queue[tuple[int, bytes] | None],
) -> None:
    """
    Stream ``(part_index, chunk_bytes)`` into queue asynchronously without blocking the event loop.
    Supports file paths, raw bytes, and file-like objects with safe task cancellation handling.
    """
    try:
        if isinstance(source, str):
            with open(source, "rb") as f:
                idx = 0
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    await queue.put((idx, chunk))
                    idx += 1
        elif isinstance(source, bytes):
            for idx, offset in enumerate(range(0, len(source), chunk_size)):
                await queue.put((idx, source[offset : offset + chunk_size]))
        else:
            idx = 0
            while True:
                chunk = source.read(chunk_size)
                if not chunk:
                    break
                await queue.put((idx, chunk))
                idx += 1
    except (asyncio.CancelledError, GeneratorExit):
        return


class FileUploader:
    """
    High-performance MTProto file uploader with parallel chunk transfers.
    """

    def __init__(self, client: MTProtoClient, workers: int = 8, max_retries: int = 3) -> None:
        self.client = client
        self.workers = max(1, workers)
        self.max_retries = max_retries
        self.semaphore = asyncio.Semaphore(self.workers)

    async def upload(
        self,
        source: bytes | BinaryIO | str,
        file_name: str | None = None,
        progress: ProgressCallback | None = None,
    ) -> raw_types.InputFile | raw_types.InputFileBig:
        """
        Upload file/bytes to Telegram MTProto with parallel workers and chunk retries.

        :param source: bytes, file-like object, or file path.
        :param file_name: Optional file name.
        :param progress: Progress callback (uploaded_bytes, total_bytes).
        :return: InputFile or InputFileBig instance.
        """
        file_id = random.getrandbits(63)

        if isinstance(source, str):
            # File path on disk – get size without reading into RAM
            if file_name is None:
                file_name = os.path.basename(source)
            file_size = os.path.getsize(source)
        elif isinstance(source, bytes):
            file_size = len(source)
            if file_name is None:
                file_name = "file.bin"
        else:
            # File-like object: seek to end to measure, then rewind
            pos = source.tell()
            source.seek(0, 2)
            file_size = source.tell() - pos
            source.seek(pos)
            if file_name is None:
                file_name = getattr(source, "name", "file.bin")

        max_allowed = getattr(self.client, "max_file_size", 2000 * 1024 * 1024)
        if not isinstance(max_allowed, int):
            max_allowed = 2000 * 1024 * 1024

        if file_size > max_allowed:
            is_prem = getattr(self.client, "is_premium", False)
            account_desc = (
                "Telegram Premium User session" if not is_prem else "Telegram's 4GB ceiling"
            )
            msg = (
                f"File size {file_size / (1024 * 1024):.2f}MB exceeds maximum permitted limit "
                f"({max_allowed / (1024 * 1024):.0f}MB). Uploading files >2GB requires a {account_desc}."
            )
            raise ValueError(msg)

        chunk_size = min(get_chunk_size(file_size), MAX_PART_SIZE)
        total_parts = max(1, math.ceil(file_size / chunk_size))
        is_big = file_size > BIG_FILE_THRESHOLD

        import time

        uploaded_bytes = 0
        lock = asyncio.Lock()
        queue: asyncio.Queue[tuple[int, bytes] | None] = asyncio.Queue(maxsize=self.workers * 2)

        # Determine correct home Data Center for upload
        target_dc = getattr(self.client, "dc_id", 2)
        if hasattr(self.client, "dc_manager") and getattr(self.client, "dc_manager", None):
            target_dc = self.client.dc_manager.main_dc_id
        elif hasattr(self.client, "session_storage") and self.client.session_storage:
            load_fn = getattr(self.client.session_storage, "load", None)
            if callable(load_fn):
                res = load_fn()
                session_data = await res if inspect.isawaitable(res) else res
                if session_data and getattr(session_data, "dc_id", None):
                    target_dc = session_data.dc_id

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

        async def _resolve_media_client(dc: int, worker_id: int) -> Any:
            if hasattr(self.client, "get_media_client"):
                try:
                    res = self.client.get_media_client(
                        dc, worker_idx=worker_id, pool_size=self.workers
                    )
                    if asyncio.iscoroutine(res) or hasattr(res, "__await__"):
                        resolved = await res
                        if resolved is not None:
                            return resolved
                    elif res is not None:
                        return res
                except Exception:
                    pass
            return self.client

        async def _worker(worker_id: int) -> None:
            nonlocal uploaded_bytes, target_dc
            upload_client = await _resolve_media_client(target_dc, worker_id)

            while True:
                item = await queue.get()
                if item is None:
                    queue.task_done()
                    break

                part_index, part_bytes = item
                try:
                    for attempt in range(self.max_retries):
                        try:
                            if is_big:
                                await upload_client.invoke(
                                    raw_funcs.upload.SaveBigFilePart(
                                        file_id=file_id,
                                        file_part=part_index,
                                        file_total_parts=total_parts,
                                        bytes=part_bytes,
                                    )
                                )
                            else:
                                await upload_client.invoke(
                                    raw_funcs.upload.SaveFilePart(
                                        file_id=file_id,
                                        file_part=part_index,
                                        bytes=part_bytes,
                                    )
                                )
                            break
                        except Exception as exc:
                            # Handle FloodWait automatically
                            from aiogram.errors.mtproto import FileMigrate, FloodWait, UserMigrate

                            if isinstance(exc, FloodWait):
                                await asyncio.sleep(exc.value + 0.2)
                                continue

                            # Handle DC migration if returned during upload
                            if isinstance(exc, (UserMigrate, FileMigrate)):
                                new_dc = getattr(exc, "new_dc", getattr(exc, "dc_id", target_dc))
                                target_dc = new_dc
                                upload_client = await _resolve_media_client(target_dc, worker_id)
                                continue
                            if attempt == self.max_retries - 1:
                                raise
                            await asyncio.sleep(0.3 * (attempt + 1))
                finally:
                    queue.task_done()

                async with lock:
                    uploaded_bytes += len(part_bytes)
                    _dispatch_progress(uploaded_bytes, file_size)

        # Spawn persistent upload workers
        worker_tasks = [asyncio.create_task(_worker(w_id)) for w_id in range(self.workers)]
        producer_task = asyncio.create_task(_stream_file_chunks(source, chunk_size, queue))

        try:
            # Wait for producer to finish feeding chunks and queue to be completely processed
            await producer_task
            await queue.join()
        except BaseException:
            producer_task.cancel()
            for t in worker_tasks:
                t.cancel()
            raise
        finally:
            # Signal workers to exit
            for _ in range(self.workers):
                await queue.put(None)
            await asyncio.gather(*worker_tasks, return_exceptions=True)
            if progress_task and not progress_task.done():
                with contextlib.suppress(Exception):
                    await progress_task

        if is_big:
            return raw_types.InputFileBig(
                id=file_id, parts=total_parts, name=file_name or "file.bin"
            )
        return raw_types.InputFile(id=file_id, parts=total_parts, name=file_name or "file.bin")
