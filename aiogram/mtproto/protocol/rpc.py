"""
MTProto RPC Engine and packet multiplexer.
"""

from __future__ import annotations

import asyncio
import contextlib
import io
import logging
import struct
from collections.abc import Callable
from typing import Any, TypeVar

from aiogram.errors.mtproto import AuthKeyNotFound, RPCError, parse_rpc_error
from aiogram.mtproto.connection.tcp import TCPConnection
from aiogram.mtproto.crypto.auth_key import AuthKey
from aiogram.mtproto.protocol.ids import IdGenerator, generate_session_id
from aiogram.mtproto.protocol.message import MessageCodec, MTProtoMessage
from aiogram.raw.all import read_tl_object
from aiogram.raw.core.primitives import TLObject, TLRequest, read_uint
from aiogram.raw.core.tl_core_types import (
    BadMsgNotification,
    BadServerSalt,
    GzipPacked,
    InitConnection,
    InvokeWithLayer,
    MsgsAck,
    NewSessionCreated,
    Ping,
    PingDelayDisconnect,
    Pong,
    RpcError,
    RpcResult,
)

logger = logging.getLogger("aiogram.mtproto.rpc")
T = TypeVar("T")

LAYER = 184


def _is_init_exempt(query: TLObject) -> bool:
    c_id = getattr(query, "ID", 0)
    return c_id in (
        Ping.ID,
        PingDelayDisconnect.ID,
        MsgsAck.ID,
    )


class RPCEngine:
    """
    MTProto 2.0 RPC Engine managing session state, request correlation, and update routing.
    """

    def __init__(
        self,
        connection: TCPConnection,
        auth_key: AuthKey,
        server_salt: int,
        session_id: int | None = None,
        api_id: int = 6,
        app_version: str = "aiogram-mtproto",
        device_model: str = "PC",
        system_version: str = "Windows",
        lang_code: str = "en",
    ) -> None:
        self.connection = connection
        self.auth_key = auth_key
        self.server_salt = server_salt
        self.session_id = session_id or generate_session_id()
        self.api_id = api_id
        self.app_version = app_version
        self.device_model = device_model
        self.system_version = system_version
        self.lang_code = lang_code

        self.id_gen = IdGenerator()
        self._seq_no = 0
        self._pending_requests: dict[int, tuple[asyncio.Future[Any], TLRequest[Any]]] = {}
        self._update_callbacks: list[Callable[[Any], None]] = []
        self._reader_task: asyncio.Task[None] | None = None
        self._send_lock = asyncio.Lock()
        self._initialized = False
        self._ack_queue: list[int] = []

    def add_update_handler(self, callback: Callable[[Any], None]) -> None:
        self._update_callbacks.append(callback)

    def start(self) -> None:
        if self._reader_task is None or self._reader_task.done():
            self._reader_task = asyncio.create_task(self._reader_loop())

    async def stop(self) -> None:
        if self._reader_task and not self._reader_task.done():
            self._reader_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._reader_task
            self._reader_task = None
        for fut, _ in list(self._pending_requests.values()):
            if not fut.done():
                fut.set_exception(ConnectionError("RPCEngine stopped"))
        self._pending_requests.clear()

    def __repr__(self) -> str:
        is_conn = bool(self.connection and self.connection.is_connected)
        return f"<RPCEngine is_connected={is_conn}>"

    async def invoke(self, query: TLRequest[T], timeout: float = 30.0) -> T:
        """
        Send an MTProto RPC query and await its typed result.
        """
        self.start()

        loop = asyncio.get_running_loop()
        future: asyncio.Future[Any] = loop.create_future()

        async with self._send_lock:
            payload_query: TLObject = query

            if not _is_init_exempt(query):
                # Wrap in initConnection / invokeWithLayer for the first non-service query
                if not self._initialized:
                    init_conn = InitConnection(
                        api_id=self.api_id,
                        device_model=self.device_model,
                        system_version=self.system_version,
                        app_version=self.app_version,
                        system_lang_code=self.lang_code,
                        lang_pack="",
                        lang_code=self.lang_code,
                        query=query,
                    )
                    payload_query = InvokeWithLayer(layer=LAYER, query=init_conn)
                    self._initialized = True

            # All RPC queries (including Ping / PingDelayDisconnect) expect a response
            # and are content-related in MTProto specification, requiring odd seq_no.
            seq_no = self._seq_no * 2 + 1
            self._seq_no += 1

            body = payload_query.write()
            msg_id = self.id_gen.generate_msg_id()

            self._pending_requests[msg_id] = (future, query)

            encrypted = await MessageCodec.async_pack_encrypted(
                auth_key=self.auth_key,
                server_salt=self.server_salt,
                session_id=self.session_id,
                msg_id=msg_id,
                seq_no=seq_no,
                body=body,
            )

            await self.connection.send(encrypted)

        try:
            return await asyncio.wait_for(future, timeout=timeout)
        except Exception:
            self._pending_requests.pop(msg_id, None)
            raise

    async def _resend_pending_request(
        self, fut: asyncio.Future[Any], query: TLRequest[Any]
    ) -> None:
        """
        Resend a pending request after updating server salt or recovering from bad msg notification.
        """
        try:
            async with self._send_lock:
                body = query.write()
                msg_id = self.id_gen.generate_msg_id()
                seq_no = self._seq_no * 2 + 1
                self._seq_no += 1
                self._pending_requests[msg_id] = (fut, query)
                encrypted = await MessageCodec.async_pack_encrypted(
                    auth_key=self.auth_key,
                    server_salt=self.server_salt,
                    session_id=self.session_id,
                    msg_id=msg_id,
                    seq_no=seq_no,
                    body=body,
                )
                await self.connection.send(encrypted)
        except Exception as ex:
            if not fut.done():
                fut.set_exception(ex)

    async def _send_ack(self) -> None:
        if not self._ack_queue:
            return
        msg_ids = list(self._ack_queue)
        self._ack_queue.clear()
        try:
            if not self.connection or not self.connection.is_connected:
                return
            ack = MsgsAck(msg_ids=msg_ids)
            msg_id = self.id_gen.generate_msg_id()
            seq_no = self._seq_no * 2
            encrypted = MessageCodec.pack_encrypted(
                auth_key=self.auth_key,
                server_salt=self.server_salt,
                session_id=self.session_id,
                msg_id=msg_id,
                seq_no=seq_no,
                body=ack.write(),
            )
            async with self._send_lock:
                await self.connection.send(encrypted)
        except Exception:
            pass

    async def _reader_loop(self) -> None:
        """
        Background task reading and dispatching encrypted packets from TCP.
        """
        while True:
            try:
                data = await self.connection.receive()
                if len(data) == 4:
                    err_code = struct.unpack_from("<i", data, 0)[0]
                    logger.error(
                        "MTProto transport returned error code: %d (hex: %s)", err_code, data.hex()
                    )
                    if err_code == -404:
                        exc: Exception = AuthKeyNotFound("AUTH_KEY_NOT_FOUND (-404)")
                    else:
                        exc = ConnectionError(f"MTProto transport error {err_code}")
                    for fut, _ in list(self._pending_requests.values()):
                        if not fut.done():
                            fut.set_exception(exc)
                    break

                salt, s_session_id, messages = MessageCodec.unpack_encrypted(
                    auth_key=self.auth_key,
                    session_id=self.session_id,
                    data=data,
                )
                self.server_salt = salt

                for msg in messages:
                    if msg.seq_no % 2 != 0:
                        self._ack_queue.append(msg.msg_id)
                    self._process_message(msg)

                # Promptly ACK content messages to keep server connection healthy
                if self._ack_queue:
                    await self._send_ack()

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.debug("MTProto reader loop notice: %s", e)
                # Fail any pending futures if connection broke
                if not self.connection.is_connected:
                    for fut, _ in list(self._pending_requests.values()):
                        if not fut.done():
                            fut.set_exception(ConnectionError("MTProto connection closed"))
                    break
                await asyncio.sleep(0.5)

    def _process_message(self, msg: MTProtoMessage) -> None:
        """
        Process a single unpacked MTProto message with zero-overhead offset parsing.
        """
        body = msg.body
        if len(body) < 4:
            return
        c_id = struct.unpack_from("<I", body, 0)[0]

        # 1. MessageContainer (0x73F1F8DC)
        if c_id == 0x73F1F8DC:
            if len(body) < 8:
                return
            count = struct.unpack_from("<I", body, 4)[0]
            offset = 8
            body_len = len(body)
            for _ in range(count):
                if offset + 16 > body_len:
                    break
                c_msg_id, c_seq_no, c_len = struct.unpack_from("<qII", body, offset)
                offset += 16
                if offset + c_len > body_len:
                    break
                c_body = body[offset : offset + c_len]
                offset += c_len
                self._process_message(
                    MTProtoMessage(msg_id=c_msg_id, seq_no=c_seq_no, body=c_body)
                )
            return

        # 2. GzipPacked top-level message (0x3072CFA1)
        if c_id == GzipPacked.ID:
            b_io = io.BytesIO(body)
            try:
                read_uint(b_io)  # consume GzipPacked.ID
                decompressed = GzipPacked.read(b_io)
                self._process_message(
                    MTProtoMessage(msg_id=msg.msg_id, seq_no=msg.seq_no, body=decompressed)
                )
            except Exception as e:
                logger.warning("Failed to decompress top-level GzipPacked: %s", e)
            return

        # 3. RpcResult (0xf35c6d01)
        if c_id == RpcResult.ID:
            if len(body) < 12:
                return
            req_msg_id = struct.unpack_from("<q", body, 4)[0]
            req_entry = self._pending_requests.pop(req_msg_id, None)

            raw_result_data = body[12:]
            # Check if result payload is GzipPacked
            if (
                len(raw_result_data) >= 4
                and struct.unpack_from("<I", raw_result_data, 0)[0] == GzipPacked.ID
            ):
                try:
                    gzip_io = io.BytesIO(raw_result_data)
                    read_uint(gzip_io)  # consume GzipPacked.ID
                    raw_result_data = GzipPacked.read(gzip_io)
                except Exception as e:
                    logger.warning("Failed to decompress RpcResult GzipPacked: %s", e)

            # Check if result is an RpcError (0x2144ca19)
            if (
                len(raw_result_data) >= 8
                and struct.unpack_from("<I", raw_result_data, 0)[0] == RpcError.ID
            ):
                err_code = struct.unpack_from("<i", raw_result_data, 4)[0]
                b_io = io.BytesIO(raw_result_data[8:])
                from aiogram.raw.core.primitives import read_string

                err_msg_str = read_string(b_io)
                exc = parse_rpc_error(err_code, err_msg_str)
                if req_entry:
                    fut, _ = req_entry
                    if not fut.done():
                        fut.set_exception(exc)
                return

            if req_entry:
                fut, original_req = req_entry
                if not fut.done():
                    try:
                        b_io = io.BytesIO(raw_result_data)
                        result = original_req.read_result(b_io)
                        fut.set_result(result)
                    except Exception as ex:
                        fut.set_exception(ex)
            return

        # 4. Pong (0x347773C5)
        if c_id == Pong.ID:
            b_io = io.BytesIO(body)
            read_uint(b_io)  # consume Pong.ID
            pong = Pong.read(b_io)
            req_entry = self._pending_requests.pop(pong.msg_id, None)
            if req_entry:
                fut, original_req = req_entry
                if not fut.done():
                    try:
                        pong_io = io.BytesIO(body)
                        result = original_req.read_result(pong_io)
                        fut.set_result(result)
                    except Exception:
                        fut.set_result(pong.ping_id)
            return

        # 5. BadServerSalt (0xedab447b)
        if c_id == BadServerSalt.ID:
            b_io = io.BytesIO(body)
            read_uint(b_io)  # consume BadServerSalt.ID
            bad_salt = BadServerSalt.read(b_io)
            self.server_salt = bad_salt.new_server_salt
            logger.debug(
                "Received BadServerSalt: updated server salt and resending pending requests"
            )
            req_entry = self._pending_requests.pop(bad_salt.bad_msg_id, None)
            if req_entry:
                fut, original_req = req_entry
                if not fut.done():
                    asyncio.create_task(self._resend_pending_request(fut, original_req))
            return

        # 6. BadMsgNotification (0xa7eff811)
        if c_id == BadMsgNotification.ID:
            b_io = io.BytesIO(body)
            read_uint(b_io)  # consume BadMsgNotification.ID
            bad_msg = BadMsgNotification.read(b_io)
            logger.warning(
                "Received BadMsgNotification: error_code=%d for msg_id=%d",
                bad_msg.error_code,
                bad_msg.bad_msg_id,
            )
            req_entry = self._pending_requests.pop(bad_msg.bad_msg_id, None)
            if req_entry:
                fut, original_req = req_entry
                if not fut.done():
                    if bad_msg.error_code in (16, 17, 32, 33, 34, 35):
                        logger.info(
                            "Auto-recovering and resending request for BadMsgNotification error %d",
                            bad_msg.error_code,
                        )
                        asyncio.create_task(self._resend_pending_request(fut, original_req))
                    else:
                        fut.set_exception(
                            RPCError(
                                bad_msg.error_code, f"BadMsgNotification {bad_msg.error_code}"
                            )
                        )
            return

        # 7. NewSessionCreated (0x9ec20908)
        if c_id == NewSessionCreated.ID:
            b_io = io.BytesIO(body)
            read_uint(b_io)  # consume NewSessionCreated.ID
            new_session = NewSessionCreated.read(b_io)
            self.server_salt = new_session.server_salt
            logger.debug("New session established on Telegram server")
            return

        # 8. MsgsAck (0x62d6b459)
        if c_id == MsgsAck.ID:
            b_io = io.BytesIO(body)
            read_uint(b_io)  # consume MsgsAck.ID
            ack = MsgsAck.read(b_io)
            logger.debug("Received MsgsAck for msg_ids: %s", ack.msg_ids)
            return

        # 9. Updates or other TL objects
        try:
            b_io = io.BytesIO(body)
            tl_obj = read_tl_object(b_io)
            if tl_obj:
                for cb in self._update_callbacks:
                    try:
                        cb(tl_obj)
                    except Exception as e:
                        logger.error("Error in update callback: %s", e)
        except Exception as e:
            logger.debug(
                "Failed to parse incoming TL object (c_id=%08x, len=%d): %s",
                c_id,
                len(body),
                e,
            )
