"""
MTProto RPC Engine and packet multiplexer.
"""

from __future__ import annotations

import asyncio
import io
import logging
import struct
from collections.abc import Callable
from typing import Any, Dict, List, Optional, TypeVar

from aiogram.errors.mtproto import RPCError, parse_rpc_error
from aiogram.mtproto.connection.tcp import TCPConnection
from aiogram.mtproto.crypto.auth_key import AuthKey
from aiogram.mtproto.protocol.ids import IdGenerator, generate_session_id
from aiogram.mtproto.protocol.message import MessageCodec, MTProtoMessage
from aiogram.raw.all import read_tl_object
from aiogram.raw.core.primitives import TLObject, TLRequest
from aiogram.raw.core.tl_core_types import (
    BadMsgNotification,
    BadServerSalt,
    InitConnection,
    InvokeWithLayer,
    MsgsAck,
    RpcError,
    RpcResult,
)

logger = logging.getLogger("aiogram.mtproto.rpc")
T = TypeVar("T")

LAYER = 184


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
            try:
                await self._reader_task
            except asyncio.CancelledError:
                pass
            self._reader_task = None

    async def invoke(self, query: TLRequest[T], timeout: float = 30.0) -> T:
        """
        Send an MTProto RPC query and await its typed result.
        """
        self.start()

        # Wrap in initConnection / invokeWithLayer for the first query
        payload_query: TLObject = query
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

        body = payload_query.write()
        msg_id = self.id_gen.generate_msg_id()

        # Content-related queries increment seq_no
        seq_no = self._seq_no * 2 + 1
        self._seq_no += 1

        loop = asyncio.get_running_loop()
        future: asyncio.Future[Any] = loop.create_future()
        self._pending_requests[msg_id] = (future, query)

        encrypted = MessageCodec.pack_encrypted(
            auth_key=self.auth_key,
            server_salt=self.server_salt,
            session_id=self.session_id,
            msg_id=msg_id,
            seq_no=seq_no,
            body=body,
        )

        async with self._send_lock:
            await self.connection.send(encrypted)

        try:
            return await asyncio.wait_for(future, timeout=timeout)
        except Exception:
            self._pending_requests.pop(msg_id, None)
            raise

    async def _send_ack(self) -> None:
        if not self._ack_queue:
            return
        msg_ids = list(self._ack_queue)
        self._ack_queue.clear()
        ack = MsgsAck(msg_ids=msg_ids)
        msg_id = self.id_gen.generate_msg_id()
        # Non-content message: seq_no = self._seq_no * 2
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

    async def _reader_loop(self) -> None:
        """
        Background task reading and dispatching encrypted packets from TCP.
        """
        while True:
            try:
                data = await self.connection.receive()
                salt, s_session_id, messages = MessageCodec.unpack_encrypted(
                    auth_key=self.auth_key,
                    session_id=self.session_id,
                    data=data,
                )
                self.server_salt = salt

                for msg in messages:
                    self._ack_queue.append(msg.msg_id)
                    self._process_message(msg)

                # Send acks
                if self._ack_queue:
                    asyncio.create_task(self._send_ack())

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.debug("Reader loop exception: %s", e)
                # Fail any pending futures if connection broke
                if not self.connection.is_connected:
                    for fut, _ in list(self._pending_requests.values()):
                        if not fut.done():
                            fut.set_exception(ConnectionError("MTProto connection closed"))
                    break
                await asyncio.sleep(0.1)

    def _process_message(self, msg: MTProtoMessage) -> None:
        """
        Process a single unpacked MTProto message.
        """
        b_io = io.BytesIO(msg.body)
        c_id_bytes = b_io.read(4)
        if not c_id_bytes or len(c_id_bytes) < 4:
            return
        c_id = struct.unpack("<I", c_id_bytes)[0]
        b_io.seek(0)

        # 1. RpcResult (0xf35c6d01)
        if c_id == RpcResult.ID:
            b_io.read(4)  # skip c_id
            req_msg_id = struct.unpack("<q", b_io.read(8))[0]
            req_entry = self._pending_requests.pop(req_msg_id, None)

            # Check if result is an RpcError (0x2144ca19)
            res_c_id_bytes = b_io.read(4)
            if res_c_id_bytes and len(res_c_id_bytes) == 4:
                res_c_id = struct.unpack("<I", res_c_id_bytes)[0]
                if res_c_id == RpcError.ID:
                    err_code = struct.unpack("<i", b_io.read(4))[0]
                    # read string
                    err_msg_bytes = b_io.read()
                    err_msg_str = err_msg_bytes.decode("utf-8", errors="replace")
                    exc = parse_rpc_error(err_code, err_msg_str)
                    if req_entry:
                        fut, _ = req_entry
                        if not fut.done():
                            fut.set_exception(exc)
                    return
            b_io.seek(12)  # rewind to start of result data

            if req_entry:
                fut, original_req = req_entry
                if not fut.done():
                    try:
                        result = original_req.read_result(b_io)
                        fut.set_result(result)
                    except Exception as ex:
                        fut.set_exception(ex)
            return

        # 2. BadServerSalt (0xedab447b)
        if c_id == BadServerSalt.ID:
            bad_salt = BadServerSalt.read(b_io)
            self.server_salt = bad_salt.new_server_salt
            logger.info("Updated server salt to %d", self.server_salt)
            return

        # 3. BadMsgNotification (0xa7eff811)
        if c_id == BadMsgNotification.ID:
            bad_msg = BadMsgNotification.read(b_io)
            logger.warning(
                "Received BadMsgNotification: error_code=%d for msg_id=%d",
                bad_msg.error_code,
                bad_msg.bad_msg_id,
            )
            req_entry = self._pending_requests.pop(bad_msg.bad_msg_id, None)
            if req_entry:
                fut, _ = req_entry
                if not fut.done():
                    fut.set_exception(
                        RPCError(bad_msg.error_code, f"BadMsgNotification {bad_msg.error_code}")
                    )
            return

        # 4. Updates or other TL objects
        try:
            tl_obj = read_tl_object(b_io)
            if tl_obj:
                for cb in self._update_callbacks:
                    try:
                        cb(tl_obj)
                    except Exception as e:
                        logger.error("Error in update callback: %s", e)
        except Exception as e:
            logger.debug("Failed to parse incoming TL object: %s", e)
