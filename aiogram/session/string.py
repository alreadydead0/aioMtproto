"""
MTProto String Session implementation supporting native aiogram, Pyrogram (v1/v2), and Telethon formats.
"""

from __future__ import annotations

import base64
import ipaddress
import struct
from typing import Optional

from aiogram.mtproto.connection.dc import get_dc
from aiogram.mtproto.crypto.auth_key import AuthKey
from aiogram.session.base import BaseMTProtoSession, SessionData

STRING_SESSION_MAGIC = b"AIOG"  # Native header identifier


class StringSession(BaseMTProtoSession):
    """
    String-based in-memory MTProto session.
    Encodes and decodes session data to/from compact URL-safe Base64 strings.
    Automatically parses native aiogram, Pyrogram (v1 & v2), and Telethon string sessions.
    """

    def __init__(self, session_string: str = "") -> None:
        self.session_string = session_string.strip()
        self._data: SessionData = (
            self._decode(self.session_string) if self.session_string else SessionData()
        )

    @staticmethod
    def _encode(data: SessionData) -> str:
        """
        Encode SessionData into native URL-safe Base64 string.
        """
        if not data.auth_key:
            return ""

        # Resolve IP to 4 bytes (IPv4) or 16 bytes (IPv6)
        try:
            ip_obj = ipaddress.ip_address(data.server_address)
            ip_bytes = ip_obj.packed
        except ValueError:
            ip_bytes = b"\x00" * 4

        ip_len = len(ip_bytes)
        user_id = data.user_id or 0
        server_salt = data.server_salt or 0

        # Pack binary payload:
        # Magic (4s) + DC_ID (B) + is_test (?) + is_bot (?) + port (H) + ip_len (B) + ip_bytes + user_id (q) + server_salt (q) + auth_key (256s)
        header_fmt = f">4sBBB H B{ip_len}s qq 256s"
        packed = struct.pack(
            header_fmt,
            STRING_SESSION_MAGIC,
            data.dc_id,
            1 if data.is_test else 0,
            1 if data.is_bot else 0,
            data.port,
            ip_len,
            ip_bytes,
            user_id,
            server_salt,
            data.auth_key.key,
        )
        return base64.urlsafe_b64encode(packed).decode("ascii").rstrip("=")

    @staticmethod
    def _decode(session_string: str) -> SessionData:
        """
        Decode URL-safe Base64 string into SessionData.
        Supports native aiogram, Pyrogram (v1/v2), and Telethon string formats.
        """
        if not session_string:
            return SessionData()

        # Telethon format starts with '1' and uses standard Base64
        if session_string.startswith("1") and len(session_string) > 300:
            try:
                raw_tl = base64.urlsafe_b64decode(session_string[1:] + "==")
                if len(raw_tl) >= 263:
                    # >B 4s H 256s
                    dc_id, ip_raw, port, auth_key_raw = struct.unpack(">B4sH256s", raw_tl[:263])
                    ip_str = str(ipaddress.ip_address(ip_raw))
                    return SessionData(
                        dc_id=dc_id,
                        server_address=ip_str,
                        port=port,
                        auth_key=AuthKey(auth_key_raw),
                    )
            except Exception:
                pass

        # Add padding if needed
        padded = session_string + "=" * ((4 - len(session_string) % 4) % 4)
        try:
            raw = base64.urlsafe_b64decode(padded.encode("ascii"))
        except Exception:
            return SessionData()

        # 1. Native aiogram format (Starts with b"AIOG")
        if raw.startswith(STRING_SESSION_MAGIC) and len(raw) >= 270:
            try:
                dc_id, is_test_int, is_bot_int, port, ip_len = struct.unpack(">BBB H B", raw[4:10])
                ip_bytes = raw[10 : 10 + ip_len]
                user_id, server_salt, auth_key_bytes = struct.unpack(
                    ">qq 256s", raw[10 + ip_len : 10 + ip_len + 16 + 256]
                )
                try:
                    ip_str = str(ipaddress.ip_address(ip_bytes))
                except ValueError:
                    dc = get_dc(dc_id, is_test=bool(is_test_int))
                    ip_str = dc.ip
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
            except Exception:
                pass

        # 2. Pyrogram v2 format: >B?256sQ? (267 bytes) or >B?256sq?
        if len(raw) == 267:
            try:
                dc_id, is_test, auth_key_bytes, user_id, is_bot = struct.unpack(">B?256sQ?", raw)
                dc = get_dc(dc_id, is_test=is_test)
                return SessionData(
                    dc_id=dc_id,
                    server_address=dc.ip,
                    port=dc.port,
                    auth_key=AuthKey(auth_key_bytes),
                    user_id=user_id if user_id != 0 else None,
                    is_bot=is_bot,
                    is_test=is_test,
                )
            except Exception:
                pass

        # 3. Pyrogram v1 format: >B?256sI? or >B?256sI (262-263 bytes)
        if len(raw) in (262, 263):
            try:
                dc_id, is_test, auth_key_bytes, user_id = struct.unpack(">B?256sI", raw[:262])
                dc = get_dc(dc_id, is_test=is_test)
                return SessionData(
                    dc_id=dc_id,
                    server_address=dc.ip,
                    port=dc.port,
                    auth_key=AuthKey(auth_key_bytes),
                    user_id=user_id if user_id != 0 else None,
                    is_test=is_test,
                )
            except Exception:
                pass

        return SessionData()

    def export_string(self) -> str:
        """
        Export current session as a Base64 string.
        """
        return self._encode(self._data)

    async def load(self) -> SessionData:
        return self._data

    async def save(self, data: SessionData) -> None:
        self._data = data
        self.session_string = self._encode(data)

    async def delete(self) -> None:
        self._data = SessionData()
        self.session_string = ""
