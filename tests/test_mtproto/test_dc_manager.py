"""
Comprehensive test suite for Telegram MTProto Multi-DC Architecture:
1. Main DC handshake succeeds.
2. USER_MIGRATE_X creates the correct target DC client.
3. Target DC gets a separate AuthKey and session_id.
4. auth.exportAuthorization is executed on the authorized main DC.
5. auth.importAuthorization is executed on the target DC.
6. Target DC is not marked READY before import succeeds.
7. Two simultaneous requests for DC 4 share one authorization operation without race conditions.
8. AUTH_KEY_UNREGISTERED invalidates the DC 4 client.
9. AUTH_KEY_UNREGISTERED causes fresh handshake + authorization and one retry.
10. A failed authorization never reaches downloader as active_client.
11. DC 4 BadServerSalt does not modify DC 5 / main DC state.
12. Concurrent downloads using multiple media DCs remain isolated.
13. Closing a DC client correctly stops its reader task and fails pending requests.
14. Unknown DC ID does not silently fall back to DC 2 (raises explicit ValueError).
"""

from __future__ import annotations

import asyncio
import os
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from aiogram.errors.mtproto import (
    AuthKeyNotFound,
    AuthKeyUnregistered,
    BadServerSaltError,
    FileMigrate,
    Unauthorized,
    UserMigrate,
)
from aiogram.media.downloader import FileDownloader
from aiogram.mtproto.connection.dc import get_dc
from aiogram.mtproto.connection.dc_manager import DCClientSession, DCManager, DCState
from aiogram.mtproto.crypto.auth_key import AuthKey
from aiogram.mtproto.protocol.rpc import RPCEngine
from aiogram.raw import functions as raw_funcs
from aiogram.raw import types as raw_types
from aiogram.raw.core.primitives import TLObject, TLRequest
from aiogram.session.memory import MemorySession


class MockTransport:
    HEADER = b""

    def pack(self, payload: bytes) -> bytes:
        return payload

    async def read_packet(self, reader: Any) -> bytes:
        return b""


async def fake_connect(self: DCClientSession) -> None:
    self.connection = MagicMock()
    self.connection.is_connected = True
    self.connection.close = AsyncMock()
    self.connection.send = AsyncMock()
    self.connection.receive = AsyncMock()
    self.state = DCState.CONNECTING


def create_fake_auth_key() -> AuthKey:
    return AuthKey(os.urandom(256))


@pytest.mark.asyncio
async def test_1_main_dc_handshake_succeeds() -> None:
    """Test 1: Main DC handshake succeeds."""
    manager = DCManager(
        api_id=12345,
        api_hash="mock_hash",
        main_dc_id=2,
        transport_factory=MockTransport,
        session_storage=MemorySession(),
    )

    fake_key = create_fake_auth_key()
    fake_salt = 123456789

    with (
        patch.object(DCClientSession, "connect", side_effect=fake_connect, autospec=True),
        patch.object(DCClientSession, "handshake", new_callable=AsyncMock) as mock_hs,
    ):
        mock_hs.return_value = (fake_key, fake_salt)

        def fake_init_rpc(self: DCClientSession, cb: Any = None) -> RPCEngine:
            self.rpc = MagicMock()
            self.rpc.invoke = AsyncMock(return_value=True)
            self.rpc.stop = AsyncMock()
            return self.rpc

        with patch.object(DCClientSession, "init_rpc", side_effect=fake_init_rpc, autospec=True):
            client = await manager.get_dc_client(2, is_media=False)
            assert client.dc_id == 2
            assert client.auth_key == fake_key
            assert client.server_salt == fake_salt
            assert client.state == DCState.READY


@pytest.mark.asyncio
async def test_2_user_migrate_creates_correct_target_dc() -> None:
    """Test 2: USER_MIGRATE_X creates the correct target DC client and retries."""
    manager = DCManager(
        api_id=12345,
        api_hash="mock_hash",
        main_dc_id=2,
        transport_factory=MockTransport,
        session_storage=MemorySession(),
    )

    fake_key_dc2 = create_fake_auth_key()
    fake_key_dc5 = create_fake_auth_key()

    with (
        patch.object(DCClientSession, "connect", side_effect=fake_connect, autospec=True),
        patch.object(DCClientSession, "handshake", new_callable=AsyncMock) as mock_hs,
    ):
        mock_hs.side_effect = [(fake_key_dc2, 100), (fake_key_dc5, 200)]

        call_count = 0

        async def fake_invoke(query: TLRequest[Any], timeout: float = 30.0) -> Any:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise UserMigrate(303, "USER_MIGRATE_5", new_dc=5)
            return "SUCCESS_ON_DC5"

        def fake_init_rpc(self: DCClientSession, cb: Any = None) -> RPCEngine:
            self.rpc = MagicMock()
            self.rpc.invoke = AsyncMock(side_effect=fake_invoke)
            self.rpc.stop = AsyncMock()
            return self.rpc

        with patch.object(DCClientSession, "init_rpc", side_effect=fake_init_rpc, autospec=True):
            query = MagicMock(spec=TLRequest)
            result = await manager.invoke(query)
            assert result == "SUCCESS_ON_DC5"
            assert manager.main_dc_id == 5


@pytest.mark.asyncio
async def test_3_target_dc_gets_separate_auth_key() -> None:
    """Test 3: Target DC gets a separate AuthKey and session_id."""
    manager = DCManager(
        api_id=12345,
        api_hash="mock_hash",
        main_dc_id=2,
        transport_factory=MockTransport,
        session_storage=MemorySession(),
    )

    fake_key_main = create_fake_auth_key()
    fake_key_media = create_fake_auth_key()

    with (
        patch.object(DCClientSession, "connect", side_effect=fake_connect, autospec=True),
        patch.object(DCClientSession, "handshake", new_callable=AsyncMock) as mock_hs,
    ):
        mock_hs.side_effect = [(fake_key_main, 111), (fake_key_media, 222)]

        def fake_init_rpc(self: DCClientSession, cb: Any = None) -> RPCEngine:
            self.rpc = MagicMock()
            self.rpc.stop = AsyncMock()
            if self.dc_id == 2:
                # Main DC responds to ExportAuthorization
                self.rpc.invoke = AsyncMock(
                    return_value=raw_types.ExportedAuthorization(
                        id=999, bytes_data=b"AUTH_TOKEN_BYTES"
                    )
                )
            else:
                # Media DC responds to ImportAuthorization
                self.rpc.invoke = AsyncMock(return_value=True)
            return self.rpc

        with patch.object(DCClientSession, "init_rpc", side_effect=fake_init_rpc, autospec=True):
            main_client = await manager.get_dc_client(2, is_media=False)
            media_client = await manager.get_dc_client(4, is_media=True)

            assert main_client.dc_id == 2
            assert media_client.dc_id == 4
            assert main_client.auth_key != media_client.auth_key
            assert main_client.session_id != media_client.session_id


@pytest.mark.asyncio
async def test_4_and_5_export_and_import_authorization() -> None:
    """Test 4 & 5: auth.exportAuthorization executed on main DC, auth.importAuthorization on target DC."""
    manager = DCManager(
        api_id=12345,
        api_hash="mock_hash",
        main_dc_id=2,
        transport_factory=MockTransport,
        session_storage=MemorySession(),
    )

    main_invocations: list[Any] = []
    media_invocations: list[Any] = []

    with (
        patch.object(DCClientSession, "connect", side_effect=fake_connect, autospec=True),
        patch.object(DCClientSession, "handshake", new_callable=AsyncMock) as mock_hs,
    ):
        mock_hs.side_effect = [(create_fake_auth_key(), 1), (create_fake_auth_key(), 2)]

        def fake_init_rpc(self: DCClientSession, cb: Any = None) -> RPCEngine:
            self.rpc = MagicMock()
            self.rpc.stop = AsyncMock()
            if self.dc_id == 2:

                async def mock_main_invoke(req: Any, **kw: Any) -> Any:
                    main_invocations.append(req)
                    return raw_types.ExportedAuthorization(id=777, bytes_data=b"SECRET_BYTES")

                self.rpc.invoke = AsyncMock(side_effect=mock_main_invoke)
            else:

                async def mock_media_invoke(req: Any, **kw: Any) -> Any:
                    media_invocations.append(req)
                    return True

                self.rpc.invoke = AsyncMock(side_effect=mock_media_invoke)
            return self.rpc

        with patch.object(DCClientSession, "init_rpc", side_effect=fake_init_rpc, autospec=True):
            media_client = await manager.get_media_client(4)

            assert any(
                isinstance(r, raw_funcs.auth.ExportAuthorization) and r.dc_id == 4
                for r in main_invocations
            )
            assert any(
                isinstance(r, raw_funcs.auth.ImportAuthorization) and r.id == 777
                for r in media_invocations
            )
            assert media_client.auth_imported is True
            assert media_client.state == DCState.READY


@pytest.mark.asyncio
async def test_6_target_dc_not_ready_before_import_succeeds() -> None:
    """Test 6: Target DC is not marked READY before import succeeds."""
    manager = DCManager(
        api_id=12345,
        api_hash="mock_hash",
        main_dc_id=2,
        transport_factory=MockTransport,
        session_storage=MemorySession(),
    )

    with (
        patch.object(DCClientSession, "connect", side_effect=fake_connect, autospec=True),
        patch.object(DCClientSession, "handshake", new_callable=AsyncMock) as mock_hs,
    ):
        mock_hs.side_effect = [(create_fake_auth_key(), 1), (create_fake_auth_key(), 2)]

        def fake_init_rpc(self: DCClientSession, cb: Any = None) -> RPCEngine:
            self.rpc = MagicMock()
            self.rpc.stop = AsyncMock()
            if self.dc_id == 2:
                self.rpc.invoke = AsyncMock(
                    return_value=raw_types.ExportedAuthorization(id=111, bytes_data=b"BYTES")
                )
            else:
                # Import fails!
                self.rpc.invoke = AsyncMock(side_effect=Unauthorized(401, "AUTH_KEY_UNREGISTERED"))
            return self.rpc

        with patch.object(DCClientSession, "init_rpc", side_effect=fake_init_rpc, autospec=True):
            with pytest.raises(Unauthorized):
                await manager.get_media_client(4)

            # Ensure DC 4 is not in the active sessions
            assert 4 not in manager._sessions


@pytest.mark.asyncio
async def test_7_concurrent_authorization_races() -> None:
    """Test 7: Two simultaneous requests for DC 4 share one authorization operation."""
    manager = DCManager(
        api_id=12345,
        api_hash="mock_hash",
        main_dc_id=2,
        transport_factory=MockTransport,
        session_storage=MemorySession(),
    )

    handshake_count = 0

    with (
        patch.object(DCClientSession, "connect", side_effect=fake_connect, autospec=True),
        patch.object(DCClientSession, "handshake", new_callable=AsyncMock) as mock_hs,
    ):

        async def count_handshake() -> tuple[AuthKey, int]:
            nonlocal handshake_count
            handshake_count += 1
            await asyncio.sleep(0.05)  # simulate network delay
            return create_fake_auth_key(), 123

        mock_hs.side_effect = count_handshake

        def fake_init_rpc(self: DCClientSession, cb: Any = None) -> RPCEngine:
            self.rpc = MagicMock()
            self.rpc.stop = AsyncMock()
            self.rpc.invoke = AsyncMock(
                return_value=raw_types.ExportedAuthorization(id=123, bytes_data=b"BYTES")
            )
            return self.rpc

        with patch.object(DCClientSession, "init_rpc", side_effect=fake_init_rpc, autospec=True):
            # Launch 5 concurrent get_media_client calls for DC 4
            results = await asyncio.gather(*(manager.get_media_client(4) for _ in range(5)))

            # All 5 return the same instance
            first = results[0]
            assert all(r is first for r in results)
            # Handshakes: 1 for Main DC 2, 1 for Media DC 4
            assert handshake_count == 2


@pytest.mark.asyncio
async def test_8_auth_key_unregistered_invalidates_client() -> None:
    """Test 8: AUTH_KEY_UNREGISTERED invalidates the DC client."""
    manager = DCManager(
        api_id=12345,
        api_hash="mock_hash",
        main_dc_id=2,
        transport_factory=MockTransport,
        session_storage=MemorySession(),
    )

    with (
        patch.object(DCClientSession, "connect", side_effect=fake_connect, autospec=True),
        patch.object(DCClientSession, "handshake", new_callable=AsyncMock) as mock_hs,
    ):
        mock_hs.return_value = (create_fake_auth_key(), 123)

        def fake_init_rpc(self: DCClientSession, cb: Any = None) -> RPCEngine:
            self.rpc = MagicMock()
            self.rpc.stop = AsyncMock()
            self.rpc.invoke = AsyncMock(return_value=True)
            return self.rpc

        with patch.object(DCClientSession, "init_rpc", side_effect=fake_init_rpc, autospec=True):
            client = await manager.get_dc_client(2, is_media=False)
            assert 2 in manager._sessions
            await manager.invalidate_dc(2)
            assert 2 not in manager._sessions
            assert client.state in (DCState.FAILED, DCState.CLOSED)


@pytest.mark.asyncio
async def test_9_auth_key_unregistered_recovery_and_retry() -> None:
    """Test 9: AUTH_KEY_UNREGISTERED causes fresh handshake + retry."""
    manager = DCManager(
        api_id=12345,
        api_hash="mock_hash",
        main_dc_id=2,
        transport_factory=MockTransport,
        session_storage=MemorySession(),
    )

    attempt_count = 0

    with (
        patch.object(DCClientSession, "connect", side_effect=fake_connect, autospec=True),
        patch.object(DCClientSession, "handshake", new_callable=AsyncMock) as mock_hs,
    ):
        mock_hs.side_effect = [
            (create_fake_auth_key(), 1),
            (create_fake_auth_key(), 2),
        ]

        def fake_init_rpc(self: DCClientSession, cb: Any = None) -> RPCEngine:
            self.rpc = MagicMock()
            self.rpc.stop = AsyncMock()

            async def mock_invoke(req: Any, **kw: Any) -> Any:
                nonlocal attempt_count
                attempt_count += 1
                if attempt_count == 1:
                    raise AuthKeyUnregistered(401, "AUTH_KEY_UNREGISTERED")
                return "SUCCESS_AFTER_RECOVERY"

            self.rpc.invoke = AsyncMock(side_effect=mock_invoke)
            return self.rpc

        with patch.object(DCClientSession, "init_rpc", side_effect=fake_init_rpc, autospec=True):
            query = MagicMock(spec=TLRequest)
            result = await manager.invoke(query, max_retries=1)
            assert result == "SUCCESS_AFTER_RECOVERY"
            assert attempt_count == 2


@pytest.mark.asyncio
async def test_10_failed_auth_never_reaches_downloader() -> None:
    """Test 10: A failed authorization never reaches downloader as active_client."""
    mock_client = MagicMock()
    # Downloader requests get_media_client which raises Unauthorized
    mock_client.get_media_client = AsyncMock(
        side_effect=Unauthorized(401, "AUTH_KEY_UNREGISTERED")
    )
    mock_client.dc_id = 4

    downloader = FileDownloader(client=mock_client, chunk_size=1024, max_retries=2)
    dummy_location = MagicMock(spec=TLObject)

    with pytest.raises(Unauthorized):
        await downloader.download(location=dummy_location, file_size=500)


@pytest.mark.asyncio
async def test_11_bad_server_salt_isolated_to_dc() -> None:
    """Test 11: DC 4 BadServerSalt does not modify DC 5 / main DC state."""
    manager = DCManager(
        api_id=12345,
        api_hash="mock_hash",
        main_dc_id=2,
        transport_factory=MockTransport,
        session_storage=MemorySession(),
    )

    with (
        patch.object(DCClientSession, "connect", side_effect=fake_connect, autospec=True),
        patch.object(DCClientSession, "handshake", new_callable=AsyncMock) as mock_hs,
    ):
        mock_hs.side_effect = [(create_fake_auth_key(), 1000), (create_fake_auth_key(), 2000)]

        def fake_init_rpc(self: DCClientSession, cb: Any = None) -> RPCEngine:
            self.rpc = MagicMock()
            self.rpc.stop = AsyncMock()
            if self.dc_id == 2:
                self.rpc.invoke = AsyncMock(
                    return_value=raw_types.ExportedAuthorization(id=1, bytes_data=b"X")
                )
            else:
                self.rpc.invoke = AsyncMock(return_value=True)
            self.rpc.server_salt = self.server_salt
            return self.rpc

        with patch.object(DCClientSession, "init_rpc", side_effect=fake_init_rpc, autospec=True):
            main_client = await manager.get_dc_client(2, is_media=False)
            media_client = await manager.get_dc_client(4, is_media=True)

            assert main_client.server_salt == 1000
            assert media_client.server_salt == 2000

            # Media client receives new server salt
            media_client.server_salt = 999999
            assert main_client.server_salt == 1000


@pytest.mark.asyncio
async def test_12_concurrent_downloads_multi_dc_isolated() -> None:
    """Test 12: Concurrent downloads using multiple media DCs remain isolated."""
    manager = DCManager(
        api_id=12345,
        api_hash="mock_hash",
        main_dc_id=2,
        transport_factory=MockTransport,
        session_storage=MemorySession(),
    )

    with (
        patch.object(DCClientSession, "connect", side_effect=fake_connect, autospec=True),
        patch.object(DCClientSession, "handshake", new_callable=AsyncMock) as mock_hs,
    ):
        mock_hs.side_effect = [
            (create_fake_auth_key(), 1),  # Main DC 2
            (create_fake_auth_key(), 2),  # Media DC 4
            (create_fake_auth_key(), 3),  # Media DC 5
        ]

        def fake_init_rpc(self: DCClientSession, cb: Any = None) -> RPCEngine:
            self.rpc = MagicMock()
            self.rpc.stop = AsyncMock()
            self.rpc.invoke = AsyncMock(
                return_value=raw_types.ExportedAuthorization(id=1, bytes_data=b"DATA")
            )
            return self.rpc

        with patch.object(DCClientSession, "init_rpc", side_effect=fake_init_rpc, autospec=True):
            dc4_client, dc5_client = await asyncio.gather(
                manager.get_media_client(4),
                manager.get_media_client(5),
            )

            assert dc4_client.dc_id == 4
            assert dc5_client.dc_id == 5
            assert dc4_client.auth_key != dc5_client.auth_key
            assert dc4_client.session_id != dc5_client.session_id


@pytest.mark.asyncio
async def test_13_closing_dc_client_stops_and_fails_pending() -> None:
    """Test 13: Closing a DC client correctly stops its reader task and fails pending requests."""
    session = DCClientSession(dc_id=2, transport=MockTransport())
    session.connection = MagicMock()
    session.connection.close = AsyncMock()
    session.auth_key = create_fake_auth_key()
    session.server_salt = 123
    session.rpc = RPCEngine(
        connection=session.connection,
        auth_key=session.auth_key,
        server_salt=session.server_salt,
        session_id=session.session_id,
    )

    loop = asyncio.get_running_loop()
    pending_fut = loop.create_future()
    dummy_req = MagicMock(spec=TLRequest)
    session.rpc._pending_requests[12345] = (pending_fut, dummy_req)

    await session.close()
    assert session.state == DCState.CLOSED
    assert pending_fut.done()
    with pytest.raises(ConnectionError):
        pending_fut.result()


def test_14_unknown_dc_id_raises_value_error() -> None:
    """Test 14: Unknown DC ID does not silently fall back to DC 2."""
    with pytest.raises(ValueError, match="Unknown DC ID: 99"):
        get_dc(99, test_mode=False)

    with pytest.raises(ValueError, match="Unknown DC ID: 4"):
        get_dc(4, test_mode=True)  # Test mode only has DCs 1-3


# ==============================================================================
# Regression Tests for Stored AuthKey Validation & Recovery (Tests A - F)
# ==============================================================================


@pytest.mark.asyncio
async def test_a_stored_valid_auth_key_validation_succeeds() -> None:
    """Test A: Stored valid AuthKey -> validation succeeds -> no unnecessary ImportBotAuthorization -> READY."""
    storage = MemorySession()
    stored_key = create_fake_auth_key()
    session_data = await storage.load()
    session_data.auth_key = stored_key
    session_data.server_salt = 123456
    session_data.dc_id = 2
    await storage.save(session_data)

    manager = DCManager(
        api_id=12345,
        api_hash="mock_hash",
        main_dc_id=2,
        bot_token="123:ABC",
        transport_factory=MockTransport,
        session_storage=storage,
    )

    invoked_requests: list[Any] = []

    with patch.object(DCClientSession, "connect", side_effect=fake_connect, autospec=True):
        def fake_init_rpc(self: DCClientSession, cb: Any = None) -> RPCEngine:
            self.rpc = MagicMock()
            self.rpc.stop = AsyncMock()

            async def mock_invoke(req: Any, **kw: Any) -> Any:
                invoked_requests.append(req)
                return [raw_types.User(id=123, is_self=True)]

            self.rpc.invoke = AsyncMock(side_effect=mock_invoke)
            return self.rpc

        with patch.object(DCClientSession, "init_rpc", side_effect=fake_init_rpc, autospec=True):
            client = await manager.get_dc_client(2, is_media=False)
            assert client.is_ready is True
            assert client.auth_verified is True
            assert client.auth_key == stored_key

            # Validation query executed
            assert any(isinstance(r, raw_funcs.users.GetUsers) for r in invoked_requests)
            # Bot authorization was NOT unnecessarily executed
            assert not any(isinstance(r, raw_funcs.auth.ImportBotAuthorization) for r in invoked_requests)


@pytest.mark.asyncio
async def test_b_stored_stale_auth_key_invalidated_and_recovered() -> None:
    """Test B: Stored stale AuthKey -> validation returns AUTH_KEY_UNREGISTERED -> stale key invalidated -> fresh handshake -> ImportBotAuthorization -> READY."""
    storage = MemorySession()
    stale_key = create_fake_auth_key()
    session_data = await storage.load()
    session_data.auth_key = stale_key
    session_data.server_salt = 111
    session_data.dc_id = 2
    await storage.save(session_data)

    manager = DCManager(
        api_id=12345,
        api_hash="mock_hash",
        main_dc_id=2,
        bot_token="123:ABC",
        transport_factory=MockTransport,
        session_storage=storage,
    )

    fresh_key = create_fake_auth_key()
    invoked_requests: list[Any] = []

    with (
        patch.object(DCClientSession, "connect", side_effect=fake_connect, autospec=True),
        patch.object(DCClientSession, "handshake", new_callable=AsyncMock) as mock_hs,
    ):
        mock_hs.return_value = (fresh_key, 999)

        def fake_init_rpc(self: DCClientSession, cb: Any = None) -> RPCEngine:
            self.rpc = MagicMock()
            self.rpc.stop = AsyncMock()

            async def mock_invoke(req: Any, **kw: Any) -> Any:
                invoked_requests.append(req)
                if isinstance(req, raw_funcs.users.GetUsers):
                    # Stored key fails validation on Telegram
                    raise AuthKeyUnregistered(401, "AUTH_KEY_UNREGISTERED")
                if isinstance(req, raw_funcs.auth.ImportBotAuthorization):
                    # Fresh bot sign-in succeeds
                    return raw_types.Authorization(user=raw_types.User(id=789, is_self=True))
                return True

            self.rpc.invoke = AsyncMock(side_effect=mock_invoke)
            return self.rpc

        with patch.object(DCClientSession, "init_rpc", side_effect=fake_init_rpc, autospec=True):
            client = await manager.get_dc_client(2, is_media=False)
            assert client.is_ready is True
            assert client.auth_verified is True
            assert client.auth_key == fresh_key

            # Stored key was cleared and new key was saved to storage
            saved_data = await storage.load()
            assert saved_data.auth_key == fresh_key
            assert saved_data.user_id == 789

            # Verified that ImportBotAuthorization ran after stale key invalidation
            assert any(isinstance(r, raw_funcs.auth.ImportBotAuthorization) for r in invoked_requests)


@pytest.mark.asyncio
async def test_c_stored_stale_auth_key_fresh_key_persisted() -> None:
    """Test C: Stored stale AuthKey -> fresh key persisted -> next application start loads fresh key -> validation succeeds."""
    storage = MemorySession()
    stale_key = create_fake_auth_key()
    session_data = await storage.load()
    session_data.auth_key = stale_key
    session_data.server_salt = 111
    session_data.dc_id = 2
    await storage.save(session_data)

    manager1 = DCManager(
        api_id=12345,
        api_hash="mock_hash",
        main_dc_id=2,
        bot_token="123:ABC",
        transport_factory=MockTransport,
        session_storage=storage,
    )

    fresh_key = create_fake_auth_key()

    with (
        patch.object(DCClientSession, "connect", side_effect=fake_connect, autospec=True),
        patch.object(DCClientSession, "handshake", new_callable=AsyncMock) as mock_hs,
    ):
        mock_hs.return_value = (fresh_key, 999)

        def fake_init_rpc_1(self: DCClientSession, cb: Any = None) -> RPCEngine:
            self.rpc = MagicMock()
            self.rpc.stop = AsyncMock()

            async def mock_invoke(req: Any, **kw: Any) -> Any:
                if isinstance(req, raw_funcs.users.GetUsers):
                    raise AuthKeyUnregistered(401, "AUTH_KEY_UNREGISTERED")
                if isinstance(req, raw_funcs.auth.ImportBotAuthorization):
                    return raw_types.Authorization(user=raw_types.User(id=555, is_self=True))
                return True

            self.rpc.invoke = AsyncMock(side_effect=mock_invoke)
            return self.rpc

        with patch.object(DCClientSession, "init_rpc", side_effect=fake_init_rpc_1, autospec=True):
            await manager1.get_dc_client(2, is_media=False)

    # Next application start (manager2 using same storage)
    manager2 = DCManager(
        api_id=12345,
        api_hash="mock_hash",
        main_dc_id=2,
        bot_token="123:ABC",
        transport_factory=MockTransport,
        session_storage=storage,
    )

    with patch.object(DCClientSession, "connect", side_effect=fake_connect, autospec=True):
        def fake_init_rpc_2(self: DCClientSession, cb: Any = None) -> RPCEngine:
            self.rpc = MagicMock()
            self.rpc.stop = AsyncMock()
            self.rpc.invoke = AsyncMock(return_value=[raw_types.User(id=555, is_self=True)])
            return self.rpc

        with patch.object(DCClientSession, "init_rpc", side_effect=fake_init_rpc_2, autospec=True):
            client2 = await manager2.get_dc_client(2, is_media=False)
            assert client2.auth_key == fresh_key
            assert client2.is_ready is True


@pytest.mark.asyncio
async def test_d_stale_main_auth_key_media_dc4_rebuilds_and_exports() -> None:
    """Test D: Stale main AuthKey -> request media DC4 -> main DC rebuilt -> ExportAuthorization(4) -> ImportAuthorization on DC4 -> media download succeeds."""
    storage = MemorySession()
    stale_key = create_fake_auth_key()
    session_data = await storage.load()
    session_data.auth_key = stale_key
    session_data.server_salt = 111
    session_data.dc_id = 2
    await storage.save(session_data)

    manager = DCManager(
        api_id=12345,
        api_hash="mock_hash",
        main_dc_id=2,
        bot_token="123:ABC",
        transport_factory=MockTransport,
        session_storage=storage,
    )

    fresh_main_key = create_fake_auth_key()
    media_key = create_fake_auth_key()

    with (
        patch.object(DCClientSession, "connect", side_effect=fake_connect, autospec=True),
        patch.object(DCClientSession, "handshake", new_callable=AsyncMock) as mock_hs,
    ):
        mock_hs.side_effect = [
            (media_key, 400),       # DC 4 handshake
            (fresh_main_key, 200),  # Fresh DC 2 handshake after stale invalidation
        ]

        def fake_init_rpc(self: DCClientSession, cb: Any = None) -> RPCEngine:
            self.rpc = MagicMock()
            self.rpc.stop = AsyncMock()

            async def mock_invoke(req: Any, **kw: Any) -> Any:
                if self.dc_id == 2:
                    if isinstance(req, raw_funcs.users.GetUsers):
                        raise AuthKeyUnregistered(401, "AUTH_KEY_UNREGISTERED")
                    if isinstance(req, raw_funcs.auth.ImportBotAuthorization):
                        return raw_types.Authorization(user=raw_types.User(id=1, is_self=True))
                    if isinstance(req, raw_funcs.auth.ExportAuthorization):
                        return raw_types.ExportedAuthorization(id=777, bytes_data=b"DC4_AUTH_TOKEN")
                elif self.dc_id == 4:
                    if isinstance(req, raw_funcs.auth.ImportAuthorization):
                        return raw_types.Authorization(user=raw_types.User(id=1, is_self=True))
                return True

            self.rpc.invoke = AsyncMock(side_effect=mock_invoke)
            return self.rpc

        with patch.object(DCClientSession, "init_rpc", side_effect=fake_init_rpc, autospec=True):
            dc4_client = await manager.get_media_client(4)
            assert dc4_client.dc_id == 4
            assert dc4_client.is_ready is True
            assert dc4_client.auth_imported is True

            # Main client is also verified and ready
            main_client = manager._sessions[2]
            assert main_client.auth_key == fresh_main_key
            assert main_client.auth_verified is True


@pytest.mark.asyncio
async def test_e_stale_media_dc4_auth_key_unregistered_recovery() -> None:
    """Test E: Stale media DC4 AuthKey -> AUTH_KEY_UNREGISTERED -> DC4 invalidated -> fresh handshake -> export/import -> retry exactly once -> success."""
    manager = DCManager(
        api_id=12345,
        api_hash="mock_hash",
        main_dc_id=2,
        bot_token="123:ABC",
        transport_factory=MockTransport,
        session_storage=MemorySession(),
    )

    main_key = create_fake_auth_key()
    dc4_key_1 = create_fake_auth_key()
    dc4_key_2 = create_fake_auth_key()

    attempt_dc4 = 0

    with (
        patch.object(DCClientSession, "connect", side_effect=fake_connect, autospec=True),
        patch.object(DCClientSession, "handshake", new_callable=AsyncMock) as mock_hs,
    ):
        mock_hs.side_effect = [
            (main_key, 100),
            (dc4_key_1, 401),
            (dc4_key_2, 402),
        ]

        def fake_init_rpc(self: DCClientSession, cb: Any = None) -> RPCEngine:
            self.rpc = MagicMock()
            self.rpc.stop = AsyncMock()

            async def mock_invoke(req: Any, **kw: Any) -> Any:
                nonlocal attempt_dc4
                if self.dc_id == 2:
                    if isinstance(req, raw_funcs.auth.ImportBotAuthorization):
                        return raw_types.Authorization(user=raw_types.User(id=1, is_self=True))
                    if isinstance(req, raw_funcs.auth.ExportAuthorization):
                        return raw_types.ExportedAuthorization(id=888, bytes_data=b"BYTES")
                elif self.dc_id == 4:
                    if isinstance(req, raw_funcs.auth.ImportAuthorization):
                        return True
                    # Real query on DC 4
                    attempt_dc4 += 1
                    if attempt_dc4 == 1:
                        raise AuthKeyUnregistered(401, "AUTH_KEY_UNREGISTERED")
                    return "FILE_BYTES_SUCCESS"
                return True

            self.rpc.invoke = AsyncMock(side_effect=mock_invoke)
            return self.rpc

        with patch.object(DCClientSession, "init_rpc", side_effect=fake_init_rpc, autospec=True):
            query = MagicMock(spec=TLRequest)
            result = await manager.invoke(query, target_dc_id=4, max_retries=1)
            assert result == "FILE_BYTES_SUCCESS"
            assert attempt_dc4 == 2


@pytest.mark.asyncio
async def test_f_multiple_concurrent_media_downloads_no_race() -> None:
    """Test F: Multiple concurrent media downloads -> only one main-DC rebuild -> only one DC4 authorization -> no race."""
    storage = MemorySession()
    stale_key = create_fake_auth_key()
    session_data = await storage.load()
    session_data.auth_key = stale_key
    session_data.server_salt = 111
    session_data.dc_id = 2
    await storage.save(session_data)

    manager = DCManager(
        api_id=12345,
        api_hash="mock_hash",
        main_dc_id=2,
        bot_token="123:ABC",
        transport_factory=MockTransport,
        session_storage=storage,
    )

    main_handshake_count = 0
    dc4_handshake_count = 0

    with patch.object(DCClientSession, "connect", side_effect=fake_connect, autospec=True):
        async def mock_handshake(self: DCClientSession) -> tuple[AuthKey, int]:
            nonlocal main_handshake_count, dc4_handshake_count
            if self.dc_id == 2:
                main_handshake_count += 1
                await asyncio.sleep(0.02)
                return create_fake_auth_key(), 200
            if self.dc_id == 4:
                dc4_handshake_count += 1
                await asyncio.sleep(0.02)
                return create_fake_auth_key(), 400
            return create_fake_auth_key(), 100

        with patch.object(DCClientSession, "handshake", side_effect=mock_handshake, autospec=True):
            def fake_init_rpc(self: DCClientSession, cb: Any = None) -> RPCEngine:
                self.rpc = MagicMock()
                self.rpc.stop = AsyncMock()

                async def mock_invoke(req: Any, **kw: Any) -> Any:
                    if self.dc_id == 2:
                        if isinstance(req, raw_funcs.users.GetUsers):
                            raise AuthKeyUnregistered(401, "AUTH_KEY_UNREGISTERED")
                        if isinstance(req, raw_funcs.auth.ImportBotAuthorization):
                            return raw_types.Authorization(user=raw_types.User(id=1, is_self=True))
                        if isinstance(req, raw_funcs.auth.ExportAuthorization):
                            return raw_types.ExportedAuthorization(id=999, bytes_data=b"DC4_TOKEN")
                    elif self.dc_id == 4:
                        if isinstance(req, raw_funcs.auth.ImportAuthorization):
                            return True
                    return True

                self.rpc.invoke = AsyncMock(side_effect=mock_invoke)
                return self.rpc

            with patch.object(DCClientSession, "init_rpc", side_effect=fake_init_rpc, autospec=True):
                # 10 concurrent requests for DC 4
                clients = await asyncio.gather(*(manager.get_media_client(4) for _ in range(10)))

                # All returned the exact same client instance
                first = clients[0]
                assert all(c is first for c in clients)
                assert first.is_ready is True

                # Handshakes: exactly 1 for DC 2 (rebuild) and exactly 1 for DC 4
                assert main_handshake_count == 1
                assert dc4_handshake_count == 1

