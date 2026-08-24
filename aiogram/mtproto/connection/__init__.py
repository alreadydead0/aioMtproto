"""
MTProto connection components (TCP, Transports, DCs, Pool).
"""

from __future__ import annotations

from .dc import PROD_DCS, TEST_DCS, DataCenter, get_dc
from .pool import DCSessionPool, TokenBucketLimiter
from .tcp import TCPConnection
from .transport import (
    AbridgedTransport,
    BaseTransport,
    FullTransport,
    IntermediateTransport,
    PaddedIntermediateTransport,
)

__all__ = (
    "AbridgedTransport",
    "BaseTransport",
    "DCSessionPool",
    "DataCenter",
    "FullTransport",
    "IntermediateTransport",
    "PaddedIntermediateTransport",
    "PROD_DCS",
    "TEST_DCS",
    "TCPConnection",
    "TokenBucketLimiter",
    "get_dc",
)
