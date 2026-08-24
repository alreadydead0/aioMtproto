"""
Tests for high-speed parallel MTProto media uploader, downloader, and chunker.
"""

import asyncio
import base64
import os
import struct
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiogram.errors.mtproto import (
    AuthKeyNotFound,
    AuthKeyUnregistered,
    FileMigrate,
    FileReferenceExpired,
)
from aiogram.media.chunker import (
    BIG_FILE_THRESHOLD,
    CHUNK_SIZE_BIG,
    CHUNK_SIZE_SMALL,
    chunk_bytes,
    get_chunk_size,
)
from aiogram.media.downloader import FileDownloader
from aiogram.media.file_id import decode_file_id, file_id_to_input_location, rle_encode
from aiogram.media.uploader import FileUploader
from aiogram.raw.core.primitives import TLObject
from aiogram.raw.types import (
    InputDocumentFileLocation,
    InputFile,
    InputFileBig,
)


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
    mock_client.dc_id = 2
    mock_client.invoke = AsyncMock(side_effect=lambda req: True)
    mock_client.get_media_client = AsyncMock(side_effect=lambda *args, **kwargs: mock_client)

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
    mock_client.get_media_client = AsyncMock(return_value=mock_client)
    mock_client.dc_id = 2

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


# ==============================================================================
# Tests A through L: File ID decoding & FILE_REFERENCE_EXPIRED refresh handling
# ==============================================================================


def test_a_decode_file_id_with_file_reference() -> None:
    """Test A: Decode file_id with file_reference preserves all fields."""
    from aiogram.raw.core.primitives import write_bytes

    # Construct raw payload: type=3 (document) with file_reference flag, dc_id=4, ref=b"REF1", id=12345, access_hash=67890
    type_id = 3 | (1 << 24)
    raw = (
        struct.pack("<i", type_id)
        + struct.pack("<i", 4)
        + write_bytes(b"REF1")
        + struct.pack("<q", 12345)
        + struct.pack("<q", 67890)
    )
    encoded = base64.urlsafe_b64encode(rle_encode(raw)).decode().rstrip("=")

    decoded = decode_file_id(encoded)
    assert decoded is not None
    assert decoded.dc_id == 4
    assert decoded.id == 12345
    assert decoded.access_hash == 67890
    assert decoded.file_reference == b"REF1"

    loc = file_id_to_input_location(encoded)
    assert isinstance(loc, InputDocumentFileLocation)
    assert loc.id == 12345
    assert loc.access_hash == 67890
    assert loc.file_reference == b"REF1"


def test_b_decode_file_id_without_file_reference() -> None:
    """Test B: Decode file_id without file_reference returns b'' reference."""
    type_id = 3  # Document without ref flag
    raw = (
        struct.pack("<i", type_id)
        + struct.pack("<i", 5)
        + struct.pack("<q", 9999)
        + struct.pack("<q", 8888)
    )
    encoded = base64.urlsafe_b64encode(rle_encode(raw)).decode().rstrip("=")

    decoded = decode_file_id(encoded)
    assert decoded is not None
    assert decoded.dc_id == 5
    assert decoded.id == 9999
    assert decoded.access_hash == 8888
    assert decoded.file_reference == b""

    loc = file_id_to_input_location(encoded)
    assert loc.file_reference == b""


def test_c_invalid_dc_id_does_not_silently_become_dc2() -> None:
    """Test C: Invalid DC ID does not silently fallback to DC 2."""
    type_id = 3
    # Invalid DC ID: 99
    raw = (
        struct.pack("<i", type_id)
        + struct.pack("<i", 99)
        + struct.pack("<q", 100)
        + struct.pack("<q", 200)
    )
    encoded = base64.urlsafe_b64encode(rle_encode(raw)).decode().rstrip("=")

    decoded = decode_file_id(encoded)
    assert decoded is None

    with pytest.raises(ValueError, match="Invalid or unsupported Telegram file_id"):
        file_id_to_input_location(encoded)


@pytest.mark.asyncio
async def test_d_get_file_succeeds_normally() -> None:
    """Test D: GetFile succeeds normally."""
    mock_client = MagicMock()
    mock_client.invoke = AsyncMock(return_value=b"NORMAL_FILE_CONTENT")
    mock_client.get_media_client = AsyncMock(return_value=mock_client)
    mock_client.dc_id = 4

    downloader = FileDownloader(client=mock_client, chunk_size=1024)
    loc = InputDocumentFileLocation(id=1, access_hash=2, file_reference=b"REF")

    result = await downloader.download(location=loc)
    assert result == b"NORMAL_FILE_CONTENT"


@pytest.mark.asyncio
async def test_e_get_file_file_reference_expired_refresh_succeeds() -> None:
    """Test E: GetFile returns FILE_REFERENCE_EXPIRED -> refresh callback -> retry succeeds."""
    mock_client = MagicMock()
    mock_client.dc_id = 4
    mock_client.get_media_client = AsyncMock(return_value=mock_client)

    invoked_locations: list[Any] = []
    old_loc = InputDocumentFileLocation(id=1, access_hash=2, file_reference=b"OLD_REF")
    new_loc = InputDocumentFileLocation(id=1, access_hash=2, file_reference=b"FRESH_REF")

    async def mock_invoke(req: Any) -> bytes:
        loc = getattr(req, "location", None)
        invoked_locations.append(loc)
        if loc.file_reference == b"OLD_REF":
            raise FileReferenceExpired(400, "FILE_REFERENCE_EXPIRED")
        return b"FRESH_DOWNLOAD_BYTES"

    mock_client.invoke = AsyncMock(side_effect=mock_invoke)

    refresh_called = 0

    async def my_refresh(loc: TLObject) -> TLObject:
        nonlocal refresh_called
        refresh_called += 1
        assert loc.file_reference == b"OLD_REF"
        return new_loc

    downloader = FileDownloader(client=mock_client, chunk_size=1024)
    result = await downloader.download(
        location=old_loc,
        refresh_location=my_refresh,
    )

    assert result == b"FRESH_DOWNLOAD_BYTES"
    assert refresh_called == 1
    assert len(invoked_locations) == 2
    assert invoked_locations[0].file_reference == b"OLD_REF"
    assert invoked_locations[1].file_reference == b"FRESH_REF"


@pytest.mark.asyncio
async def test_f_refresh_callback_fails_propagates_exception() -> None:
    """Test F: Refresh callback itself fails -> exception propagates cleanly."""
    mock_client = MagicMock()
    mock_client.dc_id = 4
    mock_client.get_media_client = AsyncMock(return_value=mock_client)
    mock_client.invoke = AsyncMock(side_effect=FileReferenceExpired(400, "FILE_REFERENCE_EXPIRED"))

    async def failing_refresh(loc: TLObject) -> TLObject:
        raise RuntimeError("Message deleted from chat")

    downloader = FileDownloader(client=mock_client, chunk_size=1024)
    loc = InputDocumentFileLocation(id=1, access_hash=2, file_reference=b"EXPIRED")

    with pytest.raises(RuntimeError, match="Message deleted from chat"):
        await downloader.download(location=loc, refresh_location=failing_refresh)


@pytest.mark.asyncio
async def test_g_second_file_reference_expired_does_not_cause_infinite_loop() -> None:
    """Test G: Second FILE_REFERENCE_EXPIRED does not cause infinite refresh (bounded)."""
    mock_client = MagicMock()
    mock_client.dc_id = 4
    mock_client.get_media_client = AsyncMock(return_value=mock_client)
    # Server always returns FileReferenceExpired even after refresh
    mock_client.invoke = AsyncMock(side_effect=FileReferenceExpired(400, "FILE_REFERENCE_EXPIRED"))

    refresh_call_count = 0

    async def test_refresh(loc: TLObject) -> TLObject:
        nonlocal refresh_call_count
        refresh_call_count += 1
        return InputDocumentFileLocation(id=1, access_hash=2, file_reference=b"ANOTHER_REF")

    downloader = FileDownloader(
        client=mock_client, chunk_size=1024, max_file_reference_refreshes=1
    )
    loc = InputDocumentFileLocation(id=1, access_hash=2, file_reference=b"OLD")

    with pytest.raises(FileReferenceExpired):
        await downloader.download(location=loc, refresh_location=test_refresh)

    # Exactly 1 refresh attempted, not an infinite loop
    assert refresh_call_count == 1


@pytest.mark.asyncio
async def test_h_and_i_parallel_download_single_refresh_and_future_chunks() -> None:
    """Test H & I: Parallel download coordinates a single refresh operation and all subsequent chunks use fresh location."""
    chunk_size = 1000
    file_size = 4000  # 4 chunks
    mock_client = MagicMock()
    mock_client.dc_id = 4
    mock_client.get_media_client = AsyncMock(return_value=mock_client)

    old_loc = InputDocumentFileLocation(id=1, access_hash=2, file_reference=b"OLD")
    fresh_loc = InputDocumentFileLocation(id=1, access_hash=2, file_reference=b"FRESH")

    refresh_count = 0
    invoked_per_chunk: list[bytes] = []

    async def mock_invoke(req: Any) -> bytes:
        loc = getattr(req, "location", None)
        invoked_per_chunk.append(loc.file_reference)

        if loc.file_reference == b"OLD":
            # Simulate initial expired reference
            raise FileReferenceExpired(400, "FILE_REFERENCE_EXPIRED")
        return b"D" * chunk_size

    mock_client.invoke = AsyncMock(side_effect=mock_invoke)

    async def coordinated_refresh(loc: TLObject) -> TLObject:
        nonlocal refresh_count
        refresh_count += 1
        await asyncio.sleep(0.05)  # Simulate network latency of fetching new message
        return fresh_loc

    downloader = FileDownloader(client=mock_client, chunk_size=chunk_size, workers=4)
    result = await downloader.download(
        location=old_loc,
        file_size=file_size,
        refresh_location=coordinated_refresh,
    )

    assert len(result) == file_size
    # Exactly ONE refresh operation occurred despite 4 parallel workers
    assert refresh_count == 1
    # All successful chunk downloads used the FRESH location
    successful_invocations = [ref for ref in invoked_per_chunk if ref == b"FRESH"]
    assert len(successful_invocations) == 4


@pytest.mark.asyncio
async def test_j_file_migrate_still_works() -> None:
    """Test J: FileMigrate dynamically switches media client."""
    mock_dc4 = MagicMock()
    mock_dc4.dc_id = 4
    mock_dc5 = MagicMock()
    mock_dc5.dc_id = 5

    main_client = MagicMock()
    main_client.dc_id = 2

    async def get_media_client_mock(target_dc: int, *args: Any, **kwargs: Any) -> Any:
        if target_dc == 5:
            return mock_dc5
        return mock_dc4

    main_client.get_media_client = AsyncMock(side_effect=get_media_client_mock)

    # First invoke on DC 4 raises FileMigrate(5), then DC 5 succeeds
    mock_dc4.invoke = AsyncMock(side_effect=FileMigrate(303, "FILE_MIGRATE_5", new_dc=5))
    mock_dc5.invoke = AsyncMock(return_value=b"FILE_FROM_DC5")

    downloader = FileDownloader(client=main_client, chunk_size=1024)
    loc = InputDocumentFileLocation(id=1, access_hash=2, file_reference=b"REF")

    result = await downloader.download(location=loc)
    assert result == b"FILE_FROM_DC5"


@pytest.mark.asyncio
async def test_k_auth_key_unregistered_delegates_to_dc_manager() -> None:
    """Test K: AuthKeyUnregistered re-fetches media client from DCManager."""
    mock_client = MagicMock()
    mock_client.dc_id = 4

    attempt = 0

    async def mock_invoke(req: Any) -> bytes:
        nonlocal attempt
        attempt += 1
        if attempt == 1:
            raise AuthKeyUnregistered(401, "AUTH_KEY_UNREGISTERED")
        return b"RECOVERED_AFTER_REAUTH"

    mock_client.invoke = AsyncMock(side_effect=mock_invoke)
    mock_client.get_media_client = AsyncMock(return_value=mock_client)

    downloader = FileDownloader(client=mock_client, chunk_size=1024, max_retries=2)
    loc = InputDocumentFileLocation(id=1, access_hash=2, file_reference=b"REF")

    result = await downloader.download(location=loc)
    assert result == b"RECOVERED_AFTER_REAUTH"
    assert attempt == 2


@pytest.mark.asyncio
async def test_l_normal_network_retry_remains_unchanged() -> None:
    """Test L: Normal network error retries within max_retries limit."""
    mock_client = MagicMock()
    mock_client.dc_id = 4
    mock_client.get_media_client = AsyncMock(return_value=mock_client)

    attempt = 0

    async def mock_invoke(req: Any) -> bytes:
        nonlocal attempt
        attempt += 1
        if attempt < 3:
            raise ConnectionResetError("Connection lost")
        return b"SUCCESS_AFTER_NETWORK_RETRY"

    mock_client.invoke = AsyncMock(side_effect=mock_invoke)

    downloader = FileDownloader(client=mock_client, chunk_size=1024, max_retries=4)
    loc = InputDocumentFileLocation(id=1, access_hash=2, file_reference=b"REF")

    result = await downloader.download(location=loc)
    assert result == b"SUCCESS_AFTER_NETWORK_RETRY"
    assert attempt == 3
