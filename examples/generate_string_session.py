"""
Interactive script to generate a portable MTProto String Session.

Usage:
    python examples/generate_string_session.py
"""

import asyncio

from aiogram import Bot


async def main() -> None:
    print("=== aiogram MTProto String Session Generator ===\n")
    api_id_input = input("Enter Telegram API ID: ").strip()
    api_hash = input("Enter Telegram API HASH: ").strip()
    api_id = int(api_id_input)

    bot_token = input("Enter Bot Token (leave empty for User login): ").strip() or None

    bot = Bot(
        api_id=api_id,
        api_hash=api_hash,
        token=bot_token,
        mtproto_session=":memory:",
    )

    print("\nConnecting to Telegram MTProto...")
    await bot.connect()

    if bot_token:
        print("Authorizing as Bot...")
        await bot.mtproto.sign_in_bot(bot_token)
    else:
        phone = input("Enter Phone Number (with country code e.g. +91...): ").strip()
        print("Sending login code...")
        sent_code = await bot.mtproto.send_code(phone)
        code = input("Enter the login code you received in Telegram: ").strip()
        await bot.mtproto.sign_in(
            phone=phone,
            code=code,
            phone_code_hash=sent_code.phone_code_hash,
        )

    session_string = await bot.export_session_string()

    print("\n" + "=" * 60)
    print("YOUR STRING SESSION:")
    print("=" * 60)
    print(session_string)
    print("=" * 60)
    print("\nKeep this string secret! You can now use it in your code as:")
    print(
        f'bot = Bot(api_id={api_id}, api_hash="{api_hash}", mtproto_session="{session_string[:15]}...")'
    )

    await bot.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
