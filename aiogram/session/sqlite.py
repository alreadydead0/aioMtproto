"""
Persistent SQLite MTProto session storage.
"""

from __future__ import annotations

import asyncio
import os
import sqlite3
from typing import Optional

from aiogram.mtproto.crypto.auth_key import AuthKey
from aiogram.session.base import BaseMTProtoSession, SessionData


class SQLiteSession(BaseMTProtoSession):
    """
    Thread-safe / async-safe SQLite session storage for MTProto.
    """

    SCHEMA = """
    CREATE TABLE IF NOT EXISTS session (
        dc_id INTEGER PRIMARY KEY,
        server_address TEXT NOT NULL,
        port INTEGER NOT NULL,
        auth_key BLOB,
        server_salt INTEGER DEFAULT 0,
        seq_no INTEGER DEFAULT 0,
        user_id INTEGER,
        is_bot INTEGER DEFAULT 0,
        phone TEXT,
        is_test INTEGER DEFAULT 0
    );
    """

    def __init__(self, filename: str = "aiogram_session.session") -> None:
        if not filename.endswith(".session") and not filename.endswith(".db") and not filename.endswith(".sqlite"):
            filename = f"{filename}.session"
        self.filename = filename
        self._lock = asyncio.Lock()
        self._init_db()

    def _init_db(self) -> None:
        parent_dir = os.path.dirname(self.filename)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
        with sqlite3.connect(self.filename) as conn:
            conn.execute(self.SCHEMA)
            conn.commit()

    async def load(self) -> SessionData:
        async with self._lock:
            with sqlite3.connect(self.filename) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT dc_id, server_address, port, auth_key, server_salt, seq_no, user_id, is_bot, phone, is_test FROM session LIMIT 1"
                )
                row = cursor.fetchone()
                if not row:
                    return SessionData()

                dc_id, server_address, port, auth_key_blob, server_salt, seq_no, user_id, is_bot, phone, is_test = row
                auth_key = AuthKey(auth_key_blob) if auth_key_blob else None

                return SessionData(
                    dc_id=dc_id,
                    server_address=server_address,
                    port=port,
                    auth_key=auth_key,
                    server_salt=server_salt,
                    seq_no=seq_no,
                    user_id=user_id,
                    is_bot=bool(is_bot),
                    phone=phone,
                    is_test=bool(is_test),
                )

    async def save(self, data: SessionData) -> None:
        async with self._lock:
            with sqlite3.connect(self.filename) as conn:
                auth_key_blob = data.auth_key.key if data.auth_key else None
                conn.execute("DELETE FROM session")
                conn.execute(
                    """
                    INSERT INTO session (dc_id, server_address, port, auth_key, server_salt, seq_no, user_id, is_bot, phone, is_test)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        data.dc_id,
                        data.server_address,
                        data.port,
                        auth_key_blob,
                        data.server_salt,
                        data.seq_no,
                        data.user_id,
                        1 if data.is_bot else 0,
                        data.phone,
                        1 if data.is_test else 0,
                    ),
                )
                conn.commit()

    async def delete(self) -> None:
        async with self._lock:
            if os.path.exists(self.filename):
                try:
                    os.remove(self.filename)
                except OSError:
                    with sqlite3.connect(self.filename) as conn:
                        conn.execute("DELETE FROM session")
                        conn.commit()
