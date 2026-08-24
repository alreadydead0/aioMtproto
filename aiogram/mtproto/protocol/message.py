"""
MTProto Message packing, encryption, decryption, and parsing.
"""

from __future__ import annotations

import io
import os
import struct
from dataclasses import dataclass
from typing import TYPE_CHECKING

from aiogram.mtproto.crypto.aes_ige import (
    aes_ige_decrypt,
    aes_ige_encrypt,
    async_aes_ige_decrypt,
    async_aes_ige_encrypt,
)
from aiogram.mtproto.crypto.kdf import compute_kdf, compute_msg_key

if TYPE_CHECKING:
    from aiogram.mtproto.crypto.auth_key import AuthKey


@dataclass
class MTProtoMessage:
    """
    Decrypted inner MTProto message payload.
    """

    msg_id: int
    seq_no: int
    body: bytes


class MessageCodec:
    """
    Handles serialization and encryption of MTProto packets.
    """

    @staticmethod
    def pack_plain(msg_id: int, body: bytes) -> bytes:
        """
        Pack an unencrypted plain MTProto message (auth_key_id = 0).
        """
        # auth_key_id (8 bytes 0) + msg_id (8 bytes) + msg_len (4 bytes) + body
        header = struct.pack("<qqI", 0, msg_id, len(body))
        return header + body

    @staticmethod
    def unpack_plain(data: bytes) -> tuple[int, bytes]:
        """
        Unpack an unencrypted plain MTProto message.
        :return: (msg_id, body)
        """
        if len(data) < 20:
            msg = f"Plain message too short ({len(data)} bytes)"
            raise ValueError(msg)
        auth_key_id, msg_id, msg_len = struct.unpack("<qqI", data[:20])
        if auth_key_id != 0:
            msg = f"Expected auth_key_id=0 for plain message (got {auth_key_id})"
            raise ValueError(msg)
        body = data[20 : 20 + msg_len]
        return msg_id, body

    @staticmethod
    def pack_encrypted(
        auth_key: AuthKey,
        server_salt: int,
        session_id: int,
        msg_id: int,
        seq_no: int,
        body: bytes,
    ) -> bytes:
        """
        Pack and encrypt an MTProto 2.0 message synchronously.
        """
        # Header: salt (8) + session_id (8) + msg_id (8) + seq_no (4) + msg_len (4) + body
        inner_header = struct.pack("<qqqII", server_salt, session_id, msg_id, seq_no, len(body))
        unpadded = inner_header + body

        # MTProto 2.0 padding: 12 to 1024 bytes, and len(payload) % 16 == 0
        pad_len = 16 - (len(unpadded) % 16)
        if pad_len < 12:
            pad_len += 16
        padding = os.urandom(pad_len)
        plaintext = unpadded + padding

        # Calculate msg_key = SHA256(auth_key[88:120] + plaintext)[:16]
        msg_key = compute_msg_key(auth_key.key, plaintext, is_client=True)

        # Derive AES key and IV
        aes_key, aes_iv = compute_kdf(auth_key.key, msg_key, is_client=True)

        # Encrypt with AES-IGE
        ciphertext = aes_ige_encrypt(plaintext, aes_key, aes_iv)

        # Outer envelope: auth_key_id (8) + msg_key (16) + ciphertext
        return auth_key.key_id_bytes + msg_key + ciphertext

    @staticmethod
    async def async_pack_encrypted(
        auth_key: AuthKey,
        server_salt: int,
        session_id: int,
        msg_id: int,
        seq_no: int,
        body: bytes,
    ) -> bytes:
        """
        Pack and encrypt an MTProto 2.0 message asynchronously (offloading
        large payloads to thread pool).
        """
        inner_header = struct.pack("<qqqII", server_salt, session_id, msg_id, seq_no, len(body))
        unpadded = inner_header + body

        pad_len = 16 - (len(unpadded) % 16)
        if pad_len < 12:
            pad_len += 16
        padding = os.urandom(pad_len)
        plaintext = unpadded + padding

        msg_key = compute_msg_key(auth_key.key, plaintext, is_client=True)
        aes_key, aes_iv = compute_kdf(auth_key.key, msg_key, is_client=True)

        ciphertext = await async_aes_ige_encrypt(plaintext, aes_key, aes_iv)
        return auth_key.key_id_bytes + msg_key + ciphertext

    @staticmethod
    def unpack_encrypted(
        auth_key: AuthKey,
        session_id: int,
        data: bytes,
        is_client: bool = False,
    ) -> tuple[int, int, list[MTProtoMessage]]:
        """
        Decrypt and parse an MTProto 2.0 message from the server (or client when is_client=True).
        :return: (server_salt, server_session_id, list of messages)
        """
        if len(data) < 24:
            msg = f"Encrypted payload too short ({len(data)} bytes)"
            raise ValueError(msg)

        auth_key_id_bytes = data[:8]
        if auth_key_id_bytes != auth_key.key_id_bytes:
            msg = "Auth key ID mismatch"
            raise ValueError(msg)

        msg_key = data[8:24]
        ciphertext = data[24:]

        if len(ciphertext) % 16 != 0:
            msg = f"Ciphertext length must be a multiple of 16 (got {len(ciphertext)})"
            raise ValueError(msg)

        # Derive AES key and IV
        aes_key, aes_iv = compute_kdf(auth_key.key, msg_key, is_client=is_client)

        # Decrypt
        plaintext = aes_ige_decrypt(ciphertext, aes_key, aes_iv)

        # Validate msg_key
        expected_msg_key = compute_msg_key(auth_key.key, plaintext, is_client=is_client)
        if msg_key != expected_msg_key:
            msg = "Checksum mismatch: invalid msg_key in encrypted message"
            raise ValueError(msg)

        # Parse header
        salt, s_session_id, msg_id, seq_no, msg_len = struct.unpack("<qqqII", plaintext[:32])

        if len(plaintext) < 32 + msg_len:
            msg = f"Truncated message body ({len(plaintext)} < {32 + msg_len})"
            raise ValueError(msg)

        body = plaintext[32 : 32 + msg_len]

        # Check if container (0x73f1f8dc)
        messages: list[MTProtoMessage] = []
        if len(body) >= 8 and struct.unpack("<I", body[:4])[0] == 0x73F1F8DC:
            # Message Container
            count = struct.unpack("<I", body[4:8])[0]
            offset = 8
            for _ in range(count):
                c_msg_id, c_seq_no, c_len = struct.unpack("<qII", body[offset : offset + 16])
                offset += 16
                c_body = body[offset : offset + c_len]
                offset += c_len
                messages.append(MTProtoMessage(msg_id=c_msg_id, seq_no=c_seq_no, body=c_body))
        else:
            messages.append(MTProtoMessage(msg_id=msg_id, seq_no=seq_no, body=body))

        return salt, s_session_id, messages

    @staticmethod
    async def async_unpack_encrypted(
        auth_key: AuthKey,
        session_id: int,
        data: bytes,
        is_client: bool = False,
    ) -> tuple[int, int, list[MTProtoMessage]]:
        """
        Decrypt and parse an MTProto 2.0 message asynchronously.
        """
        if len(data) < 24:
            msg = f"Encrypted payload too short ({len(data)} bytes)"
            raise ValueError(msg)

        auth_key_id_bytes = data[:8]
        if auth_key_id_bytes != auth_key.key_id_bytes:
            msg = "Auth key ID mismatch"
            raise ValueError(msg)

        msg_key = data[8:24]
        ciphertext = data[24:]

        if len(ciphertext) % 16 != 0:
            msg = f"Ciphertext length must be a multiple of 16 (got {len(ciphertext)})"
            raise ValueError(msg)

        aes_key, aes_iv = compute_kdf(auth_key.key, msg_key, is_client=is_client)

        plaintext = await async_aes_ige_decrypt(ciphertext, aes_key, aes_iv)

        expected_msg_key = compute_msg_key(auth_key.key, plaintext, is_client=is_client)
        if msg_key != expected_msg_key:
            msg = "Checksum mismatch: invalid msg_key in encrypted message"
            raise ValueError(msg)

        salt, s_session_id, msg_id, seq_no, msg_len = struct.unpack("<qqqII", plaintext[:32])

        if len(plaintext) < 32 + msg_len:
            msg = f"Truncated message body ({len(plaintext)} < {32 + msg_len})"
            raise ValueError(msg)

        body = plaintext[32 : 32 + msg_len]

        messages: list[MTProtoMessage] = []
        if len(body) >= 8 and struct.unpack("<I", body[:4])[0] == 0x73F1F8DC:
            count = struct.unpack("<I", body[4:8])[0]
            offset = 8
            for _ in range(count):
                c_msg_id, c_seq_no, c_len = struct.unpack("<qII", body[offset : offset + 16])
                offset += 16
                c_body = body[offset : offset + c_len]
                offset += c_len
                messages.append(MTProtoMessage(msg_id=c_msg_id, seq_no=c_seq_no, body=c_body))
        else:
            messages.append(MTProtoMessage(msg_id=msg_id, seq_no=seq_no, body=body))

        return salt, s_session_id, messages
