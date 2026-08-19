"""
aiogram MTProto Quickstart Example.

Demonstrates:
1. Initializing aiogram Bot in MTProto mode with (api_id, api_hash).
2. Registering message handlers with aiogram Router and F filters.
3. Invoking raw Telegram TL RPC functions.
4. Sending and editing messages.
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher, F, Router, raw
from aiogram.types import Message

logging.basicConfig(level=logging.INFO)

API_ID = 12345
API_HASH = "0123456789abcdef0123456789abcdef"
BOT_TOKEN = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"

router = Router()


@router.message(F.text == "/start")
async def handle_start(message: Message) -> None:
    await message.answer("Hello! This is aiogram running natively on MTProto 2.0!")


@router.message(F.text)
async def handle_echo(message: Message) -> None:
    await message.reply(f"MTProto Echo: {message.text}")


async def main() -> None:
    # Initialize Bot in MTProto mode
    bot = Bot(
        api_id=API_ID,
        api_hash=API_HASH,
        token=BOT_TOKEN,
        mtproto_session="my_bot.session",
    )

    dp = Dispatcher()
    dp.include_router(router)

    print("Connecting to Telegram MTProto...")
    # await bot.connect()

    # Raw TL RPC Invocation example:
    # me = await bot.invoke(raw.functions.help.GetNearestDc())
    # print(f"Nearest DC: {me.nearest_dc} (Country: {me.country})")

    # Start event loop / polling
    # await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
