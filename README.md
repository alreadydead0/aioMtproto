# aiogram MTProto 🚀

<p align="center">
  <img src="docs/_static/logo.png" width="200" alt="aiogram logo"/>
</p>

<p align="center">
  <b>A modern, high-performance, asynchronous Telegram framework for Python 3.10+</b><br/>
  <i>Featuring dual-engine support for both native <b>MTProto 2.0</b> and <b>Telegram Bot API</b>.</i>
</p>

---

## 🌟 Key Highlights

- **Dual-Engine Architecture**: Seamlessly run via **Telegram MTProto 2.0** or traditional **HTTP Bot API** using the same `Dispatcher`, `Router`, `F` filters, and handler logic.
- **Pure MTProto 2.0 Stack**:
  - Hardware-accelerated AES-256-IGE cipher (with pure Python fallback).
  - Sub-millisecond Brent's cycle PQ factorization.
  - Official Telegram Diffie-Hellman & RSA cryptographic handshakes.
  - Full TL binary codecs & polymorphic constructor registry.
- **Ultra-Fast Parallel Media Engine**:
  - 512 KB adaptive chunking (4x fewer roundtrips for large files).
  - Multi-worker concurrent upload and download pipelines (8 workers by default).
  - Direct disk streaming (`file.seek(offset)`) for zero-memory footprint on multi-GB transfers.
- **Universal Session Persistence**:
  - `MemorySession`: In-memory ephemeral storage for tests and temporary instances.
  - `SQLiteSession`: ACID-compliant persistent on-disk database.
  - `StringSession`: Portable Base64 string sessions with **built-in Pyrogram (v1/v2) and Telethon compatibility**.
- **Full aiogram Ergonomics**:
  - `Router` & `Dispatcher` event routing.
  - Powerful `magic filters` (`F.text == "/start"`, `F.photo`, `F.chat.id`).
  - Finite State Machine (FSM), Middlewares, and dependency injection.
- **Raw MTProto Access**: Directly invoke official Telegram TL RPC functions via `await bot.invoke(raw.functions...)`.

---

## ⚡ Quickstart

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/aiogram/aiogram.git
cd aiogram

# Install with development & test dependencies using uv
uv sync --all-extras --group dev --group test
```

---

### 2. MTProto Mode (Using `api_id` & `api_hash`)

```python
import asyncio
from aiogram import Bot, Dispatcher, F, Router, raw
from aiogram.types import Message

# Initialize Bot in MTProto mode
bot = Bot(
    api_id=123456,
    api_hash="0123456789abcdef0123456789abcdef",
    token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
    mtproto_session="my_session.session",
)

router = Router()

@router.message(F.text == "/start")
async def handle_start(message: Message):
    await message.answer("Hello from aiogram running natively on MTProto 2.0!")

@router.message(F.text)
async def handle_echo(message: Message):
    await message.reply(f"MTProto Echo: {message.text}")

async def main():
    dp = Dispatcher()
    dp.include_router(router)
    
    await bot.connect()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
```

---

### 3. Portable String Sessions

You can run your bot or userbot anywhere (Heroku, Docker, Serverless) using string sessions without `.session` files on disk:

#### Interactive Generator CLI:
```bash
python examples/generate_string_session.py
```

#### Usage in Code:
```python
# Accepts native aiogram, Pyrogram (v1/v2), or Telethon string sessions
bot = Bot(
    api_id=123456,
    api_hash="0123456789abcdef0123456789abcdef",
    mtproto_session="AIOGAQEBAAE...your_string_session...",
)
```

---

### 4. High-Speed Media Upload & Download

```python
# Upload with 8 parallel workers and real-time progress
input_file = await bot.upload_file(
    source="my_large_video.mp4",
    progress=lambda current, total: print(f"{current}/{total} bytes"),
    workers=8,
)

# Download directly to disk without RAM overhead
file_path = await bot.download_file_mtproto(
    location=input_file_location,
    file_size=file_size,
    destination="downloads/video.mp4",
    progress=lambda current, total: print(f"{current}/{total} bytes"),
    workers=8,
)
```

---

### 5. Raw MTProto RPC Invocations

```python
# Directly invoke any official Telegram TL method
nearest_dc = await bot.invoke(raw.functions.help.GetNearestDc())
print(f"Connected to DC: {nearest_dc.this_dc} (Nearest: {nearest_dc.nearest_dc})")

user_full = await bot.invoke(
    raw.functions.users.GetFullUser(id=raw.types.InputUserSelf())
)
```

---

## 🏛️ Architecture Overview

```text
┌────────────────────────────────────────────────────────┐
│  Application Layer (Router, Handlers, Filters)        │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│  aiogram API (Bot, Dispatcher, Middlewares, FSM, Types)│
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│  Telegram Abstraction (Messaging, Media Engine, Normal)│
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│  MTProto RPC Layer (raw.functions, raw.types, Results) │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│  MTProto Core (AuthKey, MessageCodec, MsgContainers)   │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│  Transport Layer (Abridged, Intermediate, Full, CRC32) │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│  Telegram Data Centers (TCP Async Sockets, DCs 1–5)    │
└────────────────────────────────────────────────────────┘
```

---

## 🧪 Testing

Run the full verified test suite:

```bash
uv run python tests/test_mtproto/run_full_check.py
```

Or via pytest:

```bash
uv run pytest tests/test_mtproto -o addopts="" -W ignore -v
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
