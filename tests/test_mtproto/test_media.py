"""
Tests for high-speed parallel MTProto media uploader, downloader, and chunker.
"""

import asyncio
import os
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiogram.media.chunker import (
    BIG_FILE_THRESHOLD,
    CHUNK_SIZE_BIG,
    CHUNK_SIZE_SMALL,
    chunk_bytes,
    get_chunk_size,
)
from aiogram.media.downloader import FileDownloader
from aiogram.media.uploader import FileUploader
from aiogram.raw.core.primitives import TLObject
from aiogram.raw.types import InputFile, InputFileBig


def test_chunker_sizes_and_partitioning() -> None:
    assert get_chunk_size(1024 * 1024) == CHUNK_SIZE_SMALL
    assert get_chunk_size(15 * 1024 * 1024) == CHUNK_SIZE_BIG

    sample_data = b"0123456789" * 100  # 1000 bytes
    chunks = list(chunk_bytes(sample_data, 250))
    assert len(chunks) == 4
    assert chunks[0][0] == 0
    assert len(chunks[0][1]) == 250
    assert chunks[3][0] == 3


@pytest.mark.asyncio
async def test_file_uploader_small_and_big() -> None:
    mock_client = MagicMock()
    mock_client.invoke = AsyncMock(return_value=True)

    uploader = FileUploader(client=mock_client, workers=4)

    # 1. Small file upload
    small_data = b"small_file_content" * 100
    progress_updates: list[tuple[int, int]] = []

    def on_progress(current: int, total: int) -> None:
        progress_updates.append((current, total))

    result = await uploader.upload(
        source=small_data,
        file_name="small.txt",
        progress=on_progress,
    )
    assert isinstance(result, InputFile)
    assert result.name == "small.txt"
    assert result.parts == 1
    assert len(progress_updates) > 0
    assert progress_updates[-1][0] == len(small_data)

    # 2. Big file upload (> 10 MB)
    big_data = b"X" * (11 * 1024 * 1024)
    result_big = await uploader.upload(source=big_data, file_name="big.iso")
    assert isinstance(result_big, InputFileBig)
    assert result_big.name == "big.iso"
    assert result_big.parts == 22


@pytest.mark.asyncio
async def test_file_downloader_parallel_and_disk_stream(tmp_path: pytest.TempPathFactory) -> None:
    chunk1 = b"Part 1 Data " * 100
    chunk2 = b"Part 2 Data " * 100
    total_data = chunk1 + chunk2

    mock_client = MagicMock()

    async def mock_invoke(req: TLObject) -> bytes:
        offset = getattr(req, "offset", 0)
        limit = getattr(req, "limit", 0)
        return total_data[offset : offset + limit]

    mock_client.invoke = AsyncMock(side_effect=mock_invoke)

    downloader = FileDownloader(client=mock_client, chunk_size=len(chunk1), workers=2)

    dummy_location = MagicMock(spec=TLObject)

    # 1. Download to memory (parallel)
    downloaded_bytes = await downloader.download(
        location=dummy_location,
        file_size=len(total_data),
    )
    assert downloaded_bytes == total_data

    # 2. Stream to disk
    out_file = str(tmp_path / "downloaded_file.bin")
    out_path = await downloader.download(
        location=dummy_location,
        file_size=len(total_data),
        destination=out_file,
    )
    assert out_path == out_file
    with open(out_file, "rb") as f:
        assert f.read() == total_data
