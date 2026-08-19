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
