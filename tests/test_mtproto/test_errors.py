"""
Tests for MTProto error hierarchy and dynamic RPC error parser.
"""

import pytest

from aiogram.errors.mtproto import (
    BadRequest,
    FileMigrate,
    FloodWait,
    PhoneCodeInvalid,
    PhoneMigrate,
    RPCError,
    SessionPasswordNeeded,
    SlowmodeWait,
    Unauthorized,
    parse_rpc_error,
)


def test_parse_flood_wait() -> None:
    exc = parse_rpc_error(420, "FLOOD_WAIT_15")
    assert isinstance(exc, FloodWait)
    assert exc.value == 15
    assert exc.error_code == 420


def test_parse_slowmode_wait() -> None:
    exc = parse_rpc_error(420, "SLOWMODE_WAIT_60")
    assert isinstance(exc, SlowmodeWait)
    assert exc.value == 60


def test_parse_dc_migrates() -> None:
    file_err = parse_rpc_error(303, "FILE_MIGRATE_4")
    assert isinstance(file_err, FileMigrate)
    assert file_err.new_dc == 4

    phone_err = parse_rpc_error(303, "PHONE_MIGRATE_1")
    assert isinstance(phone_err, PhoneMigrate)
    assert phone_err.new_dc == 1


def test_parse_auth_errors() -> None:
    pwd_err = parse_rpc_error(401, "SESSION_PASSWORD_NEEDED")
    assert isinstance(pwd_err, SessionPasswordNeeded)

    code_err = parse_rpc_error(400, "PHONE_CODE_INVALID")
    assert isinstance(code_err, PhoneCodeInvalid)
