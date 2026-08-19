"""
Async TCP connection manager for Telegram MTProto.
"""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Optional

from aiogram.mtproto.connection.dc import DataCenter, get_dc
from aiogram.mtproto.connection.transport import (
    AbridgedTransport,
    BaseTransport,
    IntermediateTransport,
)

if TYPE_CHECKING:
    from aiogram.mtproto.crypto.auth_key import AuthKey

logger = logging.getLogger("aiogram.mtproto.connection")


class TCPConnection:
    """
    Manages an async TCP connection to a Telegram Data Center.
    """

    def __init__(
        self,
        dc: DataCenter,
        transport: BaseTransport | None = None,
        timeout: float = 10.0,
    ) -> None:
        self.dc = dc
        self.transport: BaseTransport = transport or IntermediateTransport()
        self.timeout = timeout
        self.reader: asyncio.StreamReader | None = None
        self.writer: asyncio.StreamWriter | None = None
        self._connected = False
        self._send_lock = asyncio.Lock()

    @property
    def is_connected(self) -> bool:
        return self._connected and self.writer is not None and not self.writer.is_closing()

    async def connect(self) -> None:
        """
        Establish TCP connection and send initial transport handshake header.
        """
        if self.is_connected:
            return

        logger.debug(
            "Connecting to DC %d (%s:%d)...", self.dc.dc_id, self.dc.ip_address, self.dc.port
        )
        try:
            self.reader, self.writer = await asyncio.wait_for(
                asyncio.open_connection(self.dc.ip_address, self.dc.port),
                timeout=self.timeout,
            )
        except Exception as e:
            logger.error("Failed to connect to DC %d: %s", self.dc.dc_id, e)
            self._connected = False
            raise

        # Send transport header if required
        if self.transport.HEADER:
            assert self.writer is not None
            self.writer.write(self.transport.HEADER)
            await self.writer.drain()

        self._connected = True
        logger.debug("Connected to DC %d successfully", self.dc.dc_id)

    async def send(self, payload: bytes) -> None:
        """
        Frame and send payload over the TCP connection.
        """
        if not self.is_connected or self.writer is None:
            msg = "Connection is closed"
            raise ConnectionError(msg)

        framed = self.transport.pack(payload)
        async with self._send_lock:
            self.writer.write(framed)
            await self.writer.drain()

    async def receive(self) -> bytes:
        """
        Read the next MTProto payload from the TCP stream.
        """
        if not self.is_connected or self.reader is None:
            msg = "Connection is closed"
            raise ConnectionError(msg)

        try:
            return await self.transport.read_packet(self.reader)
        except (asyncio.IncompleteReadError, ConnectionResetError) as e:
            self._connected = False
            logger.warning("Connection closed by server on DC %d: %s", self.dc.dc_id, e)
            raise ConnectionError("Connection lost") from e

    async def close(self) -> None:
        """
        Close the connection cleanly.
        """
        self._connected = False
        if self.writer:
            try:
                self.writer.close()
                await self.writer.wait_closed()
            except Exception:
                pass
            finally:
                self.writer = None
                self.reader = None
        logger.debug("Disconnected from DC %d", self.dc.dc_id)
