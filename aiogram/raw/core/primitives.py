"""
Telegram TL binary serialization primitives.
"""

from __future__ import annotations

import gzip
import io
import struct
from typing import Any, BinaryIO, Generic, TypeVar, cast

T = TypeVar("T")


class TLObject:
    """
    Base class for all Telegram TL types and functions.
    """

    ID: int = 0
    QUALNAME: str = "TLObject"

    def write(self) -> bytes:
        raise NotImplementedError

    @classmethod
    def read(cls, b: BinaryIO, *args: Any) -> Any:
        raise NotImplementedError

    def __repr__(self) -> str:
        fields = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items() if not k.startswith("_"))
        return f"{self.QUALNAME}({fields})"


class TLRequest(TLObject, Generic[T]):
    """
    Base class for all Telegram TL RPC function requests.
    """

    def read_result(self, b: BinaryIO) -> T:
        raise NotImplementedError


# --- Primitive Reading/Writing Helpers ---


def write_int(val: int) -> bytes:
    return struct.pack("<i", val)


def read_int(b: BinaryIO) -> int:
    return struct.unpack("<i", b.read(4))[0]


def write_uint(val: int) -> bytes:
    return struct.pack("<I", val)


def read_uint(b: BinaryIO) -> int:
    return struct.unpack("<I", b.read(4))[0]


def write_long(val: int) -> bytes:
    return struct.pack("<q", val)


def read_long(b: BinaryIO) -> int:
    return struct.unpack("<q", b.read(8))[0]


def write_int128(val: bytes | int) -> bytes:
    if isinstance(val, int):
        return val.to_bytes(16, "little", signed=True)
    return val


def read_int128(b: BinaryIO) -> bytes:
    return b.read(16)


def write_int256(val: bytes | int) -> bytes:
    if isinstance(val, int):
        return val.to_bytes(32, "little", signed=True)
    return val


def read_int256(b: BinaryIO) -> bytes:
    return b.read(32)


def write_double(val: float) -> bytes:
    return struct.pack("<d", val)


def read_double(b: BinaryIO) -> float:
    return struct.unpack("<d", b.read(8))[0]


def write_bool(val: bool) -> bytes:
    # boolTrue: 0x997275b5, boolFalse: 0xbc799737
    return struct.pack("<I", 0x997275B5 if val else 0xBC799737)


def read_bool(b: BinaryIO) -> bool:
    c_id = read_uint(b)
    if c_id == 0x997275B5:
        return True
    if c_id == 0xBC799737:
        return False
    msg = f"Invalid boolean constructor ID: {c_id:#010x}"
    raise ValueError(msg)


def write_bytes(data: bytes) -> bytes:
    """
    Serializes bytes according to Telegram TL string/bytes specification:
    - If length < 254: 1 byte len + data + padding (0..3 bytes to align to 4 bytes).
    - If length >= 254: 0xFE (1 byte) + 3 bytes len (little endian) + data + padding.
    """
    length = len(data)
    if length < 254:
        header = bytes([length])
        padding = (4 - ((length + 1) % 4)) % 4
    else:
        header = b"\xfe" + length.to_bytes(3, "little")
        padding = (4 - ((length + 4) % 4)) % 4

    return header + data + (b"\x00" * padding)


def read_bytes(b: BinaryIO) -> bytes:
    """
    Deserializes Telegram TL bytes.
    """
    first_byte = b.read(1)
    if not first_byte:
        return b""
    length = first_byte[0]
    if length == 254:
        length_bytes = b.read(3)
        length = int.from_bytes(length_bytes, "little")
        padding = (4 - ((length + 4) % 4)) % 4
    else:
        padding = (4 - ((length + 1) % 4)) % 4

    data = b.read(length)
    if padding:
        b.read(padding)
    return data


def write_string(text: str) -> bytes:
    return write_bytes(text.encode("utf-8"))


def read_string(b: BinaryIO) -> str:
    return read_bytes(b).decode("utf-8", errors="replace")


def write_vector(items: list[Any], item_writer: Any) -> bytes:
    """
    Serialize a TL Vector (0x1cb5c415).
    """
    res = bytearray(struct.pack("<II", 0x1CB5C415, len(items)))
    for item in items:
        if hasattr(item, "write"):
            res.extend(item.write())
        elif callable(item_writer):
            res.extend(item_writer(item))
    return bytes(res)


def read_vector(b: BinaryIO, item_reader: Any) -> list[Any]:
    """
    Deserialize a TL Vector.
    """
    c_id = read_uint(b)
    if c_id != 0x1CB5C415:
        msg = f"Invalid vector constructor ID: {c_id:#010x}"
        raise ValueError(msg)
    count = read_uint(b)
    return [item_reader(b) for _ in range(count)]
