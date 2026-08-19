"""
Tests for MTProto session persistence (MemorySession, SQLiteSession).
"""

import os

import pytest

from aiogram.mtproto.crypto.auth_key import AuthKey
from aiogram.session.base import SessionData
from aiogram.session.memory import MemorySession
from aiogram.session.sqlite import SQLiteSession
from aiogram.session.string import StringSession


@pytest.mark.asyncio
async def test_memory_session() -> None:
    session = MemorySession()
    data = await session.load()
    assert data.dc_id == 2

    auth_key = AuthKey(os.urandom(256))
    data.auth_key = auth_key
    data.user_id = 12345
    await session.save(data)

    loaded = await session.load()
    assert loaded.auth_key is not None
    assert loaded.auth_key.key == auth_key.key
    assert loaded.user_id == 12345


@pytest.mark.asyncio
async def test_sqlite_session(tmp_path: pytest.TempPathFactory) -> None:
    db_file = str(tmp_path / "test_session.session")
    session = SQLiteSession(db_file)

    auth_key = AuthKey(os.urandom(256))
    data = SessionData(
        dc_id=4,
        server_address="149.154.167.91",
        port=443,
        auth_key=auth_key,
        server_salt=987654321,
        user_id=55555,
        is_bot=True,
    )
    await session.save(data)

    # Re-open database with new instance to verify on-disk persistence
    session2 = SQLiteSession(db_file)
    loaded = await session2.load()

    assert loaded.dc_id == 4
    assert loaded.server_address == "149.154.167.91"
    assert loaded.auth_key is not None
    assert loaded.auth_key.key == auth_key.key
    assert loaded.server_salt == 987654321
    assert loaded.user_id == 55555
    assert loaded.is_bot is True
    await session2.delete()
    deleted = await session2.load()
    assert deleted.auth_key is None


@pytest.mark.asyncio
async def test_string_session() -> None:
    auth_key = AuthKey(os.urandom(256))
    data = SessionData(
        dc_id=2,
        server_address="149.154.167.51",
        port=443,
        auth_key=auth_key,
        server_salt=123456789,
        user_id=999888777,
        is_bot=False,
    )

    session = StringSession()
    await session.save(data)
    exported = session.export_string()
    assert isinstance(exported, str)
    assert len(exported) > 100

    # Roundtrip from string
    session2 = StringSession(exported)
    loaded = await session2.load()

    assert loaded.dc_id == 2
    assert loaded.server_address == "149.154.167.51"
    assert loaded.auth_key is not None
    assert loaded.auth_key.key == auth_key.key
    assert loaded.user_id == 999888777
    assert loaded.server_salt == 123456789
    assert loaded.is_bot is False
