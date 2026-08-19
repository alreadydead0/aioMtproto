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
