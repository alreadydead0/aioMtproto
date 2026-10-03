"""
Composable filters for userbot event handling.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Sequence
from re import Pattern
from typing import Any

from aiogram import types as tg_types
from aiogram.enums import ChatType


class Filter:
    """
    Base filter class supporting boolean composition (&, |, ~).
    """

    async def check(self, client: Any, update: Any) -> bool:
        raise NotImplementedError

    def __and__(self, other: Filter) -> Filter:
        return AndFilter(self, other)

    def __or__(self, other: Filter) -> Filter:
        return OrFilter(self, other)

    def __invert__(self) -> Filter:
        return InvertFilter(self)


class AndFilter(Filter):
    def __init__(self, *filters: Filter) -> None:
        self.filters = filters

    async def check(self, client: Any, update: Any) -> bool:
        for f in self.filters:
            if not await f.check(client, update):
                return False
        return True


class OrFilter(Filter):
    def __init__(self, *filters: Filter) -> None:
        self.filters = filters

    async def check(self, client: Any, update: Any) -> bool:
        for f in self.filters:
            if await f.check(client, update):
                return True
        return False


class InvertFilter(Filter):
    def __init__(self, base_filter: Filter) -> None:
        self.base_filter = base_filter

    async def check(self, client: Any, update: Any) -> bool:
        return not await self.base_filter.check(client, update)


class CustomFilter(Filter):
    def __init__(self, func: Callable[..., Any]) -> None:
        self.func = func

    async def check(self, client: Any, update: Any) -> bool:
        import inspect

        res = self.func(client, update)
        if inspect.isawaitable(res):
            return bool(await res)
        return bool(res)


class _MeFilter(Filter):
    async def check(self, client: Any, update: Any) -> bool:
        msg = update.message if isinstance(update, tg_types.Update) else update
        if msg is None:
            return False
        from_user = getattr(msg, "from_user", None)
        if not from_user:
            return False
        me = getattr(client, "me", None)
        me_id = getattr(me, "id", None)
        return bool(me_id and from_user.id == me_id)


class _IncomingFilter(Filter):
    async def check(self, client: Any, update: Any) -> bool:
        msg = update.message if isinstance(update, tg_types.Update) else update
        if msg is None:
            return False
        if hasattr(msg, "is_outgoing"):
            return not msg.is_outgoing
        me = getattr(client, "me", None)
        me_id = getattr(me, "id", None)
        from_user = getattr(msg, "from_user", None)
        if from_user is not None and me_id:
            return bool(from_user.id != me_id)
        return True


class _OutgoingFilter(Filter):
    async def check(self, client: Any, update: Any) -> bool:
        msg = update.message if isinstance(update, tg_types.Update) else update
        if msg is None:
            return False
        if hasattr(msg, "is_outgoing"):
            return bool(msg.is_outgoing)
        me = getattr(client, "me", None)
        me_id = getattr(me, "id", None)
        from_user = getattr(msg, "from_user", None)
        if from_user is not None and me_id:
            return bool(from_user.id == me_id)
        return False


class _PrivateFilter(Filter):
    async def check(self, client: Any, update: Any) -> bool:
        msg = update.message if isinstance(update, tg_types.Update) else update
        chat = getattr(msg, "chat", None)
        return bool(chat and chat.type == ChatType.PRIVATE)


class _GroupFilter(Filter):
    async def check(self, client: Any, update: Any) -> bool:
        msg = update.message if isinstance(update, tg_types.Update) else update
        chat = getattr(msg, "chat", None)
        return bool(chat and chat.type in (ChatType.GROUP, ChatType.SUPERGROUP))


class _ChannelFilter(Filter):
    async def check(self, client: Any, update: Any) -> bool:
        msg = update.message if isinstance(update, tg_types.Update) else update
        chat = getattr(msg, "chat", None)
        return bool(chat and chat.type == ChatType.CHANNEL)


class _TextFilter(Filter):
    async def check(self, client: Any, update: Any) -> bool:
        msg = update.message if isinstance(update, tg_types.Update) else update
        return bool(getattr(msg, "text", None))


class _PhotoFilter(Filter):
    async def check(self, client: Any, update: Any) -> bool:
        msg = update.message if isinstance(update, tg_types.Update) else update
        return bool(getattr(msg, "photo", None))


class _VideoFilter(Filter):
    async def check(self, client: Any, update: Any) -> bool:
        msg = update.message if isinstance(update, tg_types.Update) else update
        return bool(getattr(msg, "video", None))


class _DocumentFilter(Filter):
    async def check(self, client: Any, update: Any) -> bool:
        msg = update.message if isinstance(update, tg_types.Update) else update
        return bool(getattr(msg, "document", None))


class _AudioFilter(Filter):
    async def check(self, client: Any, update: Any) -> bool:
        msg = update.message if isinstance(update, tg_types.Update) else update
        return bool(getattr(msg, "audio", None))


class _VoiceFilter(Filter):
    async def check(self, client: Any, update: Any) -> bool:
        msg = update.message if isinstance(update, tg_types.Update) else update
        return bool(getattr(msg, "voice", None))


class _MediaFilter(Filter):
    async def check(self, client: Any, update: Any) -> bool:
        msg = update.message if isinstance(update, tg_types.Update) else update
        return bool(
            getattr(msg, "photo", None)
            or getattr(msg, "video", None)
            or getattr(msg, "document", None)
            or getattr(msg, "audio", None)
            or getattr(msg, "voice", None)
            or getattr(msg, "animation", None)
            or getattr(msg, "sticker", None)
        )


class CommandFilter(Filter):
    def __init__(self, commands: str | Sequence[str], prefixes: str | Sequence[str] = "/") -> None:
        self.commands = [commands] if isinstance(commands, str) else list(commands)
        self.prefixes = [prefixes] if isinstance(prefixes, str) else list(prefixes)

    async def check(self, client: Any, update: Any) -> bool:
        msg = update.message if isinstance(update, tg_types.Update) else update
        text = getattr(msg, "text", "") or getattr(msg, "caption", "") or ""
        if not text:
            return False

        for prefix in self.prefixes:
            if text.startswith(prefix):
                without_prefix = text[len(prefix) :]
                parts = without_prefix.split(maxsplit=1)
                cmd = parts[0].split("@")[0] if parts else ""
                if cmd in self.commands:
                    return True
        return False


class RegexFilter(Filter):
    def __init__(self, pattern: str | Pattern[str], flags: int = 0) -> None:
        self.pattern = re.compile(pattern, flags) if isinstance(pattern, str) else pattern

    async def check(self, client: Any, update: Any) -> bool:
        msg = update.message if isinstance(update, tg_types.Update) else update
        text = getattr(msg, "text", "") or getattr(msg, "caption", "") or ""
        if not text:
            return False
        return bool(self.pattern.search(text))


class UserFilter(Filter):
    def __init__(self, users: int | str | Sequence[int | str]) -> None:
        self.users = {users} if isinstance(users, (int, str)) else set(users)

    async def check(self, client: Any, update: Any) -> bool:
        msg = update.message if isinstance(update, tg_types.Update) else update
        user = getattr(msg, "from_user", None)
        if not user:
            return False
        if user.id in self.users:
            return True
        return bool(
            user.username
            and (user.username.lower() in self.users or f"@{user.username.lower()}" in self.users)
        )


class ChatFilter(Filter):
    def __init__(self, chats: int | str | Sequence[int | str]) -> None:
        self.chats = {chats} if isinstance(chats, (int, str)) else set(chats)

    async def check(self, client: Any, update: Any) -> bool:
        msg = update.message if isinstance(update, tg_types.Update) else update
        chat = getattr(msg, "chat", None)
        if not chat:
            return False
        if chat.id in self.chats:
            return True
        return bool(
            chat.username
            and (chat.username.lower() in self.chats or f"@{chat.username.lower()}" in self.chats)
        )


class filters:
    """
    Namespace for userbot event filters.
    """

    me: Filter = _MeFilter()
    incoming: Filter = _IncomingFilter()
    outgoing: Filter = _OutgoingFilter()
    private: Filter = _PrivateFilter()
    group: Filter = _GroupFilter()
    channel: Filter = _ChannelFilter()
    text: Filter = _TextFilter()
    photo: Filter = _PhotoFilter()
    video: Filter = _VideoFilter()
    document: Filter = _DocumentFilter()
    audio: Filter = _AudioFilter()
    voice: Filter = _VoiceFilter()
    media: Filter = _MediaFilter()

    @staticmethod
    def command(commands: str | Sequence[str], prefixes: str | Sequence[str] = "/") -> Filter:
        return CommandFilter(commands=commands, prefixes=prefixes)

    @staticmethod
    def regex(pattern: str | Pattern[str], flags: int = 0) -> Filter:
        return RegexFilter(pattern=pattern, flags=flags)

    @staticmethod
    def user(users: int | str | Sequence[int | str]) -> Filter:
        return UserFilter(users=users)

    @staticmethod
    def chat(chats: int | str | Sequence[int | str]) -> Filter:
        return ChatFilter(chats=chats)

    @staticmethod
    def custom(func: Callable[..., Any]) -> Filter:
        return CustomFilter(func=func)

    @staticmethod
    def create(func: Callable[..., Any]) -> Filter:
        return CustomFilter(func=func)
