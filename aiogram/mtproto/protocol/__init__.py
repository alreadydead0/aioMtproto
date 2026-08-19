"""
MTProto protocol primitives, message framing, containers, IDs, and RPC engine.
"""

from __future__ import annotations

from .ids import IdGenerator, generate_session_id
from .message import MessageCodec, MTProtoMessage
from .rpc import RPCEngine

__all__ = (
    "IdGenerator",
    "MTProtoMessage",
    "MessageCodec",
    "RPCEngine",
    "generate_session_id",
)
