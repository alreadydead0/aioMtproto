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


_STRUCT_i = struct.Struct("<i")
_STRUCT_I = struct.Struct("<I")
_STRUCT_q = struct.Struct("<q")
_STRUCT_d = struct.Struct("<d")

# --- Primitive Reading/Writing Helpers ---


def write_int(val: int) -> bytes:
    return _STRUCT_i.pack(val)


def read_int(b: BinaryIO) -> int:
    buf = b.read(4)
    if len(buf) < 4:
        raise ValueError(f"Truncated stream: expected 4 bytes for int, got {len(buf)}")
    return int(_STRUCT_i.unpack(buf)[0])


def write_uint(val: int) -> bytes:
    return _STRUCT_I.pack(val)


def read_uint(b: BinaryIO) -> int:
    buf = b.read(4)
    if len(buf) < 4:
        raise ValueError(f"Truncated stream: expected 4 bytes for uint, got {len(buf)}")
    return int(_STRUCT_I.unpack(buf)[0])


def write_long(val: int) -> bytes:
    return _STRUCT_q.pack(val)


def read_long(b: BinaryIO) -> int:
    buf = b.read(8)
    if len(buf) < 8:
        raise ValueError(f"Truncated stream: expected 8 bytes for long, got {len(buf)}")
    return int(_STRUCT_q.unpack(buf)[0])


def write_int128(val: bytes | int) -> bytes:
    if isinstance(val, int):
        return val.to_bytes(16, "little", signed=True)
    return val


def read_int128(b: BinaryIO) -> bytes:
    buf = b.read(16)
    if len(buf) < 16:
        raise ValueError(f"Truncated stream: expected 16 bytes for int128, got {len(buf)}")
    return buf


def write_int256(val: bytes | int) -> bytes:
    if isinstance(val, int):
        return val.to_bytes(32, "little", signed=True)
    return val


def read_int256(b: BinaryIO) -> bytes:
    buf = b.read(32)
    if len(buf) < 32:
        raise ValueError(f"Truncated stream: expected 32 bytes for int256, got {len(buf)}")
    return buf


def write_double(val: float) -> bytes:
    return _STRUCT_d.pack(val)


def read_double(b: BinaryIO) -> float:
    buf = b.read(8)
    if len(buf) < 8:
        raise ValueError(f"Truncated stream: expected 8 bytes for double, got {len(buf)}")
    return float(_STRUCT_d.unpack(buf)[0])


def write_bool(val: bool) -> bytes:
    # boolTrue: 0x997275b5, boolFalse: 0xbc799737
    return _STRUCT_I.pack(0x997275B5 if val else 0xBC799737)


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
        if len(length_bytes) < 3:
            raise ValueError(f"Truncated stream: expected 3 length bytes, got {len(length_bytes)}")
        length = int.from_bytes(length_bytes, "little")
        padding = (4 - ((length + 4) % 4)) % 4
    else:
        padding = (4 - ((length + 1) % 4)) % 4

    data = b.read(length)
    if len(data) < length:
        raise ValueError(f"Truncated TL bytes: expected {length} bytes, got {len(data)}")
    if padding:
        pad_bytes = b.read(padding)
        if len(pad_bytes) < padding:
            raise ValueError(
                f"Truncated TL bytes padding: expected {padding} bytes, got {len(pad_bytes)}"
            )
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
    if count > 100000:
        raise ValueError(f"Vector count {count} exceeds sanity limit (100000)")
    return [item_reader(b) for _ in range(count)]
