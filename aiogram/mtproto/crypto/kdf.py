"""
MTProto 2.0 Key Derivation Function (KDF).
"""

from __future__ import annotations

import hashlib


def compute_kdf(auth_key: bytes, msg_key: bytes, is_client: bool) -> tuple[bytes, bytes]:
    """
    Derive AES key and IV for MTProto 2.0 message encryption/decryption.

    :param auth_key: 256-byte AuthKey.
    :param msg_key: 16-byte Message Key.
    :param is_client: True if the message was sent by the client, False if by the server.
    :return: (aes_key, aes_iv) both 32 bytes.
    """
    x = 0 if is_client else 8

    sha256_a = hashlib.sha256(msg_key + auth_key[x : x + 36]).digest()
    sha256_b = hashlib.sha256(auth_key[x + 40 : x + 76] + msg_key).digest()
    sha256_c = hashlib.sha256(auth_key[x + 120 : x + 120 + 36] + msg_key).digest()
    sha256_d = hashlib.sha256(msg_key + auth_key[x + 160 : x + 160 + 36]).digest()

    aes_key = sha256_a[:8] + sha256_b[8:24] + sha256_c[24:32]
    aes_iv = sha256_b[:8] + sha256_c[8:24] + sha256_d[24:32]

    return aes_key, aes_iv


def compute_msg_key(auth_key: bytes, plaintext: bytes, is_client: bool) -> bytes:
    """
    Compute MTProto 2.0 msg_key (16 bytes) from auth_key and plaintext.

    :param auth_key: 256-byte AuthKey.
    :param plaintext: Unencrypted payload (including salt, session_id, msg_id, seq_no, msg_len, inner_data, padding).
    :param is_client: True if client is sending, False if server is sending.
    :return: 16-byte msg_key.
    """
    x = 88 if is_client else 96
    return hashlib.sha256(auth_key[x : x + 32] + plaintext).digest()[:16]
