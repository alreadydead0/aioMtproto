"""
MTProto Client for aiogram.
"""

from __future__ import annotations

import asyncio
import logging
import os
import random
from collections.abc import AsyncGenerator, Callable
from typing import Any, BinaryIO, List, Optional, TypeVar, Union

logger = logging.getLogger("aiogram.client.mtproto")

from aiogram import types as tg_types
from aiogram.enums import ChatType
from aiogram.mtproto.auth.handshake import do_handshake
from aiogram.mtproto.connection.dc import DataCenter, get_dc
from aiogram.mtproto.connection.dc_manager import DCClientSession, DCManager
from aiogram.mtproto.connection.tcp import TCPConnection
from aiogram.mtproto.connection.transport import BaseTransport, IntermediateTransport
from aiogram.mtproto.protocol.rpc import RPCEngine
from aiogram.mtproto.updates.normalizer import normalize_tl_update
from aiogram.raw import functions as raw_funcs
from aiogram.raw import types as raw_types
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

        self.dc_manager = DCManager(
            api_id=self.api_id,
            api_hash=self.api_hash,
            main_dc_id=self.dc_id,
            test_mode=self.test_mode,
            bot_token=self.bot_token,
            transport_factory=lambda: self.transport,
            session_storage=self.session_storage,
        )
        self.dc_manager.add_update_handler(self._on_raw_update)

        self.session_data: SessionData | None = None
        self.me: tg_types.User | None = None
        self._update_queue: asyncio.Queue[tg_types.Update] = asyncio.Queue()
        self._update_counter = 1

    @property
    def connection(self) -> TCPConnection | None:
        main = self.dc_manager._sessions.get(self.dc_manager.main_dc_id)
        return main.connection if main else None

    @property
    def rpc(self) -> RPCEngine | None:
        main = self.dc_manager._sessions.get(self.dc_manager.main_dc_id)
        return main.rpc if main else None

    @property
    def is_connected(self) -> bool:
        main = self.dc_manager._sessions.get(self.dc_manager.main_dc_id)
        return main is not None and main.is_ready

    async def get_media_client(self, dc_id: int) -> DCClientSession:
        """
        Get or spawn an MTProto client connected and authorized to a specific Data Center.
        """
        return await self.dc_manager.get_media_client(dc_id)

    async def connect(self) -> None:
        """
        Connect to Telegram MTProto, load/generate AuthKey, and start RPC engine.
        """
        main_client = await self.dc_manager.get_dc_client(
            self.dc_manager.main_dc_id, is_media=False
        )
        self.session_data = await self.session_storage.load()
        self.dc_id = self.dc_manager.main_dc_id

        if self.bot_token and not getattr(self.session_data, "user_id", None):
            try:
                await self.sign_in_bot()
            except Exception as e:
                logger.debug("Auto sign_in_bot in connect: %s", e)

    def _on_raw_update(self, raw_update_obj: Any) -> None:
        """
        Callback when raw update is received from MTProto stream.
        """
        normalized_updates = normalize_tl_update(raw_update_obj, update_id=self._update_counter)
        self._update_counter += len(normalized_updates)
        for upd in normalized_updates:
            self._update_queue.put_nowait(upd)

    async def updates_stream(self) -> AsyncGenerator[tg_types.Update, None]:
        """
        Stream normalized Telegram updates from the MTProto event loop.
        """
        if not self.is_connected:
            await self.connect()
        while self.is_connected:
            try:
                update = await asyncio.wait_for(self._update_queue.get(), timeout=1.0)
                yield update
            except asyncio.TimeoutError:
                continue

    async def disconnect(self) -> None:
        """
        Disconnect from MTProto and close all active DC sessions.
        """
        if self.session_data and self.rpc:
            self.session_data.server_salt = self.rpc.server_salt
            await self.session_storage.save(self.session_data)
        await self.dc_manager.close_all()

    async def invoke(
        self, query: TLRequest[T], timeout: float = 30.0, target_dc_id: int | None = None
    ) -> T:
        """
        Execute raw Telegram MTProto RPC query with automatic AuthKey regeneration,
        automatic DC migration (USER_MIGRATE, NETWORK_MIGRATE, PHONE_MIGRATE),
        and AUTH_KEY_UNREGISTERED recovery.
        """
        res = await self.dc_manager.invoke(query, timeout=timeout, target_dc_id=target_dc_id)
        self.dc_id = self.dc_manager.main_dc_id
        return res

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

    async def sign_in(
        self, phone_number: str, phone_code_hash: str, phone_code: str
    ) -> tg_types.User:
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

        if self.bot_token:
            return await self.sign_in_bot()

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

    async def send_document(
        self,
        chat_id: int | str,
        document: Any,
        file_name: str | None = None,
        caption: str = "",
        mime_type: str = "application/octet-stream",
        reply_to_message_id: int | None = None,
        progress: Callable[[int, int], None] | None = None,
        workers: int = 8,
        force_file: bool = True,
    ) -> tg_types.Message:
        """
        Upload and send any document/file up to 2GB via MTProto without Bot API 50MB HTTP limit.
        """
        if isinstance(document, (raw_types.InputFile, raw_types.InputFileBig)):
            input_file = document
        else:
            input_file = await self.upload_file(
                source=document,
                file_name=file_name,
                progress=progress,
                workers=workers,
            )

        actual_name = file_name or getattr(input_file, "name", "file.bin")
        attributes: list[raw_types.TLObject] = [
            raw_types.DocumentAttributeFilename(file_name=actual_name)
        ]
        media = raw_types.InputMediaUploadedDocument(
            file=input_file,
            mime_type=mime_type,
            attributes=attributes,
            force_file=force_file,
        )
        peer = _to_input_peer(chat_id)
        random_id = random.getrandbits(63)
        await self.invoke(
            raw_funcs.messages.SendMedia(
                peer=peer,
                media=media,
                message=caption,
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
            text=caption,
        )

    async def send_video(
        self,
        chat_id: int | str,
        video: Any,
        file_name: str | None = None,
        caption: str = "",
        duration: float = 0.0,
        width: int = 0,
        height: int = 0,
        supports_streaming: bool = True,
        reply_to_message_id: int | None = None,
        progress: Callable[[int, int], None] | None = None,
        workers: int = 8,
    ) -> tg_types.Message:
        """
        Upload and send any video up to 2GB via MTProto without Bot API 50MB HTTP limit.
        """
        if isinstance(video, (raw_types.InputFile, raw_types.InputFileBig)):
            input_file = video
        else:
            input_file = await self.upload_file(
                source=video,
                file_name=file_name,
                progress=progress,
                workers=workers,
            )

        actual_name = file_name or getattr(input_file, "name", "video.mp4")
        attributes: list[raw_types.TLObject] = [
            raw_types.DocumentAttributeFilename(file_name=actual_name),
            raw_types.DocumentAttributeVideo(
                duration=duration,
                w=width,
                h=height,
                supports_streaming=supports_streaming,
            ),
        ]
        media = raw_types.InputMediaUploadedDocument(
            file=input_file,
            mime_type="video/mp4",
            attributes=attributes,
            force_file=False,
        )
        peer = _to_input_peer(chat_id)
        random_id = random.getrandbits(63)
        await self.invoke(
            raw_funcs.messages.SendMedia(
                peer=peer,
                media=media,
                message=caption,
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
            text=caption,
        )

    async def download_file(
        self,
        location: Any,
        file_size: int | None = None,
        destination: Any = None,
        progress: Callable[[int, int], None] | None = None,
        workers: int = 8,
        refresh_location: Any = None,
    ) -> bytes | str | BinaryIO:
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
            refresh_location=refresh_location,
        )

    async def export_session_string(self) -> str:
        """
        Export the current authorized MTProto session as a portable Base64 string.
        """
        data = await self.session_storage.load()
        return StringSession._encode(data)
