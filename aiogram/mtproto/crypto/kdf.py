"""
MTProto 2.0 Key Derivation Function (KDF).
"""

from __future__ import annotations

import hashlib
from typing import Any, cast

_HAS_HYPERCRYPTO = False
_hypercrypto: Any = None
try:
    import hypercrypto as _hypercrypto  # type: ignore[import-untyped,no-redef]

    _HAS_HYPERCRYPTO = hasattr(_hypercrypto, "kdf") and hasattr(_hypercrypto, "sha256")
except ImportError:
    pass


def compute_kdf(auth_key: bytes, msg_key: bytes, is_client: bool) -> tuple[bytes, bytes]:
    """
    Derive AES key and IV for MTProto 2.0 message encryption/decryption.

    Official MTProto 2.0 spec (https://core.telegram.org/mtproto/description):
        x = 0  (client → server)  or  8  (server → client)
        sha256_a = SHA256(msg_key + substr(auth_key, x, 36))
        sha256_b = SHA256(substr(auth_key, 40 + x, 36) + msg_key)

        aes_key  = sha256_a[0:8] + sha256_b[8:24] + sha256_a[24:32]
        aes_iv   = sha256_b[0:8] + sha256_a[8:24] + sha256_b[24:32]

    :param auth_key: 256-byte AuthKey.
    :param msg_key: 16-byte Message Key.
    :param is_client: True if the message was sent by the client, False if by the server.
    :return: (aes_key, aes_iv) both 32 bytes.
    """
    if _HAS_HYPERCRYPTO and _hypercrypto is not None:
        return cast("tuple[bytes, bytes]", _hypercrypto.kdf(auth_key, msg_key, is_client))

    x = 0 if is_client else 8

    sha256_a = hashlib.sha256(msg_key + auth_key[x : x + 36]).digest()
    sha256_b = hashlib.sha256(auth_key[40 + x : 40 + x + 36] + msg_key).digest()

    aes_key = sha256_a[0:8] + sha256_b[8:24] + sha256_a[24:32]
    aes_iv = sha256_b[0:8] + sha256_a[8:24] + sha256_b[24:32]

    return aes_key, aes_iv


def compute_msg_key(auth_key: bytes, plaintext: bytes, is_client: bool) -> bytes:
    """
    Compute MTProto 2.0 msg_key (16 bytes) from auth_key and plaintext.

    Official MTProto 2.0 spec:
        x = 0  (client → server)  or  8  (server → client)
        msg_key_large = SHA256(substr(auth_key, 88 + x, 32) + plaintext)
        msg_key = substr(msg_key_large, 8, 16)

    :param auth_key: 256-byte AuthKey.
    :param plaintext: Unencrypted payload (including salt, session_id,
        msg_id, seq_no, msg_len, inner_data, padding).
    :param is_client: True if client is sending, False if server is sending.
    :return: 16-byte msg_key (middle 128 bits of SHA256).
    """
    x = 0 if is_client else 8
    if _HAS_HYPERCRYPTO and _hypercrypto is not None:
        msg_key_large = _hypercrypto.sha256(auth_key[88 + x : 88 + x + 32] + plaintext)
        return cast(bytes, msg_key_large[8:24])

    msg_key_large = hashlib.sha256(auth_key[88 + x : 88 + x + 32] + plaintext).digest()
    return msg_key_large[8:24]
