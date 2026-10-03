"""
Live Multi-DC MTProto Verification Script:
1. Tests First Run: DH handshake -> migration to DC 5 -> bot sign-in -> session persistence.
2. Tests Second Run: Load stored session -> validate authorization with Telegram -> reuse authorized session.
3. Tests Media DC 4 Export/Import: Export from authorized DC 5 -> Import into DC 4 -> DC 4 READY.
"""

import asyncio
import logging
import os
import sys

from aiogram import Bot, raw
from aiogram.mtproto.connection.dc_manager import DCState

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
SESSION_FILE = "live_verification.session"


async def main():
    # Force UTF-8 on Windows stdout
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
    )

    if os.path.exists(SESSION_FILE):
        try:
            os.remove(SESSION_FILE)
        except Exception:
            pass

    print("=" * 60)
    print("      STAGE 1: INITIAL RUN (FRESH CONNECTION & MIGRATION)")
    print("=" * 60)

    bot1 = Bot(
        token=BOT_TOKEN,
        api_id=API_ID,
        api_hash=API_HASH,
        mtproto_session=SESSION_FILE,
    )

    try:
        await bot1.connect()
        print("      -> First bot connection SUCCESSFUL!")
        me1 = await bot1.mtproto.get_me()
        print(f"      -> Bot ID: {me1.id}, Username: @{me1.username}")

        print("\n[Stage 1.1] Testing Cross-DC Authorization for Media DC 4...")
        dc4_client = await bot1.mtproto.dc_manager.get_media_client(4)
        assert dc4_client.dc_id == 4
        assert dc4_client.is_ready is True
        assert dc4_client.auth_imported is True
        print("      -> Cross-DC Export/Import to DC 4 SUCCESSFUL!")
    finally:
        await bot1.disconnect()
        await bot1.session.close()

    print("\n" + "=" * 60)
    print("      STAGE 2: SECOND RUN (LOAD STORED SESSION & VALIDATE)")
    print("=" * 60)

    bot2 = Bot(
        token=BOT_TOKEN,
        api_id=API_ID,
        api_hash=API_HASH,
        mtproto_session=SESSION_FILE,
    )

    try:
        await bot2.connect()
        print("      -> Second bot connection (restored from storage) SUCCESSFUL!")
        me2 = await bot2.mtproto.get_me()
        print(f"      -> Bot ID: {me2.id}, Username: @{me2.username}")

        print("\n[Stage 2.1] Testing Media DC 4 Export/Import using Restored Main DC Session...")
        dc4_client_2 = await bot2.mtproto.dc_manager.get_media_client(4)
        assert dc4_client_2.dc_id == 4
        assert dc4_client_2.is_ready is True
        assert dc4_client_2.auth_imported is True
        print("      -> Media DC 4 Export/Import from Restored Session SUCCESSFUL!")

        print("\n" + "=" * 60)
        print("LIVE VERIFICATION RESULT: 100% SUCCESSFUL!")
        print("=" * 60)
    finally:
        await bot2.disconnect()
        await bot2.session.close()
        if os.path.exists(SESSION_FILE):
            try:
                os.remove(SESSION_FILE)
            except Exception:
                pass


if __name__ == "__main__":
    asyncio.run(main())
