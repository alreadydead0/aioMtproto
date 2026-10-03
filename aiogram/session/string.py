"""
Native aioMtproto MTProto String Session implementation.
"""

from __future__ import annotations

import base64
import ipaddress
import struct
from typing import Any

from aiogram.mtproto.connection.dc import get_dc
from aiogram.mtproto.crypto.auth_key import AuthKey
from aiogram.session.base import BaseMTProtoSession, SessionData

MAGIC_V1 = b"AIOG"
MAGIC_V2 = b"AIO2"


MIN_V1_LEN = 270
MIN_V2_LEN = 278


class StringSession(BaseMTProtoSession):
    """
    Native aioMtproto URL-safe Base64 MTProto String Session.
    Encodes and decodes normalized session data (DC, IP, port, user_id, auth_key, salt, api_id).
    """

    def __init__(self, session_string: str = "") -> None:
        self.session_string = session_string.strip()
        self._data: SessionData = (
            self._decode(self.session_string) if self.session_string else SessionData()
        )

    @classmethod
    def is_valid(cls, session_string: str) -> bool:
        """Check if string is a valid native aioMtproto session."""
        if not session_string:
            return False
        s = session_string.strip()
        padded = s + "=" * ((4 - len(s) % 4) % 4)
        try:
            raw = base64.urlsafe_b64decode(padded.encode("ascii"))
            has_magic = raw.startswith(MAGIC_V1) or raw.startswith(MAGIC_V2)
            return has_magic and len(raw) >= MIN_V1_LEN
        except Exception:
            return False

    @classmethod
    def info(cls, session_string: str) -> dict[str, Any]:
        """
        Extract normalized session metadata without exposing secret auth keys.
        """
        session = cls(session_string)
        data = session._data
        if not data.auth_key:
            msg = "Unrecognized or invalid string session format"
            raise ValueError(msg)

        return {
            "format": "aio",
            "dc_id": data.dc_id,
            "server_address": data.server_address,
            "port": data.port,
            "user_id": data.user_id,
            "is_bot": data.is_bot,
            "is_test": data.is_test,
            "api_id": data.api_id,
            "has_auth": bool(data.auth_key),
        }

    @staticmethod
    def _encode(data: SessionData) -> str:
        """
        Encode SessionData into native aioMtproto URL-safe Base64 string.
        """
        if not data.auth_key:
            return ""

        try:
            ip_obj = ipaddress.ip_address(data.server_address)
            ip_bytes = ip_obj.packed
        except ValueError:
            ip_bytes = b"\x00" * 4

        ip_len = len(ip_bytes)
        user_id = data.user_id or 0
        server_salt = data.server_salt or 0
        api_id = data.api_id or 0

        header_fmt = f">4sBBB H B{ip_len}s qq I 256s"
        packed = struct.pack(
            header_fmt,
            MAGIC_V2,
            data.dc_id,
            1 if data.is_test else 0,
            1 if data.is_bot else 0,
            data.port,
            ip_len,
            ip_bytes,
            user_id,
            server_salt,
            api_id,
            data.auth_key.key,
        )
        return base64.urlsafe_b64encode(packed).decode("ascii").rstrip("=")

    @staticmethod
    def _decode(session_string: str) -> SessionData:
        """
        Decode native aioMtproto string session into SessionData.
        """
        s = session_string.strip()
        if not s:
            return SessionData()

        padded = s + "=" * ((4 - len(s) % 4) % 4)
        try:
            raw = base64.urlsafe_b64decode(padded.encode("ascii"))
        except Exception as e:
            msg = f"Failed to base64 decode session string: {e}"
            raise ValueError(msg) from e

        if raw.startswith(MAGIC_V2) and len(raw) >= MIN_V2_LEN:
            dc_id, is_test_int, is_bot_int, port, ip_len = struct.unpack(">BBB H B", raw[4:10])
            ip_bytes = raw[10 : 10 + ip_len]
            user_id, server_salt, api_id, auth_key_bytes = struct.unpack(
                ">qq I 256s", raw[10 + ip_len : 10 + ip_len + 20 + 256]
            )
            try:
                ip_str = str(ipaddress.ip_address(ip_bytes))
            except ValueError:
                dc = get_dc(dc_id, test_mode=bool(is_test_int))
                ip_str = dc.ip_address

            return SessionData(
                dc_id=dc_id,
                server_address=ip_str,
                port=port,
                auth_key=AuthKey(auth_key_bytes),
                server_salt=server_salt,
                user_id=user_id if user_id != 0 else None,
                is_bot=bool(is_bot_int),
                is_test=bool(is_test_int),
                api_id=api_id if api_id != 0 else None,
            )

        if raw.startswith(MAGIC_V1) and len(raw) >= MIN_V1_LEN:
            dc_id, is_test_int, is_bot_int, port, ip_len = struct.unpack(">BBB H B", raw[4:10])
            ip_bytes = raw[10 : 10 + ip_len]
            user_id, server_salt, auth_key_bytes = struct.unpack(
                ">qq 256s", raw[10 + ip_len : 10 + ip_len + 16 + 256]
            )
            try:
                ip_str = str(ipaddress.ip_address(ip_bytes))
            except ValueError:
                dc = get_dc(dc_id, test_mode=bool(is_test_int))
                ip_str = dc.ip_address

            return SessionData(
                dc_id=dc_id,
                server_address=ip_str,
                port=port,
                auth_key=AuthKey(auth_key_bytes),
                server_salt=server_salt,
                user_id=user_id if user_id != 0 else None,
                is_bot=bool(is_bot_int),
                is_test=bool(is_test_int),
            )

        msg = "Invalid binary layout for aioMtproto string session"
        raise ValueError(msg)

    def export_session_string(self) -> str:
        """Export session as a native aioMtproto Base64 string."""
        return self._encode(self._data)

    def export_string(self) -> str:
        """Backward-compatible alias."""
        return self.export_session_string()

    async def load(self) -> SessionData:
        return self._data

    async def save(self, data: SessionData) -> None:
        self._data = data
        self.session_string = self._encode(data)

    async def delete(self) -> None:
        self._data = SessionData()
        self.session_string = ""

    def __repr__(self) -> str:
        masked = (self.session_string[:10] + "...") if self.session_string else "empty"
        return f"<StringSession session={masked}>"
