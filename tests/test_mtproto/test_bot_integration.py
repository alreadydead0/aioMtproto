"""
Tests for aiogram Bot MTProto mode initialization and Dispatcher / Router integration.
"""

import asyncio
import datetime
import pytest

from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums import ChatType
from aiogram.mtproto.updates.normalizer import normalize_tl_update
from aiogram.raw.types import UpdateShortMessage
from aiogram.types import Chat, Message, Update, User


@pytest.mark.asyncio
async def test_bot_mtproto_initialization() -> None:
    bot = Bot(
        token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
        api_id=12345,
        api_hash="0123456789abcdef0123456789abcdef",
        mtproto_session=":memory:",
    )
    assert bot.mtproto is not None
    assert bot.mtproto.api_id == 12345
    assert bot.mtproto.api_hash == "0123456789abcdef0123456789abcdef"


@pytest.mark.asyncio
async def test_dispatcher_mtproto_event_routing() -> None:
    dp = Dispatcher()
    router = Router()
    received_messages: list[str] = []

    @router.message(F.text == "Hello MTProto")
    async def handle_hello(message: Message) -> None:
        received_messages.append(message.text)

    dp.include_router(router)

    # Simulate normalized MTProto short message update
    raw_update = UpdateShortMessage(
        id=1001,
        user_id=777888,
        message="Hello MTProto",
        pts=1,
        pts_count=1,
        date=int(datetime.datetime.now(datetime.timezone.utc).timestamp()),
    )
    normalized = normalize_tl_update(raw_update, update_id=1)
    assert len(normalized) == 1

    bot = Bot(
        token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
        api_id=12345,
        api_hash="0123456789abcdef0123456789abcdef",
        mtproto_session=":memory:",
    )

    await dp.feed_update(bot=bot, update=normalized[0])
    assert len(received_messages) == 1
    assert received_messages[0] == "Hello MTProto"
