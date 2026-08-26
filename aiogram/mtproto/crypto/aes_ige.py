"""
AES-IGE (Infinite Garble Extension) mode implementation for MTProto.
"""

from __future__ import annotations

import asyncio
import os
from collections.abc import Callable
from typing import Any

# Check for cryptographic backends in order of performance
_HAS_HYPERCRYPTO = False
_HAS_TGCRYPTO = False
_HAS_CRYPTG = False
_HAS_PYCRYPTODOME_IGE = False
_HAS_CRYPTOGRAPHY = False
_HAS_PYCRYPTODOME = False

_hypercrypto: Any = None
try:
    import hypercrypto as _hypercrypto

    _HAS_HYPERCRYPTO = hasattr(_hypercrypto, "ige256_encrypt") and hasattr(
        _hypercrypto, "ige256_decrypt"
    )
except ImportError:
    pass

_tgcrypto: Any = None
try:
    import tgcrypto as _tgcrypto  # type: ignore[import-untyped,no-redef]

    _HAS_TGCRYPTO = hasattr(_tgcrypto, "ige256_encrypt") and hasattr(_tgcrypto, "ige256_decrypt")
except ImportError:
    pass

_cryptg: Any = None
if not _HAS_TGCRYPTO:
    try:
        import cryptg as _cryptg  # type: ignore[import-not-found,no-redef]

        _HAS_CRYPTG = hasattr(_cryptg, "encrypt_ige") and hasattr(_cryptg, "decrypt_ige")
    except ImportError:
        pass

_AES: Any = None
try:
    from Cryptodome.Cipher import AES as _AES

    _HAS_PYCRYPTODOME = True
except ImportError:
    try:
        from Crypto.Cipher import AES as _AES  # type: ignore[import-not-found,no-redef]

        _HAS_PYCRYPTODOME = True
    except ImportError:
        pass

if _HAS_PYCRYPTODOME and hasattr(_AES, "MODE_IGE"):
    _HAS_PYCRYPTODOME_IGE = True

try:
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

    _HAS_CRYPTOGRAPHY = True
except ImportError:
    pass


def _xor(a: bytes, b: bytes) -> bytes:
    """XOR two byte strings of equal length."""
    return bytes(x ^ y for x, y in zip(a, b, strict=True))


class PureAES:
    """
    Pure Python AES-256 implementation as a guaranteed fallback.
    """

    # S-Box
    SBOX = (
        0x63,
        0x7C,
        0x77,
        0x7B,
        0xF2,
        0x6B,
        0x6F,
        0xC5,
        0x30,
        0x01,
        0x67,
        0x2B,
        0xFE,
        0xD7,
        0xAB,
        0x76,
        0xCA,
        0x82,
        0xC9,
        0x7D,
        0xFA,
        0x59,
        0x47,
        0xF0,
        0xAD,
        0xD4,
        0xA2,
        0xAF,
        0x9C,
        0xA4,
        0x72,
        0xC0,
        0xB7,
        0xFD,
        0x93,
        0x26,
        0x36,
        0x3F,
        0xF7,
        0xCC,
        0x34,
        0xA5,
        0xE5,
        0xF1,
        0x71,
        0xD8,
        0x31,
        0x15,
        0x04,
        0xC7,
        0x23,
        0xC3,
        0x18,
        0x96,
        0x05,
        0x9A,
        0x07,
        0x12,
        0x80,
        0xE2,
        0xEB,
        0x27,
        0xB2,
        0x75,
        0x09,
        0x83,
        0x2C,
        0x1A,
        0x1B,
        0x6E,
        0x5A,
        0xA0,
        0x52,
        0x3B,
        0xD6,
        0xB3,
        0x29,
        0xE3,
        0x2F,
        0x84,
        0x53,
        0xD1,
        0x00,
        0xED,
        0x20,
        0xFC,
        0xB1,
        0x5B,
        0x6A,
        0xCB,
        0xBE,
        0x39,
        0x4A,
        0x4C,
        0x58,
        0xCF,
        0xD0,
        0xEF,
        0xAA,
        0xFB,
        0x43,
        0x4D,
        0x33,
        0x85,
        0x45,
        0xF9,
        0x02,
        0x7F,
        0x50,
        0x3C,
        0x9F,
        0xA8,
        0x51,
        0xA3,
        0x40,
        0x8F,
        0x92,
        0x9D,
        0x38,
        0xF5,
        0xBC,
        0xB6,
        0xDA,
        0x21,
        0x10,
        0xFF,
        0xF3,
        0xD2,
        0xCD,
        0x0C,
        0x13,
        0xEC,
        0x5F,
        0x97,
        0x44,
        0x17,
        0xC4,
        0xA7,
        0x7E,
        0x3D,
        0x64,
        0x5D,
        0x19,
        0x73,
        0x60,
        0x81,
        0x4F,
        0xDC,
        0x22,
        0x2A,
        0x90,
        0x88,
        0x46,
        0xEE,
        0xB8,
        0x14,
        0xDE,
        0x5E,
        0x0B,
        0xDB,
        0xE0,
        0x32,
        0x3A,
        0x0A,
        0x49,
        0x06,
        0x24,
        0x5C,
        0xC2,
        0xD3,
        0xAC,
        0x62,
        0x91,
        0x95,
        0xE4,
        0x79,
        0xE7,
        0xC8,
        0x37,
        0x6D,
        0x8D,
        0xD5,
        0x4E,
        0xA9,
        0x6C,
        0x56,
        0xF4,
        0xEA,
        0x65,
        0x7A,
        0xAE,
        0x08,
        0xBA,
        0x78,
        0x25,
        0x2E,
        0x1C,
        0xA6,
        0xB4,
        0xC6,
        0xE8,
        0xDD,
        0x74,
        0x1F,
        0x4B,
        0xBD,
        0x8B,
        0x8A,
        0x70,
        0x3E,
        0xB5,
        0x66,
        0x48,
        0x03,
        0xF6,
        0x0E,
        0x61,
        0x35,
        0x57,
        0xB9,
        0x86,
        0xC1,
        0x1D,
        0x9E,
        0xE1,
        0xF8,
        0x98,
        0x11,
        0x69,
        0xD9,
        0x8E,
        0x94,
        0x9B,
        0x1E,
        0x87,
        0xE9,
        0xCE,
        0x55,
        0x28,
        0xDF,
        0x8C,
        0xA1,
        0x89,
        0x0D,
        0xBF,
        0xE6,
        0x42,
        0x68,
        0x41,
        0x99,
        0x2D,
        0x0F,
        0xB0,
        0x54,
        0xBB,
        0x16,
    )
    _inv_sbox_list = [0] * 256
    for i, v in enumerate(SBOX):
        _inv_sbox_list[v] = i
    INV_SBOX = tuple(_inv_sbox_list)

    RCON = (
        0x00,
        0x01,
        0x02,
        0x04,
        0x08,
        0x10,
        0x20,
        0x40,
        0x80,
        0x1B,
        0x36,
        0x6C,
        0xD8,
        0xAB,
        0x4D,
        0x9A,
    )

    def __init__(self, key: bytes) -> None:
        self.key = key
        self.nk = len(key) // 4
        self.nr = self.nk + 6
        self._key_expansion()

    def _sub_word(self, word: int) -> int:
        return (
            (self.SBOX[(word >> 24) & 0xFF] << 24)
            | (self.SBOX[(word >> 16) & 0xFF] << 16)
            | (self.SBOX[(word >> 8) & 0xFF] << 8)
            | self.SBOX[word & 0xFF]
        )

    def _rot_word(self, word: int) -> int:
        return ((word << 8) & 0xFFFFFFFF) | (word >> 24)

    def _key_expansion(self) -> None:
        w: list[int] = []
        for i in range(self.nk):
            w.append(
                (self.key[4 * i] << 24)
                | (self.key[4 * i + 1] << 16)
                | (self.key[4 * i + 2] << 8)
                | self.key[4 * i + 3]
            )
        for i in range(self.nk, 4 * (self.nr + 1)):
            temp = w[i - 1]
            if i % self.nk == 0:
                temp = self._sub_word(self._rot_word(temp)) ^ (self.RCON[i // self.nk] << 24)
            elif self.nk > 6 and (i % self.nk == 4):
                temp = self._sub_word(temp)
            w.append(w[i - self.nk] ^ temp)
        self.expanded_key = w

    @staticmethod
    def _xtime(a: int) -> int:
        return (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else ((a << 1) & 0xFF)

    def encrypt_block(self, block: bytes) -> bytes:
        state = [[block[r + 4 * c] for c in range(4)] for r in range(4)]

        # AddRoundKey 0
        for c in range(4):
            k = self.expanded_key[c]
            for r in range(4):
                state[r][c] ^= (k >> (24 - 8 * r)) & 0xFF

        for rnd in range(1, self.nr):
            # SubBytes
            for r in range(4):
                for c in range(4):
                    state[r][c] = self.SBOX[state[r][c]]
            # ShiftRows
            state[1] = state[1][1:] + state[1][:1]
            state[2] = state[2][2:] + state[2][:2]
            state[3] = state[3][3:] + state[3][:3]
            # MixColumns
            for c in range(4):
                a0, a1, a2, a3 = state[0][c], state[1][c], state[2][c], state[3][c]
                t = a0 ^ a1 ^ a2 ^ a3
                state[0][c] ^= t ^ self._xtime(a0 ^ a1)
                state[1][c] ^= t ^ self._xtime(a1 ^ a2)
                state[2][c] ^= t ^ self._xtime(a2 ^ a3)
                state[3][c] ^= t ^ self._xtime(a3 ^ a0)
            # AddRoundKey
            for c in range(4):
                k = self.expanded_key[rnd * 4 + c]
                for r in range(4):
                    state[r][c] ^= (k >> (24 - 8 * r)) & 0xFF

        # Final round
        for r in range(4):
            for c in range(4):
                state[r][c] = self.SBOX[state[r][c]]
        state[1] = state[1][1:] + state[1][:1]
        state[2] = state[2][2:] + state[2][:2]
        state[3] = state[3][3:] + state[3][:3]
        for c in range(4):
            k = self.expanded_key[self.nr * 4 + c]
            for r in range(4):
                state[r][c] ^= (k >> (24 - 8 * r)) & 0xFF

        out = bytearray(16)
        for c in range(4):
            for r in range(4):
                out[c * 4 + r] = state[r][c]
        return bytes(out)

    @staticmethod
    def _mul(a: int, b: int) -> int:
        p = 0
        for _ in range(8):
            if b & 1:
                p ^= a
            hi = a & 0x80
            a = (a << 1) & 0xFF
            if hi:
                a ^= 0x1B
            b >>= 1
        return p

    def decrypt_block(self, block: bytes) -> bytes:
        state = [[block[r + 4 * c] for c in range(4)] for r in range(4)]

        # AddRoundKey Nr
        for c in range(4):
            k = self.expanded_key[self.nr * 4 + c]
            for r in range(4):
                state[r][c] ^= (k >> (24 - 8 * r)) & 0xFF

        for rnd in range(self.nr - 1, 0, -1):
            # InvShiftRows
            state[1] = state[1][-1:] + state[1][:-1]
            state[2] = state[2][-2:] + state[2][:-2]
            state[3] = state[3][-3:] + state[3][:-3]
            # InvSubBytes
            for r in range(4):
                for c in range(4):
                    state[r][c] = self.INV_SBOX[state[r][c]]
            # AddRoundKey
            for c in range(4):
                k = self.expanded_key[rnd * 4 + c]
                for r in range(4):
                    state[r][c] ^= (k >> (24 - 8 * r)) & 0xFF
            # InvMixColumns
            for c in range(4):
                s0, s1, s2, s3 = state[0][c], state[1][c], state[2][c], state[3][c]
                state[0][c] = (
                    self._mul(s0, 0x0E)
                    ^ self._mul(s1, 0x0B)
                    ^ self._mul(s2, 0x0D)
                    ^ self._mul(s3, 0x09)
                )
                state[1][c] = (
                    self._mul(s0, 0x09)
                    ^ self._mul(s1, 0x0E)
                    ^ self._mul(s2, 0x0B)
                    ^ self._mul(s3, 0x0D)
                )
                state[2][c] = (
                    self._mul(s0, 0x0D)
                    ^ self._mul(s1, 0x09)
                    ^ self._mul(s2, 0x0E)
                    ^ self._mul(s3, 0x0B)
                )
                state[3][c] = (
                    self._mul(s0, 0x0B)
                    ^ self._mul(s1, 0x0D)
                    ^ self._mul(s2, 0x09)
                    ^ self._mul(s3, 0x0E)
                )

        # InvShiftRows
        state[1] = state[1][-1:] + state[1][:-1]
        state[2] = state[2][-2:] + state[2][:-2]
        state[3] = state[3][-3:] + state[3][:-3]
        # InvSubBytes
        for r in range(4):
            for c in range(4):
                state[r][c] = self.INV_SBOX[state[r][c]]
        # AddRoundKey 0
        for c in range(4):
            k = self.expanded_key[c]
            for r in range(4):
                state[r][c] ^= (k >> (24 - 8 * r)) & 0xFF

        out = bytearray(16)
        for c in range(4):
            for r in range(4):
                out[c * 4 + r] = state[r][c]
        return bytes(out)


def _get_cipher_ecb(key: bytes) -> tuple[Callable[[bytes], bytes], Callable[[bytes], bytes]]:
    """Returns encrypt_block and decrypt_block functions."""
    if _HAS_CRYPTOGRAPHY:
        encryptor = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend()).encryptor()
        decryptor = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend()).decryptor()
        return encryptor.update, decryptor.update
    if _HAS_PYCRYPTODOME:
        cipher = _AES.new(key, _AES.MODE_ECB)
        return cipher.encrypt, cipher.decrypt
    pure = PureAES(key)
    return pure.encrypt_block, pure.decrypt_block


# Threshold above which crypto is offloaded to a thread pool
# to avoid blocking the event loop on large file chunks (e.g. 512 KiB).
CRYPTO_THREAD_POOL_THRESHOLD = 64 * 1024


def aes_ige_encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    """
    Encrypt data using AES-256-IGE mode.

    :param data: Plaintext data (must be 16-byte aligned).
    :param key: 32-byte AES key.
    :param iv: 32-byte IV (16 bytes IV1 + 16 bytes IV2).
    :return: Encrypted ciphertext.
    """
    if len(data) % 16 != 0:
        msg = f"Data length must be a multiple of 16 bytes (got {len(data)})"
        raise ValueError(msg)
    if len(key) != 32:
        msg = f"Key length must be 32 bytes (got {len(key)})"
        raise ValueError(msg)
    if len(iv) != 32:
        msg = f"IV length must be 32 bytes (got {len(iv)})"
        raise ValueError(msg)

    # Ultra-Fast Tier 0: hypercrypto (Vectorized SIMD & hardware-accelerated Rust)
    if _HAS_HYPERCRYPTO and _hypercrypto is not None:
        return bytes(_hypercrypto.ige256_encrypt(data, key, iv))

    # Fast Tier 1: tgcrypto (C-accelerated whole buffer)
    if _HAS_TGCRYPTO and _tgcrypto is not None:
        return bytes(_tgcrypto.ige256_encrypt(data, key, iv))

    # Fast Tier 2: cryptg (C-accelerated whole buffer)
    if _HAS_CRYPTG and _cryptg is not None:
        return bytes(_cryptg.encrypt_ige(data, key, iv))

    # Fast Tier 3: PyCryptodome / Cryptodome MODE_IGE (C-accelerated whole buffer)
    if _HAS_PYCRYPTODOME_IGE and _AES is not None:
        cipher = _AES.new(key, _AES.MODE_IGE, iv)
        return bytes(cipher.encrypt(data))

    # Fallback Tier: Block-by-block ECB (cryptography or PureAES)
    encrypt_block, _ = _get_cipher_ecb(key)
    iv1 = iv[:16]
    iv2 = iv[16:]

    out = bytearray(len(data))
    for offset in range(0, len(data), 16):
        chunk = data[offset : offset + 16]
        # c_i = E(p_i ^ c_{i-1}) ^ m_{i-1}
        x = _xor(chunk, iv1)
        y = encrypt_block(x)
        c = _xor(y, iv2)
        out[offset : offset + 16] = c
        iv1 = c
        iv2 = chunk

    return bytes(out)


def aes_ige_decrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    """
    Decrypt data using AES-256-IGE mode.

    :param data: Ciphertext data (must be 16-byte aligned).
    :param key: 32-byte AES key.
    :param iv: 32-byte IV (16 bytes IV1 + 16 bytes IV2).
    :return: Decrypted plaintext.
    """
    if len(data) % 16 != 0:
        msg = f"Data length must be a multiple of 16 bytes (got {len(data)})"
        raise ValueError(msg)
    if len(key) != 32:
        msg = f"Key length must be 32 bytes (got {len(key)})"
        raise ValueError(msg)
    if len(iv) != 32:
        msg = f"IV length must be 32 bytes (got {len(iv)})"
        raise ValueError(msg)

    # Ultra-Fast Tier 0: hypercrypto (Vectorized SIMD & hardware-accelerated Rust)
    if _HAS_HYPERCRYPTO and _hypercrypto is not None:
        return bytes(_hypercrypto.ige256_decrypt(data, key, iv))

    # Fast Tier 1: tgcrypto (C-accelerated whole buffer)
    if _HAS_TGCRYPTO and _tgcrypto is not None:
        return bytes(_tgcrypto.ige256_decrypt(data, key, iv))

    # Fast Tier 2: cryptg (C-accelerated whole buffer)
    if _HAS_CRYPTG and _cryptg is not None:
        return bytes(_cryptg.decrypt_ige(data, key, iv))

    # Fast Tier 3: PyCryptodome / Cryptodome MODE_IGE (C-accelerated whole buffer)
    if _HAS_PYCRYPTODOME_IGE and _AES is not None:
        cipher = _AES.new(key, _AES.MODE_IGE, iv)
        return bytes(cipher.decrypt(data))

    # Fallback Tier: Block-by-block ECB (cryptography or PureAES)
    _, decrypt_block = _get_cipher_ecb(key)
    iv1 = iv[:16]
    iv2 = iv[16:]

    out = bytearray(len(data))
    for offset in range(0, len(data), 16):
        chunk = data[offset : offset + 16]
        # p_i = D(c_i ^ m_{i-1}) ^ c_{i-1}
        x = _xor(chunk, iv2)
        y = decrypt_block(x)
        p = _xor(y, iv1)
        out[offset : offset + 16] = p
        iv1 = chunk
        iv2 = p

    return bytes(out)


async def async_aes_ige_encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    """
    Asynchronously encrypt data using AES-256-IGE mode.
    HyperCrypto natively releases the GIL in Rust for large buffers, avoiding Python
    thread pool overhead.
    """
    if _HAS_HYPERCRYPTO or len(data) <= CRYPTO_THREAD_POOL_THRESHOLD:
        return aes_ige_encrypt(data, key, iv)
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, aes_ige_encrypt, data, key, iv)


async def async_aes_ige_decrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    """
    Asynchronously decrypt data using AES-256-IGE mode.
    HyperCrypto natively releases the GIL in Rust for large buffers, avoiding Python
    thread pool overhead.
    """
    if _HAS_HYPERCRYPTO or len(data) <= CRYPTO_THREAD_POOL_THRESHOLD:
        return aes_ige_decrypt(data, key, iv)
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, aes_ige_decrypt, data, key, iv)
