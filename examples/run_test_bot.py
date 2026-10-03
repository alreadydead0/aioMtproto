# ruff: noqa: T201
"""
Live Test Bot using provided Telegram credentials.
"""

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

router = Router()


@router.message(CommandStart())
async def handle_start(message: Message):
    user_name = message.from_user.first_name if message.from_user else "User"
    await message.reply(
        f"👋 **Namaste {user_name}!**\n\n"
        "🤖 **Bot is LIVE and working perfectly!**\n"
        "⚡ Powered by **aiogram MTProto 2.0** (`aioMtproto`)\n\n"
        "Try sending any text message or media file!",
        parse_mode="Markdown",
    )


@router.message(F.text)
async def handle_text(message: Message):
    await message.reply(
        f"✅ **Received Text:** `{message.text}`\n"
        f"🆔 **User ID:** `{message.from_user.id if message.from_user else 'Unknown'}`",
        parse_mode="Markdown",
    )


@router.message(F.document | F.video | F.audio | F.photo)
async def handle_media(message: Message):
    doc = message.document or message.video or message.audio
    file_name = getattr(doc, "file_name", "Media File")
    file_size = getattr(doc, "file_size", 0)
    await message.reply(
        f"📁 **Media Received!**\n"
        f"📄 **Name:** `{file_name}`\n"
        f"📦 **Size:** `{file_size} bytes`\n"
        "⚡ MTProto transfer pipeline ready!",
        parse_mode="Markdown",
    )


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
    )

    bot = Bot(
        token=BOT_TOKEN,
        api_id=API_ID,
        api_hash=API_HASH,
        mtproto_session="test_bot.session",
    )

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    print("🚀 Test Bot is starting...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\nBot stopped by user.")
