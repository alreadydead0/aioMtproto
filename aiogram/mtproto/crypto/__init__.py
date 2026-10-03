"""
MTProto cryptographic primitives and helpers.
"""

from __future__ import annotations

from .aes_ige import (
    aes_ige_decrypt,
    aes_ige_encrypt,
    async_aes_ige_decrypt,
    async_aes_ige_encrypt,
)
from .auth_key import AuthKey
from .dh import check_dh_g, check_dh_params, compute_auth_key, factorize_pq, generate_dh_b
from .kdf import compute_kdf, compute_msg_key
from .rsa import TELEGRAM_RSA_KEYS, RSAKey, find_rsa_key, rsa_encrypt
from .srp import compute_srp_password

__all__ = (
    "AuthKey",
    "RSAKey",
    "TELEGRAM_RSA_KEYS",
    "aes_ige_decrypt",
    "aes_ige_encrypt",
    "async_aes_ige_decrypt",
    "async_aes_ige_encrypt",
    "check_dh_g",
    "check_dh_params",
    "compute_auth_key",
    "compute_kdf",
    "compute_msg_key",
    "compute_srp_password",
    "factorize_pq",
    "find_rsa_key",
    "generate_dh_b",
    "rsa_encrypt",
)
