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

DEFAULT_POOL_SIZE = 4
MAX_SAFE_POOL_SIZE = 8


class TokenBucketLimiter:
    """
    Token-bucket rate limiter shared across all pooled connections to a specific DC.
    Prevents flooding Telegram DC with concurrent bursts.
    """

    def __init__(self, rate: float = 25.0, capacity: float = 25.0) -> None:
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
        self._initialized = False

    @property
    def sessions(self) -> list[DCClientSession]:
        return self._sessions

    @sessions.setter
    def sessions(self, value: list[DCClientSession]) -> None:
        self._sessions = value

    @property
    def is_ready(self) -> bool:
        return self._initialized and any(s.is_ready for s in self._sessions)

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

    async def init_pool(self) -> None:
        """
        Initialize all sessions in the pool concurrently with partial-failure tolerance.
        """
        async with self._lock:
            self._sessions = [s for s in self._sessions if s.is_ready]
            needed = self.pool_size - len(self._sessions)
            if needed <= 0 and self._sessions:
                return

            logger.info(
                "[DC %d] Initializing session pool (needed=%d, total=%d)...",
                self.dc_id,
                needed,
                self.pool_size,
            )
            tasks = [self._create_pooled_session() for _ in range(needed)]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            first_exc: BaseException | None = None

            for res in results:
                if isinstance(res, BaseException):
                    if first_exc is None:
                        first_exc = res
                    logger.warning("[DC %d] Pool session creation error: %s", self.dc_id, res)
                elif hasattr(res, "is_ready") and res.is_ready:
                    self._sessions.append(res)
                elif hasattr(res, "close"):
                    # Connected/handshaken but failed auth import — must be closed,
                    # not just dropped, or its reader task leaks.
                    await res.close()

            if not self._sessions:
                if first_exc:
                    raise first_exc
                msg = f"Failed to initialize any session in pool for DC {self.dc_id}"
                raise RuntimeError(msg)

            self._initialized = True
            logger.info(
                "[DC %d] Pool ready: %d/%d sessions active",
                self.dc_id,
                len(self._sessions),
                self.pool_size,
            )

    initialize = init_pool

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
        if not self.is_ready:
            await self.init_pool()
        return self.get_session(worker_idx)

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
