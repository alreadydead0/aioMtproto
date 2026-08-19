"""
In-memory MTProto session storage.
"""

from __future__ import annotations

from aiogram.session.base import BaseMTProtoSession, SessionData


class MemorySession(BaseMTProtoSession):
    """
    Volatile in-memory MTProto session storage.
    """

    def __init__(self, data: SessionData | None = None) -> None:
        self._data = data or SessionData()

    async def load(self) -> SessionData:
        return self._data

    async def save(self, data: SessionData) -> None:
        self._data = data

    async def delete(self) -> None:
        self._data = SessionData()
