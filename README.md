# aiogram MTProto 🚀

<p align="center">
  <img src="docs/_static/logo.png" width="200" alt="aiogram logo"/>
</p>

<p align="center">
  <b>A modern, high-performance, asynchronous Telegram framework for Python 3.10+</b><br/>
  <i>Featuring dual-engine support for both native <b>MTProto 2.0</b> and traditional <b>Telegram Bot API</b>.</i>
</p>

<p align="center">
  <a href="https://pypi.org/project/aiogram/"><img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python Version"></a>
  <a href="https://github.com/astral-sh/uv"><img src="https://img.shields.io/badge/package%20manager-uv-blueviolet" alt="uv"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License"></a>
</p>

---

## 🌟 Key Highlights

- **Dual-Engine Architecture**: Seamlessly run via **Telegram MTProto 2.0** or traditional **HTTP Bot API** using the exact same `Dispatcher`, `Router`, `F` filters, middlewares, and handler logic.
- **Pure MTProto 2.0 Binary Protocol**:
  - Hardware-accelerated AES-256-IGE cipher (with pure Python fallback).
  - Sub-millisecond Brent's cycle PQ factorization.
  - Official Telegram Diffie-Hellman & RSA cryptographic handshakes.
  - Full TL binary codecs & polymorphic constructor registry (`aiogram.raw`).
- **Ultra-Fast Parallel Media Engine**:
  - **512 KB adaptive chunking** (4x fewer roundtrips for large files).
  - Multi-worker concurrent upload and download pipelines (default: 8 parallel workers).
  - Direct disk streaming (`file.seek(offset)`) with near-zero memory footprint on multi-GB transfers.
  - Automatic Bot API `file_id` decoding to MTProto `InputFileLocation`.
- **Automatic Multi-DC & Cross-DC Routing**:
  - Automatic DC discovery, connection pooling, and seamless migration (e.g., DC 1 to DC 5).
  - Automatic cross-DC authorization transfer (`auth.exportAuthorization` / `auth.importAuthorization`) for media operations on DC 2, DC 4, etc.
- **Universal Session Persistence**:
  - `SQLiteSession`: ACID-compliant persistent on-disk database (`.session`).
  - `MemorySession`: Ephemeral in-memory storage for test suites and serverless setups.
  - `StringSession`: Portable Base64 string sessions with **built-in compatibility for Pyrogram (v1/v2) and Telethon sessions**.
- **Raw MTProto Access**: Invoke any official Telegram TL method directly with `await bot.invoke(raw.functions...)`.

---

## 📦 Installation & Setup

Using [uv](https://github.com/astral-sh/uv) (recommended):

```bash
# Clone the repository
git clone https://github.com/alreadydead0/aioMtproto.git
cd aioMtproto

# Synchronize dependencies with uv
uv sync --all-extras --group dev --group test
```

---

## 🚀 Usage Guide

### 1. MTProto 2.0 Mode (Native Binary Protocol)

Run your bot over high-speed MTProto binary TCP connection using your Telegram `api_id` & `api_hash`:

```python
import asyncio
from aiogram import Bot, Dispatcher, F, Router, raw
from aiogram.types import Message

# Initialize Bot in MTProto mode
bot = Bot(
    token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
    api_id=123456,
    api_hash="0123456789abcdef0123456789abcdef",
    mtproto_session="my_bot.session",  # SQLite session file
)

router = Router()

@router.message(F.text == "/start")
async def handle_start(message: Message):
    await message.answer("👋 Hello! Running natively on Telegram MTProto 2.0!")

@router.message(F.text)
async def handle_echo(message: Message):
    await message.reply(f"Echo: {message.text}")

async def main():
    dp = Dispatcher()
    dp.include_router(router)

    await bot.connect()
    print("MTProto Bot connected successfully!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
```

---

### 2. Traditional Bot API Mode (HTTP)

If `api_id` and `api_hash` are omitted, `aiogram` operates in traditional HTTP Bot API mode without any code changes needed in your handlers:

```python
bot = Bot(token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
```

---

### 3. Universal Session Management & String Sessions

`aiogram` supports SQLite on-disk files, in-memory sessions, and string sessions:

#### Interactive String Session Generator CLI
```bash
python examples/generate_string_session.py
```

#### Using Portable String Sessions
Deploy without creating files on disk (e.g. Docker, Heroku, AWS Lambda):

```python
from aiogram import Bot

bot = Bot(
    token="BOT_TOKEN",
    api_id=123456,
    api_hash="0123456789abcdef0123456789abcdef",
    # Works with aiogram StringSession, Pyrogram (v1/v2), or Telethon session strings
    mtproto_session="AIOGAQEBAAE...your_base64_session_string...",
)
```

#### Exporting Current Session to String
```python
session_string = await bot.export_session_string()
print("Exported session string:", session_string)
```

---

### 4. High-Speed Parallel Media Engine

Upload and download files at maximum wire speed using multi-worker parallel 512 KB chunking.

#### Parallel File Upload
```python
# Upload large files with parallel workers and live progress
input_file = await bot.upload_file(
    source="large_video.mp4",
    workers=8,
    progress=lambda current, total: print(f"Uploaded: {current}/{total} bytes ({current/total*100:.1f}%)"),
)
```

#### Parallel File Download (Direct Disk Streaming)
Stream media directly to disk with constant low RAM usage:

```python
from aiogram.media.file_id import file_id_to_input_location

@router.message(F.document)
async def handle_document(message: Message, bot: Bot):
    doc = message.document
    
    # Download directly using Bot API document or file_id
    await message.reply("Downloading via parallel MTProto engine...")
    
    dest_path = await bot.download_file_mtproto(
        location=file_id_to_input_location(doc.file_id),
        file_size=doc.file_size,
        destination=f"downloads/{doc.file_name}",
        workers=8,
        progress=lambda current, total: print(f"Downloaded {current}/{total} bytes"),
    )
    
    await message.reply(f"File saved to {dest_path}!")
```

---

### 5. Multi-DC & Cross-DC Media Operations

Telegram stores files across multiple Data Centers (DC 1 to DC 5). `aiogram` handles DC migrations and authorization exports automatically:

```python
# Access media client on a different DC (e.g., DC 4)
# Auth export from main DC and import into target DC happens automatically
dc4_client = await bot.mtproto.dc_manager.get_media_client(4)
print(f"DC 4 Client Ready: {dc4_client.is_ready}")
```

---

### 6. Raw MTProto RPC Invocations

Directly invoke any official Telegram MTProto method using typed `raw.functions` and receive typed `raw.types`:

```python
from aiogram import raw

# Get Nearest DC & User Country
nearest_dc = await bot.invoke(raw.functions.help.GetNearestDc())
print(f"Connected DC: {nearest_dc.this_dc} | Nearest DC: {nearest_dc.nearest_dc} ({nearest_dc.country})")

# Get Bot/User Profile
me = await bot.invoke(raw.functions.users.GetFullUser(id=raw.types.InputUserSelf()))
print(f"About: {me.full_user.about}")

# Invoke custom messaging methods
await bot.invoke(
    raw.functions.messages.SendMessage(
        peer=raw.types.InputPeerSelf(),
        message="Message sent via raw MTProto RPC!",
        random_id=123456789,
    )
)
```

---

## 🏛️ Architecture Overview

```text
┌────────────────────────────────────────────────────────┐
│  Application Layer (Routers, Handlers, Magic Filters)  │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│  aiogram Core (Bot, Dispatcher, Middlewares, FSM)      │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│  Dual Engine Layer                                     │
│  ├─ HTTP Bot API Client (aiohttp)                      │
│  └─ MTProto 2.0 Binary Engine (Async TCP)              │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│  MTProto Subsystems                                    │
│  ├─ Parallel Media Chunker (512 KB, Multi-Worker)      │
│  ├─ DC Manager & Connection Pool (DCs 1–5, Auto-Auth)  │
│  ├─ Session Manager (SQLite, In-Memory, StringSession) │
│  └─ Binary Codecs & TL Registry (aiogram.raw)          │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│  Cryptographic Core                                    │
│  ├─ AES-256-IGE Cipher (Hardware Accelerated)          │
│  ├─ Brent's PQ Factorization Algorithm                 │
│  └─ Telegram Diffie-Hellman / RSA Handshake            │
└────────────────────────────────────────────────────────┘
```

---

## 🧪 Testing & Verification

Run the MTProto test suite:

```bash
# Run verified full MTProto check suite
uv run python tests/test_mtproto/run_full_check.py

# Run with pytest
uv run pytest tests/test_mtproto -o addopts="" -W ignore -v

# Run full project tests
uv run pytest tests
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
