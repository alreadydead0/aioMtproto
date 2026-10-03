# ruff: noqa: T201
"""
Tests for MTProto cryptographic primitives (AES-IGE, DH, Pollard's rho, RSA, KDF, AuthKey).
"""

import hashlib
import os

import pytest

from aiogram.mtproto.crypto.aes_ige import (
    PureAES,
    aes_ige_decrypt,
    aes_ige_encrypt,
    async_aes_ige_decrypt,
    async_aes_ige_encrypt,
)
from aiogram.mtproto.crypto.auth_key import AuthKey
from aiogram.mtproto.crypto.dh import (
    check_dh_g,
    check_dh_params,
    compute_auth_key,
    factorize_pq,
    generate_dh_b,
)
from aiogram.mtproto.crypto.kdf import compute_kdf, compute_msg_key
from aiogram.mtproto.crypto.rsa import TELEGRAM_RSA_KEYS, find_rsa_key, rsa_encrypt


def test_pure_aes_roundtrip() -> None:
    key = os.urandom(32)
    block = b"1234567890abcdef"
    cipher = PureAES(key)
    encrypted = cipher.encrypt_block(block)
    decrypted = cipher.decrypt_block(encrypted)
    assert decrypted == block


def test_aes_ige_roundtrip() -> None:
    key = os.urandom(32)
    iv = os.urandom(32)
    plaintext = b"0123456789abcdef" * 10  # exactly 160 bytes
    assert len(plaintext) % 16 == 0

    ciphertext = aes_ige_encrypt(plaintext, key, iv)
    assert len(ciphertext) == len(plaintext)
    assert ciphertext != plaintext

    decrypted = aes_ige_decrypt(ciphertext, key, iv)
    assert decrypted == plaintext


@pytest.mark.asyncio
async def test_async_aes_ige_roundtrip_large() -> None:
    key = os.urandom(32)
    iv = os.urandom(32)
    # 128 KiB (> 64 KiB threshold to trigger thread-pool offloading)
    plaintext = os.urandom(128 * 1024)

    ciphertext = await async_aes_ige_encrypt(plaintext, key, iv)
    assert len(ciphertext) == len(plaintext)
    assert ciphertext != plaintext

    decrypted = await async_aes_ige_decrypt(ciphertext, key, iv)
    assert decrypted == plaintext


def test_backend_status() -> None:
    from aiogram.mtproto.crypto import aes_ige

    print(f"\n[BACKEND STATUS] TGCRYPTO: {aes_ige._HAS_TGCRYPTO}")
    print(f"[BACKEND STATUS] CRYPTG: {aes_ige._HAS_CRYPTG}")
    print(f"[BACKEND STATUS] CRYPTOGRAPHY: {aes_ige._HAS_CRYPTOGRAPHY}")
    print(f"[BACKEND STATUS] PYCRYPTODOME: {aes_ige._HAS_PYCRYPTODOME}")
    assert aes_ige._HAS_TGCRYPTO is True


def test_aes_ige_benchmark_5_1(capsys: pytest.CaptureFixture[str]) -> None:
    import time

    key, iv = os.urandom(32), os.urandom(32)
    data = os.urandom(10 * 1024 * 1024)  # 10 MB

    start = time.perf_counter()
    for _ in range(10):
        aes_ige_encrypt(data, key, iv)
    elapsed = time.perf_counter() - start
    speed = 100 / elapsed
    print(f"\n[CRYPTO BENCHMARK] 100MB Encrypt Throughput: {speed:.1f} MB/s in {elapsed:.4f}s")
    assert speed > 30.0


def test_factorize_pq() -> None:
    # 64-bit PQ test vector with verified prime factors
    p_expected = 49979687
    q_expected = 49979693
    pq = p_expected * q_expected

    p, q = factorize_pq(pq)
    assert p * q == pq
    assert p <= q
    assert p == p_expected
    assert q == q_expected


def test_auth_key_and_kdf() -> None:
    auth_key_bytes = os.urandom(256)
    auth_key = AuthKey(auth_key_bytes)

    assert len(auth_key.key_id_bytes) == 8
    assert isinstance(auth_key.key_id, int)

    plaintext = os.urandom(64)
    msg_key_client = compute_msg_key(auth_key.key, plaintext, is_client=True)
    assert len(msg_key_client) == 16

    aes_key_c, aes_iv_c = compute_kdf(auth_key.key, msg_key_client, is_client=True)
    assert len(aes_key_c) == 32
    assert len(aes_iv_c) == 32

    # Server perspective
    msg_key_server = compute_msg_key(auth_key.key, plaintext, is_client=False)
    assert len(msg_key_server) == 16
    aes_key_s, aes_iv_s = compute_kdf(auth_key.key, msg_key_server, is_client=False)
    assert len(aes_key_s) == 32
    assert len(aes_iv_s) == 32


def test_rsa_encryption() -> None:
    key = TELEGRAM_RSA_KEYS[0]
    matched = find_rsa_key([key.fingerprint])
    assert matched is not None
    assert matched.fingerprint == key.fingerprint

    data = b"sample_pq_inner_data_for_handshake"
    encrypted = rsa_encrypt(data, key)
    assert len(encrypted) == 256


def test_rsa_fingerprint_computation() -> None:
    from aiogram.raw.core.primitives import write_bytes
    import struct

    # Test independent fingerprint calculation on verified production keys (4, 5, 6, 7)
    for key in TELEGRAM_RSA_KEYS[4:]:
        n_bytes = key.n.to_bytes((key.n.bit_length() + 7) // 8, "big")
        e_bytes = key.e.to_bytes((key.e.bit_length() + 7) // 8, "big")
        serialized = write_bytes(n_bytes) + write_bytes(e_bytes)
        digest = hashlib.sha1(serialized).digest()
        computed_fp = struct.unpack("<q", digest[-8:])[0]
        assert computed_fp == key.fingerprint


def test_dh_security_validation_negative_cases() -> None:
    # 1. Invalid generator g
    assert check_dh_params(1 << 2045, g=1) is False
    assert check_dh_params(1 << 2045, g=8) is False
    assert check_dh_params(1 << 2045, g=100) is False

    # 2. Invalid DH prime bit length (< 2040 or > 2048)
    small_prime = (1 << 1024) - 1
    assert check_dh_params(small_prime, g=3) is False

    large_prime = (1 << 4096) - 1
    assert check_dh_params(large_prime, g=3) is False

    # 3. Valid 2048-bit prime bounds
    valid_prime = (1 << 2047) + 1
    assert check_dh_params(valid_prime, g=3) is True

    # 4. Check g_a bounds
    min_bound = 1 << (2048 - 64)
    assert check_dh_g(min_bound - 1, valid_prime) is False
    assert check_dh_g(min_bound, valid_prime) is True
    assert check_dh_g(valid_prime - min_bound, valid_prime) is True
    assert check_dh_g(valid_prime - min_bound + 1, valid_prime) is False


def test_aes_ige_corrupted_ciphertext_detection() -> None:
    key = os.urandom(32)
    iv = os.urandom(32)
    plaintext = b"A" * 64

    ciphertext = aes_ige_encrypt(plaintext, key, iv)
    # Corrupt last byte of ciphertext
    corrupted = ciphertext[:-1] + bytes([ciphertext[-1] ^ 0xFF])

    decrypted = aes_ige_decrypt(corrupted, key, iv)
    assert decrypted != plaintext
