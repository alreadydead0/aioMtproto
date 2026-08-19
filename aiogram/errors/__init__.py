"""
aiogram MTProto and API error classes.
"""

from __future__ import annotations

from .mtproto import (
    BadRequest,
    CryptoError,
    FileMigrate,
    FloodWait,
    Forbidden,
    InternalServerError,
    MigrationError,
    MTProtoError,
    NetworkMigrate,
    NotFound,
    PhoneCodeExpired,
    PhoneCodeInvalid,
    PhoneMigrate,
    PhoneNumberInvalid,
    RPCError,
    SessionPasswordNeeded,
    SlowmodeWait,
    TransportError,
    Unauthorized,
    UserMigrate,
    parse_rpc_error,
)

__all__ = (
    "BadRequest",
    "CryptoError",
    "FileMigrate",
    "FloodWait",
    "Forbidden",
    "InternalServerError",
    "MTProtoError",
    "MigrationError",
    "NetworkMigrate",
    "NotFound",
    "PhoneCodeExpired",
    "PhoneCodeInvalid",
    "PhoneMigrate",
    "PhoneNumberInvalid",
    "RPCError",
    "SessionPasswordNeeded",
    "SlowmodeWait",
    "TransportError",
    "Unauthorized",
    "UserMigrate",
    "parse_rpc_error",
)
