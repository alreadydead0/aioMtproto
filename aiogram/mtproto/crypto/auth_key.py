"""
MTProto AuthKey representation and sequence number management.
"""

from __future__ import annotations

import hashlib
import struct


class AuthKey:
    """
    Represents a 2048-bit (256-byte) MTProto AuthKey.
    """

    def __init__(self, key: bytes) -> None:
        if len(key) != 256:
            msg = f"AuthKey must be exactly 256 bytes (got {len(key)})"
            raise ValueError(msg)
        self.key = key
        # key_id is lower 64 bits of SHA1(key), as signed 64-bit int and bytes
        sha1 = hashlib.sha1(key).digest()
        self.key_id_bytes = sha1[-8:]
        self.key_id: int = struct.unpack("<q", self.key_id_bytes)[0]
        self.aux_hash = sha1[:8]

    def calc_new_nonce_hash(self, new_nonce: bytes, number: int) -> bytes:
        """
        Calculate new_nonce_hash for handshake verification:
        SHA1(new_nonce + chr(number) + aux_hash)[-16:]
        """
        return hashlib.sha1(new_nonce + bytes([number]) + self.aux_hash).digest()[-16:]

    def __repr__(self) -> str:
        return "<AuthKey>"
