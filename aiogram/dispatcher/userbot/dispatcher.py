"""
Userbot event dispatcher and background update worker loop.
"""

from __future__ import annotations

import asyncio
import inspect
import logging
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from aiogram import types as tg_types
from aiogram.dispatcher.userbot.filters import Filter

if TYPE_CHECKING:
    from aiogram.client.user import UserClient

logger = logging.getLogger("aiogram.dispatcher.userbot")

HandlerFunc = Callable[..., Any]


class HandlerEntry:
    def __init__(self, callback: HandlerFunc, filter_obj: Filter | None = None) -> None:
        self.callback = callback
        self.filter_obj = filter_obj

    async def check_and_execute(self, client: UserClient, event: Any) -> bool:
        if self.filter_obj is not None:
            try:
                matched = await self.filter_obj.check(client, event)
                if not matched:
                    return False
            except Exception as e:
                logger.error("Filter evaluation error in %s: %s", self.callback, e)
                return False

        try:
            res = self.callback(client, event)
            if inspect.isawaitable(res):
                await res
            return True
        except Exception as e:
            logger.exception("Error executing handler %s: %s", self.callback, e)
            return False


class UserbotDispatcher:
    """
    Event dispatcher for UserClient / userbots.
    Consumes normalized updates asynchronously without blocking MTProto stream.
    """

    def __init__(self, client: UserClient) -> None:
        self.client = client
        self._message_handlers: list[HandlerEntry] = []
        self._edited_message_handlers: list[HandlerEntry] = []
        self._deleted_messages_handlers: list[HandlerEntry] = []
        self._raw_update_handlers: list[HandlerEntry] = []
        self._worker_task: asyncio.Task[None] | None = None
        self._is_running = False

    def add_message_handler(self, callback: HandlerFunc, filter_obj: Filter | None = None) -> None:
        self._message_handlers.append(HandlerEntry(callback, filter_obj))

    def add_edited_message_handler(
        self, callback: HandlerFunc, filter_obj: Filter | None = None
    ) -> None:
        self._edited_message_handlers.append(HandlerEntry(callback, filter_obj))

    def add_deleted_messages_handler(
        self, callback: HandlerFunc, filter_obj: Filter | None = None
    ) -> None:
        self._deleted_messages_handlers.append(HandlerEntry(callback, filter_obj))

    def add_raw_update_handler(self, callback: HandlerFunc) -> None:
        self._raw_update_handlers.append(HandlerEntry(callback, None))

    def on_message(self, filters: Filter | None = None) -> Callable[[HandlerFunc], HandlerFunc]:
        def decorator(func: HandlerFunc) -> HandlerFunc:
            self.add_message_handler(func, filters)
            return func

        return decorator

    def on_edited_message(
        self, filters: Filter | None = None
    ) -> Callable[[HandlerFunc], HandlerFunc]:
        def decorator(func: HandlerFunc) -> HandlerFunc:
            self.add_edited_message_handler(func, filters)
            return func

        return decorator

    def on_deleted_messages(
        self, filters: Filter | None = None
    ) -> Callable[[HandlerFunc], HandlerFunc]:
        def decorator(func: HandlerFunc) -> HandlerFunc:
            self.add_deleted_messages_handler(func, filters)
            return func

        return decorator

    def on_raw_update(self) -> Callable[[HandlerFunc], HandlerFunc]:
        def decorator(func: HandlerFunc) -> HandlerFunc:
            self.add_raw_update_handler(func)
            return func

        return decorator

    async def _process_update(self, update: tg_types.Update) -> None:
        """
        Process a single update against registered event handlers.
        """
        tasks = [h.check_and_execute(self.client, update) for h in self._raw_update_handlers]

        # New message
        if getattr(update, "message", None):
            tasks.extend(
                h.check_and_execute(self.client, update.message) for h in self._message_handlers
            )

        # Edited message
        if getattr(update, "edited_message", None):
            tasks.extend(
                h.check_and_execute(self.client, update.edited_message)
                for h in self._edited_message_handlers
            )

        # Deleted messages
        deleted_msgs = getattr(update, "deleted_messages", None)
        if deleted_msgs is not None:
            tasks.extend(
                h.check_and_execute(self.client, deleted_msgs)
                for h in self._deleted_messages_handlers
            )

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _worker_loop(self) -> None:
        """
        Background loop consuming update stream.
        """
        try:
            async for update in self.client.mtproto.updates_stream():
                if not self._is_running:
                    break
                asyncio.create_task(self._process_update(update))
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.debug("Userbot dispatcher worker loop exception: %s", e)

    def start(self) -> None:
        """
        Start the background dispatcher worker loop.
        """
        if not self._is_running:
            self._is_running = True
            self._worker_task = asyncio.create_task(self._worker_loop())

    def stop(self) -> None:
        """
        Stop the background dispatcher worker loop.
        """
        self._is_running = False
        if self._worker_task and not self._worker_task.done():
            self._worker_task.cancel()
            self._worker_task = None
