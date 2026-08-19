"""
Telegram Bot API FileId decoder.
Parses Bot API file_id strings into MTProto InputFileLocation.
"""

from __future__ import annotations

import base64
import io
import struct
from typing import Any, NamedTuple

from aiogram.raw.core.primitives import TLObject, read_bytes
from aiogram.raw.types import (
    InputDocumentFileLocation,
    InputPhotoFileLocation,
)

MAX_BYTE_VALUE = 255
BASE64_BLOCK_SIZE = 4


class DecodedFileId(NamedTuple):
    file_type: int
    dc_id: int
    id: int
    access_hash: int
    file_reference: bytes


def rle_encode(data: bytes) -> bytes:
    """Run-length encoding used by Telegram FileId."""
    out = bytearray()
    i = 0
    while i < len(data):
        if data[i] == 0:
            count = 0
            while i < len(data) and data[i] == 0 and count < MAX_BYTE_VALUE:
                count += 1
                i += 1
            out.append(0)
            out.append(count)
        else:
            out.append(data[i])
            i += 1
    return bytes(out)


def rle_decode(data: bytes) -> bytes:
    """Run-length decoding used by Telegram FileId."""
    out = bytearray()
    i = 0
    while i < len(data):
        b = data[i]
        i += 1
        if b == 0:
            if i < len(data):
                count = data[i]
                i += 1
                out.extend(b"\x00" * count)
        else:
            out.append(b)
    return bytes(out)


def decode_file_id(file_id: str) -> DecodedFileId | None:
    """
    Decode standard Telegram Bot API file_id into components.
    """
    try:
        # Base64 urlsafe decode with padding
        padding = BASE64_BLOCK_SIZE - (len(file_id) % BASE64_BLOCK_SIZE)
        if padding != BASE64_BLOCK_SIZE:
            file_id += "=" * padding
        raw = base64.urlsafe_b64decode(file_id)
        raw = rle_decode(raw)

        b = io.BytesIO(raw)

        # Read type and dc_id
        type_id = struct.unpack("<i", b.read(4))[0]
        file_type = type_id & 0xFF
        has_file_reference = bool(
            ((type_id >> 24) & 1)
            or ((type_id >> 25) & 1)
            or (raw[-2:] == b"\x1e\x04")
            or (raw[-1:] in (b"\x04", b"\x03"))
        )

        dc_id = struct.unpack("<i", b.read(4))[0]
        if dc_id not in (1, 2, 3, 4, 5):
            return None

        # Read file_reference (TL serialized bytes with proper 4-byte padding alignment)
        if has_file_reference:
            file_reference = read_bytes(b)
        else:
            file_reference = b""

        # Read file id and access_hash
        id_val = struct.unpack("<q", b.read(8))[0]
        access_hash = struct.unpack("<q", b.read(8))[0]

        return DecodedFileId(
            file_type=file_type,
            dc_id=dc_id,
            id=id_val,
            access_hash=access_hash,
            file_reference=file_reference,
        )
    except Exception:
        return None


def file_id_to_input_location(file_id_or_obj: Any) -> Any:
    """
    Convert a Bot API file_id or Media object to an MTProto InputFileLocation.
    """
    if isinstance(file_id_or_obj, TLObject):
        return file_id_or_obj

    if hasattr(file_id_or_obj, "file_id"):
        file_id_str = getattr(file_id_or_obj, "file_id")  # noqa: B009
    else:
        file_id_str = str(file_id_or_obj)

    decoded = decode_file_id(file_id_str)
    if decoded is None:
        msg = f"Invalid or unsupported Telegram file_id: {file_id_str!r}"
        raise ValueError(msg)

    # If photo type (1 or 2 in TDLib format)
    if decoded.file_type in (1, 2):
        return InputPhotoFileLocation(
            id=decoded.id,
            access_hash=decoded.access_hash,
            file_reference=decoded.file_reference,
            thumb_size="",
        )

    return InputDocumentFileLocation(
        id=decoded.id,
        access_hash=decoded.access_hash,
        file_reference=decoded.file_reference,
        thumb_size="",
    )
