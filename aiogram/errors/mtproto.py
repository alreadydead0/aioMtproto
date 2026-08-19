"""
MTProto exception hierarchy and RPC error parser.
"""

from __future__ import annotations

import re


class MTProtoError(Exception):
    """
    Base exception for MTProto errors.
    """


class TransportError(MTProtoError):
    """
    Error in MTProto transport framing or TCP connection.
    """


class AuthKeyNotFound(TransportError):
    """
    -404 AuthKey not found or unregistered on the Telegram server.
    """


class CryptoError(MTProtoError):
    """
    Cryptographic verification or decryption error.
    """


class RPCError(MTProtoError):
    """
    Base class for RPC error responses returned by Telegram MTProto servers.
    """

    def __init__(self, error_code: int, error_message: str) -> None:
        super().__init__(f"[{error_code}] {error_message}")
        self.error_code = error_code
        self.error_message = error_message


class BadRequest(RPCError):
    """
    400 Bad Request error.
    """


class Unauthorized(RPCError):
    """
    401 Unauthorized error.
    """


class AuthKeyUnregistered(Unauthorized):
    """
    401 AUTH_KEY_UNREGISTERED error: AuthKey is not registered in the auth system.
    """


class AuthKeyInvalid(Unauthorized):
    """
    401 AUTH_KEY_INVALID error: AuthKey is invalid.
    """


class BadMsgNotificationError(RPCError):
    """
    MTProto BadMsgNotification error.
    """


class BadServerSaltError(RPCError):
    """
    MTProto BadServerSalt error.
    """


class Forbidden(RPCError):
    """
    403 Forbidden error.
    """


class NotFound(RPCError):
    """
    404 Not Found error.
    """


class FloodWait(RPCError):
    """
    420 Flood Wait error. Indicates the client should sleep for `value` seconds.
    """

    def __init__(self, error_code: int, error_message: str, value: int) -> None:
        super().__init__(error_code, error_message)
        self.value = value


class SlowmodeWait(RPCError):
    """
    Slowmode wait error in chat.
    """

    def __init__(self, error_code: int, error_message: str, value: int) -> None:
        super().__init__(error_code, error_message)
        self.value = value


class MigrationError(RPCError):
    """
    Telegram DC migration error.
    """

    def __init__(self, error_code: int, error_message: str, new_dc: int) -> None:
        super().__init__(error_code, error_message)
        self.new_dc = new_dc
        self.dc_id = new_dc


class FileMigrate(MigrationError):
    """
    FILE_MIGRATE_X error: The file is located in a different DC.
    """


class PhoneMigrate(MigrationError):
    """
    PHONE_MIGRATE_X error: The phone number belongs to a different DC.
    """


class NetworkMigrate(MigrationError):
    """
    NETWORK_MIGRATE_X error: Network redirect to a different DC.
    """


class UserMigrate(MigrationError):
    """
    USER_MIGRATE_X error: User account belongs to a different DC.
    """


class FileReferenceExpired(BadRequest):
    """
    FILE_REFERENCE_EXPIRED (400) error: The file_reference of the media location has expired.
    """


class SessionPasswordNeeded(Unauthorized):
    """
    2FA password is required to sign in (SESSION_PASSWORD_NEEDED).
    """


class PhoneCodeInvalid(BadRequest):
    """
    PHONE_CODE_INVALID.
    """


class PhoneCodeExpired(BadRequest):
    """
    PHONE_CODE_EXPIRED.
    """


class PhoneNumberInvalid(BadRequest):
    """
    PHONE_NUMBER_INVALID.
    """


class InternalServerError(RPCError):
    """
    500 Internal Server Error.
    """


def parse_rpc_error(error_code: int, error_message: str) -> RPCError:
    """
    Parse an RPC error response from Telegram into a specialized exception.
    """
    error_message = error_message.strip()
    flood_match = re.match(r"^(?:FLOOD_WAIT_|SLOWMODE_WAIT_)(\d+)$", error_message)
    if flood_match:
        seconds = int(flood_match.group(1))
        if error_message.startswith("SLOWMODE_WAIT"):
            return SlowmodeWait(error_code, error_message, value=seconds)
        return FloodWait(error_code, error_message, value=seconds)

    file_migrate_match = re.match(r"^FILE_MIGRATE_(\d+)$", error_message)
    if file_migrate_match:
        return FileMigrate(error_code, error_message, new_dc=int(file_migrate_match.group(1)))

    phone_migrate_match = re.match(r"^PHONE_MIGRATE_(\d+)$", error_message)
    if phone_migrate_match:
        return PhoneMigrate(error_code, error_message, new_dc=int(phone_migrate_match.group(1)))

    net_migrate_match = re.match(r"^NETWORK_MIGRATE_(\d+)$", error_message)
    if net_migrate_match:
        return NetworkMigrate(error_code, error_message, new_dc=int(net_migrate_match.group(1)))

    user_migrate_match = re.match(r"^USER_MIGRATE_(\d+)$", error_message)
    if user_migrate_match:
        return UserMigrate(error_code, error_message, new_dc=int(user_migrate_match.group(1)))

    if error_message == "FILE_REFERENCE_EXPIRED":
        return FileReferenceExpired(error_code, error_message)
    if error_message == "SESSION_PASSWORD_NEEDED":
        return SessionPasswordNeeded(error_code, error_message)
    if error_message == "AUTH_KEY_UNREGISTERED":
        return AuthKeyUnregistered(error_code, error_message)
    if error_message == "AUTH_KEY_INVALID":
        return AuthKeyInvalid(error_code, error_message)
    if error_message == "PHONE_CODE_INVALID":
        return PhoneCodeInvalid(error_code, error_message)
    if error_message == "PHONE_CODE_EXPIRED":
        return PhoneCodeExpired(error_code, error_message)
    if error_message == "PHONE_NUMBER_INVALID":
        return PhoneNumberInvalid(error_code, error_message)

    if error_code == 400:
        return BadRequest(error_code, error_message)
    if error_code == 401:
        return Unauthorized(error_code, error_message)
    if error_code == 403:
        return Forbidden(error_code, error_message)
    if error_code == 404:
        return NotFound(error_code, error_message)
    if error_code == 500:
        return InternalServerError(error_code, error_message)

    return RPCError(error_code, error_message)
