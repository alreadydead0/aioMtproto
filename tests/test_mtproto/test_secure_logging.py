import os
from unittest.mock import MagicMock

from aiogram.mtproto.connection.dc_manager import DCClientSession
from aiogram.mtproto.crypto.auth_key import AuthKey
from aiogram.mtproto.protocol.rpc import RPCEngine
from aiogram.session.base import SessionData


def test_auth_key_repr_is_safe() -> None:
    raw_key = os.urandom(256)
    key = AuthKey(raw_key)
    repr_str = repr(key)
    assert repr_str == "<AuthKey>"
    assert str(key.key_id) not in repr_str
    assert key.key.hex() not in repr_str


def test_session_data_repr_is_safe() -> None:
    raw_key = os.urandom(256)
    key = AuthKey(raw_key)
    data = SessionData(
        dc_id=2,
        server_address="149.154.167.51",
        port=443,
        auth_key=key,
        server_salt=1234567890,
        user_id=987654321,
        phone="+1234567890",
    )
    repr_str = repr(data)
    assert "1234567890" not in repr_str
    assert "+1234567890" not in repr_str
    assert "987654321" not in repr_str
    assert "has_auth=yes" in repr_str


def test_dc_client_session_repr_is_safe() -> None:
    raw_key = os.urandom(256)
    key = AuthKey(raw_key)
    session = DCClientSession(dc_id=2, is_media=False, api_id=6)
    session.auth_key = key
    session.session_id = 999988887777
    session.server_salt = 111122223333

    repr_str = repr(session)
    assert "999988887777" not in repr_str
    assert "111122223333" not in repr_str
    assert str(key.key_id) not in repr_str
    assert "<DCClientSession dc_id=2 is_media=False" in repr_str


def test_rpc_engine_repr_is_safe() -> None:
    raw_key = os.urandom(256)
    key = AuthKey(raw_key)
    mock_conn = MagicMock()
    mock_conn.is_connected = True
    rpc = RPCEngine(
        connection=mock_conn,
        auth_key=key,
        server_salt=123456,
        session_id=789012,
    )
    repr_str = repr(rpc)
    assert "123456" not in repr_str
    assert "789012" not in repr_str
    assert str(key.key_id) not in repr_str
    assert "<RPCEngine is_connected=True>" in repr_str
