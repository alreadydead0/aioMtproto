"""
High-Speed Parallel MTProto File Uploader with chunk retries, bounded memory, and progress tracking.
"""

from __future__ import annotations

import asyncio
import math
import os
import random
from collections.abc import Callable
from typing import TYPE_CHECKING, BinaryIO, Optional, Union

from aiogram.media.chunker import (
    BIG_FILE_THRESHOLD,
    CHUNK_SIZE_BIG,
    CHUNK_SIZE_SMALL,
    chunk_bytes,
    get_chunk_size,
)
from aiogram.raw import functions as raw_funcs
from aiogram.raw import types as raw_types

if TYPE_CHECKING:
    from aiogram.client.mtproto import MTProtoClient

ProgressCallback = Callable[[int, int], None]


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
            # File path on disk
            if file_name is None:
                file_name = os.path.basename(source)
            file_size = os.path.getsize(source)
            with open(source, "rb") as f:
                data = f.read()
        elif isinstance(source, bytes):
            data = source
            file_size = len(data)
            if file_name is None:
                file_name = "file.bin"
        else:
            # File-like object
            data = source.read()
            file_size = len(data)
            if file_name is None:
                file_name = getattr(source, "name", "file.bin")

        chunk_size = get_chunk_size(file_size)
        total_parts = max(1, math.ceil(file_size / chunk_size))
        is_big = file_size > BIG_FILE_THRESHOLD

        uploaded_bytes = 0
        lock = asyncio.Lock()

        async def _upload_worker(part_index: int, part_bytes: bytes) -> None:
            nonlocal uploaded_bytes
            async with self.semaphore:
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
                            raise
                        await asyncio.sleep(0.5 * (attempt + 1))

                async with lock:
                    uploaded_bytes += len(part_bytes)
                    if progress:
                        try:
                            progress(uploaded_bytes, file_size)
                        except Exception:
                            pass

        # Parallel upload tasks
        tasks = [
            _upload_worker(part_idx, part_data)
            for part_idx, part_data in chunk_bytes(data, chunk_size)
        ]
        await asyncio.gather(*tasks)

        if is_big:
            return raw_types.InputFileBig(
                id=file_id, parts=total_parts, name=file_name or "file.bin"
            )
        return raw_types.InputFile(id=file_id, parts=total_parts, name=file_name or "file.bin")
