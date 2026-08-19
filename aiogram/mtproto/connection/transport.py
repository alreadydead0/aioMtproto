"""
MTProto TCP Transport framing protocols (Abridged, Intermediate, Padded Intermediate, Full).
"""

from __future__ import annotations

import abc
import asyncio
import os
import struct
import zlib
from typing import AsyncGenerator


class BaseTransport(abc.ABC):
    """
    Base class for MTProto transport framing protocols.
    """

    HEADER: bytes = b""

    @abc.abstractmethod
    def pack(self, payload: bytes) -> bytes:
        """
        Packs a raw MTProto payload with framing bytes according to the transport protocol.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def read_packet(self, reader: asyncio.StreamReader) -> bytes:
        """
        Reads a framed packet from the stream reader and returns the un-framed MTProto payload.
        """
        raise NotImplementedError


class AbridgedTransport(BaseTransport):
    """
    Abridged Transport:
    Header: 0xef
    Small packets (< 127 words): 1 byte length in 4-byte words.
    Large packets (>= 127 words): 0x7f followed by 3 bytes length in 4-byte words (little-endian).
    """

    HEADER = b"\xef"

    def pack(self, payload: bytes) -> bytes:
        length = len(payload) // 4
        if length < 127:
            return bytes([length]) + payload
        return b"\x7f" + length.to_bytes(3, "little") + payload

    async def read_packet(self, reader: asyncio.StreamReader) -> bytes:
        length_bytes = await reader.readexactly(1)
        length = length_bytes[0]
        if length == 0x7F:
            length_bytes = await reader.readexactly(3)
            length = int.from_bytes(length_bytes, "little")
        payload_len = length * 4
        return await reader.readexactly(payload_len)


class IntermediateTransport(BaseTransport):
    """
    Intermediate Transport:
    Header: 0xeeeeeeee
    Length: 4 bytes unsigned int (little-endian) representing payload length in bytes.
    """

    HEADER = b"\xee\xee\xee\xee"

    def pack(self, payload: bytes) -> bytes:
        return struct.pack("<I", len(payload)) + payload

    async def read_packet(self, reader: asyncio.StreamReader) -> bytes:
        length_bytes = await reader.readexactly(4)
        length = struct.unpack("<I", length_bytes)[0]
        return await reader.readexactly(length)


class PaddedIntermediateTransport(BaseTransport):
    """
    Padded Intermediate Transport:
    Header: 0xdddddddd
    Length: 4 bytes unsigned int (little-endian) representing (payload_len + padding_len).
    Appends 0-15 bytes of random padding to obscure packet sizes.
    """

    HEADER = b"\xdd\xdd\xdd\xdd"

    def pack(self, payload: bytes) -> bytes:
        pad_len = os.urandom(1)[0] % 16
        padding = os.urandom(pad_len)
        total_len = len(payload) + pad_len
        return struct.pack("<I", total_len) + payload + padding

    async def read_packet(self, reader: asyncio.StreamReader) -> bytes:
        length_bytes = await reader.readexactly(4)
        length = struct.unpack("<I", length_bytes)[0]
        # In padded intermediate, the whole padded buffer is read
        return await reader.readexactly(length)


class FullTransport(BaseTransport):
    """
    Full Transport:
    No header.
    Format: length (4 bytes) + seq_no (4 bytes) + payload + CRC32 (4 bytes).
    Length includes the length, seq_no, payload, and crc32 (12 + len(payload)).
    """

    HEADER = b""

    def __init__(self) -> None:
        self.send_seq_no = 0
        self.recv_seq_no = 0

    def pack(self, payload: bytes) -> bytes:
        length = len(payload) + 12
        packet = struct.pack("<II", length, self.send_seq_no) + payload
        crc = struct.pack("<I", zlib.crc32(packet) & 0xFFFFFFFF)
        self.send_seq_no += 1
        return packet + crc

    async def read_packet(self, reader: asyncio.StreamReader) -> bytes:
        length_bytes = await reader.readexactly(4)
        length = struct.unpack("<I", length_bytes)[0]
        rest = await reader.readexactly(length - 4)

        seq_no = struct.unpack("<I", rest[:4])[0]
        payload = rest[4:-4]
        crc_received = struct.unpack("<I", rest[-4:])[0]

        expected_crc = zlib.crc32(length_bytes + rest[:-4]) & 0xFFFFFFFF
        if crc_received != expected_crc:
            msg = f"CRC32 mismatch in FullTransport (expected {expected_crc:#010x}, got {crc_received:#010x})"
            raise ValueError(msg)

        self.recv_seq_no += 1
        return payload
