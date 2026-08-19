"""
Tests for Telegram TL binary serialization and parsing.
"""

import io

import pytest

from aiogram.raw.all import read_tl_object
from aiogram.raw.core.primitives import (
    read_bool,
    read_bytes,
    read_double,
    read_int,
    read_long,
    read_string,
    write_bool,
    write_bytes,
    write_double,
    write_int,
    write_long,
    write_string,
)
from aiogram.raw.core.tl_core_types import GzipPacked, Ping, Pong, ResPQ
from aiogram.raw.types import Message, PeerUser, UpdateShortMessage, User


def test_tl_primitives() -> None:
    # Int
    assert read_int(io.BytesIO(write_int(42))) == 42
    assert read_int(io.BytesIO(write_int(-100))) == -100

    # Long
    assert read_long(io.BytesIO(write_long(123456789012345))) == 123456789012345

    # Double
    assert read_double(io.BytesIO(write_double(3.14159))) == pytest.approx(3.14159)

    # Bool
    assert read_bool(io.BytesIO(write_bool(True))) is True
    assert read_bool(io.BytesIO(write_bool(False))) is False

    # String & Bytes (< 254 bytes)
    sample_str = "Hello Telegram MTProto!"
    assert read_string(io.BytesIO(write_string(sample_str))) == sample_str

    # String & Bytes (>= 254 bytes)
    large_bytes = b"X" * 1000
    assert read_bytes(io.BytesIO(write_bytes(large_bytes))) == large_bytes


def test_tl_user_serialization() -> None:
    user = User(
        id=123456789,
        is_self=True,
        first_name="Alex",
        last_name="Root",
        username="alexroot",
        premium=True,
    )
    serialized = user.write()
    # Read back (skip 4 bytes ID)
    b_io = io.BytesIO(serialized[4:])
    deserialized = User.read(b_io)

    assert deserialized.id == user.id
    assert deserialized.is_self is True
    assert deserialized.first_name == "Alex"
    assert deserialized.last_name == "Root"
    assert deserialized.username == "alexroot"
    assert deserialized.premium is True


def test_tl_polymorphic_reader_and_gzip() -> None:
    user = User(id=987654, first_name="GzipUser")
    user_bytes = user.write()

    # Wrap in GzipPacked
    gzip_packed = GzipPacked(user_bytes)
    packed_bytes = gzip_packed.write()

    # Read polymorphic
    unpacked_obj = read_tl_object(io.BytesIO(packed_bytes))
    assert isinstance(unpacked_obj, User)
    assert unpacked_obj.id == 987654
    assert unpacked_obj.first_name == "GzipUser"
