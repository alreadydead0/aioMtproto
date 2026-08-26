"""
Base MTProto session interface.
"""

from __future__ import annotations

import abc
from dataclasses import dataclass, field
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
    # Multi-DC mapping: dc_id -> (AuthKey, server_salt)
    dc_auth_keys: dict[int, tuple[AuthKey, int]] = field(default_factory=dict)
    # Set of DC IDs where media authorization has been successfully exported/imported
    auth_imported_dcs: set[int] = field(default_factory=set)

    def get_dc_auth(self, dc_id: int) -> tuple[AuthKey, int] | None:
        if dc_id in self.dc_auth_keys:
            return self.dc_auth_keys[dc_id]
        if dc_id == self.dc_id and self.auth_key:
            return self.auth_key, self.server_salt
        return None

    def set_dc_auth(self, dc_id: int, auth_key: AuthKey | None, server_salt: int = 0) -> None:
        if auth_key is not None:
            self.dc_auth_keys[dc_id] = (auth_key, server_salt)
            if dc_id == self.dc_id:
                self.auth_key = auth_key
                self.server_salt = server_salt
        else:
            self.dc_auth_keys.pop(dc_id, None)
            if dc_id == self.dc_id:
                self.auth_key = None
                self.server_salt = 0

    def __repr__(self) -> str:
        has_auth = "yes" if self.auth_key else "no"
        return f"<SessionData dc_id={self.dc_id} is_bot={self.is_bot} has_auth={has_auth}>"


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

    async def invalidate_auth_key(self, dc_id: int | None = None) -> None:
        """
        Atomically clear auth_key, server_salt, and user credentials for a specific DC or main DC.
        """
        data = await self.load()
        if dc_id is None or dc_id == data.dc_id:
            data.auth_key = None
            data.server_salt = 0
            data.user_id = None
            if dc_id is not None:
                data.dc_auth_keys.pop(dc_id, None)
                data.auth_imported_dcs.discard(dc_id)
        else:
            data.dc_auth_keys.pop(dc_id, None)
            data.auth_imported_dcs.discard(dc_id)
        await self.save(data)
