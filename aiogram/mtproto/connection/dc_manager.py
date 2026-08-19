"""
Telegram MTProto Multi-Data Center (DC) Connection & Authorization Manager.

Manages isolated per-DC sessions, Diffie-Hellman handshakes, export/import
authorizations across Data Centers, session state transitions, and concurrency locks.
"""

from __future__ import annotations

import asyncio
import enum
import logging
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
from aiogram.mtproto.connection.tcp import TCPConnection
from aiogram.mtproto.connection.transport import BaseTransport, IntermediateTransport
from aiogram.mtproto.crypto.auth_key import AuthKey
from aiogram.mtproto.protocol.ids import generate_session_id
from aiogram.mtproto.protocol.rpc import RPCEngine
from aiogram.raw import functions as raw_funcs
from aiogram.raw import types as raw_types
from aiogram.raw.core.primitives import TLRequest
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
        logger.info(
            "[DC %d] Handshake complete auth_key_id=%016x session_id=%016x",
            self.dc_id,
            self.auth_key.key_id & 0xFFFFFFFFFFFFFFFF,
            self.session_id & 0xFFFFFFFFFFFFFFFF,
        )
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
        Cleanly stop RPC and close the TCP connection.
        """
        self.state = DCState.CLOSED
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
        key_id = f"{self.auth_key.key_id:#018x}" if self.auth_key else "None"
        return (
            f"<DCClientSession dc_id={self.dc_id} is_media={self.is_media} "
            f"state={self.state.value} auth_key_id={key_id} session_id={self.session_id:#018x}>"
        )


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

        dc_lock = self.get_dc_lock(dc_id)
        async with dc_lock:
            # 1. Check if an active, healthy, READY session exists
            existing = self._sessions.get(dc_id)
            if existing is not None:
                if existing.is_ready:
                    key_id_int = (
                        existing.auth_key.key_id & 0xFFFFFFFFFFFFFFFF if existing.auth_key else 0
                    )
                    logger.debug(
                        "[DC %d] Reusing active READY DC client (key=%016x, session=%016x)",
                        dc_id,
                        key_id_int,
                        existing.session_id & 0xFFFFFFFFFFFFFFFF,
                    )
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
            logger.info("[DC %d] state NEW -> CONNECTING (is_media=%s)", dc_id, is_media)
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

                if dc_id == self.main_dc_id and not is_media:
                    # ------------------------------------------------------------------
                    # MAIN DC FLOW
                    # ------------------------------------------------------------------
                    loaded_from_storage = False
                    if self.session_storage:
                        session_data = await self.session_storage.load()
                        if session_data.auth_key and session_data.dc_id == dc_id:
                            session.auth_key = session_data.auth_key
                            session.server_salt = session_data.server_salt
                            session.state = DCState.HANDSHAKEN
                            loaded_from_storage = True
                            logger.info(
                                "[DC %d] Loaded existing auth_key (id=%016x) from session storage",
                                dc_id,
                                session.auth_key.key_id & 0xFFFFFFFFFFFFFFFF,
                            )

                    if loaded_from_storage:
                        # Initialize RPC Engine for validation
                        session.init_rpc(self._on_update)
                        logger.info(
                            "[DC %d] Validating stored authorization with Telegram...", dc_id
                        )
                        is_valid = False
                        try:
                            await session.invoke(
                                raw_funcs.users.GetUsers(id=[raw_types.InputPeerSelf()]),
                                timeout=10.0,
                            )
                            is_valid = True
                            logger.info("[DC %d] Stored authorization is VALID", dc_id)
                        except (AuthKeyUnregistered, AuthKeyNotFound, Unauthorized) as val_err:
                            logger.warning(
                                "[DC %d] Stored auth is INVALID (%s). Rebuilding session...",
                                dc_id,
                                val_err,
                            )
                        except Exception as other_err:
                            logger.debug(
                                "[DC %d] Validation check response: %s", dc_id, other_err
                            )
                            is_valid = True

                        if is_valid:
                            session.auth_verified = True
                            session.state = DCState.READY
                            logger.info("[DC %d] state HANDSHAKEN -> AUTHORIZED -> READY", dc_id)
                            self._sessions[dc_id] = session
                            return session

                        # Invalidate stale key from session storage and rebuild fresh
                        logger.info(
                            "[DC %d] Invalidating stale AuthKey and performing fresh handshake...",
                            dc_id,
                        )
                        await session.close()
                        if self.session_storage:
                            await self.session_storage.invalidate_auth_key()

                        session = DCClientSession(
                            dc_id=dc_id,
                            is_media=False,
                            test_mode=self.test_mode,
                            transport=self.transport_factory(),
                            api_id=self.api_id,
                        )
                        await session.connect()

                    # Perform fresh DH Handshake
                    logger.info("[DC %d] Performing MTProto DH handshake...", dc_id)
                    auth_key, server_salt = await session.handshake()
                    session.auth_key = auth_key
                    session.server_salt = server_salt
                    logger.info(
                        "[DC %d] Handshake complete auth_key_id=%016x",
                        dc_id,
                        session.auth_key.key_id & 0xFFFFFFFFFFFFFFFF if session.auth_key else 0,
                    )

                    # Initialize RPC Engine
                    session.init_rpc(self._on_update)

                    # Persist raw key data
                    if self.session_storage:
                        session_data = await self.session_storage.load()
                        session_data.auth_key = session.auth_key
                        session_data.server_salt = session.server_salt
                        session_data.dc_id = dc_id
                        dc_info = get_dc(dc_id, test_mode=self.test_mode)
                        session_data.server_address = dc_info.ip_address
                        session_data.port = dc_info.port
                        await self.session_storage.save(session_data)

                    # Authenticate bot if bot_token is present
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
                                await self.session_storage.save(session_data)
                            return await self.get_dc_client(mig_err.new_dc, is_media=False)

                        session.auth_verified = True
                        user_id = getattr(getattr(res, "user", None), "id", None)
                        logger.info(
                            "[DC %d] Bot authorization successful (user_id=%s)",
                            dc_id,
                            user_id,
                        )
                        if self.session_storage:
                            session_data = await self.session_storage.load()
                            session_data.user_id = user_id
                            session_data.is_bot = True
                            await self.session_storage.save(session_data)
                    else:
                        session.auth_verified = True

                    session.state = DCState.READY
                    logger.info("[DC %d] state HANDSHAKEN -> AUTHORIZED -> READY", dc_id)
                    self._sessions[dc_id] = session
                    return session

                # ------------------------------------------------------------------
                # MEDIA DC (non-main DC) FLOW
                # ------------------------------------------------------------------
                logger.info("[DC %d] Performing Media DC DH handshake...", dc_id)
                auth_key, server_salt = await session.handshake()
                session.auth_key = auth_key
                session.server_salt = server_salt
                logger.info(
                    "[DC %d] Media DC handshake complete auth_key_id=%016x",
                    dc_id,
                    session.auth_key.key_id & 0xFFFFFFFFFFFFFFFF if session.auth_key else 0,
                )

                # Initialize RPC Engine
                session.init_rpc(None)

                # Export auth from main DC and import into media DC
                session.state = DCState.AUTHORIZING
                logger.info(
                    "[DC %d] state HANDSHAKEN -> AUTHORIZING. Exporting auth from main DC %d...",
                    dc_id,
                    self.main_dc_id,
                )

                # Obtain validated main DC client
                main_client = await self._get_main_client_unlocked()

                exported = await main_client.invoke(
                    raw_funcs.auth.ExportAuthorization(dc_id=dc_id)
                )
                auth_id = getattr(exported, "id", None)
                auth_bytes = getattr(exported, "bytes_data", getattr(exported, "bytes", None))

                if auth_id is None or auth_bytes is None:
                    msg = (
                        f"Invalid ExportedAuthorization from main DC {self.main_dc_id} "
                        f"for target DC {dc_id}"
                    )
                    raise Unauthorized(401, msg)

                logger.info(
                    "[DC %d] Importing exported authorization (id=%d, bytes=%d)...",
                    dc_id,
                    auth_id,
                    len(auth_bytes),
                )
                await session.invoke(
                    raw_funcs.auth.ImportAuthorization(id=auth_id, bytes_data=auth_bytes)
                )
                session.auth_imported = True
                session.state = DCState.READY
                logger.info("[DC %d] Authorization import successful -> READY", dc_id)
                self._sessions[dc_id] = session
                return session

            except Exception as exc:
                logger.error(
                    "[DC %d] Initialization/Authorization failed: %s. Closing connection.",
                    dc_id,
                    exc,
                )
                session.state = DCState.FAILED
                await session.close()
                self._sessions.pop(dc_id, None)
                raise

    async def _get_main_client_unlocked(self) -> DCClientSession:
        """
        Internal helper to get main client.
        """
        main_client = self._sessions.get(self.main_dc_id)
        if main_client is not None and main_client.is_ready:
            return main_client
        return await self.get_dc_client(self.main_dc_id, is_media=False)

    async def get_media_client(self, dc_id: int) -> DCClientSession:
        """
        Get or spawn an authorized MTProto client connected to a specific Data Center.
        """
        if dc_id == self.main_dc_id:
            return await self.get_dc_client(dc_id, is_media=False)
        return await self.get_dc_client(dc_id, is_media=True)

    async def invalidate_dc(self, dc_id: int) -> None:
        """
        Invalidate, close, and purge cached client state for a given DC.
        If it is the main DC, also atomically clear the persisted stale AuthKey.
        """
        dc_lock = self.get_dc_lock(dc_id)
        async with dc_lock:
            session = self._sessions.pop(dc_id, None)
            if session:
                logger.warning(
                    "[DC %d] Invalidating cached DC client (auth_key_id=%016x)",
                    dc_id,
                    session.auth_key.key_id & 0xFFFFFFFFFFFFFFFF if session.auth_key else 0,
                )
                session.invalidate()
                await session.close()
            if dc_id == self.main_dc_id and self.session_storage:
                try:
                    await self.session_storage.invalidate_auth_key()
                    logger.info("[DC %d] Persisted auth_key invalidated in session storage", dc_id)
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
        Gracefully close all active DC sessions.
        """
        self._is_closing = True
        for dc_id, session in list(self._sessions.items()):
            try:
                await session.close()
            except Exception as e:
                logger.debug("Error closing DC %d: %s", dc_id, e)
        self._sessions.clear()
