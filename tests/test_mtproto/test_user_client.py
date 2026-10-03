from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from aiogram import UserClient, filters
from aiogram.enums import ChatType
from aiogram.session.string import StringSession
from aiogram.types import Chat, Message, User


@pytest.mark.asyncio
async def test_user_client_initialization():
    client = UserClient(
        api_id=12345,
        api_hash="test_hash",
        session=":memory:",
    )
    assert client.api_id == 12345
    assert client.api_hash == "test_hash"
    assert client.mtproto is not None


@pytest.mark.asyncio
async def test_user_client_filters():
    client = MagicMock()
    client.me = User(id=111, is_bot=False, first_name="Me")

    msg_from_me = Message(
        message_id=1,
        date=1000,
        chat=Chat(id=222, type=ChatType.PRIVATE),
        from_user=User(id=111, is_bot=False, first_name="Me"),
        text="/start help",
    )

    msg_from_other = Message(
        message_id=2,
        date=1000,
        chat=Chat(id=333, type=ChatType.GROUP),
        from_user=User(id=999, is_bot=False, first_name="Other", username="otheruser"),
        text="Hello world",
    )

    # filters.me
    assert await filters.me.check(client, msg_from_me) is True
    assert await filters.me.check(client, msg_from_other) is False

    # filters.private & filters.group
    assert await filters.private.check(client, msg_from_me) is True
    assert await filters.group.check(client, msg_from_other) is True

    # filters.command
    cmd_filter = filters.command("start")
    assert await cmd_filter.check(client, msg_from_me) is True
    assert await cmd_filter.check(client, msg_from_other) is False

    # filters composition: (filters.private & filters.me)
    composed = filters.private & filters.me
    assert await composed.check(client, msg_from_me) is True
    assert await composed.check(client, msg_from_other) is False

    # inverted filter: ~filters.me
    not_me = ~filters.me
    assert await not_me.check(client, msg_from_me) is False
    assert await not_me.check(client, msg_from_other) is True
