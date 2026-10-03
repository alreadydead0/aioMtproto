import pytest

from aiogram.session.string import StringSession


def test_invalid_session_strings():
    # Empty string returns empty session data
    s = StringSession("")
    assert s._data.auth_key is None

    # Corrupt base64 or wrong header
    assert StringSession.is_valid("not_a_valid_session_string") is False

    with pytest.raises(ValueError):
        StringSession("totally_invalid_session_data_123")

    with pytest.raises(ValueError):
        StringSession.info("totally_invalid_session_data_123")
