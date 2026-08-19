"""
Live MTProto Test Script using Telegram credentials.
Tests MTProto 2.0 handshake, authentication, and get_me call.
"""

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F, Router, raw
from aiogram.types import Message

API_ID = 9241668
API_HASH = "99f6e5250ed7ef3a09686190c730f294"
BOT_TOKEN = "7597391690:AAGJW5ncXDILbBvUqu1epeKtrQyFth75xKE"


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
    )

    print("=" * 60)
    print("      TESTING AIOGRAM MTPROTO 2.0 LIVE CONNECTION")
    print("=" * 60)

    # Initialize bot in MTProto mode with memory session
    bot = Bot(
        token=BOT_TOKEN,
        api_id=API_ID,
        api_hash=API_HASH,
        mtproto_session=":memory:",
    )

    try:
        print("\n[1/3] Initiating MTProto TCP Connection & Diffie-Hellman Handshake...")
        await bot.connect()
        print("      -> MTProto Handshake & AuthKey Derivation SUCCESSFUL!")

        print("\n[2/3] Fetching Bot Details via MTProto get_me()...")
        me = await bot.mtproto.get_me()
        print(f"      -> Bot ID       : {me.id}")
        print(f"      -> Bot Name     : {me.first_name}")
        print(f"      -> Bot Username : @{me.username}")
        print(f"      -> Is Bot       : {me.is_bot}")

        print("\n[3/3] Exporting Portable StringSession...")
        session_str = bot.export_session_string()
        print(f"      -> Session String Preview: {session_str[:35]}... (Length: {len(session_str)})")

        print("\n" + "=" * 60)
        print("RESULT: LIVE MTPROTO BOT VERIFICATION 100% SUCCESSFUL!")
        print("=" * 60)

    except Exception as e:
        logging.exception("Error during MTProto live test")
        print(f"\n[ERROR] MTProto Test Failed: {e}")

    finally:
        await bot.disconnect()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
