"""
Interactive script to generate a portable native aioMtproto MTProto String Session.

Usage:
    python examples/generate_string_session.py
"""

from __future__ import annotations

import asyncio
import getpass

from aiogram import UserClient


async def main() -> None:
    print("=" * 60)
    print("      aioMtproto Native String Session Generator")
    print("=" * 60)

    print("Select Login Type:")
    print("  1. Telegram User Account (Phone / Code / 2FA)")
    print("  2. Telegram Bot (Bot Token)")
    choice = input("Enter choice (1/2, default 1): ").strip() or "1"

    api_id_str = input("\nEnter API ID: ").strip()
    api_hash = input("Enter API HASH: ").strip()
    api_id = int(api_id_str)

    if choice == "2":
        bot_token = input("Enter Bot Token: ").strip()
        client = UserClient(
            api_id=api_id,
            api_hash=api_hash,
            bot_token=bot_token,
            session=":memory:",
        )
        print("\nConnecting to MTProto & authorizing bot...")
        await client.start()
    else:
        phone = input("Enter Phone Number (e.g. +1234567890): ").strip()
        client = UserClient(
            api_id=api_id,
            api_hash=api_hash,
            phone=phone,
            session=":memory:",
        )
        print("\nConnecting to MTProto...")
        await client.mtproto.connect()

        print(f"Sending login code to {phone}...")
        sent_code = await client.mtproto.send_code(phone)
        code = input("Enter the login code you received: ").strip()

        try:
            await client.mtproto.sign_in(
                phone_number=phone,
                phone_code_hash=sent_code.phone_code_hash,
                phone_code=code,
            )
        except Exception as e:
            if "SESSION_PASSWORD_NEEDED" in str(e) or type(e).__name__ == "SessionPasswordNeeded":
                pwd = getpass.getpass("Enter 2FA Password (input is hidden for security): ")
                await client.mtproto.check_password(pwd)
            else:
                raise

    me = await client.get_me()
    print(f"\n✅ Authenticated successfully as: {me.first_name} (@{me.username or me.id})")

    session_string = await client.export_session_string()

    print("\n" + "=" * 60)
    print("🌟 YOUR NATIVE aioMtproto STRING SESSION:")
    print("=" * 60)
    print(session_string)
    print("=" * 60)

    print("\n⚠️ Keep this session string secret! Never commit it to public repos.")
    print("Usage in your userbot:")
    print(
        f'client = UserClient(api_id={api_id}, api_hash="{api_hash}", session_string="{session_string[:15]}...")'
    )
    await client.stop()


if __name__ == "__main__":
    asyncio.run(main())
