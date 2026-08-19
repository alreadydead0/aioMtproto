"""
MTProto connection components (TCP, Transports, DCs, Pool).
"""

from __future__ import annotations

from .dc import DataCenter, get_dc, PROD_DCS, TEST_DCS
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
    "DataCenter",
    "FullTransport",
    "IntermediateTransport",
    "PaddedIntermediateTransport",
    "PROD_DCS",
    "TEST_DCS",
    "TCPConnection",
    "get_dc",
)
