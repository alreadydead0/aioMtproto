"""
Translates MTProto TL updates into aiogram Update and Message objects.
"""

from __future__ import annotations

import datetime
from typing import Any, List, Optional

from aiogram import types as tg_types
from aiogram.enums import ChatType
from aiogram.raw.types import (
    Message as RawMessage,
)
from aiogram.raw.types import (
    PeerChannel,
    PeerChat,
    PeerUser,
)
from aiogram.raw.types import (
    UpdateNewMessage as RawUpdateNewMessage,
)
from aiogram.raw.types import (
    Updates as RawUpdates,
)
from aiogram.raw.types import (
    UpdatesCombined as RawUpdatesCombined,
)
from aiogram.raw.types import (
    UpdateShort as RawUpdateShort,
)
from aiogram.raw.types import (
    UpdateShortChatMessage as RawUpdateShortChatMessage,
)
from aiogram.raw.types import (
    UpdateShortMessage as RawUpdateShortMessage,
)
from aiogram.raw.types import (
    User as RawUser,
)


def _convert_user(raw: RawUser) -> tg_types.User:
    return tg_types.User(
        id=raw.id,
        is_bot=raw.bot,
        first_name=raw.first_name or "User",
        last_name=raw.last_name,
        username=raw.username,
        language_code=raw.lang_code,
        is_premium=raw.premium,
    )


def normalize_tl_update(update_obj: Any, update_id: int = 1) -> list[tg_types.Update]:
    """
    Normalize a Telegram MTProto TL update into one or more aiogram.types.Update instances.
    """
    results: list[tg_types.Update] = []

    if isinstance(update_obj, RawUpdateShortMessage):
        chat = tg_types.Chat(
            id=update_obj.user_id,
            type="private",
            first_name="User",
            username=None,
        )
        user = tg_types.User(
            id=update_obj.user_id,
            is_bot=False,
            first_name="User",
            username=None,
        )
        msg_date = datetime.datetime.fromtimestamp(update_obj.date, tz=datetime.timezone.utc)
        msg = tg_types.Message(
            message_id=update_obj.id,
            date=msg_date,
            chat=chat,
            from_user=user,
            text=update_obj.message,
        )
        results.append(tg_types.Update(update_id=update_id, message=msg))

    elif isinstance(update_obj, RawUpdateShortChatMessage):
        chat = tg_types.Chat(
            id=-update_obj.chat_id,
            type="group",
            title="Group Chat",
        )
        user = tg_types.User(
            id=update_obj.from_id,
            is_bot=False,
            first_name="User",
        )
        msg_date = datetime.datetime.fromtimestamp(update_obj.date, tz=datetime.timezone.utc)
        msg = tg_types.Message(
            message_id=update_obj.id,
            date=msg_date,
            chat=chat,
            from_user=user,
            text=update_obj.message,
        )
        results.append(tg_types.Update(update_id=update_id, message=msg))

    elif isinstance(update_obj, RawUpdateNewMessage):
        raw_msg = update_obj.message
        if isinstance(raw_msg, RawMessage):
            # Resolve chat_id and type
            if isinstance(raw_msg.peer_id, PeerUser):
                chat_id = raw_msg.peer_id.user_id
                chat_type = "private"
            elif isinstance(raw_msg.peer_id, PeerChat):
                chat_id = -raw_msg.peer_id.chat_id
                chat_type = "group"
            elif isinstance(raw_msg.peer_id, PeerChannel):
                chat_id = int(f"-100{raw_msg.peer_id.channel_id}")
                chat_type = "supergroup"
            else:
                chat_id = 0
                chat_type = "private"

            from_user = None
            if raw_msg.from_id and isinstance(raw_msg.from_id, PeerUser):
                from_user = tg_types.User(
                    id=raw_msg.from_id.user_id, is_bot=False, first_name="User"
                )

            chat = tg_types.Chat(
                id=chat_id,
                type=chat_type,
                title="Chat" if chat_type != "private" else None,
                first_name="User" if chat_type == "private" else None,
            )
            msg_date = datetime.datetime.fromtimestamp(raw_msg.date, tz=datetime.timezone.utc)

            msg = tg_types.Message(
                message_id=raw_msg.id,
                date=msg_date,
                chat=chat,
                from_user=from_user,
                text=raw_msg.message,
            )
            results.append(tg_types.Update(update_id=update_id, message=msg))

    elif isinstance(update_obj, RawUpdateShort):
        results.extend(normalize_tl_update(update_obj.update, update_id))

    elif isinstance(update_obj, (RawUpdates, RawUpdatesCombined)):
        for idx, sub_upd in enumerate(update_obj.updates):
            results.extend(normalize_tl_update(sub_upd, update_id + idx))

    return results
