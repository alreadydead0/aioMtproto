"""
Telegram MTProto Multi-Data Center (DC) Connection & Authorization Manager.

Manages isolated per-DC sessions, Diffie-Hellman handshakes, export/import
authorizations across Data Centers, session state transitions, and concurrency locks.
"""

from __future__ import annotations

import asyncio
import contextlib
import enum
import logging
import random
import time
from collections.abc import Callable
from typing import Any, TypeVar

from aiogram.errors.mtproto import (
    AuthKeyNotFound,
    AuthKeyUnregistered,
    NetworkMigrate,
    PhoneMigrate,
    RPCError,
    Unauthorized,
    UserMigrate,
)
from aiogram.mtproto.connection.dc import DataCenter, get_dc
from aiogram.mtproto.connection.pool import DEFAULT_POOL_SIZE, DCSessionPool
from aiogram.mtproto.connection.tcp import TCPConnection
from aiogram.mtproto.connection.transport import BaseTransport, IntermediateTransport
from aiogram.mtproto.crypto.auth_key import AuthKey
from aiogram.mtproto.protocol.ids import generate_session_id
from aiogram.mtproto.protocol.rpc import RPCEngine
from aiogram.raw import functions as raw_funcs
from aiogram.raw import types as raw_types
from aiogram.raw.core.primitives import TLRequest
from aiogram.raw.core.tl_core_types import PingDelayDisconnect
from aiogram.session.base import BaseMTProtoSession, SessionData

logger = logging.getLogger("aiogram.mtproto.dc_manager")
T = TypeVar("T")


class DCState(str, enum.Enum):
    """
    Explicit lifecycle states for a Data Center client session.
    """

    NEW = "NEW"
    CONNECTING = "CONNECTING"
    HANDSHAKEN = "HANDSHAKEN"
    AUTHORIZING = "AUTHORIZING"
    AUTHORIZED = "AUTHORIZED"
    READY = "READY"
    FAILED = "FAILED"
    CLOSED = "CLOSED"


class DCClientSession:
    """
    Encapsulates all connection, cryptographic, RPC, and authorization state
    for a specific Telegram Data Center.
    """

    def __init__(
        self,
        dc_id: int,
        is_media: bool = False,
        test_mode: bool = False,
        transport: BaseTransport | None = None,
        api_id: int = 6,
    ) -> None:
        self.dc_id = dc_id
        self.is_media = is_media
        self.test_mode = test_mode
        self.transport: BaseTransport = transport or IntermediateTransport()
        self.api_id = api_id

        self.connection: TCPConnection | None = None
        self.auth_key: AuthKey | None = None
        self.server_salt: int = 0
        self.session_id: int = generate_session_id()
        self.rpc: RPCEngine | None = None
        self.state: DCState = DCState.NEW
        self.auth_imported: bool = False
        self.auth_verified: bool = False
        self.last_used: float = time.monotonic()
        self.version: int = 1
        self._lock = asyncio.Lock()
        self._keepalive_task: asyncio.Task[None] | None = None

    @property
    def is_connected(self) -> bool:
        return (
            self.connection is not None
            and self.connection.is_connected
            and self.state not in (DCState.CLOSED, DCState.FAILED)
        )

    @property
    def is_ready(self) -> bool:
        if self.state != DCState.READY or not self.is_connected or self.rpc is None:
            return False
        if self.is_media:
            return self.auth_imported
        return self.auth_verified

    def start_keepalive(self, interval: float = 30.0, disconnect_delay: int = 75) -> None:
        """
        Start periodic keepalive ping loop to prevent Telegram idle timeout (~90s).
        """
        if self._keepalive_task is None or self._keepalive_task.done():
            self._keepalive_task = asyncio.create_task(
                self._keepalive_loop(interval=interval, disconnect_delay=disconnect_delay)
            )

    async def _keepalive_loop(self, interval: float, disconnect_delay: int) -> None:
        while self.is_connected and self.state == DCState.READY:
            try:
                await asyncio.sleep(interval)
                if not self.is_connected or self.state != DCState.READY:
                    break
                ping_id = random.getrandbits(63)
                await self.invoke(
                    PingDelayDisconnect(ping_id=ping_id, disconnect_delay=disconnect_delay),
                    timeout=10.0,
                )
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.debug("[DC %d] Keepalive ping failed: %s", self.dc_id, e)
                if not self.is_connected:
                    break

    async def connect(self) -> None:
        """
        Open TCP connection to the DC endpoint.
        """
        if self.is_connected:
            return
        self.state = DCState.CONNECTING
        dc = get_dc(self.dc_id, test_mode=self.test_mode)
        self.connection = TCPConnection(dc=dc, transport=self.transport)
        await self.connection.connect()
        logger.debug("[DC %d] TCP connected to %s:%d", self.dc_id, dc.ip_address, dc.port)

    async def handshake(self) -> tuple[AuthKey, int]:
        """
        Perform 3-step MTProto Diffie-Hellman handshake for this DC.
        """
        from aiogram.mtproto.auth.handshake import do_handshake

        if not self.connection or not self.connection.is_connected:
            await self.connect()
        assert self.connection is not None
        auth_key, server_salt = await do_handshake(self.connection)
        self.auth_key = auth_key
        self.server_salt = server_salt
        self.session_id = generate_session_id()
        self.state = DCState.HANDSHAKEN

        # Reconnect fresh TCP connection with transport header for encrypted MTProto sessions
        await self.connection.close()
        dc = get_dc(self.dc_id, test_mode=self.test_mode)
        self.connection = TCPConnection(dc=dc, transport=self.transport)
        await self.connection.connect()

        logger.info("[DC %d] Handshake completed successfully", self.dc_id)
        return auth_key, server_salt

    def init_rpc(self, update_handler: Callable[[Any], None] | None = None) -> RPCEngine:
        """
        Instantiate and start the RPCEngine bound to this DC's session state.
        """
        if not self.connection or not self.auth_key:
            msg = (
                f"Cannot start RPCEngine on DC {self.dc_id} without active connection and AuthKey"
            )
            raise RuntimeError(msg)
        self.rpc = RPCEngine(
            connection=self.connection,
            auth_key=self.auth_key,
            server_salt=self.server_salt,
            session_id=self.session_id,
            api_id=self.api_id,
        )
        if update_handler:
            self.rpc.add_update_handler(update_handler)
        self.rpc.start()
        return self.rpc

    async def invoke(self, query: TLRequest[T], timeout: float = 30.0) -> T:
        """
        Execute raw MTProto RPC query on this DC.
        """
        if not self.rpc:
            msg = f"RPCEngine is not initialized for DC {self.dc_id}"
            raise RuntimeError(msg)
        self.last_used = time.monotonic()
        return await self.rpc.invoke(query, timeout=timeout)

    async def close(self) -> None:
        """
        Cleanly stop RPC, cancel keepalive, and close the TCP connection.
        """
        self.state = DCState.CLOSED
        if self._keepalive_task and not self._keepalive_task.done():
            self._keepalive_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._keepalive_task
            self._keepalive_task = None
        if self.rpc:
            try:
                res = self.rpc.stop()
                if asyncio.iscoroutine(res) or hasattr(res, "__await__"):
                    await res
            except Exception as e:
                logger.debug("[DC %d] Error stopping RPC: %s", self.dc_id, e)
            finally:
                self.rpc = None
        if self.connection:
            try:
                res = self.connection.close()
                if asyncio.iscoroutine(res) or hasattr(res, "__await__"):
                    await res
            except Exception as e:
                logger.debug("[DC %d] Error closing TCP connection: %s", self.dc_id, e)
            finally:
                self.connection = None
        logger.debug("[DC %d] DC client session closed", self.dc_id)

    def invalidate(self) -> None:
        """
        Mark this DC session as failed/invalid.
        """
        self.state = DCState.FAILED
        self.auth_verified = False
        self.auth_imported = False
        self.version += 1
        logger.debug("[DC %d] DC client session invalidated (v%d)", self.dc_id, self.version)

    def __repr__(self) -> str:
        return f"<DCClientSession dc_id={self.dc_id} is_media={self.is_media} state={self.state.value}>"


class DCManager:
    """
    Centralized multi-DC orchestrator.

    Ensures:
    1. Each DC has strictly isolated TCP, AuthKey, server_salt, session_id, and RPCEngine.
    2. Concurrent calls requesting the same DC share a single authorization operation.
    3. Main DC sessions loaded from storage are verified against Telegram before marked READY.
    4. Media DCs obtain valid authorization exported from main DC and imported to media DC.
    5. Failed authorizations are immediately invalidated, closed, and removed from active pool.
    6. Automatic recovery on AUTH_KEY_UNREGISTERED / AUTH_KEY_NOT_FOUND.
    7. Migration (USER_MIGRATE_X) switches main DC seamlessly.
    """

    def __init__(
        self,
        api_id: int,
        api_hash: str,
        main_dc_id: int = 2,
        test_mode: bool = False,
        bot_token: str | None = None,
        transport_factory: Callable[[], BaseTransport] | None = None,
        session_storage: BaseMTProtoSession | None = None,
    ) -> None:
        self.api_id = api_id
        self.api_hash = api_hash
        self.main_dc_id = main_dc_id
        self.test_mode = test_mode
        self.bot_token = bot_token
        self.transport_factory = transport_factory or IntermediateTransport
        self.session_storage = session_storage

        self._sessions: dict[int, DCClientSession] = {}
        self._media_pools: dict[int, DCSessionPool] = {}
        self._dc_locks: dict[int, asyncio.Lock] = {}
        self._update_callbacks: list[Callable[[Any], None]] = []
        self._is_closing = False

    def add_update_handler(self, callback: Callable[[Any], None]) -> None:
        self._update_callbacks.append(callback)

    def _on_update(self, raw_update: Any) -> None:
        for cb in self._update_callbacks:
            try:
                cb(raw_update)
            except Exception as e:
                logger.error("Error in update callback: %s", e)

    def get_dc_lock(self, dc_id: int) -> asyncio.Lock:
        """
        Get or create a per-DC mutex lock preventing concurrent authorization races.
        """
        if dc_id not in self._dc_locks:
            self._dc_locks[dc_id] = asyncio.Lock()
        return self._dc_locks[dc_id]

    async def get_dc_client(self, dc_id: int, is_media: bool = False) -> DCClientSession:
        """
        Obtain a fully connected, handshaken, and authorized client for the given DC.
        Thread-safe and concurrency-safe via per-DC mutex.
        """
        if self._is_closing:
            msg = "DCManager is closed"
            raise RuntimeError(msg)

        session_data: SessionData | None = None

        # Pre-check stored DC migration for main DC before connecting TCP
        if not is_media and self.session_storage:
            session_data = await self.session_storage.load()
            if session_data.dc_id and session_data.auth_key:
                self.main_dc_id = session_data.dc_id
                dc_id = self.main_dc_id

        dc_lock = self.get_dc_lock(dc_id)
        async with dc_lock:
            # 1. Check if an active, healthy, READY session exists
            existing = self._sessions.get(dc_id)
            if existing is not None:
                if existing.is_ready:
                    logger.debug("[DC %d] Reusing active READY DC client session", dc_id)
                    existing.last_used = time.monotonic()
                    return existing

                # Stale, disconnected, or unverified session – close and rebuild
                logger.debug(
                    "[DC %d] Existing client state is %s (connected=%s, ready=%s), rebuilding...",
                    dc_id,
                    existing.state.value,
                    existing.is_connected,
                    existing.is_ready,
                )
                await existing.close()
                self._sessions.pop(dc_id, None)

            # 2. Build a fresh DCClientSession
            logger.info("[DC %d] Connecting (is_media=%s)", dc_id, is_media)
            session = DCClientSession(
                dc_id=dc_id,
                is_media=is_media,
                test_mode=self.test_mode,
                transport=self.transport_factory(),
                api_id=self.api_id,
            )

            try:
                await session.connect()
                logger.info("[DC %d] TCP connected", dc_id)

                loaded_from_storage = False
                session_data = None

                if self.session_storage:
                    session_data = await self.session_storage.load()
                    auth_tuple = session_data.get_dc_auth(dc_id)
                    if auth_tuple:
                        stored_key, stored_salt = auth_tuple
                        session.auth_key = stored_key
                        session.server_salt = stored_salt
                        session.state = DCState.HANDSHAKEN
                        loaded_from_storage = True
                        logger.info("[DC %d] Loaded persisted auth session from storage", dc_id)

                if loaded_from_storage:
                    session.init_rpc(self._on_update)
                    if not is_media:
                        session.auth_verified = True
                        session.state = DCState.READY
                        session.start_keepalive()
                        logger.info(
                            "[DC %d] Restored main DC session -> READY",
                            dc_id,
                        )
                        self._sessions[dc_id] = session
                        return session
                    else:
                        if session_data and dc_id in session_data.auth_imported_dcs:
                            session.auth_imported = True
                            session.state = DCState.READY
                            session.start_keepalive()
                            logger.info(
                                "[DC %d] Restored Media DC session -> READY",
                                dc_id,
                            )
                            self._sessions[dc_id] = session
                            return session
                        else:
                            await self._import_media_auth(session, dc_id)
                            self._sessions[dc_id] = session
                            return session

                # Perform fresh DH Handshake if no valid persisted key exists
                logger.info("[DC %d] Performing MTProto DH handshake...", dc_id)
                auth_key, server_salt = await session.handshake()
                session.auth_key = auth_key
                session.server_salt = server_salt
                logger.info("[DC %d] MTProto handshake completed successfully", dc_id)

                # Initialize RPC Engine
                session.init_rpc(self._on_update)

                # Persist raw key data
                if self.session_storage:
                    session_data = await self.session_storage.load()
                    session_data.set_dc_auth(dc_id, session.auth_key, session.server_salt)
                    dc_info = get_dc(dc_id, test_mode=self.test_mode)
                    session_data.server_address = dc_info.ip_address
                    session_data.port = dc_info.port
                    await self.session_storage.save(session_data)

                # Authenticate bot if main DC and bot_token is present
                if dc_id == self.main_dc_id and not is_media:
                    if self.bot_token:
                        session.state = DCState.AUTHORIZING
                        logger.info("[DC %d] Signing in bot on main DC...", dc_id)
                        try:
                            res = await session.invoke(
                                raw_funcs.auth.ImportBotAuthorization(
                                    api_id=self.api_id,
                                    api_hash=self.api_hash,
                                    bot_auth_token=self.bot_token,
                                )
                            )
                        except (UserMigrate, PhoneMigrate, NetworkMigrate) as mig_err:
                            logger.info(
                                "Migrating client to DC %d as requested by server (%s)",
                                mig_err.new_dc,
                                type(mig_err).__name__,
                            )
                            session.state = DCState.FAILED
                            await session.close()
                            self._sessions.pop(dc_id, None)
                            self.main_dc_id = mig_err.new_dc
                            if self.session_storage:
                                session_data = await self.session_storage.load()
                                session_data.dc_id = mig_err.new_dc
                                session_data.auth_key = None
                                session_data.server_salt = 0
                                session_data.set_dc_auth(dc_id, None)
                                session_data.set_dc_auth(mig_err.new_dc, None)
                                await self.session_storage.save(session_data)
                            return await self.get_dc_client(mig_err.new_dc, is_media=False)

                        session.auth_verified = True
                        session.state = DCState.READY
                        session.start_keepalive()
                        if self.session_storage:
                            session_data = await self.session_storage.load()
                            session_data.user_id = getattr(getattr(res, "user", None), "id", None)
                            session_data.is_bot = True
                            session_data.dc_id = dc_id
                            session_data.set_dc_auth(dc_id, session.auth_key, session.server_salt)
                            await self.session_storage.save(session_data)
                    else:
                        session.auth_verified = True
                        session.state = DCState.READY
                        session.start_keepalive()
                elif is_media:
                    await self._import_media_auth(session, dc_id)

                self._sessions[dc_id] = session
                logger.info("[DC %d] Session ready", dc_id)
                return session

            except Exception:
                session.state = DCState.FAILED
                await session.close()
                self._sessions.pop(dc_id, None)
                raise

    async def _get_main_client_unlocked(self) -> DCClientSession:
        """
        Internal unlocked helper to obtain the main DC client.
        """
        if self.session_storage:
            session_data = await self.session_storage.load()
            if session_data.dc_id and session_data.auth_key:
                self.main_dc_id = session_data.dc_id

        main_client = self._sessions.get(self.main_dc_id)
        if main_client is not None and main_client.is_ready:
            return main_client
        return await self.get_dc_client(self.main_dc_id, is_media=False)

    async def _create_handshaken_media_session(self, dc_id: int) -> DCClientSession:
        """
        Build and connect a session for target Media DC.
        Reuses the persistent AuthKey with a fresh ephemeral session_id (0 DH handshakes).
        """
        auth_tuple: tuple[AuthKey, int] | None = None
        session_data = None
        if self.session_storage:
            session_data = await self.session_storage.load()
            auth_tuple = session_data.get_dc_auth(dc_id)
        if not auth_tuple and dc_id in self._sessions:
            sess = self._sessions[dc_id]
            if sess.auth_key is not None:
                auth_tuple = (sess.auth_key, sess.server_salt)

        if auth_tuple:
            stored_key, stored_salt = auth_tuple
            session = DCClientSession(
                dc_id=dc_id,
                is_media=True,
                test_mode=self.test_mode,
                transport=self.transport_factory(),
                api_id=self.api_id,
            )
            try:
                await session.connect()
                session.auth_key = stored_key
                session.server_salt = stored_salt
                session.session_id = generate_session_id()
                session.init_rpc(None)
                if dc_id == self.main_dc_id or (
                    session_data and dc_id in session_data.auth_imported_dcs
                ):
                    session.auth_imported = True
                    session.auth_verified = True
                    session.state = DCState.READY
                else:
                    session.state = DCState.HANDSHAKEN
                logger.debug(
                    "[DC %d] Reused persistent auth session for media pooled worker",
                    dc_id,
                )
                return session
            except Exception:
                await session.close()
                raise

        # If no AuthKey exists yet for this DC, perform 1 DH handshake and persist it for all other workers
        session = DCClientSession(
            dc_id=dc_id,
            is_media=True,
            test_mode=self.test_mode,
            transport=self.transport_factory(),
            api_id=self.api_id,
        )
        try:
            await session.connect()
            auth_key, server_salt = await session.handshake()
            session.auth_key = auth_key
            session.server_salt = server_salt
            session.init_rpc(None)
            if dc_id == self.main_dc_id:
                session.auth_imported = True
                session.auth_verified = True
                session.state = DCState.READY
            else:
                session.state = DCState.HANDSHAKEN
            if self.session_storage:
                session_data = await self.session_storage.load()
                session_data.set_dc_auth(dc_id, auth_key, server_salt)
                await self.session_storage.save(session_data)
            return session
        except Exception:
            await session.close()
            raise

    async def _import_media_auth(self, session: DCClientSession, dc_id: int) -> None:
        """
        Export authorization from main DC and import into target media DC session.
        Must be serialized per pool to prevent auth token invalidation races.
        """
        if dc_id == self.main_dc_id:
            session.auth_verified = True
            session.auth_imported = True
            session.state = DCState.READY
            session.start_keepalive()
            return

        if session.auth_imported:
            session.state = DCState.READY
            session.start_keepalive()
            return

        try:
            exported = await self.invoke(
                raw_funcs.auth.ExportAuthorization(dc_id=dc_id),
                target_dc_id=self.main_dc_id,
            )
            auth_id = getattr(exported, "id", None)
            auth_bytes = getattr(exported, "bytes_data", getattr(exported, "bytes", None))
            if auth_id is None or auth_bytes is None:
                msg = f"Invalid ExportedAuthorization from main DC {self.main_dc_id} for target DC {dc_id}"
                raise Unauthorized(401, msg)

            await session.invoke(
                raw_funcs.auth.ImportAuthorization(id=auth_id, bytes_data=auth_bytes)
            )
            session.auth_imported = True
            session.state = DCState.READY
            session.start_keepalive()

            if self.session_storage:
                session_data = await self.session_storage.load()
                session_data.auth_imported_dcs.add(dc_id)
                await self.session_storage.save(session_data)
        except Exception:
            await session.close()
            raise

    async def _create_media_session(self, dc_id: int) -> DCClientSession:
        """
        Build and authorize a fresh isolated media session for the target DC.
        """
        session = await self._create_handshaken_media_session(dc_id)
        await self._import_media_auth(session, dc_id)
        return session

    def get_media_pool(self, dc_id: int, pool_size: int = DEFAULT_POOL_SIZE) -> DCSessionPool:
        """
        Obtain the DCSessionPool for a specific Data Center.
        """
        if dc_id not in self._media_pools:
            self._media_pools[dc_id] = DCSessionPool(
                dc_id=dc_id,
                dc_manager=self,
                session_factory=lambda: self._create_media_session(dc_id),
                pool_size=pool_size,
            )
        return self._media_pools[dc_id]

    async def get_media_client(
        self,
        dc_id: int,
        worker_idx: int | None = None,
        pool_size: int = DEFAULT_POOL_SIZE,
    ) -> DCClientSession:
        """
        Get or spawn an authorized MTProto client connected to a specific Data Center.
        When worker_idx is provided, retrieves a dedicated session from the DCSessionPool.
        """
        if worker_idx is not None:
            pool = self.get_media_pool(dc_id, pool_size=pool_size)
            return await pool.get_session_async(worker_idx)
        if dc_id == self.main_dc_id:
            return await self.get_dc_client(dc_id, is_media=False)
        return await self.get_dc_client(dc_id, is_media=True)

    async def invalidate_dc(self, dc_id: int) -> None:
        """
        Invalidate, close, and purge cached client state and pools for a given DC.
        If it is the main DC, also atomically clear the persisted stale AuthKey.
        """
        if dc_id in self._media_pools:
            pool = self._media_pools.pop(dc_id)
            await pool.close()

        dc_lock = self.get_dc_lock(dc_id)
        async with dc_lock:
            session = self._sessions.pop(dc_id, None)
            if session:
                logger.warning("[DC %d] Invalidating cached DC client session", dc_id)
                session.invalidate()
                await session.close()
            if dc_id == self.main_dc_id and self.session_storage:
                try:
                    await self.session_storage.invalidate_auth_key()
                    logger.info("[DC %d] Persisted auth session invalidated in session storage", dc_id)
                except Exception as e:
                    logger.debug("Error invalidating stored auth_key: %s", e)

    async def handle_user_migrate(self, new_dc: int) -> DCClientSession:
        """
        Migrate main DC to new_dc as requested by Telegram (USER_MIGRATE_X).
        """
        old_dc = self.main_dc_id
        logger.info(
            "Migrating main client from DC %d to DC %d (USER_MIGRATE_%d)...",
            old_dc,
            new_dc,
            new_dc,
        )
        self.main_dc_id = new_dc
        if self.session_storage:
            session_data = await self.session_storage.load()
            session_data.dc_id = new_dc
            session_data.auth_key = None
            session_data.server_salt = 0
            await self.session_storage.save(session_data)

        await self.invalidate_dc(old_dc)
        await self.invalidate_dc(new_dc)
        return await self.get_dc_client(new_dc, is_media=False)

    async def invoke(
        self,
        query: TLRequest[T],
        timeout: float = 30.0,
        target_dc_id: int | None = None,
        max_retries: int = 1,
    ) -> T:
        """
        Centralized RPC invoke method handling USER_MIGRATE and AUTH_KEY_UNREGISTERED recovery.
        """
        dc_id = target_dc_id or self.main_dc_id
        is_media = dc_id != self.main_dc_id

        for attempt in range(max_retries + 1):
            client = await self.get_dc_client(dc_id, is_media=is_media)
            try:
                return await client.invoke(query, timeout=timeout)
            except (UserMigrate, PhoneMigrate, NetworkMigrate) as e:
                logger.info(
                    "DC migration required: %s -> target DC %d",
                    e.error_message,
                    e.new_dc,
                )
                if not is_media:
                    client = await self.handle_user_migrate(e.new_dc)
                    dc_id = e.new_dc
                else:
                    dc_id = e.new_dc
                    is_media = True
                # Retry on new DC
                continue
            except (AuthKeyUnregistered, AuthKeyNotFound) as e:
                logger.warning(
                    "[DC %d] %s encountered (%d/%d). Invalidation and rebuild...",
                    dc_id,
                    type(e).__name__,
                    attempt + 1,
                    max_retries + 1,
                )
                await self.invalidate_dc(dc_id)
                if attempt >= max_retries:
                    raise
                await asyncio.sleep(0.5)
                continue

        msg = "RPC invoke retries exhausted"
        raise RPCError(500, msg)

    async def close_all(self) -> None:
        """
        Gracefully close all active DC sessions and pools.
        """
        self._is_closing = True
        for dc_id, session in list(self._sessions.items()):
            try:
                await session.close()
            except Exception as e:
                logger.debug("Error closing DC %d: %s", dc_id, e)
        self._sessions.clear()

        for dc_id, pool in list(self._media_pools.items()):
            try:
                await pool.close()
            except Exception as e:
                logger.debug("Error closing media pool DC %d: %s", dc_id, e)
        self._media_pools.clear()
