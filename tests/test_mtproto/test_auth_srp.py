import io
import struct

import pytest

from aiogram.mtproto.crypto.srp import compute_srp_password
from aiogram.raw import functions as raw_funcs
from aiogram.raw import types as raw_types


def test_send_code_serialization():
    # Verify auth.sendCode serializes CodeSettings with 0xAD253D78
    settings = raw_types.CodeSettings()
    req = raw_funcs.auth.SendCode(
        phone_number="+1234567890",
        api_id=12345,
        api_hash="abcdef0123456789",
        settings=settings,
    )
    serialized = req.write()

    # Must start with SendCode ID (0xA677244F)
    assert serialized[:4] == struct.pack("<I", 0xA677244F)
    # Must contain CodeSettings ID (0xAD253D78)
    assert struct.pack("<I", 0xAD253D78) in serialized


def test_srp_password_computation():
    algo = raw_types.PasswordKdfAlgoSHA256SHA256PBKDF2HMACSHA512(
        salt1=b"salt1_bytes_for_testing",
        salt2=b"salt2_bytes_for_testing",
        g=3,
        p=b"\xff" * 256,  # 256-byte prime placeholder
    )
    account_pwd = raw_types.AccountPassword(
        has_password=True,
        current_algo=algo,
        srp_B=b"\x01\x23" * 128,
        srp_id=987654321,
    )

    srp_result = compute_srp_password("secret_2fa_password", account_pwd)
    assert srp_result.srp_id == 987654321
    assert len(srp_result.A) == 256
    assert len(srp_result.M1) == 32
    # Verify write serialization
    written = srp_result.write()
    assert written[:4] == struct.pack("<I", raw_types.InputCheckPasswordSRP.ID)


def test_resend_code_and_cancel_code():
    resend = raw_funcs.auth.ResendCode(phone_number="+123456", phone_code_hash="hash123")
    assert resend.write()[:4] == struct.pack("<I", raw_funcs.auth.ResendCode.ID)

    cancel = raw_funcs.auth.CancelCode(phone_number="+123456", phone_code_hash="hash123")
    assert cancel.write()[:4] == struct.pack("<I", raw_funcs.auth.CancelCode.ID)


def test_sign_in_serialization():
    sign_in = raw_funcs.auth.SignIn(
        phone_number="+123456", phone_code_hash="hash123", phone_code="12345"
    )
    written = sign_in.write()
    assert written[:4] == struct.pack("<I", raw_funcs.auth.SignIn.ID)
    assert b"12345" in written


def test_account_get_password_constructor():
    # Verify exact official constructor ID 0x548A30F5
    assert raw_funcs.account.GetPassword.ID == 0x548A30F5
    req = raw_funcs.account.GetPassword()
    written = req.write()
    assert written == b"\xf5\x30\x8a\x54"
    assert written[:4] == struct.pack("<I", 0x548A30F5)


def test_auth_check_password_constructor():
    # Verify auth.checkPassword constructor 0xD18B4D16
    assert raw_funcs.auth.CheckPassword.ID == 0xD18B4D16
    srp = raw_types.InputCheckPasswordSRP(srp_id=123, A=b"\x01" * 256, M1=b"\x02" * 32)
    req = raw_funcs.auth.CheckPassword(password=srp)
    written = req.write()
    assert written[:4] == struct.pack("<I", 0xD18B4D16)


def test_secure_password_kdf_algo_registration():
    from aiogram.raw.all import TL_REGISTRY
    from aiogram.raw.core.primitives import write_bytes

    assert 0xBBF2DDA0 in TL_REGISTRY
    assert TL_REGISTRY[0xBBF2DDA0] == raw_types.SecurePasswordKdfAlgoPBKDF2HMACSHA512

    # Test reading SecurePasswordKdfAlgoPBKDF2HMACSHA512 with proper TL padding
    stream = io.BytesIO(write_bytes(b"salt"))
    algo = raw_types.SecurePasswordKdfAlgoPBKDF2HMACSHA512.read(stream)
    assert algo.salt == b"salt"
