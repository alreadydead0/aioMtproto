# AIROGRAM → MTProto Framework — Master Implementation Prompt

## Project Goal

Fork the existing **aiogram** codebase and transform it into a **Telegram MTProto-first framework** while preserving the familiar aiogram developer experience and import style as much as realistically possible.

The target is **NOT** a custom file-transfer protocol.

The target is:

> **aiogram-compatible framework API + real Telegram MTProto backend + Telegram TL schema + high-level and raw MTProto APIs + optimized media transfer.**

The framework should eventually allow developers to write Telegram applications using an aiogram-like architecture while having access to MTProto capabilities normally associated with MTProto libraries.

---

# 1. NON-NEGOTIABLE REQUIREMENTS

### 1.1 Fork aiogram, do not build an unrelated framework

Use the existing aiogram source tree as the architectural starting point.

Preserve and reuse where practical:

- Dispatcher
- Router
- Event system
- Filters
- Middleware
- Handler registration
- Dependency injection
- Telegram object modeling concepts
- Async architecture
- Error handling patterns
- Plugin architecture
- Type hints
- Developer ergonomics

Do not throw away aiogram's architecture and replace it with a completely unrelated Pyrogram-style framework.

### 1.2 Preserve the import philosophy

The end goal should remain as close as possible to:

```python
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message
```

Do not rename the entire framework to an unrelated package unless technically unavoidable.

The fork should continue to feel like aiogram from the user's perspective.

### 1.3 Use REAL Telegram MTProto

Do NOT invent:

- MTPRTO packet formats
- custom Telegram-like RPC methods
- custom server protocols
- fake Telegram DC implementations
- custom `auth.sendCode` semantics
- custom `upload.initFileUpload` semantics
- custom file IDs unrelated to Telegram

Implement Telegram's actual MTProto protocol and Telegram's actual TL schema.

---

# 2. HIGH-LEVEL ARCHITECTURE

The framework should consist of these major layers:

```text
Application Layer
        │
        ▼
aiogram-compatible API
        │
        ├── Bot
        ├── Dispatcher
        ├── Router
        ├── Filters
        ├── Middleware
        └── Types
        │
        ▼
Telegram Abstraction Layer
        │
        ├── Message API
        ├── User API
        ├── Chat/Channel API
        ├── Media API
        └── Update API
        │
        ▼
MTProto RPC Layer
        │
        ├── TL Functions
        ├── TL Types
        ├── RPC Errors
        └── Raw API
        │
        ▼
MTProto Core
        │
        ├── Auth Key
        ├── Message IDs
        ├── Msg Containers
        ├── Sequence Numbers
        ├── Salt
        ├── Encryption
        ├── Acks
        └── Updates
        │
        ▼
MTProto Transport
        │
        ├── Abridged
        ├── Intermediate
        ├── Padded Intermediate
        └── Full
        │
        ▼
Telegram DC
```

---

# 3. PHASE 0 — REPOSITORY AUDIT

Before modifying code:

1. Scan the complete aiogram repository.
2. Identify:
   - Bot implementation
   - Dispatcher
   - Router
   - Telegram API methods
   - Types
   - Filters
   - Middleware
   - Sessions
   - HTTP transport
   - Update polling
   - Error hierarchy
   - Serialization
   - Dependency injection
3. Create a dependency map.
4. Identify which parts are Bot API-specific.
5. Identify which parts can remain unchanged.
6. Identify which parts need an MTProto adapter.
7. Do not make destructive changes before understanding the existing architecture.

Create an architectural report before implementation.

---

# 4. PHASE 1 — CORE CLIENT ABSTRACTION

Create a clean client abstraction that can support both:

```python
Bot(...)
```

and MTProto functionality.

Possible internal architecture:

```text
BaseClient
├── BotAPIClient
└── MTProtoClient
```

or an equivalent design that fits aiogram naturally.

The public API must remain simple.

Example:

```python
bot = Bot(
    api_id=API_ID,
    api_hash=API_HASH,
    session="my_session"
)
```

For bot authentication, support the appropriate Telegram authentication flow.

For user accounts, support MTProto authorization and persistent sessions.

Do not force all MTProto concepts into the public API if they can remain internal.

---

# 5. PHASE 2 — MTProto TRANSPORT

Implement the real Telegram MTProto transport layer.

Support:

- TCP connections
- Telegram DC addresses
- DC selection
- Connection lifecycle
- Reconnection
- Exponential backoff
- Ping/pong
- Message acknowledgements
- Transport framing
- Packet reading/writing
- Clean shutdown

Implement transport variants where appropriate:

```text
Abridged
Intermediate
PaddedIntermediate
Full
```

Do not implement HTTP/2 as a fake MTProto replacement.

WebSocket/HTTP transports should only be added if there is a real compatibility requirement.

---

# 6. PHASE 3 — MTProto CRYPTOGRAPHY

Implement the actual cryptographic requirements of Telegram MTProto.

Required areas:

- RSA key exchange
- DH key exchange
- Auth key generation
- Auth key ID
- Server salt
- Message key
- AES-IGE encryption/decryption
- MTProto message encryption
- Plain MTProto messages where required
- Correct endian handling
- Correct SHA-1/SHA-256 usage according to the relevant MTProto layer
- Secure random generation

Never replace Telegram's cryptographic protocol with:

```text
AES-256-GCM
ChaCha20-Poly1305
X25519
```

unless a feature specifically requires those independently.

Do not invent cryptographic shortcuts.

Security-sensitive code must include tests against known protocol vectors.

---

# 7. PHASE 4 — MESSAGE CONTAINER / RPC ENGINE

Implement the MTProto message engine.

Support:

- msg_id
- seq_no
- salt
- session_id
- message_key
- encrypted payload
- msg_container
- invokeWithLayer
- initConnection
- invokeAfterMsg
- invokeWithoutUpdates
- acknowledgements
- bad_server_salt
- bad_msg_notification
- bad_msg_id
- rpc_result

Implement request/response correlation safely.

Example internal API:

```python
result = await mtproto.invoke(
    functions.messages.GetHistory(...)
)
```

---

# 8. PHASE 5 — TELEGRAM TL SCHEMA

Use Telegram's actual TL schema.

Create/generate:

```text
raw/
├── types/
├── functions/
└── core/
```

The generated layer must support:

- constructors
- functions
- flags
- optional fields
- vectors
- nested objects
- serialization
- deserialization
- type IDs
- constructor IDs

The schema generator should be maintainable so that Telegram API layer updates can be integrated later.

Do not manually hard-code hundreds of methods if code generation can safely handle them.

---

# 9. PHASE 6 — RAW MTProto API

Expose a raw API similar in spirit to Pyrogram's raw layer.

Example:

```python
from aiogram.raw import functions

result = await bot.invoke(
    functions.messages.GetHistory(
        peer=peer,
        offset_id=0,
        offset_date=0,
        add_offset=0,
        limit=100,
        max_id=0,
        min_id=0,
        hash=0,
    )
)
```

Raw API should provide:

- Full TL functions
- Full TL types
- Direct RPC invocation
- RPC error propagation
- Type-safe objects
- IDE autocomplete

---

# 10. PHASE 7 — MTProto SESSION SYSTEM

Implement persistent MTProto sessions.

Session data may include:

- API ID
- DC ID
- DC address
- port
- auth key
- auth key ID
- server salt
- session ID
- last message ID
- authorization state

Recommended backend:

```text
SQLite
```

Allow future alternative session storage backends.

Example:

```python
Bot(
    api_id=12345,
    api_hash="...",
    session="sessions/main"
)
```

The session must survive application restarts.

Never store sensitive authentication material in logs.

---

# 11. PHASE 8 — AUTHORIZATION

Support real Telegram authorization flows as required.

At minimum design for:

### User account

```text
connect
→ get nearest DC
→ auth key exchange
→ send code
→ sign in
→ handle 2FA/password
→ save session
```

### Bot account

Support Telegram's actual bot authentication mechanism over MTProto where applicable.

Design authentication so that:

- code callbacks are configurable
- password callbacks are configurable
- session persistence is automatic
- reconnect does not require re-login

---

# 12. PHASE 9 — UPDATE SYSTEM

This is critical.

MTProto updates must be translated into aiogram-compatible events.

Implement support for the relevant Telegram update families:

```text
updates.UpdateShort
updates.UpdateShortMessage
updates.UpdateShortChatMessage
updates.UpdateShortSentMessage
updates.Updates
updates.UpdatesCombined
updates.ChannelDifference
updates.Difference
```

Build an update normalization layer:

```text
MTProto Update
      ↓
Update Normalizer
      ↓
aiogram Event
      ↓
Router
      ↓
Handler
```

The existing aiogram Dispatcher/Router should receive normalized events instead of knowing every MTProto wire-level detail.

---

# 13. PHASE 10 — TYPES / OBJECT MAPPING

Create a mapping layer between Telegram TL objects and the framework's public types.

For example:

```text
TL Message
    ↓
aiogram.types.Message
```

```text
TL User
    ↓
aiogram.types.User
```

```text
TL Chat / Channel
    ↓
aiogram.types.Chat
```

Where Telegram MTProto exposes more information than Bot API, do not silently discard useful fields.

Consider exposing MTProto-specific information through optional/raw properties.

Example:

```python
message.raw
message.raw_chat
message.raw_sender
```

Use names that do not conflict with existing aiogram APIs.

---

# 14. PHASE 11 — HIGH-LEVEL MESSAGE API

Build ergonomic high-level methods.

Examples:

```python
await message.answer("Hello")
await message.reply("Hello")
await message.delete()
await message.edit_text("Updated")
await message.pin()
await message.forward(...)
```

For MTProto-only capabilities, add appropriate methods without breaking existing aiogram semantics.

Examples may include:

```python
await bot.send_message(...)
await bot.get_history(...)
await bot.get_messages(...)
await bot.download_media(...)
await bot.upload_document(...)
```

Do not blindly copy Pyrogram's API.

Use aiogram naming and architecture wherever possible.

---

# 15. PHASE 12 — MEDIA / FILE TRANSFER

Only after MTProto core is stable, implement optimized Telegram media transfer.

Required features:

- upload_file
- upload_document
- upload_video
- upload_photo
- download_media
- download_document
- resume support
- progress callbacks
- retry failed parts
- bounded concurrency
- streaming to disk
- low memory usage
- correct Telegram file part sizes
- large-file support
- media DC migration handling

Important:

Telegram's actual MTProto upload methods must be used.

Examples:

```text
upload.saveFilePart
upload.saveBigFilePart
upload.getFile
upload.getFileHashes
```

Do not invent custom equivalents.

---

# 16. PHASE 13 — PARALLEL TRANSFER ENGINE

After basic media works, optimize it.

Architecture:

```text
File
 ↓
Chunk Planner
 ↓
Worker Pool
 ↓
MTProto Sender
 ↓
Telegram DC
```

Features:

- configurable worker count
- adaptive concurrency
- retry failed parts
- backoff
- bandwidth-aware scheduling
- cancellation
- progress callbacks
- resume metadata
- bounded memory
- disk streaming

Do not assume that increasing workers always increases speed.

Benchmark worker counts against:

```text
1
2
4
8
16
```

and choose sensible defaults.

---

# 17. PHASE 14 — DC MIGRATION / FILE DC HANDLING

Telegram may require requests to be executed against a different DC.

Implement:

```text
PHONE_MIGRATE_X
NETWORK_MIGRATE_X
FILE_MIGRATE_X
USER_MIGRATE_X
```

Handle migration automatically.

For media:

```text
main DC
   ↓
FILE_MIGRATE
   ↓
temporary connection to media DC
   ↓
download/upload
   ↓
return result
```

Do not make users manually manage DC migration.

---

# 18. PHASE 15 — ERROR SYSTEM

Create a unified exception hierarchy.

Examples:

```text
MTProtoError
├── RPCError
├── FloodWait
├── AuthError
├── TransportError
├── ConnectionError
├── MigrationError
├── InvalidSession
├── CryptoError
└── SerializationError
```

Map Telegram RPC errors to useful Python exceptions.

Example:

```python
try:
    await bot.send_message(...)
except FloodWait as e:
    await asyncio.sleep(e.value)
```

Do not hide important Telegram error information.

---

# 19. PHASE 16 — RATE LIMITING / FLOOD WAIT

Implement safe handling for:

- FLOOD_WAIT
- SLOWMODE_WAIT
- retry-after style limits where applicable
- connection flood
- request throttling

The framework should never blindly hammer Telegram.

Add configurable request rate limits.

---

# 20. PHASE 17 — CONCURRENCY MODEL

Use asyncio as the primary concurrency model.

Avoid unnecessary threads.

Use:

```text
asyncio
asyncio.Queue
asyncio.Semaphore
TaskGroup where compatible
```

Workers should be bounded.

Do not create unlimited tasks for large uploads/downloads.

---

# 21. PHASE 18 — PLUGINS / ROUTERS

Preserve aiogram's routing philosophy.

Support:

```python
router = Router()

@router.message(...)
async def handler(message):
    ...
```

Allow:

```python
dp.include_router(router)
```

MTProto events should pass through the same routing architecture.

Plugin discovery should remain optional.

Do not make hot reload a core dependency.

---

# 22. PHASE 19 — FILTER SYSTEM

Preserve aiogram filter behavior.

Add MTProto-aware filters only where useful.

Examples:

```python
F.text
F.photo
F.video
F.document
F.chat.id
F.from_user.id
```

Possible advanced filters:

```python
filters.private
filters.group
filters.channel
filters.media
filters.large_file
filters.album
```

Filters must remain composable.

---

# 23. PHASE 20 — MIDDLEWARE

Keep aiogram middleware architecture.

Middleware must be able to inspect:

- event
- user
- chat
- raw MTProto update
- request context

Avoid exposing wire-level complexity unless requested.

---

# 24. PHASE 21 — BOT API COMPATIBILITY

Do not unnecessarily break existing aiogram Bot API functionality.

If practical, support:

```text
Bot API mode
MTProto mode
Hybrid mode
```

Possible design:

```python
Bot(
    token=BOT_TOKEN
)
```

→ Bot API

```python
Bot(
    api_id=API_ID,
    api_hash=API_HASH,
    session="user"
)
```

→ MTProto

```python
Bot(
    token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    session="..."
)
```

→ Hybrid, if technically valid and explicitly designed.

Do not fake Bot API methods using MTProto when semantics differ.

---

# 25. PHASE 22 — RAW + HIGH-LEVEL DUAL API

Every important feature should have two levels.

### High-level

```python
await bot.send_message(...)
```

### Raw

```python
await bot.invoke(
    functions.messages.SendMessage(...)
)
```

This is one of the most important goals of the framework.

---

# 26. PHASE 23 — TESTING

Create extensive tests.

## Unit tests

Test:

- TL serialization
- TL deserialization
- crypto primitives
- message IDs
- sequence numbers
- auth key handling
- message keys
- packet framing
- session storage
- RPC parsing
- error mapping

## Integration tests

Test:

- connect
- login
- reconnect
- send message
- receive update
- edit message
- delete message
- media upload
- media download
- large files
- DC migration
- resume after disconnect

## Regression tests

Every bug discovered during development must become a regression test.

---

# 27. PHASE 24 — PERFORMANCE BENCHMARKING

Benchmark:

- connection establishment
- RPC latency
- update throughput
- message throughput
- upload speed
- download speed
- memory usage
- reconnect time
- large-file transfer
- multiple concurrent transfers

Do not promise arbitrary targets such as 10,000 concurrent transfers before benchmarking.

Use real measurements.

---

# 28. PHASE 25 — SECURITY

Security requirements:

- Never log auth keys
- Never log session strings
- Never log passwords
- Never expose authorization codes
- Protect SQLite session files
- Secure temporary files
- Validate serialized data
- Protect against malformed TL objects
- Avoid unsafe pickle-based session storage
- Use cryptographically secure randomness
- Zero sensitive buffers where practical

Any cryptographic implementation must be reviewed carefully.

Prefer well-tested cryptographic primitives/libraries where appropriate.

---

# 29. PROJECT STRUCTURE

Target architecture should resemble:

```text
aiogram/
├── __init__.py
├── client/
│   ├── bot.py
│   ├── mtproto.py
│   └── session.py
│
├── dispatcher/
├── router/
├── handlers/
├── filters/
├── middleware/
├── types/
├── methods/
│
├── mtproto/
│   ├── connection/
│   │   ├── tcp.py
│   │   ├── transport.py
│   │   └── pool.py
│   │
│   ├── crypto/
│   │   ├── auth_key.py
│   │   ├── aes_ige.py
│   │   └── crypto.py
│   │
│   ├── protocol/
│   │   ├── message.py
│   │   ├── container.py
│   │   ├── rpc.py
│   │   └── ids.py
│   │
│   ├── auth/
│   │   ├── user.py
│   │   └── bot.py
│   │
│   ├── updates/
│   │   ├── receiver.py
│   │   └── normalizer.py
│   │
│   └── dc.py
│
├── raw/
│   ├── types/
│   ├── functions/
│   └── core/
│
├── media/
│   ├── uploader.py
│   ├── downloader.py
│   ├── chunker.py
│   └── progress.py
│
├── session/
│   ├── sqlite.py
│   └── state.py
│
├── errors/
└── utils/
```

Adapt this structure to the actual aiogram repository instead of blindly creating duplicate systems.

---

# 30. IMPLEMENTATION ORDER

Use this exact general order:

```text
1. Repository audit
2. Separate Bot API-specific code
3. Introduce client abstraction
4. MTProto transport
5. MTProto crypto
6. Auth key exchange
7. Session persistence
8. MTProto message engine
9. TL schema generator
10. Raw API
11. RPC error system
12. Updates receiver
13. Update normalization
14. aiogram event integration
15. Public types mapping
16. High-level message API
17. Media upload
18. Media download
19. DC migration
20. Flood handling
21. Middleware/filter integration
22. Testing
23. Performance optimization
24. Documentation
25. Packaging/release
```

Do not jump directly to parallel upload optimization before the MTProto core works.

---

# 31. DEVELOPMENT RULES

When modifying the repository:

### Rule 1

Never invent Telegram protocol behavior.

### Rule 2

Prefer Telegram's official TL schema and protocol definitions.

### Rule 3

Preserve aiogram compatibility whenever technically possible.

### Rule 4

Do not copy Pyrogram APIs blindly.

### Rule 5

Do not rewrite working aiogram components unnecessarily.

### Rule 6

Every major change requires tests.

### Rule 7

Every protocol layer must be independently testable.

### Rule 8

Keep raw MTProto access available.

### Rule 9

Keep high-level APIs simple.

### Rule 10

Never expose secrets in logs.

---

# 32. AI CODING AGENT WORKFLOW

When given the repository, the coding agent must follow:

```text
SCAN
 ↓
UNDERSTAND
 ↓
MAP DEPENDENCIES
 ↓
DESIGN
 ↓
IMPLEMENT ONE LAYER
 ↓
RUN TESTS
 ↓
FIX
 ↓
DOCUMENT
 ↓
NEXT LAYER
```

Do NOT modify hundreds of files at once.

After each major phase:

1. Run tests.
2. Run static/type checks where available.
3. Run import checks.
4. Verify backwards compatibility.
5. Review changed files.
6. Commit a logical checkpoint.

---

# 33. FIRST MILESTONE

The first milestone is NOT file uploading.

The first successful milestone is:

```python
from aiogram import Bot, Dispatcher

bot = Bot(
    api_id=API_ID,
    api_hash=API_HASH,
    session="test"
)

dp = Dispatcher()

await bot.connect()

me = await bot.get_me()

print(me)
```

Expected:

```text
MTProto connection established
Session authenticated
getMe equivalent works
Telegram User object returned
```

Only after this works should messaging/update handling begin.

---

# 34. SECOND MILESTONE

Successfully receive and route an MTProto update:

```python
@router.message()
async def handler(message):
    print(message.text)
```

Flow:

```text
Telegram DC
 ↓
MTProto
 ↓
updates
 ↓
normalizer
 ↓
aiogram Update/Event
 ↓
Router
 ↓
Handler
```

---

# 35. THIRD MILESTONE

High-level messaging:

```python
await bot.send_message(
    chat_id,
    "Hello from MTProto"
)
```

Then:

```python
await message.edit_text("Edited")
await message.delete()
await message.reply("Reply")
```

---

# 36. FOURTH MILESTONE

Media:

```python
await bot.send_document(...)
await bot.send_video(...)
await bot.download_media(...)
```

Then add:

- progress
- resume
- parallel parts
- retries
- DC migration

---

# 37. DEFINITION OF DONE

The framework should be considered production-ready only when:

- Real MTProto connection works.
- Session persistence works.
- User authorization works.
- Bot authorization works where supported.
- Raw TL API works.
- Updates are received reliably.
- aiogram Router/Dispatcher works with MTProto updates.
- High-level message APIs work.
- Media upload/download works.
- DC migration works.
- Flood waits are handled.
- Reconnection works.
- Tests cover protocol-critical components.
- No secrets are leaked.
- Documentation explains both high-level and raw APIs.
- Existing aiogram functionality that is intentionally preserved has regression coverage.

---

# 38. IMPORTANT CORRECTION FROM THE ORIGINAL PLAN

The previous concept contained a custom:

> "MTPRTO — Mobile Transport Protocol for Rapid Transfer Operations"

and a custom binary packet protocol.

That concept must NOT be used for this project.

The framework must implement/use **Telegram MTProto itself**.

The project name may remain temporary, but the underlying protocol must be Telegram MTProto.

---

# 39. FINAL INSTRUCTION TO THE CODING AGENT

You are working on a serious fork of aiogram.

Do not create a superficial wrapper around Pyrogram, Pyrofork, Telethon, or another MTProto library unless a temporary compatibility layer is explicitly required during development.

The long-term goal is to make the fork itself capable of handling the required MTProto stack.

Use existing libraries only where they are intentionally selected as dependencies.

Do not claim that a layer is implemented until it has been tested.

Do not replace real Telegram protocol behavior with mock/custom behavior.

Do not sacrifice aiogram's developer experience unnecessarily.

The final framework should feel like:

```text
aiogram
   +
real MTProto
   +
raw Telegram TL API
   +
high-level Telegram client API
   +
optimized media transfer
```

That is the target architecture.
