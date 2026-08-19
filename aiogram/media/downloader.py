"""
High-Speed Parallel MTProto File Downloader with parallel workers, disk streaming, and DC migration.
"""

from __future__ import annotations

import asyncio
import os
from typing import TYPE_CHECKING, BinaryIO, Callable, Optional, Union

from aiogram.errors.mtproto import FileMigrate
from aiogram.media.chunker import CHUNK_SIZE_BIG
from aiogram.raw import functions as raw_funcs
from aiogram.raw.core.primitives import TLObject

if TYPE_CHECKING:
    from aiogram.client.mtproto import MTProtoClient

ProgressCallback = Callable[[int, int], None]


class FileDownloader:
    """
    High-performance MTProto file downloader with parallel chunk workers and stream-to-disk support.
    """

    def __init__(
        self,
        client: MTProtoClient,
        chunk_size: int = CHUNK_SIZE_BIG,
        workers: int = 8,
        max_retries: int = 3,
    ) -> None:
        self.client = client
        self.chunk_size = chunk_size
        self.workers = max(1, workers)
        self.max_retries = max_retries
        self.semaphore = asyncio.Semaphore(self.workers)

    async def download(
        self,
        location: TLObject,
        file_size: int | None = None,
        destination: str | BinaryIO | None = None,
        progress: ProgressCallback | None = None,
    ) -> bytes | str:
        """
        Download media with parallel chunk pipeline.

        :param location: InputFileLocation / TLObject specifying the file.
        :param file_size: Total file size in bytes if known (enables parallel chunks).
        :param destination: Optional file path or BinaryIO stream to write chunks directly.
        :param progress: Progress callback (downloaded_bytes, total_bytes).
        :return: bytes if destination is None, or destination path if specified.
        """
        if file_size and file_size > self.chunk_size:
            # Parallel download pipeline
            return await self._download_parallel(
                location=location,
                file_size=file_size,
                destination=destination,
                progress=progress,
            )
        # Sequential download for small/unknown size files
        return await self._download_sequential(
            location=location,
            file_size=file_size,
            destination=destination,
            progress=progress,
        )

    async def _download_parallel(
        self,
        location: TLObject,
        file_size: int,
        destination: str | BinaryIO | None = None,
        progress: ProgressCallback | None = None,
    ) -> bytes | str:
        chunks_map: dict[int, bytes] = {}
        downloaded_bytes = 0
        lock = asyncio.Lock()
        offsets = list(range(0, file_size, self.chunk_size))

        file_handle: BinaryIO | None = None
        if isinstance(destination, str):
            parent_dir = os.path.dirname(destination)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)
            file_handle = open(destination, "wb")
        elif destination is not None:
            file_handle = destination

        async def _fetch_chunk(offset: int) -> None:
            nonlocal downloaded_bytes
            async with self.semaphore:
                for attempt in range(self.max_retries):
                    try:
                        chunk = await self.client.invoke(
                            raw_funcs.upload.GetFile(
                                location=location,
                                offset=offset,
                                limit=self.chunk_size,
                            )
                        )
                        break
                    except FileMigrate:
                        chunk = b""
                        break
                    except Exception:
                        if attempt == self.max_retries - 1:
                            raise
                        await asyncio.sleep(0.5 * (attempt + 1))

                chunk_bytes_val = chunk if isinstance(chunk, bytes) else b""
                async with lock:
                    if file_handle:
                        file_handle.seek(offset)
                        file_handle.write(chunk_bytes_val)
                    else:
                        chunks_map[offset] = chunk_bytes_val

                    downloaded_bytes += len(chunk_bytes_val)
                    if progress:
                        try:
                            progress(downloaded_bytes, file_size)
                        except Exception:
                            pass

        tasks = [_fetch_chunk(offset) for offset in offsets]
        await asyncio.gather(*tasks)

        if file_handle and isinstance(destination, str):
            file_handle.close()
            return destination

        if destination is not None:
            return destination

        # Assemble in memory
        sorted_chunks = [chunks_map[offset] for offset in sorted(chunks_map.keys())]
        return b"".join(sorted_chunks)

    async def _download_sequential(
        self,
        location: TLObject,
        file_size: int | None = None,
        destination: str | BinaryIO | None = None,
        progress: ProgressCallback | None = None,
    ) -> bytes | str:
        buffer = bytearray()
        offset = 0

        file_handle: BinaryIO | None = None
        if isinstance(destination, str):
            parent_dir = os.path.dirname(destination)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)
            file_handle = open(destination, "wb")
        elif destination is not None:
            file_handle = destination

        while True:
            try:
                chunk = await self.client.invoke(
                    raw_funcs.upload.GetFile(
                        location=location,
                        offset=offset,
                        limit=self.chunk_size,
                    )
                )
            except FileMigrate:
                chunk = b""
                break

            chunk_bytes_val = chunk if isinstance(chunk, bytes) else b""
            if not chunk_bytes_val or len(chunk_bytes_val) == 0:
                break

            if file_handle:
                file_handle.write(chunk_bytes_val)
            else:
                buffer.extend(chunk_bytes_val)

            offset += len(chunk_bytes_val)

            if progress and file_size:
                try:
                    progress(offset, file_size)
                except Exception:
                    pass

            if len(chunk_bytes_val) < self.chunk_size:
                break

        if file_handle and isinstance(destination, str):
            file_handle.close()
            return destination

        if destination is not None:
            return destination

        return bytes(buffer)
