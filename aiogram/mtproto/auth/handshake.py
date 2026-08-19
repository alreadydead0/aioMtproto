"""
MTProto 3-step Diffie-Hellman Handshake to generate AuthKey.
"""

from __future__ import annotations

import hashlib
import io
import logging
import os
import struct
from typing import TYPE_CHECKING, Tuple

from aiogram.mtproto.connection.tcp import TCPConnection
from aiogram.mtproto.crypto.aes_ige import aes_ige_decrypt, aes_ige_encrypt
from aiogram.mtproto.crypto.auth_key import AuthKey
from aiogram.mtproto.crypto.dh import (
    check_dh_g,
    check_dh_params,
    compute_auth_key,
    factorize_pq,
    generate_dh_b,
)
from aiogram.mtproto.crypto.rsa import find_rsa_key, rsa_encrypt
from aiogram.mtproto.protocol.ids import IdGenerator
from aiogram.mtproto.protocol.message import MessageCodec
from aiogram.raw.all import read_tl_object
from aiogram.raw.core.primitives import (
    read_bytes,
    read_int,
    read_int128,
    read_uint,
    write_bytes,
    write_int128,
)
from aiogram.raw.core.tl_core_types import (
    DhGenOk,
    ReqDHParams,
    ReqPqMulti,
    ResPQ,
    ServerDHParamsOk,
    SetClientDHParams,
)

logger = logging.getLogger("aiogram.mtproto.handshake")


async def do_handshake(conn: TCPConnection) -> tuple[AuthKey, int]:
    """
    Perform 3-step MTProto Diffie-Hellman Key Exchange with Telegram DC.

    :param conn: Open TCPConnection to DC.
    :return: (AuthKey, initial_server_salt)
    """
    id_gen = IdGenerator()

    # --- Step 1: req_pq_multi ---
    nonce = os.urandom(16)
    req_pq = ReqPqMulti(nonce=nonce)
    msg_id = id_gen.generate_msg_id()
    plain_packet = MessageCodec.pack_plain(msg_id, req_pq.write())

    await conn.send(plain_packet)
    resp_raw = await conn.receive()
    _, resp_body = MessageCodec.unpack_plain(resp_raw)

    resp = read_tl_object(io.BytesIO(resp_body))
    if not isinstance(resp, ResPQ):
        msg = f"Expected ResPQ from server (got {type(resp).__name__})"
        raise ValueError(msg)

    if resp.nonce != nonce:
        msg = "Nonce mismatch in ResPQ"
        raise ValueError(msg)

    server_nonce = resp.server_nonce
    pq_int = int.from_bytes(resp.pq, "big")
    p_int, q_int = factorize_pq(pq_int)
    p_bytes = p_int.to_bytes((p_int.bit_length() + 7) // 8, "big")
    q_bytes = q_int.to_bytes((q_int.bit_length() + 7) // 8, "big")

    rsa_key = find_rsa_key(resp.server_public_key_fingerprints)
    if not rsa_key:
        msg = f"Could not find matching Telegram RSA key from fingerprints: {resp.server_public_key_fingerprints}"
        raise ValueError(msg)

    # --- Step 2: req_DH_params ---
    new_nonce = os.urandom(32)

    # p_q_inner_data_dc (0xa9f55f95): pq (bytes), p (bytes), q (bytes), nonce (int128), server_nonce (int128), new_nonce (int256), dc (int)
    pq_inner = (
        struct.pack("<I", 0xA9F55F95)
        + write_bytes(resp.pq)
        + write_bytes(p_bytes)
        + write_bytes(q_bytes)
        + write_int128(nonce)
        + write_int128(server_nonce)
        + new_nonce
        + struct.pack("<i", conn.dc.dc_id)
    )

    encrypted_data = rsa_encrypt(pq_inner, rsa_key)

    req_dh = ReqDHParams(
        nonce=nonce,
        server_nonce=server_nonce,
        p=p_bytes,
        q=q_bytes,
        public_key_fingerprint=rsa_key.fingerprint,
        encrypted_data=encrypted_data,
    )

    msg_id = id_gen.generate_msg_id()
    await conn.send(MessageCodec.pack_plain(msg_id, req_dh.write()))
    resp_raw = await conn.receive()
    _, resp_body = MessageCodec.unpack_plain(resp_raw)

    resp_dh = read_tl_object(io.BytesIO(resp_body))
    if not isinstance(resp_dh, ServerDHParamsOk):
        msg = f"Expected ServerDHParamsOk (got {type(resp_dh).__name__})"
        raise ValueError(msg)

    if resp_dh.nonce != nonce or resp_dh.server_nonce != server_nonce:
        msg = "Nonce mismatch in ServerDHParamsOk"
        raise ValueError(msg)

    # Decrypt server_DH_inner_data with AES-IGE
    # key = sha1(new_nonce + server_nonce) + sha1(server_nonce + new_nonce)[:12]
    # iv = sha1(server_nonce + new_nonce)[12:20] + sha1(new_nonce + new_nonce) + new_nonce[:4]
    h_ns = hashlib.sha1(new_nonce + server_nonce).digest()
    h_sn = hashlib.sha1(server_nonce + new_nonce).digest()
    h_nn = hashlib.sha1(new_nonce + new_nonce).digest()

    aes_key = h_ns + h_sn[:12]
    aes_iv = h_sn[12:20] + h_nn + new_nonce[:4]

    decrypted_answer = aes_ige_decrypt(resp_dh.encrypted_answer, aes_key, aes_iv)
    # First 20 bytes is SHA1 of the rest
    expected_hash = decrypted_answer[:20]
    inner_payload = decrypted_answer[20:]
    if hashlib.sha1(inner_payload).digest() != expected_hash:
        msg = "Checksum mismatch in server_DH_inner_data"
        raise ValueError(msg)

    b_io = io.BytesIO(inner_payload)
    read_uint(b_io)  # constructor server_DH_inner_data (0xb5804368)
    if read_int128(b_io) != nonce or read_int128(b_io) != server_nonce:
        msg = "Nonce mismatch inside server_DH_inner_data"
        raise ValueError(msg)

    g = read_int(b_io)
    dh_prime_bytes = read_bytes(b_io)
    g_a_bytes = read_bytes(b_io)
    server_time = read_int(b_io)

    dh_prime = int.from_bytes(dh_prime_bytes, "big")
    g_a = int.from_bytes(g_a_bytes, "big")

    if not check_dh_params(dh_prime, g):
        msg = "Invalid DH prime or generator from server"
        raise ValueError(msg)
    if not check_dh_g(g_a, dh_prime):
        msg = "Server g_a failed security bounds check"
        raise ValueError(msg)

    # --- Step 3: set_client_DH_params ---
    b_secret, g_b = generate_dh_b(dh_prime, g)
    g_b_bytes = g_b.to_bytes(256, "big")

    auth_key_bytes = compute_auth_key(g_a, b_secret, dh_prime)
    auth_key = AuthKey(auth_key_bytes)

    # client_DH_inner_data (0x6643b654): nonce, server_nonce, retry_id (long 0), g_b (bytes)
    client_inner = (
        struct.pack("<I", 0x6643B654)
        + write_int128(nonce)
        + write_int128(server_nonce)
        + struct.pack("<q", 0)
        + write_bytes(g_b_bytes)
    )

    # Pad to multiple of 16
    client_hash = hashlib.sha1(client_inner).digest()
    client_padded = client_hash + client_inner
    pad_len = (16 - (len(client_padded) % 16)) % 16
    client_padded += os.urandom(pad_len)

    client_enc = aes_ige_encrypt(client_padded, aes_key, aes_iv)
    set_dh = SetClientDHParams(nonce=nonce, server_nonce=server_nonce, encrypted_data=client_enc)

    msg_id = id_gen.generate_msg_id()
    await conn.send(MessageCodec.pack_plain(msg_id, set_dh.write()))
    resp_raw = await conn.receive()
    _, resp_body = MessageCodec.unpack_plain(resp_raw)

    resp_dh_gen = read_tl_object(io.BytesIO(resp_body))
    if not isinstance(resp_dh_gen, DhGenOk):
        msg = f"Expected DhGenOk (got {type(resp_dh_gen).__name__})"
        raise ValueError(msg)

    expected_nonce_hash = auth_key.calc_new_nonce_hash(new_nonce, 1)
    if resp_dh_gen.new_nonce_hash1 != expected_nonce_hash:
        msg = "Handshake verification failed: invalid new_nonce_hash1"
        raise ValueError(msg)

    # Initial server salt = new_nonce[:8] ^ server_nonce[:8] (as 64-bit int)
    salt_bytes = bytes(x ^ y for x, y in zip(new_nonce[:8], server_nonce[:8]))
    server_salt = struct.unpack("<q", salt_bytes)[0]

    logger.info("MTProto handshake completed successfully. AuthKey ID: %s", repr(auth_key))
    return auth_key, server_salt
