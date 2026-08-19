"""
RSA encryption and official Telegram public keys for MTProto handshake.
"""

from __future__ import annotations

import hashlib
import os
from typing import NamedTuple


class RSAKey(NamedTuple):
    fingerprint: int
    n: int
    e: int


# Official Telegram Production and Test Server RSA Public Keys
TELEGRAM_RSA_KEYS: list[RSAKey] = [
    RSAKey(
        fingerprint=-4725062493392723383,  # 0xbe256d0f6e919849 -> signed int64
        n=int(
            "c3b42b026ce86bf15d4323502f32c36647cf776739e46e63e52a1207ae3a61d4a9"
            "07590b4904d2a48b71f974dd80464a30284d64196747dcb8b0f58f9e0115d3024c"
            "68747aec34c8525b7e2440e0aded8b3c7820b399997ce7ab7656f40032e8b23f"
            "0468e3e2454f5a436f5e6394f12287e459818d525f4b97bf3d702923b77a019be"
            "ad961c620e1743248b61a463b497714995c8e2ab7000f2934d5463f50c79744e6"
            "c9b40d2bed4fe72f69fc9b506164d47700cee4fb2206824a79a4f23e716f0c9c0"
            "c07ddda302a8d3f6f506ae4b44a5f884e864b5a073c682f32c3200a8f7a92d71d"
            "a2f2e0f20a4239ec34f22cf454d4423543e2b90837466644d",
            16,
        ),
        e=65537,
    ),
    RSAKey(
        fingerprint=-1156828557342674483,  # 0xef99824249a852cd
        n=int(
            "9a2632b19b61dd1239506452f44173871438b91037749301507f3e5b853a5298a0"
            "fb3474fc15268324ceb9517ab937fdf8614a8d6e3a95970cb72d4761016296c7b"
            "a24cf29a73884313d4957e0fc270e7cb238b812acee3e743566580d9293007e34"
            "02d4f5507c72f506b6e1265a20f59cbbd7b0691728e9c337db70fb59e048b7768"
            "3164dd3dbd0f46a97c52cfeb21b0b651587b73f2c89084fa169b2356e0004908a"
            "14627b4d160f1507764e46b5a16f40fb8766e408a29ed6d653822f0703f5e81c2"
            "b14e37da45a7063b57ddd4d14d65036f136471b505a04b154fc76fb8979da1e99"
            "e9e4d5ab7939b28292455a75897d8b6964b1bb5072e49123",
            16,
        ),
        e=65537,
    ),
    RSAKey(
        fingerprint=-3732688755609340798,  # 0xcc3b0638708c3c82
        n=int(
            "bb82457f7fb6ec142b3b4eec3910c5119f394a0f1aeb7250acab7b0f8d2a156dabb"
            "713f770a9b4da530f012421a2764b426d4bce20e00877d547b511999402e6b975e"
            "7406a4613a0b08a97cf2a1e04c85fe0101e400a4a4e6eb4984f43711fa783a129f"
            "219a863b71f50919282224f7da2f1201fa74224d51862223d61d5f21803f2972908"
            "a0d019b5a6530bc857ca742610f9d8ec75a9b99d3d404d0f3f5ce2e077501f1b37d"
            "eb69464d99141334e6d158d54c4dd44a0e8bda10e04c2e2fe63555a9ec2f599b567"
            "f3550fb73036306136ec947f637fc73d7429700e6940a60bb47b01808291e702513"
            "643d82473c3e3d40a38ec23096425a9164821",
            16,
        ),
        e=65537,
    ),
    RSAKey(
        fingerprint=-5055006677943018446,  # 0xb9dc074e6f494432
        n=int(
            "cbea526f101f3a47da2231bd71861296cd70fb32499e04b80ebecd163eec86adb28"
            "04eed79a4c3c45496ec50e5303d8272604b14d00e128bceee82b497e0fc2943415"
            "ac1eb64324d312838a2e457f5af16f96e288202203fb2a604ec2d0e835e5d3e4a7"
            "6f27712518a8d07e66d4ba701e6a2bd5a8e042b26beec11d67b410d4c82e0ad7971"
            "7491f0007d3417f1f03446494f8416e34a50f142c3e35028d3e9b151e73068154216"
            "3a83b59e7ec923c4d4d960f64142d31249942a8182b2bb9914f3fb16007e334c05"
            "2866eb30a6ce9da459be59970a02c3074d0a5f07be06bd0b296fb0fa95f2e5a8394"
            "f493a52e52221b6abb73f7348166ac130001b",
            16,
        ),
        e=65537,
    ),
]


def find_rsa_key(fingerprints: list[int]) -> RSAKey | None:
    """
    Find matching Telegram RSA key by given fingerprints list.
    """
    for fp in fingerprints:
        for key in TELEGRAM_RSA_KEYS:
            if key.fingerprint == fp:
                return key
    return None


def rsa_encrypt(data: bytes, key: RSAKey) -> bytes:
    """
    Encrypt data with Telegram RSA key using Telegram MTProto padding:
    padded = sha1(data) + data + random_bytes (total 255 bytes).
    ciphertext = (padded_int ^ e) mod n.

    :param data: Data to encrypt (e.g. PQ inner data).
    :param key: RSAKey instance.
    :return: 256-byte encrypted ciphertext.
    """
    sha1_hash = hashlib.sha1(data).digest()
    data_with_hash = sha1_hash + data
    pad_len = 255 - len(data_with_hash)
    if pad_len < 0:
        msg = f"Data is too long for 2048-bit RSA encryption (got {len(data)} bytes)"
        raise ValueError(msg)

    padded = data_with_hash + os.urandom(pad_len)
    data_int = int.from_bytes(padded, "big") % key.n
    enc_int = pow(data_int, key.e, key.n)
    return enc_int.to_bytes(256, "big")
