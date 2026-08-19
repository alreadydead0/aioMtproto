"""
Base MTProto session interface.
"""

from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import Optional

from aiogram.mtproto.crypto.auth_key import AuthKey


@dataclass
class SessionData:
    dc_id: int = 2
    server_address: str = "149.154.167.51"
    port: int = 443
    auth_key: AuthKey | None = None
    server_salt: int = 0
    seq_no: int = 0
    user_id: int | None = None
    is_bot: bool = False
    phone: str | None = None
    is_test: bool = False


class BaseMTProtoSession(abc.ABC):
    """
    Abstract interface for MTProto session persistence.
    """

    @abc.abstractmethod
    async def load(self) -> SessionData:
        """Load session state."""
        raise NotImplementedError

    @abc.abstractmethod
    async def save(self, data: SessionData) -> None:
        """Save session state."""
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self) -> None:
        """Delete session state."""
        raise NotImplementedError
