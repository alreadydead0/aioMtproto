"""
Core MTProto TL types and RPC control messages.
"""

from __future__ import annotations

import gzip
import io
import struct
from typing import Any, BinaryIO, List

from aiogram.raw.core.primitives import (
    TLObject,
    TLRequest,
    read_bytes,
    read_int,
    read_int128,
    read_int256,
    read_long,
    read_string,
    read_uint,
    read_vector,
    write_bytes,
    write_int,
    write_int128,
    write_int256,
    write_long,
    write_string,
    write_uint,
    write_vector,
)


class GzipPacked(TLObject):
    ID = 0x3072CFA1
    QUALNAME = "types.GzipPacked"

    def __init__(self, data: bytes) -> None:
        self.data = data

    def write(self) -> bytes:
        compressed = gzip.compress(self.data)
        return struct.pack("<I", self.ID) + write_bytes(compressed)

    @classmethod
    def read(cls, b: BinaryIO) -> bytes:
        compressed = read_bytes(b)
        return gzip.decompress(compressed)


class RpcResult(TLObject):
    ID = 0xF35C6D01
    QUALNAME = "types.RpcResult"

    def __init__(self, req_msg_id: int, result: Any) -> None:
        self.req_msg_id = req_msg_id
        self.result = result

    @classmethod
    def read(cls, b: BinaryIO) -> RpcResult:
        req_msg_id = read_long(b)
        # Remaining body is the serialized result or rpc_error
        return RpcResult(req_msg_id=req_msg_id, result=b.read())


class RpcError(TLObject):
    ID = 0x2144CA19
    QUALNAME = "types.RpcError"

    def __init__(self, error_code: int, error_message: str) -> None:
        self.error_code = error_code
        self.error_message = error_message

    def write(self) -> bytes:
        return struct.pack("<I", self.ID) + write_int(self.error_code) + write_string(self.error_message)

    @classmethod
    def read(cls, b: BinaryIO) -> RpcError:
        return RpcError(error_code=read_int(b), error_message=read_string(b))


class MsgsAck(TLObject):
    ID = 0x62D6B459
    QUALNAME = "types.MsgsAck"

    def __init__(self, msg_ids: list[int]) -> None:
        self.msg_ids = msg_ids

    def write(self) -> bytes:
        return struct.pack("<I", self.ID) + write_vector(self.msg_ids, write_long)

    @classmethod
    def read(cls, b: BinaryIO) -> MsgsAck:
        return MsgsAck(msg_ids=read_vector(b, read_long))


class BadServerSalt(TLObject):
    ID = 0xEDAB447B
    QUALNAME = "types.BadServerSalt"

    def __init__(self, bad_msg_id: int, bad_msg_seqno: int, error_code: int, new_server_salt: int) -> None:
        self.bad_msg_id = bad_msg_id
        self.bad_msg_seqno = bad_msg_seqno
        self.error_code = error_code
        self.new_server_salt = new_server_salt

    @classmethod
    def read(cls, b: BinaryIO) -> BadServerSalt:
        return BadServerSalt(
            bad_msg_id=read_long(b),
            bad_msg_seqno=read_int(b),
            error_code=read_int(b),
            new_server_salt=read_long(b),
        )


class BadMsgNotification(TLObject):
    ID = 0xA7EFF811
    QUALNAME = "types.BadMsgNotification"

    def __init__(self, bad_msg_id: int, bad_msg_seqno: int, error_code: int) -> None:
        self.bad_msg_id = bad_msg_id
        self.bad_msg_seqno = bad_msg_seqno
        self.error_code = error_code

    @classmethod
    def read(cls, b: BinaryIO) -> BadMsgNotification:
        return BadMsgNotification(
            bad_msg_id=read_long(b),
            bad_msg_seqno=read_int(b),
            error_code=read_int(b),
        )


class Ping(TLRequest[int]):
    ID = 0x7ABE77EC
    QUALNAME = "functions.Ping"

    def __init__(self, ping_id: int) -> None:
        self.ping_id = ping_id

    def write(self) -> bytes:
        return struct.pack("<I", self.ID) + write_long(self.ping_id)

    def read_result(self, b: BinaryIO) -> int:
        read_uint(b)  # pong constructor
        read_long(b)  # ping_id
        return read_long(b)  # pong_id


class Pong(TLObject):
    ID = 0x347773C5
    QUALNAME = "types.Pong"

    def __init__(self, msg_id: int, ping_id: int) -> None:
        self.msg_id = msg_id
        self.ping_id = ping_id

    def write(self) -> bytes:
        return struct.pack("<I", self.ID) + write_long(self.msg_id) + write_long(self.ping_id)

    @classmethod
    def read(cls, b: BinaryIO) -> Pong:
        return Pong(msg_id=read_long(b), ping_id=read_long(b))


class PingDelayDisconnect(TLRequest[int]):
    ID = 0xF34277BC
    QUALNAME = "functions.PingDelayDisconnect"

    def __init__(self, ping_id: int, disconnect_delay: int) -> None:
        self.ping_id = ping_id
        self.disconnect_delay = disconnect_delay

    def write(self) -> bytes:
        return struct.pack("<I", self.ID) + write_long(self.ping_id) + write_int(self.disconnect_delay)

    def read_result(self, b: BinaryIO) -> int:
        read_uint(b)
        read_long(b)
        return read_long(b)


class InvokeWithLayer(TLRequest[Any]):
    ID = 0xDA9B0D0D
    QUALNAME = "functions.InvokeWithLayer"

    def __init__(self, layer: int, query: TLObject) -> None:
        self.layer = layer
        self.query = query

    def write(self) -> bytes:
        return struct.pack("<I", self.ID) + write_int(self.layer) + self.query.write()

    def read_result(self, b: BinaryIO) -> Any:
        if isinstance(self.query, TLRequest):
            return self.query.read_result(b)
        return b.read()


class InitConnection(TLRequest[Any]):
    ID = 0xC1CD5EA9
    QUALNAME = "functions.InitConnection"

    def __init__(
        self,
        api_id: int,
        device_model: str,
        system_version: str,
        app_version: str,
        system_lang_code: str,
        lang_pack: str,
        lang_code: str,
        query: TLObject,
    ) -> None:
        self.api_id = api_id
        self.device_model = device_model
        self.system_version = system_version
        self.app_version = app_version
        self.system_lang_code = system_lang_code
        self.lang_pack = lang_pack
        self.lang_code = lang_code
        self.query = query

    def write(self) -> bytes:
        # flags (int) = 0
        res = (
            struct.pack("<II", self.ID, 0)
            + write_int(self.api_id)
            + write_string(self.device_model)
            + write_string(self.system_version)
            + write_string(self.app_version)
            + write_string(self.system_lang_code)
            + write_string(self.lang_pack)
            + write_string(self.lang_code)
            + self.query.write()
        )
        return res

    def read_result(self, b: BinaryIO) -> Any:
        if isinstance(self.query, TLRequest):
            return self.query.read_result(b)
        return b.read()


# --- Handshake TL Types ---


class ReqPqMulti(TLRequest[Any]):
    ID = 0xBE7E8EF1
    QUALNAME = "functions.ReqPqMulti"

    def __init__(self, nonce: bytes) -> None:
        self.nonce = nonce

    def write(self) -> bytes:
        return struct.pack("<I", self.ID) + write_int128(self.nonce)


class ResPQ(TLObject):
    ID = 0x05162463
    QUALNAME = "types.ResPQ"

    def __init__(
        self,
        nonce: bytes,
        server_nonce: bytes,
        pq: bytes,
        server_public_key_fingerprints: list[int],
    ) -> None:
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.pq = pq
        self.server_public_key_fingerprints = server_public_key_fingerprints

    @classmethod
    def read(cls, b: BinaryIO) -> ResPQ:
        nonce = read_int128(b)
        server_nonce = read_int128(b)
        pq = read_bytes(b)
        fingerprints = read_vector(b, read_long)
        return ResPQ(nonce, server_nonce, pq, fingerprints)


class ReqDHParams(TLRequest[Any]):
    ID = 0xD712E4BE
    QUALNAME = "functions.ReqDHParams"

    def __init__(
        self,
        nonce: bytes,
        server_nonce: bytes,
        p: bytes,
        q: bytes,
        public_key_fingerprint: int,
        encrypted_data: bytes,
    ) -> None:
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.p = p
        self.q = q
        self.public_key_fingerprint = public_key_fingerprint
        self.encrypted_data = encrypted_data

    def write(self) -> bytes:
        return (
            struct.pack("<I", self.ID)
            + write_int128(self.nonce)
            + write_int128(self.server_nonce)
            + write_bytes(self.p)
            + write_bytes(self.q)
            + write_long(self.public_key_fingerprint)
            + write_bytes(self.encrypted_data)
        )


class ServerDHParamsOk(TLObject):
    ID = 0xD0E8075C
    QUALNAME = "types.ServerDHParamsOk"

    def __init__(self, nonce: bytes, server_nonce: bytes, encrypted_answer: bytes) -> None:
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.encrypted_answer = encrypted_answer

    @classmethod
    def read(cls, b: BinaryIO) -> ServerDHParamsOk:
        return ServerDHParamsOk(
            nonce=read_int128(b),
            server_nonce=read_int128(b),
            encrypted_answer=read_bytes(b),
        )


class SetClientDHParams(TLRequest[Any]):
    ID = 0xF5045F1F
    QUALNAME = "functions.SetClientDHParams"

    def __init__(self, nonce: bytes, server_nonce: bytes, encrypted_data: bytes) -> None:
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.encrypted_data = encrypted_data

    def write(self) -> bytes:
        return (
            struct.pack("<I", self.ID)
            + write_int128(self.nonce)
            + write_int128(self.server_nonce)
            + write_bytes(self.encrypted_data)
        )


class DhGenOk(TLObject):
    ID = 0x3BCBF734
    QUALNAME = "types.DhGenOk"

    def __init__(self, nonce: bytes, server_nonce: bytes, new_nonce_hash1: bytes) -> None:
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.new_nonce_hash1 = new_nonce_hash1

    @classmethod
    def read(cls, b: BinaryIO) -> DhGenOk:
        return DhGenOk(
            nonce=read_int128(b),
            server_nonce=read_int128(b),
            new_nonce_hash1=read_int128(b),
        )
