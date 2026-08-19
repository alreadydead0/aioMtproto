"""
MTProto Test Suite Runner.
"""

from __future__ import annotations

import asyncio
import os
import sys

# Ensure local aiogram package is loaded
sys.path.insert(0, os.path.abspath("."))

from tests.test_mtproto.test_bot_integration import (
    test_bot_mtproto_initialization,
    test_dispatcher_mtproto_event_routing,
)
from tests.test_mtproto.test_crypto import (
    test_aes_ige_roundtrip,
    test_auth_key_and_kdf,
    test_factorize_pq,
    test_pure_aes_roundtrip,
    test_rsa_encryption,
)
from tests.test_mtproto.test_errors import (
    test_parse_auth_errors,
    test_parse_dc_migrates,
    test_parse_flood_wait,
    test_parse_slowmode_wait,
)
from tests.test_mtproto.test_media import (
    test_chunker_sizes_and_partitioning,
    test_file_downloader_parallel_and_disk_stream,
    test_file_uploader_small_and_big,
)
from tests.test_mtproto.test_rpc_engine import (
    test_encrypted_message_codec_and_containers,
    test_plain_message_codec,
)
from tests.test_mtproto.test_session import (
    test_memory_session,
    test_sqlite_session,
    test_string_session,
)
from tests.test_mtproto.test_tl import (
    test_tl_polymorphic_reader_and_gzip,
    test_tl_primitives,
    test_tl_user_serialization,
)
from tests.test_mtproto.test_transports import (
    test_abridged_transport_large_packet,
    test_abridged_transport_small_packet,
    test_full_transport,
    test_intermediate_transport,
)


class DummyTmpPath:
    def __truediv__(self, name: str) -> str:
        return os.path.join(os.getcwd(), f"test_{name}")


async def run_all_tests() -> None:
    print("=== RUNNING MTPROTO TEST SUITE ===", flush=True)

    print("1. Testing Crypto Primitives...", flush=True)
    test_pure_aes_roundtrip()
    print("   [x] Pure AES", flush=True)
    test_aes_ige_roundtrip()
    print("   [x] AES-IGE", flush=True)
    test_factorize_pq()
    print("   [x] Brent PQ factorize", flush=True)
    test_auth_key_and_kdf()
    print("   [x] AuthKey & KDF", flush=True)
    test_rsa_encryption()
    print("   [x] RSA encryption", flush=True)
    print("   -> Crypto Primitives: PASS [5/5]\n", flush=True)

    print("2. Testing TCP Transports...", flush=True)
    await test_abridged_transport_small_packet()
    print("   [x] Abridged small", flush=True)
    await test_abridged_transport_large_packet()
    print("   [x] Abridged large", flush=True)
    await test_intermediate_transport()
    print("   [x] Intermediate", flush=True)
    await test_full_transport()
    print("   [x] Full with CRC32", flush=True)
    print("   -> Transports: PASS [4/4]\n", flush=True)

    print("3. Testing TL Binary Codecs & Polymorphic Parsing...", flush=True)
    test_tl_primitives()
    print("   [x] TL Primitives", flush=True)
    test_tl_user_serialization()
    print("   [x] TL User serialization", flush=True)
    test_tl_polymorphic_reader_and_gzip()
    print("   [x] Polymorphic reader & Gzip", flush=True)
    print("   -> TL Codecs: PASS [3/3]\n", flush=True)

    print("4. Testing Session Storage...", flush=True)
    await test_memory_session()
    print("   [x] MemorySession", flush=True)
    tmp_path = DummyTmpPath()
    await test_sqlite_session(tmp_path)
    print("   [x] SQLiteSession", flush=True)
    await test_string_session()
    print("   [x] StringSession (Base64 export/import)", flush=True)
    print("   -> Sessions (Memory, SQLite, StringSession): PASS [3/3]\n", flush=True)

    print("5. Testing MTProto Error Parsing...", flush=True)
    test_parse_flood_wait()
    test_parse_slowmode_wait()
    test_parse_dc_migrates()
    test_parse_auth_errors()
    print("   -> Error System: PASS [4/4]\n", flush=True)

    print("6. Testing RPC Envelopes & Containers...", flush=True)
    test_plain_message_codec()
    test_encrypted_message_codec_and_containers()
    print("   -> RPC Codecs: PASS [2/2]\n", flush=True)

    print("7. Testing Bot MTProto Mode & Dispatcher Event Routing...", flush=True)
    await test_bot_mtproto_initialization()
    print("   [x] Bot MTProto init", flush=True)
    await test_dispatcher_mtproto_event_routing()
    print("   [x] Dispatcher event routing", flush=True)
    print("   -> Bot & Dispatcher Integration: PASS [2/2]\n", flush=True)

    print("8. Testing High-Speed Parallel Media Engine...", flush=True)
    test_chunker_sizes_and_partitioning()
    print("   [x] Chunker 512KB/128KB partitioning", flush=True)
    await test_file_uploader_small_and_big()
    print("   [x] Parallel FileUploader (small & big)", flush=True)
    await test_file_downloader_parallel_and_disk_stream(tmp_path)
    print("   [x] Parallel FileDownloader & disk streaming", flush=True)
    print("   -> Media Transfer Engine: PASS [3/3]\n", flush=True)

    print("=========================================", flush=True)
    print("ALL MTPROTO TESTS PASSED SUCCESSFULLY! (25/25)", flush=True)
    print("=========================================", flush=True)


if __name__ == "__main__":
    asyncio.run(run_all_tests())
