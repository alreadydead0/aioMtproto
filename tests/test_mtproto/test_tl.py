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


def test_upload_file_deserialization_with_storage_file_type() -> None:
    from aiogram.raw.types import StorageFileUnknown, UploadFile

    # UploadFile payload with storage.fileUnknown (0x40bc6f52), mtime=1700000000, bytes=b"FILE_CHUNK"
    upload_file = UploadFile(type=StorageFileUnknown(), mtime=1700000000, bytes=b"FILE_CHUNK")
    raw_bytes = upload_file.write()

    read_obj = read_tl_object(io.BytesIO(raw_bytes))
    assert isinstance(read_obj, UploadFile)
    assert isinstance(read_obj.type, StorageFileUnknown)
    assert read_obj.mtime == 1700000000
    assert read_obj.bytes == b"FILE_CHUNK"


def test_tl_new_session_created() -> None:
    from aiogram.raw.core.tl_core_types import NewSessionCreated

    new_session = NewSessionCreated(
        first_msg_id=111222333, unique_id=444555666, server_salt=777888999
    )
    raw_bytes = new_session.write()

    assert raw_bytes[:4] == (0x9EC20908).to_bytes(4, "little")
    parsed = read_tl_object(io.BytesIO(raw_bytes))
    assert isinstance(parsed, NewSessionCreated)
    assert parsed.first_msg_id == 111222333
    assert parsed.unique_id == 444555666
    assert parsed.server_salt == 777888999


def test_tl_pong_and_ping() -> None:
    from aiogram.raw.core.tl_core_types import Ping, PingDelayDisconnect, Pong

    pong = Pong(msg_id=123456789, ping_id=987654321)
    raw_bytes = pong.write()

    parsed_pong = read_tl_object(io.BytesIO(raw_bytes))
    assert isinstance(parsed_pong, Pong)
    assert parsed_pong.msg_id == 123456789
    assert parsed_pong.ping_id == 987654321

    ping_req = Ping(ping_id=987654321)
    res = ping_req.read_result(io.BytesIO(raw_bytes))
    assert res == 987654321

    ping_delay_req = PingDelayDisconnect(ping_id=987654321, disconnect_delay=75)
    res2 = ping_delay_req.read_result(io.BytesIO(raw_bytes))
    assert res2 == 987654321


def test_tl_primitives_bounds_checking() -> None:
    from aiogram.raw.core.primitives import (
        read_int128,
        read_int256,
        read_vector,
    )

    with pytest.raises(ValueError, match="Truncated stream.*int"):
        read_int(io.BytesIO(b"\x01\x02"))

    with pytest.raises(ValueError, match="Truncated stream.*long"):
        read_long(io.BytesIO(b"\x01\x02\x03\x04"))

    with pytest.raises(ValueError, match="Truncated stream.*int128"):
        read_int128(io.BytesIO(b"\x01" * 8))

    with pytest.raises(ValueError, match="Truncated stream.*int256"):
        read_int256(io.BytesIO(b"\x01" * 16))

    with pytest.raises(ValueError, match="Truncated TL bytes"):
        read_bytes(io.BytesIO(b"\x05\x01\x02"))

    with pytest.raises(ValueError, match="Invalid vector constructor ID"):
        read_vector(io.BytesIO(b"\x00\x00\x00\x00"), read_int)


def test_tl_unknown_constructor_diagnostics() -> None:
    corrupt_data = b"\xde\xad\xbe\xef\x01\x02\x03\x04"
    with pytest.raises(ValueError, match="Unknown TL constructor ID: 0xefbeadde"):
        read_tl_object(io.BytesIO(corrupt_data))


def test_tl_authorization_deserialization() -> None:
    import struct
    from aiogram.raw.types import Authorization, User

    user = User(id=7597391690, first_name="Terabox", bot=True)
    user_bytes = user.write()

    # auth.authorization#2ea2c0d4 flags:2 (setup_password_required=True, otherwise_relogin_days=7), user
    auth_flags = 2
    relogin_days = 7
    payload = (
        struct.pack("<IIi", 0x2EA2C0D4, auth_flags, relogin_days)
        + user_bytes
    )

    auth = read_tl_object(io.BytesIO(payload))
    assert isinstance(auth, Authorization)
    assert auth.setup_password_required is True
    assert auth.user.id == 7597391690
    assert auth.user.first_name == "Terabox"
    assert auth.user.bot is True
