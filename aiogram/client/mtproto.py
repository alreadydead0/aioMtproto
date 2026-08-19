"""
MTProto Client for aiogram.
"""

from __future__ import annotations

import asyncio
import os
import random
from collections.abc import AsyncGenerator
from typing import Any, Callable, List, Optional, TypeVar, Union

from aiogram import types as tg_types
from aiogram.enums import ChatType
from aiogram.mtproto.auth.handshake import do_handshake
from aiogram.mtproto.connection.dc import DataCenter, get_dc
from aiogram.mtproto.connection.tcp import TCPConnection
from aiogram.mtproto.connection.transport import BaseTransport, IntermediateTransport
from aiogram.mtproto.protocol.rpc import RPCEngine
from aiogram.mtproto.updates.normalizer import normalize_tl_update
from aiogram.raw import functions as raw_funcs, types as raw_types
from aiogram.raw.core.primitives import TLRequest
from aiogram.session.base import BaseMTProtoSession, SessionData
from aiogram.session.memory import MemorySession
from aiogram.session.sqlite import SQLiteSession
from aiogram.session.string import StringSession

T = TypeVar("T")


def _to_input_peer(peer_id: int | str) -> raw_types.InputPeer:
    """
    Resolve peer identifier to InputPeer.
    """
    if isinstance(peer_id, int):
        if peer_id > 0:
            return raw_types.InputPeerUser(user_id=peer_id, access_hash=0)
        if str(peer_id).startswith("-100"):
            channel_id = int(str(peer_id)[4:])
            return raw_types.InputPeerChannel(channel_id=channel_id, access_hash=0)
        return raw_types.InputPeerChat(chat_id=-peer_id)
    # Default to user
    return raw_types.InputPeerSelf()


class MTProtoClient:
    """
    Core MTProto 2.0 client managing connection, RPC engine, and updates stream.
    """

    def __init__(
        self,
        api_id: int,
        api_hash: str,
        session: str | BaseMTProtoSession = "aiogram.session",
        dc_id: int = 2,
        test_mode: bool = False,
        transport: BaseTransport | None = None,
        bot_token: str | None = None,
    ) -> None:
        self.api_id = api_id
        self.api_hash = api_hash
        self.dc_id = dc_id
        self.test_mode = test_mode
        self.bot_token = bot_token
        self.transport = transport or IntermediateTransport()

        if isinstance(session, str):
            if session == ":memory:":
                self.session_storage: BaseMTProtoSession = MemorySession()
            elif session.startswith("AIOG") or len(session) > 100:
                self.session_storage = StringSession(session)
            else:
                self.session_storage = SQLiteSession(session)
        else:
            self.session_storage = session

        self.session_data: SessionData | None = None
        self.connection: TCPConnection | None = None
        self.rpc: RPCEngine | None = None
        self.me: tg_types.User | None = None

        self._update_queue: asyncio.Queue[tg_types.Update] = asyncio.Queue()
        self._update_counter = 1
        self._is_connected = False

    @property
    def is_connected(self) -> bool:
        return self._is_connected and self.connection is not None and self.connection.is_connected

    async def connect(self) -> None:
        """
        Connect to Telegram MTProto, load/generate AuthKey, and start RPC engine.
        """
        if self.is_connected:
            return

        self.session_data = await self.session_storage.load()
        dc = get_dc(self.session_data.dc_id or self.dc_id, test_mode=self.test_mode)
        self.connection = TCPConnection(dc=dc, transport=self.transport)

        await self.connection.connect()

        # Generate AuthKey via 3-step DH handshake if not present
        if not self.session_data.auth_key:
            auth_key, server_salt = await do_handshake(self.connection)
            self.session_data.auth_key = auth_key
            self.session_data.server_salt = server_salt
            self.session_data.dc_id = dc.dc_id
            self.session_data.server_address = dc.ip_address
            self.session_data.port = dc.port
            await self.session_storage.save(self.session_data)

        self.rpc = RPCEngine(
            connection=self.connection,
            auth_key=self.session_data.auth_key,
            server_salt=self.session_data.server_salt,
            api_id=self.api_id,
        )
        self.rpc.add_update_handler(self._on_raw_update)
        self.rpc.start()
        self._is_connected = True

    def _on_raw_update(self, raw_update_obj: Any) -> None:
        """
        Callback when raw update is received from MTProto stream.
        """
        normalized_updates = normalize_tl_update(raw_update_obj, update_id=self._update_counter)
        self._update_counter += len(normalized_updates)
        for upd in normalized_updates:
            self._update_queue.put_nowait(upd)

    async def disconnect(self) -> None:
        """
        Disconnect from MTProto and save session state.
        """
        self._is_connected = False
        if self.rpc:
            if self.session_data:
                self.session_data.server_salt = self.rpc.server_salt
                await self.session_storage.save(self.session_data)
            await self.rpc.stop()
            self.rpc = None
        if self.connection:
            await self.connection.close()
            self.connection = None

    async def invoke(self, query: TLRequest[T], timeout: float = 30.0) -> T:
        """
        Execute raw Telegram MTProto RPC query.
        """
        if not self.is_connected:
            await self.connect()
        assert self.rpc is not None
        return await self.rpc.invoke(query, timeout=timeout)

    async def sign_in_bot(self, token: str | None = None) -> tg_types.User:
        """
        Sign in using Telegram Bot Token over MTProto.
        """
        token = token or self.bot_token
        if not token:
            msg = "Bot token is required for bot authentication"
            raise ValueError(msg)

        res = await self.invoke(
            raw_funcs.auth.ImportBotAuthorization(
                api_id=self.api_id,
                api_hash=self.api_hash,
                bot_auth_token=token,
            )
        )
        raw_user = res.user
        self.me = tg_types.User(
            id=raw_user.id,
            is_bot=raw_user.bot,
            first_name=raw_user.first_name or "",
            last_name=raw_user.last_name,
            username=raw_user.username,
            language_code=raw_user.lang_code,
        )
        if self.session_data:
            self.session_data.user_id = self.me.id
            self.session_data.is_bot = True
            await self.session_storage.save(self.session_data)
        return self.me

    async def send_code(self, phone_number: str) -> raw_types.SentCode:
        """
        Send SMS/Telegram login code for user authorization.
        """
        return await self.invoke(
            raw_funcs.auth.SendCode(
                phone_number=phone_number,
                api_id=self.api_id,
                api_hash=self.api_hash,
            )
        )

    async def sign_in(self, phone_number: str, phone_code_hash: str, phone_code: str) -> tg_types.User:
        """
        Complete user authorization using received code.
        """
        res = await self.invoke(
            raw_funcs.auth.SignIn(
                phone_number=phone_number,
                phone_code_hash=phone_code_hash,
                phone_code=phone_code,
            )
        )
        raw_user = res.user
        self.me = tg_types.User(
            id=raw_user.id,
            is_bot=raw_user.bot,
            first_name=raw_user.first_name or "",
            last_name=raw_user.last_name,
            username=raw_user.username,
            language_code=raw_user.lang_code,
        )
        if self.session_data:
            self.session_data.user_id = self.me.id
            self.session_data.phone = phone_number
            self.session_data.is_bot = False
            await self.session_storage.save(self.session_data)
        return self.me

    async def get_me(self) -> tg_types.User:
        """
        Get current authenticated user information.
        """
        if self.me is not None:
            return self.me

        users_res = await self.invoke(raw_funcs.users.GetUsers(id=[raw_types.InputPeerSelf()]))
        if users_res and len(users_res) > 0:
            raw_user = users_res[0]
            self.me = tg_types.User(
                id=raw_user.id,
                is_bot=raw_user.bot,
                first_name=raw_user.first_name or "",
                last_name=raw_user.last_name,
                username=raw_user.username,
                language_code=raw_user.lang_code,
            )
            return self.me

        msg = "User is not authenticated"
        raise ValueError(msg)

    async def send_message(
        self,
        chat_id: int | str,
        text: str,
        reply_to_message_id: int | None = None,
    ) -> tg_types.Message:
        """
        Send a text message via MTProto.
        """
        peer = _to_input_peer(chat_id)
        random_id = random.getrandbits(63)
        res = await self.invoke(
            raw_funcs.messages.SendMessage(
                peer=peer,
                message=text,
                random_id=random_id,
                reply_to_msg_id=reply_to_message_id,
            )
        )

        chat_id_int = chat_id if isinstance(chat_id, int) else 0
        chat = tg_types.Chat(id=chat_id_int, type=ChatType.PRIVATE)
        return tg_types.Message(
            message_id=random_id & 0x7FFFFFFF,
            date=tg_types.base.UNSET,
            chat=chat,
            from_user=self.me,
            text=text,
        )

    async def edit_message_text(
        self,
        chat_id: int | str,
        message_id: int,
        text: str,
    ) -> tg_types.Message:
        """
        Edit a message text via MTProto.
        """
        peer = _to_input_peer(chat_id)
        await self.invoke(raw_funcs.messages.EditMessage(peer=peer, id=message_id, message=text))
        chat_id_int = chat_id if isinstance(chat_id, int) else 0
        chat = tg_types.Chat(id=chat_id_int, type=ChatType.PRIVATE)
        return tg_types.Message(
            message_id=message_id,
            date=tg_types.base.UNSET,
            chat=chat,
            from_user=self.me,
            text=text,
        )

    async def delete_messages(
        self,
        chat_id: int | str,
        message_ids: list[int],
        revoke: bool = True,
    ) -> bool:
        """
        Delete messages via MTProto.
        """
        await self.invoke(raw_funcs.messages.DeleteMessages(id=message_ids, revoke=revoke))
        return True

    async def updates_stream(self) -> AsyncGenerator[tg_types.Update, None]:
        """
        Async generator yielding normalized updates received from MTProto stream.
        """
        if not self.is_connected:
            await self.connect()
        while self.is_connected:
            try:
                update = await asyncio.wait_for(self._update_queue.get(), timeout=1.0)
                yield update
            except asyncio.TimeoutError:
                continue

    async def upload_file(
        self,
        source: Any,
        file_name: str | None = None,
        progress: Callable[[int, int], None] | None = None,
        workers: int = 8,
    ) -> raw_types.InputFile | raw_types.InputFileBig:
        """
        Upload file using multi-worker parallel transfer engine.
        """
        from aiogram.media.uploader import FileUploader
        uploader = FileUploader(self, workers=workers)
        return await uploader.upload(source=source, file_name=file_name, progress=progress)

    async def download_file(
        self,
        location: Any,
        file_size: int | None = None,
        destination: Any = None,
        progress: Callable[[int, int], None] | None = None,
        workers: int = 8,
    ) -> bytes | str:
        """
        Download file using multi-worker parallel transfer engine with direct disk streaming.
        """
        from aiogram.media.downloader import FileDownloader
        downloader = FileDownloader(self, workers=workers)
        return await downloader.download(
            location=location,
            file_size=file_size,
            destination=destination,
            progress=progress,
        )

    async def export_session_string(self) -> str:
        """
        Export the current authorized MTProto session as a portable Base64 string.
        """
        data = await self.session_storage.load()
        return StringSession._encode(data)
