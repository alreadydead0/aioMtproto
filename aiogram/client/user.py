"""
Dedicated high-level MTProto UserClient (Userbot) for aioMtproto.
"""

from __future__ import annotations

import asyncio
import inspect
import logging
from collections.abc import Callable
from typing import Any, BinaryIO

from aiogram import types as tg_types
from aiogram.client.mtproto import MTProtoClient
from aiogram.dispatcher.userbot.dispatcher import UserbotDispatcher
from aiogram.dispatcher.userbot.filters import Filter
from aiogram.raw import types as raw_types
from aiogram.session.base import BaseMTProtoSession
from aiogram.session.string import StringSession

logger = logging.getLogger("aiogram.client.user")


class UserClient:
    """
    Production-grade Telegram MTProto Userbot Client.
    Supports user authentication (phone/code/2FA SRP), bot token login,
    native aioMtproto StringSessions, parallel 2GB/4GB media transfer engine,
    and event-driven update handlers.
    """

    def __init__(
        self,
        api_id: int,
        api_hash: str,
        session_string: str | None = None,
        session: str | BaseMTProtoSession | None = None,
        phone: str | None = None,
        bot_token: str | None = None,
        dc_id: int = 2,
        test_mode: bool = False,
        max_concurrent_transmissions: int = 10,
    ) -> None:
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.bot_token = bot_token
        self.dc_id = dc_id
        self.test_mode = test_mode

        session_target: str | BaseMTProtoSession = session or session_string or "userbot.session"
        self.mtproto = MTProtoClient(
            api_id=self.api_id,
            api_hash=self.api_hash,
            session=session_target,
            dc_id=self.dc_id,
            test_mode=self.test_mode,
            bot_token=self.bot_token,
            max_concurrent_transmissions=max_concurrent_transmissions,
        )
        self.dispatcher = UserbotDispatcher(self)
        self._is_started = False

    @property
    def me(self) -> tg_types.User | None:
        return self.mtproto.me

    @property
    def is_premium(self) -> bool:
        return self.mtproto.is_premium

    @property
    def is_connected(self) -> bool:
        return self.mtproto.is_connected

    async def get_me(self) -> tg_types.User:
        """
        Get current authenticated user info.
        """
        return await self.mtproto.get_me()

    async def start(
        self,
        phone: str | None = None,
        code_callback: Callable[[], Any] | None = None,
        password_callback: Callable[[], Any] | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> UserClient:
        """
        Start the user client, connect to MTProto, perform interactive or callback login
        if not authorized, and start the background update dispatcher.
        """
        if self._is_started:
            return self

        await self.mtproto.connect()

        # Check if already authenticated
        is_authenticated = False
        try:
            me = await self.mtproto.get_me()
            if me and me.id:
                is_authenticated = True
        except Exception:
            is_authenticated = False

        if not is_authenticated:
            if self.bot_token:
                await self.mtproto.sign_in_bot(self.bot_token)
            else:
                phone_number = phone or self.phone
                if not phone_number:
                    phone_number = input("Enter phone number (e.g. +1234567890): ").strip()

                sent_code = await self.mtproto.send_code(phone_number)
                phone_code_hash = sent_code.phone_code_hash

                if code_callback:
                    code_res = code_callback()
                    code = await code_res if inspect.isawaitable(code_res) else code_res
                else:
                    code = input("Enter the login code you received: ").strip()

                try:
                    await self.mtproto.sign_in(
                        phone_number=phone_number,
                        phone_code_hash=phone_code_hash,
                        phone_code=code,
                    )
                except Exception as e:
                    err_str = str(e)
                    if "SESSION_PASSWORD_NEEDED" in err_str:
                        if password_callback:
                            pwd_res = password_callback()
                            pwd = await pwd_res if inspect.isawaitable(pwd_res) else pwd_res
                        else:
                            import getpass

                            pwd = getpass.getpass("Enter 2FA password: ")
                        await self.mtproto.check_password(pwd)
                    elif "PHONE_NUMBER_UNREGISTERED" in err_str:
                        fn = first_name or input("Enter First Name for new account: ").strip()
                        ln = last_name or input("Enter Last Name: ").strip()
                        await self.mtproto.sign_up(
                            phone_number=phone_number,
                            phone_code_hash=phone_code_hash,
                            first_name=fn,
                            last_name=ln,
                        )
                    else:
                        raise

        self._is_started = True
        self.dispatcher.start()
        return self

    async def stop(self) -> None:
        """
        Stop the user client, cancel dispatcher workers, and disconnect MTProto sessions.
        """
        self.dispatcher.stop()
        await self.mtproto.disconnect()
        self._is_started = False

    async def disconnect(self) -> None:
        """Alias for stop()."""
        await self.stop()

    async def log_out(self) -> bool:
        """Log out the current user session and wipe session data."""
        self.dispatcher.stop()
        res = await self.mtproto.log_out()
        self._is_started = False
        return res

    async def export_session_string(self) -> str:
        """
        Export authorized session as a portable native aioMtproto Base64 string.
        """
        return await self.mtproto.export_session_string()

    # --- Messaging APIs ---

    async def send_message(
        self,
        chat_id: int | str,
        text: str,
        reply_to_message_id: int | None = None,
    ) -> tg_types.Message:
        """Send a text message."""
        return await self.mtproto.send_message(
            chat_id=chat_id,
            text=text,
            reply_to_message_id=reply_to_message_id,
        )

    async def edit_message_text(
        self,
        chat_id: int | str,
        message_id: int,
        text: str,
    ) -> tg_types.Message:
        """Edit message text."""
        return await self.mtproto.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
        )

    async def delete_messages(
        self,
        chat_id: int | str,
        message_ids: list[int] | int,
        revoke: bool = True,
    ) -> bool:
        """Delete one or more messages."""
        ids = [message_ids] if isinstance(message_ids, int) else list(message_ids)
        return await self.mtproto.delete_messages(chat_id=chat_id, message_ids=ids, revoke=revoke)

    async def forward_messages(
        self,
        from_chat_id: int | str,
        to_chat_id: int | str,
        message_ids: list[int] | int,
        drop_author: bool = False,
        drop_media_captions: bool = False,
    ) -> Any:
        """Forward messages between chats."""
        ids = [message_ids] if isinstance(message_ids, int) else list(message_ids)
        return await self.mtproto.forward_messages(
            from_chat_id=from_chat_id,
            to_chat_id=to_chat_id,
            message_ids=ids,
            drop_author=drop_author,
            drop_media_captions=drop_media_captions,
        )

    async def reply(
        self,
        message: tg_types.Message,
        text: str,
    ) -> tg_types.Message:
        """Reply to a message."""
        chat_id = message.chat.id
        return await self.send_message(
            chat_id=chat_id,
            text=text,
            reply_to_message_id=message.message_id,
        )

    # --- Media APIs ---

    async def upload_file(
        self,
        source: Any,
        file_name: str | None = None,
        progress: Callable[[int, int], None] | None = None,
        workers: int = 8,
    ) -> raw_types.InputFile | raw_types.InputFileBig:
        """Upload a file using parallel MTProto chunking engine."""
        return await self.mtproto.upload_file(
            source=source,
            file_name=file_name,
            progress=progress,
            workers=workers,
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
        """Download file using parallel MTProto chunking engine."""
        return await self.mtproto.download_file(
            location=location,
            file_size=file_size,
            destination=destination,
            progress=progress,
            workers=workers,
            refresh_location=refresh_location,
        )

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
        """Send any file or document."""
        return await self.mtproto.send_document(
            chat_id=chat_id,
            document=document,
            file_name=file_name,
            caption=caption,
            parse_mode=parse_mode,
            mime_type=mime_type,
            reply_to_message_id=reply_to_message_id,
            progress=progress,
            workers=workers,
            force_file=force_file,
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
        """Send video file."""
        return await self.mtproto.send_video(
            chat_id=chat_id,
            video=video,
            file_name=file_name,
            caption=caption,
            parse_mode=parse_mode,
            duration=duration,
            width=width,
            height=height,
            supports_streaming=supports_streaming,
            reply_to_message_id=reply_to_message_id,
            progress=progress,
            workers=workers,
        )

    async def send_photo(
        self,
        chat_id: int | str,
        photo: Any,
        file_name: str | None = None,
        caption: str = "",
        parse_mode: str | None = None,
        reply_to_message_id: int | None = None,
        progress: Callable[[int, int], None] | None = None,
        workers: int = 8,
    ) -> tg_types.Message:
        """Send photo."""
        return await self.send_document(
            chat_id=chat_id,
            document=photo,
            file_name=file_name or "photo.jpg",
            caption=caption,
            parse_mode=parse_mode,
            mime_type="image/jpeg",
            reply_to_message_id=reply_to_message_id,
            progress=progress,
            workers=workers,
            force_file=False,
        )

    async def send_audio(
        self,
        chat_id: int | str,
        audio: Any,
        file_name: str | None = None,
        caption: str = "",
        parse_mode: str | None = None,
        duration: int = 0,
        performer: str | None = None,
        title: str | None = None,
        reply_to_message_id: int | None = None,
        progress: Callable[[int, int], None] | None = None,
        workers: int = 8,
    ) -> tg_types.Message:
        """Send audio file."""
        return await self.send_document(
            chat_id=chat_id,
            document=audio,
            file_name=file_name or "audio.mp3",
            caption=caption,
            parse_mode=parse_mode,
            mime_type="audio/mpeg",
            reply_to_message_id=reply_to_message_id,
            progress=progress,
            workers=workers,
            force_file=False,
        )

    # --- Event Handler Decorators ---

    def on_message(self, filters: Filter | None = None) -> Callable[..., Any]:
        return self.dispatcher.on_message(filters)

    def on_edited_message(self, filters: Filter | None = None) -> Callable[..., Any]:
        return self.dispatcher.on_edited_message(filters)

    def on_deleted_messages(self, filters: Filter | None = None) -> Callable[..., Any]:
        return self.dispatcher.on_deleted_messages(filters)

    def on_raw_update(self) -> Callable[..., Any]:
        return self.dispatcher.on_raw_update()

    # --- Context Manager ---

    async def __aenter__(self) -> UserClient:
        await self.start()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.stop()
