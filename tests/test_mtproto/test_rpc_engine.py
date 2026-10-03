"""
Tests for MTProto MessageCodec, container multiplexing, and RPCEngine.
"""

import os

import pytest

from aiogram.mtproto.crypto.auth_key import AuthKey
from aiogram.mtproto.protocol.ids import IdGenerator
from aiogram.mtproto.protocol.message import MessageCodec, MTProtoMessage


def test_plain_message_codec() -> None:
    id_gen = IdGenerator()
    msg_id = id_gen.generate_msg_id()
    body = b"Sample plain payload"

    packed = MessageCodec.pack_plain(msg_id, body)
    unpacked_msg_id, unpacked_body = MessageCodec.unpack_plain(packed)

    assert unpacked_msg_id == msg_id
    assert unpacked_body == body


def test_encrypted_message_codec_and_containers() -> None:
    auth_key = AuthKey(os.urandom(256))
    server_salt = 123456789
    session_id = 987654321
    msg_id = IdGenerator().generate_msg_id()
    seq_no = 1
    body = b"Confidential MTProto 2.0 encrypted body"

    packed = MessageCodec.pack_encrypted(
        auth_key=auth_key,
        server_salt=server_salt,
        session_id=session_id,
        msg_id=msg_id,
        seq_no=seq_no,
        body=body,
    )

    unpacked_salt, unpacked_session, messages = MessageCodec.unpack_encrypted(
        auth_key=auth_key,
        session_id=session_id,
        data=packed,
        is_client=True,
    )

    assert unpacked_salt == server_salt
    assert unpacked_session == session_id
    assert len(messages) == 1
    assert messages[0].msg_id == msg_id
    assert messages[0].seq_no == seq_no
    assert messages[0].body == body


@pytest.mark.asyncio
async def test_rpc_engine_pong_handling() -> None:
    import asyncio
    from unittest.mock import AsyncMock, MagicMock

    from aiogram.mtproto.protocol.rpc import RPCEngine
    from aiogram.raw.core.tl_core_types import Ping, Pong

    conn = MagicMock()
    conn.is_connected = True
    conn.send = AsyncMock()
    auth_key = AuthKey(os.urandom(256))
    engine = RPCEngine(connection=conn, auth_key=auth_key, server_salt=100)

    loop = asyncio.get_running_loop()
    fut: asyncio.Future[int] = loop.create_future()
    req = Ping(ping_id=12345)
    req_msg_id = 999888777
    engine._pending_requests[req_msg_id] = (fut, req)

    pong = Pong(msg_id=req_msg_id, ping_id=12345)
    msg = MTProtoMessage(msg_id=111, seq_no=0, body=pong.write())
    engine._process_message(msg)

    assert fut.done()
    assert fut.result() == 12345


@pytest.mark.asyncio
async def test_rpc_engine_new_session_created() -> None:
    from unittest.mock import AsyncMock, MagicMock

    from aiogram.mtproto.protocol.rpc import RPCEngine
    from aiogram.raw.core.tl_core_types import NewSessionCreated

    conn = MagicMock()
    conn.is_connected = True
    conn.send = AsyncMock()
    auth_key = AuthKey(os.urandom(256))
    engine = RPCEngine(connection=conn, auth_key=auth_key, server_salt=100)

    new_session = NewSessionCreated(first_msg_id=10, unique_id=20, server_salt=999)
    msg = MTProtoMessage(msg_id=111, seq_no=0, body=new_session.write())
    engine._process_message(msg)

    assert engine.server_salt == 999


@pytest.mark.asyncio
async def test_rpc_engine_gzip_rpc_result() -> None:
    import asyncio
    import struct
    from unittest.mock import AsyncMock, MagicMock

    from aiogram.mtproto.protocol.rpc import RPCEngine
    from aiogram.raw import functions as raw_funcs
    from aiogram.raw.core.tl_core_types import GzipPacked, RpcResult
    from aiogram.raw.types import InputDocumentFileLocation, StorageFileUnknown, UploadFile

    conn = MagicMock()
    conn.is_connected = True
    conn.send = AsyncMock()
    auth_key = AuthKey(os.urandom(256))
    engine = RPCEngine(connection=conn, auth_key=auth_key, server_salt=100)

    upload_file = UploadFile(type=StorageFileUnknown(), mtime=1700000000, bytes=b"GZIP_CHUNK_DATA")
    compressed_file_bytes = GzipPacked(upload_file.write()).write()

    loop = asyncio.get_running_loop()
    fut: asyncio.Future[UploadFile] = loop.create_future()
    req = raw_funcs.upload.GetFile(
        location=InputDocumentFileLocation(id=1, access_hash=2, file_reference=b"", thumb_size=""),
        offset=0,
        limit=512 * 1024,
    )
    req_msg_id = 555666777
    engine._pending_requests[req_msg_id] = (fut, req)

    rpc_result_body = struct.pack("<Iq", RpcResult.ID, req_msg_id) + compressed_file_bytes
    msg = MTProtoMessage(msg_id=222, seq_no=1, body=rpc_result_body)
    engine._process_message(msg)

    assert fut.done()
    res = fut.result()
    assert isinstance(res, UploadFile)
    assert res.bytes == b"GZIP_CHUNK_DATA"


@pytest.mark.asyncio
async def test_rpc_engine_reset_initialization() -> None:
    from unittest.mock import AsyncMock, MagicMock
    from aiogram.mtproto.protocol.rpc import RPCEngine

    conn = MagicMock()
    conn.is_connected = True
    conn.send = AsyncMock()
    auth_key = AuthKey(os.urandom(256))
    engine = RPCEngine(connection=conn, auth_key=auth_key, server_salt=100)

    engine._initialized = True
    assert engine._initialized is True

    engine.reset_initialization()
    assert engine._initialized is False

    await engine.stop()
    assert engine._initialized is False
