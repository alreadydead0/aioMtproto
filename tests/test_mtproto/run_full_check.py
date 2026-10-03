# ruff: noqa: T201
import asyncio
import contextlib
import os
import sys
import time

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


class DummyTmp:
    def __truediv__(self, name: str) -> str:
        return f"temp_check_{name}"


async def run() -> None:
    print("1. Testing Crypto Primitives...", flush=True)
    test_pure_aes_roundtrip()
    test_aes_ige_roundtrip()
    test_factorize_pq()
    test_auth_key_and_kdf()
    test_rsa_encryption()
    print("   -> Crypto Primitives: 5/5 PASS", flush=True)

    print("2. Testing Transports Framing...", flush=True)
    await test_abridged_transport_small_packet()
    await test_abridged_transport_large_packet()
    await test_intermediate_transport()
    await test_full_transport()
    print("   -> Transports: 4/4 PASS", flush=True)

    print("3. Testing TL Binary Codecs & Polymorphic Parsing...", flush=True)
    test_tl_primitives()
    test_tl_user_serialization()
    test_tl_polymorphic_reader_and_gzip()
    print("   -> TL Codecs: 3/3 PASS", flush=True)

    print("4. Testing Session Storage (Memory, SQLite, StringSession)...", flush=True)
    await test_memory_session()
    tmp = DummyTmp()
    await test_sqlite_session(tmp)
    await test_string_session()
    print("   -> Sessions: 3/3 PASS", flush=True)

    print("5. Testing MTProto Error Parsing...", flush=True)
    test_parse_flood_wait()
    test_parse_slowmode_wait()
    test_parse_dc_migrates()
    test_parse_auth_errors()
    print("   -> Errors: 4/4 PASS", flush=True)

    print("6. Testing RPC Envelopes & Containers...", flush=True)
    test_plain_message_codec()
    test_encrypted_message_codec_and_containers()
    print("   -> RPC Codecs: 2/2 PASS", flush=True)

    print("7. Testing Bot & Dispatcher Event Routing...", flush=True)
    await test_bot_mtproto_initialization()
    await test_dispatcher_mtproto_event_routing()
    print("   -> Bot Integration: 2/2 PASS", flush=True)

    print("8. Testing High-Speed Parallel Media Engine...", flush=True)
    test_chunker_sizes_and_partitioning()
    await test_file_uploader_small_and_big()
    await test_file_downloader_parallel_and_disk_stream(tmp)
    print("   -> Media Transfers: 3/3 PASS", flush=True)

    print("\n" + "=" * 55)
    print("RESULT: ALL 26/26 MTPROTO TESTS PASSED PERFECTLY!")
    print("=" * 55)

    # Cleanup temp files
    for fname in ["temp_check_test_session.session", "temp_check_downloaded_file.bin"]:
        if os.path.exists(fname):
            with contextlib.suppress(Exception):
                os.remove(fname)


if __name__ == "__main__":
    asyncio.run(run())
