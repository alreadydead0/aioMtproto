"""
Unit tests for MTProto DCSessionPool and TokenBucketLimiter.
"""

from __future__ import annotations

import asyncio
import time
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiogram.mtproto.connection.dc_manager import DCClientSession, DCState
from aiogram.mtproto.connection.pool import (
    DEFAULT_POOL_SIZE,
    MAX_SAFE_POOL_SIZE,
    DCSessionPool,
    TokenBucketLimiter,
)


def _create_mock_session(dc_id: int = 4) -> DCClientSession:
    sess = MagicMock(spec=DCClientSession)
    sess.dc_id = dc_id
    sess.is_media = True
    sess.state = DCState.READY
    sess.is_ready = True
    sess.is_connected = True
    sess.close = AsyncMock()
    return sess


@pytest.mark.asyncio
async def test_pool_size_clamping() -> None:
    factory = AsyncMock(side_effect=lambda: _create_mock_session(4))
    pool = DCSessionPool(dc_id=4, session_factory=factory, pool_size=16)
    assert pool.pool_size == MAX_SAFE_POOL_SIZE


@pytest.mark.asyncio
async def test_pool_init_and_worker_assignment() -> None:
    created_sessions: list[DCClientSession] = []

    async def factory() -> DCClientSession:
        s = _create_mock_session(4)
        created_sessions.append(s)
        return s

    pool = DCSessionPool(dc_id=4, session_factory=factory, pool_size=4)
    assert not pool.is_ready

    await pool.init_pool()
    assert pool.is_ready
    assert pool.active_sessions_count == 4
    assert len(created_sessions) == 4

    # Test 1-to-1 deterministic worker assignment
    s0 = pool.get_session(0)
    s1 = pool.get_session(1)
    s2 = pool.get_session(2)
    s3 = pool.get_session(3)

    assert s0 is created_sessions[0]
    assert s1 is created_sessions[1]
    assert s2 is created_sessions[2]
    assert s3 is created_sessions[3]

    # Worker index wraps around
    s4 = pool.get_session(4)
    assert s4 is created_sessions[0]

    await pool.close()
    assert not pool.is_ready


@pytest.mark.asyncio
async def test_pool_partial_failure_tolerance() -> None:
    call_count = 0

    async def factory() -> DCClientSession:
        nonlocal call_count
        call_count += 1
        if call_count == 2:
            raise ConnectionError("DC connection failed on worker 2")
        return _create_mock_session(4)

    pool = DCSessionPool(dc_id=4, session_factory=factory, pool_size=4)
    await pool.init_pool()

    assert pool.is_ready
    assert pool.active_sessions_count == 3

    # All workers still get a valid healthy session
    for w in range(4):
        s = pool.get_session(w)
        assert s.is_ready

    await pool.close()


@pytest.mark.asyncio
async def test_token_bucket_limiter() -> None:
    limiter = TokenBucketLimiter(rate=50.0, capacity=10.0)

    # First burst of 5 tokens should succeed immediately
    start = time.perf_counter()
    for _ in range(5):
        await limiter.acquire(1.0)
    elapsed = time.perf_counter() - start
    assert elapsed < 0.1  # Immediate acquisition

    # Drain capacity
    for _ in range(5):
        await limiter.acquire(1.0)

    # Next acquire will wait for token generation (1/50th of a second = 0.02s)
    start = time.perf_counter()
    await limiter.acquire(1.0)
    elapsed = time.perf_counter() - start
    assert elapsed >= 0.015


@pytest.mark.asyncio
async def test_pool_concurrent_auth_serialization_no_overlap() -> None:
    """
    Regression test for Bug 1: Ensure concurrent handshakes run concurrently,
    but auth export/import is strictly serialized (no concurrent overlap).
    """
    handshakes_started = 0
    in_auth_import = False
    auth_overlap_detected = False

    async def mock_handshake(dc_id: int) -> DCClientSession:
        nonlocal handshakes_started
        handshakes_started += 1
        # Handshakes can run concurrently
        await asyncio.sleep(0.01)
        sess = _create_mock_session(dc_id)
        sess.is_ready = False
        return sess

    async def mock_import_auth(session: DCClientSession, dc_id: int) -> None:
        nonlocal in_auth_import, auth_overlap_detected
        if in_auth_import:
            auth_overlap_detected = True
        in_auth_import = True
        # Simulate auth export + import roundtrip
        await asyncio.sleep(0.02)
        in_auth_import = False
        session.is_ready = True
        session.state = DCState.READY

    dc_mgr = MagicMock()
    dc_mgr._create_handshaken_media_session = AsyncMock(side_effect=mock_handshake)
    dc_mgr._import_media_auth = AsyncMock(side_effect=mock_import_auth)

    pool = DCSessionPool(dc_id=4, dc_manager=dc_mgr, pool_size=8)
    await pool.initialize()

    assert not auth_overlap_detected, "Auth export/import overlapped across pool members!"
    assert pool.active_sessions_count == 8
    assert len(pool.sessions) == 8
    assert handshakes_started == 8

    await pool.close()


@pytest.mark.asyncio
async def test_pool_failed_session_closed_promptly() -> None:
    """
    Regression test for Bug 2: Ensure any session that fails auth import is
    immediately closed to prevent orphaned reader loops or dangling tasks.
    """
    failed_sessions: list[DCClientSession] = []

    async def mock_handshake(dc_id: int) -> DCClientSession:
        sess = _create_mock_session(dc_id)
        sess.is_ready = False
        return sess

    call_count = 0

    async def mock_import_auth(session: DCClientSession, dc_id: int) -> None:
        nonlocal call_count
        call_count += 1
        if call_count % 2 == 0:
            failed_sessions.append(session)
            raise ConnectionError("AUTH_BYTES_INVALID")
        session.is_ready = True
        session.state = DCState.READY

    dc_mgr = MagicMock()
    dc_mgr._create_handshaken_media_session = AsyncMock(side_effect=mock_handshake)
    dc_mgr._import_media_auth = AsyncMock(side_effect=mock_import_auth)

    pool = DCSessionPool(dc_id=4, dc_manager=dc_mgr, pool_size=4)
    await pool.initialize()

    assert pool.active_sessions_count == 2
    # Verify that failed sessions were closed
    assert len(failed_sessions) == 2
    for s in failed_sessions:
        s.close.assert_awaited()

    await pool.close()


@pytest.mark.asyncio
async def test_dc_client_session_keepalive_lifecycle() -> None:
    """
    Regression test for Bug 3: Verify keepalive starts when ready and is cancelled on close.
    """
    sess = DCClientSession(dc_id=2, is_media=True)
    sess.state = DCState.READY
    sess.connection = MagicMock()
    sess.connection.is_connected = True
    sess.invoke = AsyncMock(return_value=123)

    sess.start_keepalive(interval=0.05, disconnect_delay=10)
    assert sess._keepalive_task is not None
    assert not sess._keepalive_task.done()

    # Wait for keepalive loop to fire at least once
    await asyncio.sleep(0.12)
    assert sess.invoke.await_count >= 1

    # Closing session cleanly stops keepalive
    await sess.close()
    assert sess._keepalive_task is None or sess._keepalive_task.done()
