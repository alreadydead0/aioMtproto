"""
MTProto Client for aiogram.
"""

from __future__ import annotations

import asyncio
import datetime
import html
import logging
import os
import random
import re
from collections.abc import AsyncGenerator, Callable
from typing import Any, BinaryIO, TypeVar

from aiogram import types as tg_types
from aiogram.client.peer_resolver import PeerResolver
from aiogram.enums import ChatType
from aiogram.mtproto.auth.handshake import do_handshake
from aiogram.mtproto.connection.dc import DataCenter, get_dc
from aiogram.mtproto.connection.dc_manager import DCClientSession, DCManager
from aiogram.mtproto.connection.tcp import TCPConnection
from aiogram.mtproto.connection.transport import BaseTransport, IntermediateTransport
from aiogram.mtproto.crypto.srp import compute_srp_password
from aiogram.mtproto.protocol.rpc import RPCEngine
from aiogram.mtproto.updates.normalizer import normalize_tl_update
from aiogram.raw import functions as raw_funcs
from aiogram.raw import types as raw_types
from aiogram.raw.core.primitives import TLRequest
from aiogram.session.base import BaseMTProtoSession, SessionData
from aiogram.session.memory import MemorySession
from aiogram.session.sqlite import SQLiteSession
from aiogram.session.string import StringSession

logger = logging.getLogger("aiogram.client.mtproto")
T = TypeVar("T")


def _to_input_peer(peer_id: Any, access_hash: int = 0) -> raw_types.InputPeer:
    """
    Resolve peer identifier to InputPeer (synchronous fallback).
    """
    if isinstance(peer_id, raw_types.InputPeer):
        return peer_id
    if isinstance(peer_id, str):
        if peer_id.lower() in ("me", "self"):
            return raw_types.InputPeerSelf()
        if peer_id.lstrip("-").isdigit():
            peer_id = int(peer_id)
        else:
            return raw_types.InputPeerSelf()
    if isinstance(peer_id, int):
        if peer_id > 0:
            return raw_types.InputPeerUser(user_id=peer_id, access_hash=access_hash)
        if str(peer_id).startswith("-100"):
            channel_id = int(str(peer_id)[4:])
            return raw_types.InputPeerChannel(channel_id=channel_id, access_hash=access_hash)
        return raw_types.InputPeerChat(chat_id=-peer_id)
    # Default to self
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
        max_concurrent_transmissions: int = 10,
    ) -> None:
        self.api_id = api_id
        self.api_hash = api_hash
        self.dc_id = dc_id
        self.test_mode = test_mode
        self.bot_token = bot_token
        self.transport = transport or IntermediateTransport()
        self.max_concurrent_transmissions = max(1, max_concurrent_transmissions)
        self._transmission_semaphore = asyncio.Semaphore(self.max_concurrent_transmissions)

        if isinstance(session, str):
            if session == ":memory:":
                self.session_storage: BaseMTProtoSession = MemorySession()
            elif (
                StringSession.is_valid(session)
                or session.startswith("AIOG")
                or session.startswith("AIO2")
                or len(session) > 100
            ):
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

        self.peer_resolver = PeerResolver(self)
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

    def get_media_pool(self, dc_id: int, pool_size: int = 4) -> Any:
        """
        Get or create a DCSessionPool for the target Data Center.
        """
        return self.dc_manager.get_media_pool(dc_id, pool_size=pool_size)

    async def get_media_client(
        self,
        dc_id: int,
        worker_idx: int | None = None,
        pool_size: int = 4,
    ) -> DCClientSession:
        """
        Get or spawn an MTProto client connected and authorized to a specific Data Center.
        When worker_idx is provided, returns a dedicated session from the DCSessionPool.
        """
        return await self.dc_manager.get_media_client(
            dc_id, worker_idx=worker_idx, pool_size=pool_size
        )

    @property
    def is_premium(self) -> bool:
        """
        Check if the authenticated user has Telegram Premium.
        """
        if self.me is not None:
            return bool(getattr(self.me, "is_premium", False))
        return False

    @property
    def max_file_size(self) -> int:
        """
        Maximum supported upload/download file size:
        - 4 GB (4000 MB) for Telegram Premium users.
        - 2 GB (2000 MB) for standard non-premium users and bot accounts.
        """
        if self.is_premium:
            return 4000 * 1024 * 1024  # 4 GB
        return 2000 * 1024 * 1024  # 2 GB

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
        elif self.session_data and getattr(self.session_data, "user_id", None):
            try:
                await self.get_me()
                if self.is_premium:
                    logger.info(
                        "🌟 [DC %d] Authenticated as Telegram Premium User (4GB Uploads Enabled)",
                        self.dc_id,
                    )
                else:
                    logger.info(
                        "👤 [DC %d] Authenticated as Standard User (2GB Uploads Enabled)",
                        self.dc_id,
                    )
            except Exception as e:
                logger.debug("Auto get_me in connect: %s", e)

    async def warmup(self, media_dcs: list[int] | None = None, pool_size: int = 8) -> None:
        """
        Pre-connect main DC and pre-warm media DC session pools on bot startup/deploy.
        Eliminates startup lag, making initial media transfers 100% instantaneous.
        """
        await self.connect()
        target_dcs = media_dcs or list({self.dc_manager.main_dc_id, 4, 2, 5})
        tasks = []
        for dc_id in target_dcs:
            tasks.append(self.get_media_client(dc_id, worker_idx=0, pool_size=pool_size))
        await asyncio.gather(*tasks, return_exceptions=True)
        logger.info(
            "⚡ MTProto DC Pre-Warmup complete for DCs %s (pool_size=%d)", target_dcs, pool_size
        )

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
            is_premium=getattr(raw_user, "premium", False),
        )
        if self.session_data:
            self.session_data.user_id = self.me.id
            self.session_data.is_bot = True
            await self.session_storage.save(self.session_data)
        return self.me

    async def resolve_peer(self, peer: Any) -> raw_types.InputPeer:
        """
        Resolve peer identifier into raw InputPeer.
        """
        return await self.peer_resolver.resolve_peer(peer)

    async def send_code(
        self, phone_number: str, settings: raw_types.CodeSettings | None = None
    ) -> raw_types.SentCode:
        """
        Send SMS/Telegram login code for user authorization.
        """
        return await self.invoke(
            raw_funcs.auth.SendCode(
                phone_number=phone_number,
                api_id=self.api_id,
                api_hash=self.api_hash,
                settings=settings,
            )
        )

    async def resend_code(
        self, phone_number: str, phone_code_hash: str, reason: str | None = None
    ) -> raw_types.SentCode:
        """
        Resend SMS/Telegram login code.
        """
        return await self.invoke(
            raw_funcs.auth.ResendCode(
                phone_number=phone_number,
                phone_code_hash=phone_code_hash,
                reason=reason,
            )
        )

    async def cancel_code(self, phone_number: str, phone_code_hash: str) -> bool:
        """
        Cancel login code request.
        """
        return await self.invoke(
            raw_funcs.auth.CancelCode(
                phone_number=phone_number,
                phone_code_hash=phone_code_hash,
            )
        )

    async def sign_in(
        self, phone_number: str, phone_code_hash: str, phone_code: str | None = None
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
        self.peer_resolver.cache_user(raw_user)
        self.me = tg_types.User(
            id=raw_user.id,
            is_bot=raw_user.bot,
            first_name=raw_user.first_name or "",
            last_name=raw_user.last_name,
            username=raw_user.username,
            language_code=raw_user.lang_code,
            is_premium=getattr(raw_user, "premium", False),
        )
        if self.session_data:
            self.session_data.user_id = self.me.id
            self.session_data.phone = phone_number
            self.session_data.is_bot = False
            self.session_data.api_id = self.api_id
            await self.session_storage.save(self.session_data)
        return self.me

    async def sign_up(
        self,
        phone_number: str,
        phone_code_hash: str,
        first_name: str,
        last_name: str = "",
    ) -> tg_types.User:
        """
        Sign up a new Telegram user.
        """
        res = await self.invoke(
            raw_funcs.auth.SignUp(
                phone_number=phone_number,
                phone_code_hash=phone_code_hash,
                first_name=first_name,
                last_name=last_name,
            )
        )
        raw_user = res.user
        self.peer_resolver.cache_user(raw_user)
        self.me = tg_types.User(
            id=raw_user.id,
            is_bot=raw_user.bot,
            first_name=raw_user.first_name or "",
            last_name=raw_user.last_name,
            username=raw_user.username,
            language_code=raw_user.lang_code,
            is_premium=getattr(raw_user, "premium", False),
        )
        if self.session_data:
            self.session_data.user_id = self.me.id
            self.session_data.phone = phone_number
            self.session_data.is_bot = False
            self.session_data.api_id = self.api_id
            await self.session_storage.save(self.session_data)
        return self.me

    async def check_password(self, password: str) -> tg_types.User:
        """
        Authenticate using 2FA cloud password via MTProto SRP protocol.
        """
        acc_pwd = await self.invoke(raw_funcs.account.GetPassword())
        srp_input = compute_srp_password(password, acc_pwd)
        res = await self.invoke(raw_funcs.auth.CheckPassword(password=srp_input))
        raw_user = res.user
        self.peer_resolver.cache_user(raw_user)
        self.me = tg_types.User(
            id=raw_user.id,
            is_bot=raw_user.bot,
            first_name=raw_user.first_name or "",
            last_name=raw_user.last_name,
            username=raw_user.username,
            language_code=raw_user.lang_code,
            is_premium=getattr(raw_user, "premium", False),
        )
        if self.session_data:
            self.session_data.user_id = self.me.id
            self.session_data.is_bot = False
            self.session_data.api_id = self.api_id
            await self.session_storage.save(self.session_data)
        return self.me

    async def log_out(self) -> bool:
        """
        Log out current session and invalidate local storage.
        """
        try:
            await self.invoke(raw_funcs.auth.LogOut())
        except Exception as e:
            logger.debug("LogOut RPC returned error: %s", e)
        await self.session_storage.delete()
        self.me = None
        return True

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
            self.peer_resolver.cache_user(raw_user)
            self.me = tg_types.User(
                id=raw_user.id,
                is_bot=raw_user.bot,
                first_name=raw_user.first_name or "",
                last_name=raw_user.last_name,
                username=raw_user.username,
                language_code=raw_user.lang_code,
                is_premium=getattr(raw_user, "premium", False),
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
        peer = await self.peer_resolver.resolve_peer(chat_id)
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
            date=datetime.datetime.now(datetime.timezone.utc),
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
        peer = await self.peer_resolver.resolve_peer(chat_id)
        await self.invoke(raw_funcs.messages.EditMessage(peer=peer, id=message_id, message=text))
        chat_id_int = chat_id if isinstance(chat_id, int) else 0
        chat = tg_types.Chat(id=chat_id_int, type=ChatType.PRIVATE)
        return tg_types.Message(
            message_id=message_id,
            date=datetime.datetime.now(datetime.timezone.utc),
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

    async def forward_messages(
        self,
        from_chat_id: int | str,
        to_chat_id: int | str,
        message_ids: list[int],
        drop_author: bool = False,
        drop_media_captions: bool = False,
    ) -> Any:
        """
        Forward messages from one chat to another.
        """
        from_peer = await self.peer_resolver.resolve_peer(from_chat_id)
        to_peer = await self.peer_resolver.resolve_peer(to_chat_id)
        return await self.invoke(
            raw_funcs.messages.ForwardMessages(
                from_peer=from_peer,
                to_peer=to_peer,
                id=message_ids,
                drop_author=drop_author,
                drop_media_captions=drop_media_captions,
            )
        )

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
        async with self._transmission_semaphore:
            return await uploader.upload(source=source, file_name=file_name, progress=progress)

    async def send_document(
        self,
        chat_id: int | str,
        document: Any,
        file_name: str | None = None,
        caption: str = "",
        parse_mode: str | None = None,
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

        actual_name = str(file_name or getattr(input_file, "name", "file.bin"))
        attributes: list[raw_types.TLObject] = [
            raw_types.DocumentAttributeFilename(file_name=actual_name)
        ]
        media = raw_types.InputMediaUploadedDocument(
            file=input_file,
            mime_type=mime_type,
            attributes=attributes,
            force_file=force_file,
        )
        clean_text = html.unescape(re.sub(r"<[^>]+>", "", caption)) if caption else ""
        peer = await self.peer_resolver.resolve_peer(chat_id)
        random_id = random.getrandbits(63)
        await self.invoke(
            raw_funcs.messages.SendMedia(
                peer=peer,
                media=media,
                message=clean_text,
                random_id=random_id,
                reply_to_msg_id=reply_to_message_id,
            )
        )
        chat_id_int = chat_id if isinstance(chat_id, int) else 0
        chat = tg_types.Chat(id=chat_id_int, type=ChatType.PRIVATE)
        return tg_types.Message(
            message_id=random_id & 0x7FFFFFFF,
            date=datetime.datetime.now(datetime.timezone.utc),
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
        parse_mode: str | None = None,
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

        actual_name = str(file_name or getattr(input_file, "name", "video.mp4"))
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
        clean_text = html.unescape(re.sub(r"<[^>]+>", "", caption)) if caption else ""
        peer = await self.peer_resolver.resolve_peer(chat_id)
        random_id = random.getrandbits(63)
        await self.invoke(
            raw_funcs.messages.SendMedia(
                peer=peer,
                media=media,
                message=clean_text,
                random_id=random_id,
                reply_to_msg_id=reply_to_message_id,
            )
        )
        chat_id_int = chat_id if isinstance(chat_id, int) else 0
        chat = tg_types.Chat(id=chat_id_int, type=ChatType.PRIVATE)
        return tg_types.Message(
            message_id=random_id & 0x7FFFFFFF,
            date=datetime.datetime.now(datetime.timezone.utc),
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
        async with self._transmission_semaphore:
            return await downloader.download(
                location=location,
                file_size=file_size,
                destination=destination,
                progress=progress,
                refresh_location=refresh_location,
            )

    async def export_session_string(self) -> str:
        """
        Export current authorized MTProto session as portable native aioMtproto string.
        """
        data = await self.session_storage.load()
        return StringSession._encode(data)
