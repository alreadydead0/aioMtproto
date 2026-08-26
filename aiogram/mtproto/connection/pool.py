"""
High-performance Multi-Session Pool & Rate Limiter for Telegram MTProto Data Centers.

Features:
- Dedicated DC session pooling (default 4, max 8 with warnings).
- Partial-failure tolerant initialization via asyncio.gather(return_exceptions=True).
- Deterministic 1-to-1 session-to-worker mapping by worker index to avoid socket contention.
- Shared token-bucket rate limiter per Data Center to prevent FLOOD_WAIT.
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
import time
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from aiogram.mtproto.connection.dc_manager import DCClientSession

logger = logging.getLogger("aiogram.mtproto.pool")

DEFAULT_POOL_SIZE = 8
MAX_SAFE_POOL_SIZE = 16


class TokenBucketLimiter:
    """
    Token-bucket rate limiter shared across all pooled connections to a specific DC.
    """

    def __init__(self, rate: float = 500.0, capacity: float = 500.0) -> None:
        self.rate = rate  # Tokens per second
        self.capacity = capacity  # Maximum burst capacity
        self._tokens = capacity
        self._last_update = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self, tokens: float = 1.0) -> None:
        """
        Acquire tokens from the bucket, sleeping asynchronously if exhausted.
        """
        while True:
            async with self._lock:
                now = time.monotonic()
                elapsed = now - self._last_update
                self._last_update = now
                self._tokens = min(self.capacity, self._tokens + elapsed * self.rate)

                if self._tokens >= tokens:
                    self._tokens -= tokens
                    return

                needed = tokens - self._tokens
                wait_time = needed / self.rate

            await asyncio.sleep(wait_time)


class DCSessionPool:
    """
    Manages a pool of concurrent, isolated DCClientSession instances for a specific Data Center.
    Enforces deterministic one-session-per-worker ownership.
    """

    def __init__(
        self,
        dc_id: int,
        session_factory: Callable[[], Awaitable[DCClientSession]] | None = None,
        dc_manager: Any = None,
        pool_size: int = DEFAULT_POOL_SIZE,
        rate_limit: float = 25.0,
    ) -> None:
        if pool_size > MAX_SAFE_POOL_SIZE:
            logger.warning(
                "[DC %d] Requested pool_size=%d exceeds safe maximum (%d). "
                "Capping to %d to avoid Telegram connection limits/FLOOD_WAIT.",
                dc_id,
                pool_size,
                MAX_SAFE_POOL_SIZE,
                MAX_SAFE_POOL_SIZE,
            )
            pool_size = MAX_SAFE_POOL_SIZE

        self.dc_id = dc_id
        self._session_factory = session_factory
        self.dc_manager = dc_manager
        self.pool_size = max(1, pool_size)
        self.limiter = TokenBucketLimiter(rate=rate_limit, capacity=rate_limit)

        self._sessions: list[DCClientSession] = []
        self._lock = asyncio.Lock()
        self._auth_lock = asyncio.Lock()
        self._warmup_task: asyncio.Task[None] | None = None
        self._initialized = False

    @property
    def sessions(self) -> list[DCClientSession]:
        return self._sessions

    @sessions.setter
    def sessions(self, value: list[DCClientSession]) -> None:
        self._sessions = value

    @property
    def is_ready(self) -> bool:
        return any(s.is_ready for s in self._sessions)

    @property
    def active_sessions_count(self) -> int:
        return len([s for s in self._sessions if s.is_ready])

    async def _create_pooled_session(self) -> DCClientSession:
        """
        Create a single pooled session with concurrent handshake and serialized auth import.
        """
        if self.dc_manager is not None and hasattr(
            self.dc_manager, "_create_handshaken_media_session"
        ):
            session: DCClientSession = await self.dc_manager._create_handshaken_media_session(
                self.dc_id
            )
            try:
                async with self._auth_lock:
                    await self.dc_manager._import_media_auth(session, self.dc_id)
            except Exception:
                await session.close()
                raise
            return session
        if self._session_factory is not None:
            async with self._auth_lock:
                return await self._session_factory()
        msg = f"No session_factory or dc_manager configured for DC {self.dc_id} pool"
        raise RuntimeError(msg)

    async def _warmup_remaining(self, count: int) -> None:
        """
        Background task to warm up remaining pooled sessions without delaying startup.
        """
        tasks = [self._create_pooled_session() for _ in range(count)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        async with self._lock:
            for res in results:
                if isinstance(res, BaseException):
                    logger.debug(
                        "[DC %d] Background pool warmup session error: %s", self.dc_id, res
                    )
                elif hasattr(res, "is_ready") and res.is_ready:
                    self._sessions.append(res)
                elif hasattr(res, "close"):
                    await res.close()

            logger.info(
                "[DC %d] Background pool warmup complete: %d/%d sessions active",
                self.dc_id,
                len([s for s in self._sessions if s.is_ready]),
                self.pool_size,
            )

    async def init_pool(self, wait_full: bool = True) -> None:
        """
        Initialize the pool.
        If wait_full=False, enables fast-path 1st session with background lazy warmup.
        """
        async with self._lock:
            self._sessions = [s for s in self._sessions if s.is_ready]
            if len(self._sessions) >= self.pool_size:
                self._initialized = True
                return

            if not self._sessions:
                # Fast-path: Synchronously initialize the first session so media transfer starts instantly
                logger.info(
                    "[DC %d] Starting media session pool (fast-path 1st worker, total=%d)...",
                    self.dc_id,
                    self.pool_size,
                )
                first_session = await self._create_pooled_session()
                self._sessions.append(first_session)
                self._initialized = True
                logger.info(
                    "[DC %d] Media pool 1st worker ready -> unblocking transfer", self.dc_id
                )

            needed = self.pool_size - len(self._sessions)
            if needed > 0 and (self._warmup_task is None or self._warmup_task.done()):
                self._warmup_task = asyncio.create_task(self._warmup_remaining(needed))

        if wait_full and self._warmup_task and not self._warmup_task.done():
            await self._warmup_task

    async def initialize(self) -> None:
        """
        Fully initialize all sessions in the pool.
        """
        await self.init_pool(wait_full=True)

    def get_session(self, worker_idx: int = 0) -> DCClientSession:
        """
        Return a session assigned to a worker index for 1-to-1 deterministic socket ownership.
        """
        ready_sessions = [s for s in self._sessions if s.is_ready]
        if not ready_sessions:
            if self._sessions:
                return self._sessions[worker_idx % len(self._sessions)]
            msg = f"Session pool for DC {self.dc_id} has no initialized sessions"
            raise RuntimeError(msg)

        # Worker index modulo healthy session count guarantees exclusive assignment
        return ready_sessions[worker_idx % len(ready_sessions)]

    async def get_session_async(self, worker_idx: int = 0) -> DCClientSession:
        """
        Asynchronously ensure the pool is ready and return the worker's session.
        """
        if not self._initialized:
            await self.init_pool(wait_full=False)

        # If background warmup is in progress, wait briefly for worker's dedicated session
        if self._warmup_task and not self._warmup_task.done():
            ready_count = len([s for s in self._sessions if s.is_ready])
            if worker_idx >= ready_count:
                with contextlib.suppress(asyncio.TimeoutError, Exception):
                    await asyncio.wait_for(asyncio.shield(self._warmup_task), timeout=2.0)

        async with self._lock:
            ready_sessions = [s for s in self._sessions if s.is_ready]
            if worker_idx < len(ready_sessions):
                return ready_sessions[worker_idx]
            if ready_sessions:
                return ready_sessions[worker_idx % len(ready_sessions)]
            msg = f"Session pool for DC {self.dc_id} has no ready sessions"
            raise RuntimeError(msg)

    async def invalidate_session(self, session: DCClientSession) -> None:
        """
        Invalidate a failed session and trigger a background reconnect.
        """
        async with self._lock:
            if session in self._sessions:
                self._sessions.remove(session)
                with contextlib.suppress(Exception):
                    await session.close()

            # Attempt replacement in background
            async def _reconnect() -> None:
                try:
                    new_session = await self._create_pooled_session()
                    async with self._lock:
                        self._sessions.append(new_session)
                    logger.info("[DC %d] Replaced invalidated pooled session", self.dc_id)
                except Exception as e:
                    logger.error("[DC %d] Failed to replace pooled session: %s", self.dc_id, e)

            asyncio.create_task(_reconnect())

    async def close(self) -> None:
        """
        Close all sessions in this pool.
        """
        async with self._lock:
            self._initialized = False
            for s in self._sessions:
                with contextlib.suppress(Exception):
                    await s.close()
            self._sessions.clear()
            logger.debug("[DC %d] Session pool closed", self.dc_id)
