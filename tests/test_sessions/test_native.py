import pytest

from aiogram.mtproto.crypto.auth_key import AuthKey
from aiogram.session.base import SessionData
from aiogram.session.string import StringSession


def test_native_encode_decode_roundtrip():
    auth_key = AuthKey(b"\xaa" * 256)
    data = SessionData(
        dc_id=4,
        server_address="149.154.167.91",
        port=443,
        auth_key=auth_key,
        server_salt=123456789,
        user_id=987654321,
        is_bot=False,
        is_test=False,
        api_id=12345,
    )

    encoded = StringSession._encode(data)
    assert StringSession.is_valid(encoded)

    decoded = StringSession._decode(encoded)
    assert decoded.dc_id == 4
    assert decoded.server_address == "149.154.167.91"
    assert decoded.port == 443
    assert decoded.user_id == 987654321
    assert decoded.server_salt == 123456789
    assert decoded.api_id == 12345
    assert decoded.is_bot is False
    assert decoded.is_test is False
    assert decoded.auth_key is not None
    assert decoded.auth_key.key == auth_key.key


def test_native_string_session_class():
    auth_key = AuthKey(b"\xbb" * 256)
    data = SessionData(
        dc_id=2,
        server_address="149.154.167.51",
        port=443,
        auth_key=auth_key,
        user_id=11223344,
        is_bot=True,
    )
    s = StringSession()
    s._data = data
    encoded = s.export_session_string()

    loaded = StringSession(encoded)
    assert StringSession.is_valid(encoded)
    assert loaded._data.dc_id == 2
    assert loaded._data.user_id == 11223344
    assert loaded._data.is_bot is True
    assert loaded._data.auth_key is not None
    assert loaded._data.auth_key.key == auth_key.key

    info = StringSession.info(encoded)
    assert info["format"] == "aio"
    assert info["dc_id"] == 2
    assert info["user_id"] == 11223344
    assert info["is_bot"] is True
    assert "auth_key" not in info
