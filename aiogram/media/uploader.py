"""
High-Speed Parallel MTProto File Uploader with chunk retries, bounded memory, and progress tracking.
"""

from __future__ import annotations

import asyncio
import math
import os
import random
from collections.abc import Callable, Generator
from typing import TYPE_CHECKING, BinaryIO

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


def _iter_file_chunks(
    source: str | bytes | BinaryIO,
    chunk_size: int,
) -> Generator[tuple[int, bytes], None, None]:
    """
    Yield ``(part_index, chunk_bytes)`` without loading the entire file into RAM.
    Supports file paths, raw bytes, and file-like objects.
    """
    if isinstance(source, str):
        with open(source, "rb") as f:
            idx = 0
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield idx, chunk
                idx += 1
    elif isinstance(source, bytes):
        for idx, offset in enumerate(range(0, len(source), chunk_size)):
            yield idx, source[offset : offset + chunk_size]
    else:
        idx = 0
        while True:
            chunk = source.read(chunk_size)
            if not chunk:
                break
            yield idx, chunk
            idx += 1


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

        chunk_size = min(get_chunk_size(file_size), MAX_PART_SIZE)
        total_parts = max(1, math.ceil(file_size / chunk_size))
        is_big = file_size > BIG_FILE_THRESHOLD

        uploaded_bytes = 0
        lock = asyncio.Lock()
        queue: asyncio.Queue[tuple[int, bytes] | None] = asyncio.Queue(maxsize=self.workers * 2)

        async def _worker() -> None:
            nonlocal uploaded_bytes
            while True:
                item = await queue.get()
                if item is None:
                    queue.task_done()
                    break

                part_index, part_bytes = item
                for attempt in range(self.max_retries):
                    try:
                        if is_big:
                            await self.client.invoke(
                                raw_funcs.upload.SaveBigFilePart(
                                    file_id=file_id,
                                    file_part=part_index,
                                    file_total_parts=total_parts,
                                    bytes=part_bytes,
                                )
                            )
                        else:
                            await self.client.invoke(
                                raw_funcs.upload.SaveFilePart(
                                    file_id=file_id,
                                    file_part=part_index,
                                    bytes=part_bytes,
                                )
                            )
                        break
                    except Exception:
                        if attempt == self.max_retries - 1:
                            queue.task_done()
                            raise
                        await asyncio.sleep(0.3 * (attempt + 1))

                async with lock:
                    uploaded_bytes += len(part_bytes)
                    if progress:
                        try:
                            progress(uploaded_bytes, file_size)
                        except Exception:
                            pass
                queue.task_done()

        # Spawn persistent upload workers
        worker_tasks = [asyncio.create_task(_worker()) for _ in range(self.workers)]

        try:
            # Stream chunks from disk/source into queue with bounded memory
            for part_idx, part_data in _iter_file_chunks(source, chunk_size):
                await queue.put((part_idx, part_data))

            # Wait for all chunks to be processed
            await queue.join()
        finally:
            # Signal workers to exit
            for _ in range(self.workers):
                await queue.put(None)
            await asyncio.gather(*worker_tasks, return_exceptions=True)

        if is_big:
            return raw_types.InputFileBig(
                id=file_id, parts=total_parts, name=file_name or "file.bin"
            )
        return raw_types.InputFile(id=file_id, parts=total_parts, name=file_name or "file.bin")
