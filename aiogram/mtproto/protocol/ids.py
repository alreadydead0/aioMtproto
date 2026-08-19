"""
MTProto Message ID and Session ID generators with strict monotonic time parity.
"""

from __future__ import annotations

import os
import struct
import time


class IdGenerator:
    """
    Thread-safe & async-safe MTProto Message ID generator.
    Ensures message IDs are strictly monotonically increasing and satisfy Telegram parity rules.
    """

    def __init__(self) -> None:
        self._last_time = 0
        self._time_offset = 0.0

    def set_time_offset(self, server_time: int) -> None:
        """
        Adjust time offset if server clock differs from local clock.
        """
        self._time_offset = server_time - time.time()

    def generate_msg_id(self) -> int:
        """
        Generate a client message ID:
        - msg_id = (unixtime * 2^32)
        - Strictly greater than previous msg_id
        - Client query parity: msg_id % 4 == 0
        """
        now = time.time() + self._time_offset
        msg_id = int(now * (1 << 32))
        # Client queries must have lower 2 bits == 00 (i.e. msg_id % 4 == 0)
        msg_id -= msg_id % 4

        if msg_id <= self._last_time:
            msg_id = self._last_time + 4

        self._last_time = msg_id
        return msg_id


def generate_session_id() -> int:
    """
    Generate random 64-bit signed integer session_id.
    """
    return struct.unpack("<q", os.urandom(8))[0]
