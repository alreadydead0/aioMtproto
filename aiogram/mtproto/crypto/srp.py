"""
MTProto 2FA SRP (Secure Remote Password) protocol implementation.
"""

from __future__ import annotations

import hashlib
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiogram.raw.types import (
        AccountPassword,
        InputCheckPasswordSRP,
        PasswordKdfAlgoSHA256SHA256PBKDF2HMACSHA512,
    )


def _sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def _sh(data: bytes, salt: bytes) -> bytes:
    """
    SH(data, salt) := H(salt | data | salt)
    """
    return _sha256(salt + data + salt)


def _ph1(password: str, salt1: bytes, salt2: bytes) -> bytes:
    """
    PH1(password, salt1, salt2) := SH(SH(password, salt1), salt2)
    """
    pwd_bytes = password.encode("utf-8")
    return _sh(_sh(pwd_bytes, salt1), salt2)


def _ph2(password: str, salt1: bytes, salt2: bytes) -> bytes:
    """
    PH2(password, salt1, salt2) := SH(pbkdf2(sha512, PH1(password, salt1, salt2), salt1, 100000), salt2)
    """
    ph1 = _ph1(password, salt1, salt2)
    pbkdf2_hash = hashlib.pbkdf2_hmac("sha512", ph1, salt1, 100000)
    return _sh(pbkdf2_hash, salt2)


def _pad(data: bytes, length: int) -> bytes:
    if len(data) < length:
        return data.rjust(length, b"\x00")
    return data


def compute_srp_password(
    password: str,
    account_password: AccountPassword,
) -> InputCheckPasswordSRP:
    """
    Compute SRP InputCheckPasswordSRP from account.Password and user plaintext password
    according to Telegram's SRP 6a specification (core.telegram.org/api/srp).
    """
    from aiogram.raw.types import InputCheckPasswordSRP

    algo: PasswordKdfAlgoSHA256SHA256PBKDF2HMACSHA512 | None = account_password.current_algo  # type: ignore[assignment]
    if not algo:
        msg = "Account does not have a valid 2FA password algorithm"
        raise ValueError(msg)

    srp_B = account_password.srp_B
    srp_id = account_password.srp_id

    if not srp_B or srp_id is None:
        msg = "Missing srp_B or srp_id in account.Password"
        raise ValueError(msg)

    p_bytes = algo.p
    p_len = len(p_bytes)
    p = int.from_bytes(p_bytes, "big")
    g = algo.g
    g_bytes = g.to_bytes(p_len, "big")

    salt1 = algo.salt1
    salt2 = algo.salt2

    # 1. Compute password hash x using PH2
    x_bytes = _ph2(password, salt1, salt2)
    x = int.from_bytes(x_bytes, "big")

    # 2. Compute v = g^x mod p
    v = pow(g, x, p)

    # 3. Compute k = H(p | g)
    k_bytes = _sha256(p_bytes + g_bytes)
    k = int.from_bytes(k_bytes, "big")

    # 4. Generate random client private key a (2048 bits / 256 bytes)
    a_bytes = os.urandom(256)
    a = int.from_bytes(a_bytes, "big")

    # 5. Compute A = g^a mod p
    A_int = pow(g, a, p)
    A = _pad(A_int.to_bytes((A_int.bit_length() + 7) // 8 or 1, "big"), p_len)

    # 6. Parse server B and validate
    B_int = int.from_bytes(srp_B, "big")
    if B_int <= 0 or B_int >= p:
        msg = "Invalid server SRP B value"
        raise ValueError(msg)

    # 7. Compute u = H(A | B)
    B_padded = _pad(srp_B, p_len)
    u_bytes = _sha256(A + B_padded)
    u = int.from_bytes(u_bytes, "big")
    if u == 0:
        msg = "Computed SRP u is zero"
        raise ValueError(msg)

    # 8. Compute premaster secret S = (B - k*v)^(a + u*x) mod p
    base = (B_int - k * v) % p
    exp = a + u * x
    S_int = pow(base, exp, p)
    S = _pad(S_int.to_bytes((S_int.bit_length() + 7) // 8 or 1, "big"), p_len)

    # 9. Compute key K = H(S)
    K = _sha256(S)

    # 10. Compute M1 = H(H(p) ^ H(g) | H(salt1) | H(salt2) | A | B | K)
    p_hash = _sha256(p_bytes)
    g_hash = _sha256(g_bytes)
    p_xor_g = bytes(b1 ^ b2 for b1, b2 in zip(p_hash, g_hash))

    M1 = _sha256(p_xor_g + _sha256(salt1) + _sha256(salt2) + A + B_padded + K)

    return InputCheckPasswordSRP(srp_id=srp_id, A=A, M1=M1)
