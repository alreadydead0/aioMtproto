"""
Tests for MTProto TCP transport framing (Abridged, Intermediate, Padded Intermediate, Full).
"""

import asyncio

import pytest

from aiogram.mtproto.connection.transport import (
    AbridgedTransport,
    FullTransport,
    IntermediateTransport,
    PaddedIntermediateTransport,
)


@pytest.mark.asyncio
async def test_abridged_transport_small_packet() -> None:
    transport = AbridgedTransport()
    payload = b"test" * 4  # 16 bytes = 4 words
    packed = transport.pack(payload)

    # 1 byte header for length (4) + payload
    assert packed[0] == 4
    assert packed[1:] == payload

    reader = asyncio.StreamReader()
    reader.feed_data(packed)
    reader.feed_eof()

    unpacked = await transport.read_packet(reader)
    assert unpacked == payload


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "transport_cls",
    [AbridgedTransport, IntermediateTransport, PaddedIntermediateTransport, FullTransport],
)
async def test_transports_fragmented_reads(transport_cls: type) -> None:
    transport = transport_cls()
    # 4-byte aligned payload (64 bytes)
    payload = b"1234567890abcdef" * 4

    packed = transport.pack(payload)
    reader = asyncio.StreamReader()

    async def feeder():
        # Feed payload in tiny fragmented chunks (1, 2, 5, 17, remaining)
        chunks = [1, 2, 5, 17]
        offset = 0
        for chunk_size in chunks:
            if offset < len(packed):
                reader.feed_data(packed[offset : offset + chunk_size])
                offset += chunk_size
                await asyncio.sleep(0.001)
        if offset < len(packed):
            reader.feed_data(packed[offset:])
        reader.feed_eof()

    feeder_task = asyncio.create_task(feeder())
    unpacked = await transport.read_packet(reader)
    await feeder_task

    assert unpacked[: len(payload)] == payload


@pytest.mark.asyncio
async def test_abridged_transport_large_packet() -> None:
    transport = AbridgedTransport()
    # 200 words = 800 bytes
    payload = b"abcd" * 200
    packed = transport.pack(payload)

    assert packed[0] == 0x7F
    length = int.from_bytes(packed[1:4], "little")
    assert length == 200
    assert packed[4:] == payload

    reader = asyncio.StreamReader()
    reader.feed_data(packed)
    reader.feed_eof()

    unpacked = await transport.read_packet(reader)
    assert unpacked == payload


@pytest.mark.asyncio
async def test_intermediate_transport() -> None:
    transport = IntermediateTransport()
    payload = b"Sample MTProto intermediate payload"
    packed = transport.pack(payload)

    reader = asyncio.StreamReader()
    reader.feed_data(packed)
    reader.feed_eof()

    unpacked = await transport.read_packet(reader)
    assert unpacked == payload


@pytest.mark.asyncio
async def test_full_transport() -> None:
    transport = FullTransport()
    payload = b"Sample payload for FullTransport with CRC32"
    packed = transport.pack(payload)

    reader = asyncio.StreamReader()
    reader.feed_data(packed)
    reader.feed_eof()

    unpacked = await transport.read_packet(reader)
    assert unpacked == payload
