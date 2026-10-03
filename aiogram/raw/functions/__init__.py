"""
Official Telegram TL RPC Functions for MTProto (Layer 229).
"""

from __future__ import annotations

import struct
from typing import Any, BinaryIO, Optional

from aiogram.raw.core.primitives import (
    TLObject,
    TLRequest,
    read_bool,
    read_bytes,
    read_double,
    read_int,
    read_int128,
    read_int256,
    read_long,
    read_string,
    read_uint,
    read_vector,
    write_bool,
    write_bytes,
    write_double,
    write_int,
    write_int128,
    write_int256,
    write_long,
    write_string,
    write_uint,
    write_vector,
)
from aiogram.raw.types import *

class AccountAcceptAuthorization(TLRequest[Any]):
    ID = 0XF3ED4C73
    QUALNAME = "functions.account.acceptAuthorization"

    def __init__(self, bot_id: Any = None, scope: Any = None, public_key: Any = None, value_hashes: Any = None, credentials: Any = None) -> None:
        self.bot_id = bot_id
        self.scope = scope
        self.public_key = public_key
        self.value_hashes = value_hashes
        self.credentials = credentials

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.bot_id)
        res += write_string(self.scope)
        res += write_string(self.public_key)
        res += write_vector(self.value_hashes, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        res += (self.credentials.write() if hasattr(self.credentials, 'write') else write_bytes(self.credentials))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountCancelPasswordEmail(TLRequest[Any]):
    ID = 0XC1CBD5B6
    QUALNAME = "functions.account.cancelPasswordEmail"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountChangeAuthorizationSettings(TLRequest[Any]):
    ID = 0X40F48462
    QUALNAME = "functions.account.changeAuthorizationSettings"

    def __init__(self, confirmed: Any = None, hash: Any = None, encrypted_requests_disabled: Any = None, call_requests_disabled: Any = None) -> None:
        self.confirmed = confirmed
        self.hash = hash
        self.encrypted_requests_disabled = encrypted_requests_disabled
        self.call_requests_disabled = call_requests_disabled

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'confirmed', None):
            flags |= (1 << 3)
        if getattr(self, 'encrypted_requests_disabled', None) is not None and getattr(self, 'encrypted_requests_disabled', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'call_requests_disabled', None) is not None and getattr(self, 'call_requests_disabled', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_long(self.hash)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'encrypted_requests_disabled', None)
            if v is not None:
                res += write_bool(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'call_requests_disabled', None)
            if v is not None:
                res += write_bool(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountChangePhone(TLRequest[Any]):
    ID = 0X70C32EDB
    QUALNAME = "functions.account.changePhone"

    def __init__(self, phone_number: Any = None, phone_code_hash: Any = None, phone_code: Any = None) -> None:
        self.phone_number = phone_number
        self.phone_code_hash = phone_code_hash
        self.phone_code = phone_code

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.phone_number)
        res += write_string(self.phone_code_hash)
        res += write_string(self.phone_code)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountCheckUsername(TLRequest[Any]):
    ID = 0X2714D86C
    QUALNAME = "functions.account.checkUsername"

    def __init__(self, username: Any = None) -> None:
        self.username = username

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.username)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountClearRecentEmojiStatuses(TLRequest[Any]):
    ID = 0X18201AAE
    QUALNAME = "functions.account.clearRecentEmojiStatuses"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountConfirmBotConnection(TLRequest[Any]):
    ID = 0X67ED1F68
    QUALNAME = "functions.account.confirmBotConnection"

    def __init__(self, bot_id: Any = None) -> None:
        self.bot_id = bot_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.bot_id.write() if hasattr(self.bot_id, 'write') else write_bytes(self.bot_id))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountConfirmPasswordEmail(TLRequest[Any]):
    ID = 0X8FDF1920
    QUALNAME = "functions.account.confirmPasswordEmail"

    def __init__(self, code: Any = None) -> None:
        self.code = code

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.code)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountConfirmPhone(TLRequest[Any]):
    ID = 0X5F2178C3
    QUALNAME = "functions.account.confirmPhone"

    def __init__(self, phone_code_hash: Any = None, phone_code: Any = None) -> None:
        self.phone_code_hash = phone_code_hash
        self.phone_code = phone_code

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.phone_code_hash)
        res += write_string(self.phone_code)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountCreateBusinessChatLink(TLRequest[Any]):
    ID = 0X8851E68E
    QUALNAME = "functions.account.createBusinessChatLink"

    def __init__(self, link: Any = None) -> None:
        self.link = link

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.link.write() if hasattr(self.link, 'write') else write_bytes(self.link))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountCreateTheme(TLRequest[Any]):
    ID = 0X652E4400
    QUALNAME = "functions.account.createTheme"

    def __init__(self, slug: Any = None, title: Any = None, document: Any = None, settings: Any = None) -> None:
        self.slug = slug
        self.title = title
        self.document = document
        self.settings = settings

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'document', None) is not None and getattr(self, 'document', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'settings', None) is not None and getattr(self, 'settings', None) is not False:
            flags |= (1 << 3)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_string(self.slug)
        res += write_string(self.title)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'document', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 3)):
            v = getattr(self, 'settings', None) or []
            if v is not None:
                res += write_vector(v, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountDeclinePasswordReset(TLRequest[Any]):
    ID = 0X4C9409F6
    QUALNAME = "functions.account.declinePasswordReset"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountDeleteAccount(TLRequest[Any]):
    ID = 0XA2C0CF74
    QUALNAME = "functions.account.deleteAccount"

    def __init__(self, reason: Any = None, password: Any = None) -> None:
        self.reason = reason
        self.password = password

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'password', None) is not None and getattr(self, 'password', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_string(self.reason)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'password', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountDeleteAutoSaveExceptions(TLRequest[Any]):
    ID = 0X53BC0020
    QUALNAME = "functions.account.deleteAutoSaveExceptions"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountDeleteBusinessChatLink(TLRequest[Any]):
    ID = 0X60073674
    QUALNAME = "functions.account.deleteBusinessChatLink"

    def __init__(self, slug: Any = None) -> None:
        self.slug = slug

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.slug)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountDeletePasskey(TLRequest[Any]):
    ID = 0XF5B5563F
    QUALNAME = "functions.account.deletePasskey"

    def __init__(self, id: Any = None) -> None:
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountDeleteSecureValue(TLRequest[Any]):
    ID = 0XB880BC4B
    QUALNAME = "functions.account.deleteSecureValue"

    def __init__(self, types: Any = None) -> None:
        self.types = types

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_vector(self.types, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountDeleteWebBrowserSettingsExceptions(TLRequest[Any]):
    ID = 0X86A0765D
    QUALNAME = "functions.account.deleteWebBrowserSettingsExceptions"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountDisablePeerConnectedBot(TLRequest[Any]):
    ID = 0X5E437ED9
    QUALNAME = "functions.account.disablePeerConnectedBot"

    def __init__(self, peer: Any = None) -> None:
        self.peer = peer

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountEditBusinessChatLink(TLRequest[Any]):
    ID = 0X8C3410AF
    QUALNAME = "functions.account.editBusinessChatLink"

    def __init__(self, slug: Any = None, link: Any = None) -> None:
        self.slug = slug
        self.link = link

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.slug)
        res += (self.link.write() if hasattr(self.link, 'write') else write_bytes(self.link))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountFinishTakeoutSession(TLRequest[Any]):
    ID = 0X1D2652EE
    QUALNAME = "functions.account.finishTakeoutSession"

    def __init__(self, success: Any = None) -> None:
        self.success = success

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'success', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountGetAccountTtl(TLRequest[Any]):
    ID = 0X8FC711D
    QUALNAME = "functions.account.getAccountTTL"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetAllSecureValues(TLRequest[Any]):
    ID = 0XB288BC7D
    QUALNAME = "functions.account.getAllSecureValues"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetAuthorizationForm(TLRequest[Any]):
    ID = 0XA929597A
    QUALNAME = "functions.account.getAuthorizationForm"

    def __init__(self, bot_id: Any = None, scope: Any = None, public_key: Any = None) -> None:
        self.bot_id = bot_id
        self.scope = scope
        self.public_key = public_key

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.bot_id)
        res += write_string(self.scope)
        res += write_string(self.public_key)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetAuthorizations(TLRequest[Any]):
    ID = 0XE320C158
    QUALNAME = "functions.account.getAuthorizations"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetAutoDownloadSettings(TLRequest[Any]):
    ID = 0X56DA0B3F
    QUALNAME = "functions.account.getAutoDownloadSettings"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetAutoSaveSettings(TLRequest[Any]):
    ID = 0XADCBBCDA
    QUALNAME = "functions.account.getAutoSaveSettings"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetBotBusinessConnection(TLRequest[Any]):
    ID = 0X76A86270
    QUALNAME = "functions.account.getBotBusinessConnection"

    def __init__(self, connection_id: Any = None) -> None:
        self.connection_id = connection_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.connection_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetBusinessChatLinks(TLRequest[Any]):
    ID = 0X6F70DDE1
    QUALNAME = "functions.account.getBusinessChatLinks"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetChannelDefaultEmojiStatuses(TLRequest[Any]):
    ID = 0X7727A7D5
    QUALNAME = "functions.account.getChannelDefaultEmojiStatuses"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetChannelRestrictedStatusEmojis(TLRequest[Any]):
    ID = 0X35A9E0D5
    QUALNAME = "functions.account.getChannelRestrictedStatusEmojis"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetChatThemes(TLRequest[Any]):
    ID = 0XD638DE89
    QUALNAME = "functions.account.getChatThemes"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetCollectibleEmojiStatuses(TLRequest[Any]):
    ID = 0X2E7B4543
    QUALNAME = "functions.account.getCollectibleEmojiStatuses"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetConnectedBots(TLRequest[Any]):
    ID = 0X4EA4C80F
    QUALNAME = "functions.account.getConnectedBots"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetContactSignUpNotification(TLRequest[Any]):
    ID = 0X9F07C728
    QUALNAME = "functions.account.getContactSignUpNotification"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountGetContentSettings(TLRequest[Any]):
    ID = 0X8B9B4DAE
    QUALNAME = "functions.account.getContentSettings"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetDefaultBackgroundEmojis(TLRequest[Any]):
    ID = 0XA60AB9CE
    QUALNAME = "functions.account.getDefaultBackgroundEmojis"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetDefaultEmojiStatuses(TLRequest[Any]):
    ID = 0XD6753386
    QUALNAME = "functions.account.getDefaultEmojiStatuses"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetDefaultGroupPhotoEmojis(TLRequest[Any]):
    ID = 0X915860AE
    QUALNAME = "functions.account.getDefaultGroupPhotoEmojis"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetDefaultProfilePhotoEmojis(TLRequest[Any]):
    ID = 0XE2750328
    QUALNAME = "functions.account.getDefaultProfilePhotoEmojis"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetGlobalPrivacySettings(TLRequest[Any]):
    ID = 0XEB2B4CF6
    QUALNAME = "functions.account.getGlobalPrivacySettings"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetMultiWallPapers(TLRequest[Any]):
    ID = 0X65AD71DC
    QUALNAME = "functions.account.getMultiWallPapers"

    def __init__(self, wallpapers: Any = None) -> None:
        self.wallpapers = wallpapers

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_vector(self.wallpapers, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetNotifyExceptions(TLRequest[Any]):
    ID = 0X53577479
    QUALNAME = "functions.account.getNotifyExceptions"

    def __init__(self, compare_sound: Any = None, compare_stories: Any = None, peer: Any = None) -> None:
        self.compare_sound = compare_sound
        self.compare_stories = compare_stories
        self.peer = peer

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'compare_sound', None):
            flags |= (1 << 1)
        if getattr(self, 'compare_stories', None):
            flags |= (1 << 2)
        if getattr(self, 'peer', None) is not None and getattr(self, 'peer', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'peer', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetNotifySettings(TLRequest[Any]):
    ID = 0X12B3AD31
    QUALNAME = "functions.account.getNotifySettings"

    def __init__(self, peer: Any = None) -> None:
        self.peer = peer

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetPaidMessagesRevenue(TLRequest[Any]):
    ID = 0X19BA4A67
    QUALNAME = "functions.account.getPaidMessagesRevenue"

    def __init__(self, parent_peer: Any = None, user_id: Any = None) -> None:
        self.parent_peer = parent_peer
        self.user_id = user_id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'parent_peer', None) is not None and getattr(self, 'parent_peer', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'parent_peer', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += (self.user_id.write() if hasattr(self.user_id, 'write') else write_bytes(self.user_id))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetPasskeys(TLRequest[Any]):
    ID = 0XEA1F0C52
    QUALNAME = "functions.account.getPasskeys"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetPassword(TLRequest[Any]):
    ID = 0X548A30F5
    QUALNAME = "functions.account.getPassword"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetPasswordSettings(TLRequest[Any]):
    ID = 0X9CD4EAF9
    QUALNAME = "functions.account.getPasswordSettings"

    def __init__(self, password: Any = None) -> None:
        self.password = password

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.password.write() if hasattr(self.password, 'write') else write_bytes(self.password))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetPrivacy(TLRequest[Any]):
    ID = 0XDADBC950
    QUALNAME = "functions.account.getPrivacy"

    def __init__(self, key: Any = None) -> None:
        self.key = key

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.key.write() if hasattr(self.key, 'write') else write_bytes(self.key))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetReactionsNotifySettings(TLRequest[Any]):
    ID = 0X6DD654C
    QUALNAME = "functions.account.getReactionsNotifySettings"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetRecentEmojiStatuses(TLRequest[Any]):
    ID = 0XF578105
    QUALNAME = "functions.account.getRecentEmojiStatuses"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetSavedMusicIds(TLRequest[Any]):
    ID = 0XE09D5FAF
    QUALNAME = "functions.account.getSavedMusicIds"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetSavedRingtones(TLRequest[Any]):
    ID = 0XE1902288
    QUALNAME = "functions.account.getSavedRingtones"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetSecureValue(TLRequest[Any]):
    ID = 0X73665BC2
    QUALNAME = "functions.account.getSecureValue"

    def __init__(self, types: Any = None) -> None:
        self.types = types

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_vector(self.types, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetTheme(TLRequest[Any]):
    ID = 0X3A5869EC
    QUALNAME = "functions.account.getTheme"

    def __init__(self, format: Any = None, theme: Any = None) -> None:
        self.format = format
        self.theme = theme

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.format)
        res += (self.theme.write() if hasattr(self.theme, 'write') else write_bytes(self.theme))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetThemes(TLRequest[Any]):
    ID = 0X7206E458
    QUALNAME = "functions.account.getThemes"

    def __init__(self, format: Any = None, hash: Any = None) -> None:
        self.format = format
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.format)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetTmpPassword(TLRequest[Any]):
    ID = 0X449E0B51
    QUALNAME = "functions.account.getTmpPassword"

    def __init__(self, password: Any = None, period: Any = None) -> None:
        self.password = password
        self.period = period

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.password.write() if hasattr(self.password, 'write') else write_bytes(self.password))
        res += write_int(self.period)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetUniqueGiftChatThemes(TLRequest[Any]):
    ID = 0XE42CE9C9
    QUALNAME = "functions.account.getUniqueGiftChatThemes"

    def __init__(self, offset: Any = None, limit: Any = None, hash: Any = None) -> None:
        self.offset = offset
        self.limit = limit
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.offset)
        res += write_int(self.limit)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetWallPaper(TLRequest[Any]):
    ID = 0XFC8DDBEA
    QUALNAME = "functions.account.getWallPaper"

    def __init__(self, wallpaper: Any = None) -> None:
        self.wallpaper = wallpaper

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.wallpaper.write() if hasattr(self.wallpaper, 'write') else write_bytes(self.wallpaper))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetWallPapers(TLRequest[Any]):
    ID = 0X7967D36
    QUALNAME = "functions.account.getWallPapers"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetWebAuthorizations(TLRequest[Any]):
    ID = 0X182E6D6F
    QUALNAME = "functions.account.getWebAuthorizations"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountGetWebBrowserSettings(TLRequest[Any]):
    ID = 0X56655768
    QUALNAME = "functions.account.getWebBrowserSettings"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountInitPasskeyRegistration(TLRequest[Any]):
    ID = 0X429547E8
    QUALNAME = "functions.account.initPasskeyRegistration"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountInitTakeoutSession(TLRequest[Any]):
    ID = 0X8EF3EAB0
    QUALNAME = "functions.account.initTakeoutSession"

    def __init__(self, contacts: Any = None, message_users: Any = None, message_chats: Any = None, message_megagroups: Any = None, message_channels: Any = None, files: Any = None, file_max_size: Any = None) -> None:
        self.contacts = contacts
        self.message_users = message_users
        self.message_chats = message_chats
        self.message_megagroups = message_megagroups
        self.message_channels = message_channels
        self.files = files
        self.file_max_size = file_max_size

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'contacts', None):
            flags |= (1 << 0)
        if getattr(self, 'message_users', None):
            flags |= (1 << 1)
        if getattr(self, 'message_chats', None):
            flags |= (1 << 2)
        if getattr(self, 'message_megagroups', None):
            flags |= (1 << 3)
        if getattr(self, 'message_channels', None):
            flags |= (1 << 4)
        if getattr(self, 'files', None):
            flags |= (1 << 5)
        if getattr(self, 'file_max_size', None) is not None and getattr(self, 'file_max_size', None) is not False:
            flags |= (1 << 5)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 5)):
            v = getattr(self, 'file_max_size', None) or 0
            if v is not None:
                res += write_long(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountInstallTheme(TLRequest[Any]):
    ID = 0XC727BB3B
    QUALNAME = "functions.account.installTheme"

    def __init__(self, dark: Any = None, theme: Any = None, format: Any = None, base_theme: Any = None) -> None:
        self.dark = dark
        self.theme = theme
        self.format = format
        self.base_theme = base_theme

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'dark', None):
            flags |= (1 << 0)
        if getattr(self, 'theme', None) is not None and getattr(self, 'theme', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'format', None) is not None and getattr(self, 'format', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'base_theme', None) is not None and getattr(self, 'base_theme', None) is not False:
            flags |= (1 << 3)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'theme', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 2)):
            v = getattr(self, 'format', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 3)):
            v = getattr(self, 'base_theme', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountInstallWallPaper(TLRequest[Any]):
    ID = 0XFEED5769
    QUALNAME = "functions.account.installWallPaper"

    def __init__(self, wallpaper: Any = None, settings: Any = None) -> None:
        self.wallpaper = wallpaper
        self.settings = settings

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.wallpaper.write() if hasattr(self.wallpaper, 'write') else write_bytes(self.wallpaper))
        res += (self.settings.write() if hasattr(self.settings, 'write') else write_bytes(self.settings))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountInvalidateSignInCodes(TLRequest[Any]):
    ID = 0XCA8AE8BA
    QUALNAME = "functions.account.invalidateSignInCodes"

    def __init__(self, codes: Any = None) -> None:
        self.codes = codes

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_vector(self.codes, write_string)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountRegisterDevice(TLRequest[Any]):
    ID = 0XEC86017A
    QUALNAME = "functions.account.registerDevice"

    def __init__(self, no_muted: Any = None, token_type: Any = None, token: Any = None, app_sandbox: Any = None, secret: Any = None, other_uids: Any = None) -> None:
        self.no_muted = no_muted
        self.token_type = token_type
        self.token = token
        self.app_sandbox = app_sandbox
        self.secret = secret
        self.other_uids = other_uids

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'no_muted', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_int(self.token_type)
        res += write_string(self.token)
        res += write_bool(self.app_sandbox)
        res += write_bytes(self.secret)
        res += write_vector(self.other_uids, write_long)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountRegisterPasskey(TLRequest[Any]):
    ID = 0X55B41FD6
    QUALNAME = "functions.account.registerPasskey"

    def __init__(self, credential: Any = None) -> None:
        self.credential = credential

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.credential.write() if hasattr(self.credential, 'write') else write_bytes(self.credential))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountReorderUsernames(TLRequest[Any]):
    ID = 0XEF500EAB
    QUALNAME = "functions.account.reorderUsernames"

    def __init__(self, order: Any = None) -> None:
        self.order = order

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_vector(self.order, write_string)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountReportPeer(TLRequest[Any]):
    ID = 0XC5BA3D86
    QUALNAME = "functions.account.reportPeer"

    def __init__(self, peer: Any = None, reason: Any = None, message: Any = None) -> None:
        self.peer = peer
        self.reason = reason
        self.message = message

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += (self.reason.write() if hasattr(self.reason, 'write') else write_bytes(self.reason))
        res += write_string(self.message)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountReportProfilePhoto(TLRequest[Any]):
    ID = 0XFA8CC6F5
    QUALNAME = "functions.account.reportProfilePhoto"

    def __init__(self, peer: Any = None, photo_id: Any = None, reason: Any = None, message: Any = None) -> None:
        self.peer = peer
        self.photo_id = photo_id
        self.reason = reason
        self.message = message

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += (self.photo_id.write() if hasattr(self.photo_id, 'write') else write_bytes(self.photo_id))
        res += (self.reason.write() if hasattr(self.reason, 'write') else write_bytes(self.reason))
        res += write_string(self.message)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountResendPasswordEmail(TLRequest[Any]):
    ID = 0X7A7F2A15
    QUALNAME = "functions.account.resendPasswordEmail"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountResetAuthorization(TLRequest[Any]):
    ID = 0XDF77F3BC
    QUALNAME = "functions.account.resetAuthorization"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountResetNotifySettings(TLRequest[Any]):
    ID = 0XDB7E1747
    QUALNAME = "functions.account.resetNotifySettings"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountResetPassword(TLRequest[Any]):
    ID = 0X9308CE1B
    QUALNAME = "functions.account.resetPassword"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountResetWallPapers(TLRequest[Any]):
    ID = 0XBB3B9804
    QUALNAME = "functions.account.resetWallPapers"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountResetWebAuthorization(TLRequest[Any]):
    ID = 0X2D01B9EF
    QUALNAME = "functions.account.resetWebAuthorization"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountResetWebAuthorizations(TLRequest[Any]):
    ID = 0X682D2594
    QUALNAME = "functions.account.resetWebAuthorizations"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountResolveBusinessChatLink(TLRequest[Any]):
    ID = 0X5492E5EE
    QUALNAME = "functions.account.resolveBusinessChatLink"

    def __init__(self, slug: Any = None) -> None:
        self.slug = slug

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.slug)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountSaveAutoDownloadSettings(TLRequest[Any]):
    ID = 0X76F36233
    QUALNAME = "functions.account.saveAutoDownloadSettings"

    def __init__(self, low: Any = None, high: Any = None, settings: Any = None) -> None:
        self.low = low
        self.high = high
        self.settings = settings

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'low', None):
            flags |= (1 << 0)
        if getattr(self, 'high', None):
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.settings.write() if hasattr(self.settings, 'write') else write_bytes(self.settings))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountSaveAutoSaveSettings(TLRequest[Any]):
    ID = 0XD69B8361
    QUALNAME = "functions.account.saveAutoSaveSettings"

    def __init__(self, users: Any = None, chats: Any = None, broadcasts: Any = None, peer: Any = None, settings: Any = None) -> None:
        self.users = users
        self.chats = chats
        self.broadcasts = broadcasts
        self.peer = peer
        self.settings = settings

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'users', None):
            flags |= (1 << 0)
        if getattr(self, 'chats', None):
            flags |= (1 << 1)
        if getattr(self, 'broadcasts', None):
            flags |= (1 << 2)
        if getattr(self, 'peer', None) is not None and getattr(self, 'peer', None) is not False:
            flags |= (1 << 3)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 3)):
            v = getattr(self, 'peer', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += (self.settings.write() if hasattr(self.settings, 'write') else write_bytes(self.settings))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountSaveMusic(TLRequest[Any]):
    ID = 0XB26732A9
    QUALNAME = "functions.account.saveMusic"

    def __init__(self, unsave: Any = None, id: Any = None, after_id: Any = None) -> None:
        self.unsave = unsave
        self.id = id
        self.after_id = after_id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'unsave', None):
            flags |= (1 << 0)
        if getattr(self, 'after_id', None) is not None and getattr(self, 'after_id', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.id.write() if hasattr(self.id, 'write') else write_bytes(self.id))
        if bool(flags & (1 << 1)):
            v = getattr(self, 'after_id', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountSaveRingtone(TLRequest[Any]):
    ID = 0X3DEA5B03
    QUALNAME = "functions.account.saveRingtone"

    def __init__(self, id: Any = None, unsave: Any = None) -> None:
        self.id = id
        self.unsave = unsave

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.id.write() if hasattr(self.id, 'write') else write_bytes(self.id))
        res += write_bool(self.unsave)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountSaveSecureValue(TLRequest[Any]):
    ID = 0X899FE31D
    QUALNAME = "functions.account.saveSecureValue"

    def __init__(self, value: Any = None, secure_secret_id: Any = None) -> None:
        self.value = value
        self.secure_secret_id = secure_secret_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.value.write() if hasattr(self.value, 'write') else write_bytes(self.value))
        res += write_long(self.secure_secret_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountSaveTheme(TLRequest[Any]):
    ID = 0XF257106C
    QUALNAME = "functions.account.saveTheme"

    def __init__(self, theme: Any = None, unsave: Any = None) -> None:
        self.theme = theme
        self.unsave = unsave

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.theme.write() if hasattr(self.theme, 'write') else write_bytes(self.theme))
        res += write_bool(self.unsave)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountSaveWallPaper(TLRequest[Any]):
    ID = 0X6C5A5B37
    QUALNAME = "functions.account.saveWallPaper"

    def __init__(self, wallpaper: Any = None, unsave: Any = None, settings: Any = None) -> None:
        self.wallpaper = wallpaper
        self.unsave = unsave
        self.settings = settings

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.wallpaper.write() if hasattr(self.wallpaper, 'write') else write_bytes(self.wallpaper))
        res += write_bool(self.unsave)
        res += (self.settings.write() if hasattr(self.settings, 'write') else write_bytes(self.settings))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountSendChangePhoneCode(TLRequest[Any]):
    ID = 0X82574AE5
    QUALNAME = "functions.account.sendChangePhoneCode"

    def __init__(self, phone_number: Any = None, settings: Any = None) -> None:
        self.phone_number = phone_number
        self.settings = settings

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.phone_number)
        res += (self.settings.write() if hasattr(self.settings, 'write') else write_bytes(self.settings))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountSendConfirmPhoneCode(TLRequest[Any]):
    ID = 0X1B3FAA88
    QUALNAME = "functions.account.sendConfirmPhoneCode"

    def __init__(self, hash: Any = None, settings: Any = None) -> None:
        self.hash = hash
        self.settings = settings

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.hash)
        res += (self.settings.write() if hasattr(self.settings, 'write') else write_bytes(self.settings))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountSendVerifyEmailCode(TLRequest[Any]):
    ID = 0X98E037BB
    QUALNAME = "functions.account.sendVerifyEmailCode"

    def __init__(self, purpose: Any = None, email: Any = None) -> None:
        self.purpose = purpose
        self.email = email

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.purpose.write() if hasattr(self.purpose, 'write') else write_bytes(self.purpose))
        res += write_string(self.email)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountSendVerifyPhoneCode(TLRequest[Any]):
    ID = 0XA5A356F9
    QUALNAME = "functions.account.sendVerifyPhoneCode"

    def __init__(self, phone_number: Any = None, settings: Any = None) -> None:
        self.phone_number = phone_number
        self.settings = settings

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.phone_number)
        res += (self.settings.write() if hasattr(self.settings, 'write') else write_bytes(self.settings))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountSetAccountTtl(TLRequest[Any]):
    ID = 0X2442485E
    QUALNAME = "functions.account.setAccountTTL"

    def __init__(self, ttl: Any = None) -> None:
        self.ttl = ttl

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.ttl.write() if hasattr(self.ttl, 'write') else write_bytes(self.ttl))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountSetAuthorizationTtl(TLRequest[Any]):
    ID = 0XBF899AA0
    QUALNAME = "functions.account.setAuthorizationTTL"

    def __init__(self, authorization_ttl_days: Any = None) -> None:
        self.authorization_ttl_days = authorization_ttl_days

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.authorization_ttl_days)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountSetContactSignUpNotification(TLRequest[Any]):
    ID = 0XCFF43F61
    QUALNAME = "functions.account.setContactSignUpNotification"

    def __init__(self, silent: Any = None) -> None:
        self.silent = silent

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_bool(self.silent)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountSetContentSettings(TLRequest[Any]):
    ID = 0XB574B16B
    QUALNAME = "functions.account.setContentSettings"

    def __init__(self, sensitive_enabled: Any = None) -> None:
        self.sensitive_enabled = sensitive_enabled

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'sensitive_enabled', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountSetGlobalPrivacySettings(TLRequest[Any]):
    ID = 0X1EDAAAC2
    QUALNAME = "functions.account.setGlobalPrivacySettings"

    def __init__(self, settings: Any = None) -> None:
        self.settings = settings

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.settings.write() if hasattr(self.settings, 'write') else write_bytes(self.settings))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountSetMainProfileTab(TLRequest[Any]):
    ID = 0X5DEE78B0
    QUALNAME = "functions.account.setMainProfileTab"

    def __init__(self, tab: Any = None) -> None:
        self.tab = tab

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.tab.write() if hasattr(self.tab, 'write') else write_bytes(self.tab))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountSetPrivacy(TLRequest[Any]):
    ID = 0XC9F81CE8
    QUALNAME = "functions.account.setPrivacy"

    def __init__(self, key: Any = None, rules: Any = None) -> None:
        self.key = key
        self.rules = rules

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.key.write() if hasattr(self.key, 'write') else write_bytes(self.key))
        res += write_vector(self.rules, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountSetReactionsNotifySettings(TLRequest[Any]):
    ID = 0X316CE548
    QUALNAME = "functions.account.setReactionsNotifySettings"

    def __init__(self, settings: Any = None) -> None:
        self.settings = settings

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.settings.write() if hasattr(self.settings, 'write') else write_bytes(self.settings))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountToggleConnectedBotPaused(TLRequest[Any]):
    ID = 0X646E1097
    QUALNAME = "functions.account.toggleConnectedBotPaused"

    def __init__(self, peer: Any = None, paused: Any = None) -> None:
        self.peer = peer
        self.paused = paused

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_bool(self.paused)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountToggleNoPaidMessagesException(TLRequest[Any]):
    ID = 0XFE2EDA76
    QUALNAME = "functions.account.toggleNoPaidMessagesException"

    def __init__(self, refund_charged: Any = None, require_payment: Any = None, parent_peer: Any = None, user_id: Any = None) -> None:
        self.refund_charged = refund_charged
        self.require_payment = require_payment
        self.parent_peer = parent_peer
        self.user_id = user_id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'refund_charged', None):
            flags |= (1 << 0)
        if getattr(self, 'require_payment', None):
            flags |= (1 << 2)
        if getattr(self, 'parent_peer', None) is not None and getattr(self, 'parent_peer', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'parent_peer', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += (self.user_id.write() if hasattr(self.user_id, 'write') else write_bytes(self.user_id))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountToggleSponsoredMessages(TLRequest[Any]):
    ID = 0XB9D9A38D
    QUALNAME = "functions.account.toggleSponsoredMessages"

    def __init__(self, enabled: Any = None) -> None:
        self.enabled = enabled

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_bool(self.enabled)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountToggleUsername(TLRequest[Any]):
    ID = 0X58D6B376
    QUALNAME = "functions.account.toggleUsername"

    def __init__(self, username: Any = None, active: Any = None) -> None:
        self.username = username
        self.active = active

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.username)
        res += write_bool(self.active)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountToggleWebBrowserSettingsException(TLRequest[Any]):
    ID = 0X60ED4229
    QUALNAME = "functions.account.toggleWebBrowserSettingsException"

    def __init__(self, delete: Any = None, open_external_browser: Any = None, url: Any = None) -> None:
        self.delete = delete
        self.open_external_browser = open_external_browser
        self.url = url

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'delete', None):
            flags |= (1 << 1)
        if getattr(self, 'open_external_browser', None) is not None and getattr(self, 'open_external_browser', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'open_external_browser', None)
            if v is not None:
                res += write_bool(v)
        res += write_string(self.url)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountUnregisterDevice(TLRequest[Any]):
    ID = 0X6A0D3206
    QUALNAME = "functions.account.unregisterDevice"

    def __init__(self, token_type: Any = None, token: Any = None, other_uids: Any = None) -> None:
        self.token_type = token_type
        self.token = token
        self.other_uids = other_uids

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.token_type)
        res += write_string(self.token)
        res += write_vector(self.other_uids, write_long)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountUpdateBirthday(TLRequest[Any]):
    ID = 0XCC6E0C11
    QUALNAME = "functions.account.updateBirthday"

    def __init__(self, birthday: Any = None) -> None:
        self.birthday = birthday

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'birthday', None) is not None and getattr(self, 'birthday', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'birthday', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountUpdateBusinessAwayMessage(TLRequest[Any]):
    ID = 0XA26A7FA5
    QUALNAME = "functions.account.updateBusinessAwayMessage"

    def __init__(self, message: Any = None) -> None:
        self.message = message

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'message', None) is not None and getattr(self, 'message', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'message', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountUpdateBusinessGreetingMessage(TLRequest[Any]):
    ID = 0X66CDAFC4
    QUALNAME = "functions.account.updateBusinessGreetingMessage"

    def __init__(self, message: Any = None) -> None:
        self.message = message

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'message', None) is not None and getattr(self, 'message', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'message', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountUpdateBusinessIntro(TLRequest[Any]):
    ID = 0XA614D034
    QUALNAME = "functions.account.updateBusinessIntro"

    def __init__(self, intro: Any = None) -> None:
        self.intro = intro

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'intro', None) is not None and getattr(self, 'intro', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'intro', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountUpdateBusinessLocation(TLRequest[Any]):
    ID = 0X9E6B131A
    QUALNAME = "functions.account.updateBusinessLocation"

    def __init__(self, geo_point: Any = None, address: Any = None) -> None:
        self.geo_point = geo_point
        self.address = address

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'geo_point', None) is not None and getattr(self, 'geo_point', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'address', None) is not None and getattr(self, 'address', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'geo_point', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'address', None) or ''
            if v is not None:
                res += write_string(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountUpdateBusinessWorkHours(TLRequest[Any]):
    ID = 0X4B00E066
    QUALNAME = "functions.account.updateBusinessWorkHours"

    def __init__(self, business_work_hours: Any = None) -> None:
        self.business_work_hours = business_work_hours

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'business_work_hours', None) is not None and getattr(self, 'business_work_hours', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'business_work_hours', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountUpdateColor(TLRequest[Any]):
    ID = 0X684D214E
    QUALNAME = "functions.account.updateColor"

    def __init__(self, for_profile: Any = None, color: Any = None) -> None:
        self.for_profile = for_profile
        self.color = color

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'for_profile', None):
            flags |= (1 << 1)
        if getattr(self, 'color', None) is not None and getattr(self, 'color', None) is not False:
            flags |= (1 << 2)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'color', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountUpdateConnectedBot(TLRequest[Any]):
    ID = 0X66A08C7E
    QUALNAME = "functions.account.updateConnectedBot"

    def __init__(self, deleted: Any = None, rights: Any = None, bot: Any = None, recipients: Any = None) -> None:
        self.deleted = deleted
        self.rights = rights
        self.bot = bot
        self.recipients = recipients

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'deleted', None):
            flags |= (1 << 1)
        if getattr(self, 'rights', None) is not None and getattr(self, 'rights', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'rights', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        res += (self.recipients.write() if hasattr(self.recipients, 'write') else write_bytes(self.recipients))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountUpdateDeviceLocked(TLRequest[Any]):
    ID = 0X38DF3532
    QUALNAME = "functions.account.updateDeviceLocked"

    def __init__(self, period: Any = None) -> None:
        self.period = period

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.period)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountUpdateEmojiStatus(TLRequest[Any]):
    ID = 0XFBD3DE6B
    QUALNAME = "functions.account.updateEmojiStatus"

    def __init__(self, emoji_status: Any = None) -> None:
        self.emoji_status = emoji_status

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.emoji_status.write() if hasattr(self.emoji_status, 'write') else write_bytes(self.emoji_status))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountUpdateNotifySettings(TLRequest[Any]):
    ID = 0X84BE5B93
    QUALNAME = "functions.account.updateNotifySettings"

    def __init__(self, peer: Any = None, settings: Any = None) -> None:
        self.peer = peer
        self.settings = settings

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += (self.settings.write() if hasattr(self.settings, 'write') else write_bytes(self.settings))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountUpdatePasswordSettings(TLRequest[Any]):
    ID = 0XA59B102F
    QUALNAME = "functions.account.updatePasswordSettings"

    def __init__(self, password: Any = None, new_settings: Any = None) -> None:
        self.password = password
        self.new_settings = new_settings

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.password.write() if hasattr(self.password, 'write') else write_bytes(self.password))
        res += (self.new_settings.write() if hasattr(self.new_settings, 'write') else write_bytes(self.new_settings))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountUpdatePersonalChannel(TLRequest[Any]):
    ID = 0XD94305E0
    QUALNAME = "functions.account.updatePersonalChannel"

    def __init__(self, channel: Any = None) -> None:
        self.channel = channel

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountUpdateProfile(TLRequest[Any]):
    ID = 0X78515775
    QUALNAME = "functions.account.updateProfile"

    def __init__(self, first_name: Any = None, last_name: Any = None, about: Any = None) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.about = about

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'first_name', None) is not None and getattr(self, 'first_name', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'last_name', None) is not None and getattr(self, 'last_name', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'about', None) is not None and getattr(self, 'about', None) is not False:
            flags |= (1 << 2)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'first_name', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'last_name', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'about', None) or ''
            if v is not None:
                res += write_string(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountUpdateStatus(TLRequest[Any]):
    ID = 0X6628562C
    QUALNAME = "functions.account.updateStatus"

    def __init__(self, offline: Any = None) -> None:
        self.offline = offline

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_bool(self.offline)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AccountUpdateTheme(TLRequest[Any]):
    ID = 0X2BF40CCC
    QUALNAME = "functions.account.updateTheme"

    def __init__(self, format: Any = None, theme: Any = None, slug: Any = None, title: Any = None, document: Any = None, settings: Any = None) -> None:
        self.format = format
        self.theme = theme
        self.slug = slug
        self.title = title
        self.document = document
        self.settings = settings

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'slug', None) is not None and getattr(self, 'slug', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'title', None) is not None and getattr(self, 'title', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'document', None) is not None and getattr(self, 'document', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'settings', None) is not None and getattr(self, 'settings', None) is not False:
            flags |= (1 << 3)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_string(self.format)
        res += (self.theme.write() if hasattr(self.theme, 'write') else write_bytes(self.theme))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'slug', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'title', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'document', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 3)):
            v = getattr(self, 'settings', None) or []
            if v is not None:
                res += write_vector(v, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountUpdateUsername(TLRequest[Any]):
    ID = 0X3E0BDD7C
    QUALNAME = "functions.account.updateUsername"

    def __init__(self, username: Any = None) -> None:
        self.username = username

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.username)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountUpdateWebBrowserSettings(TLRequest[Any]):
    ID = 0X9ADF82FE
    QUALNAME = "functions.account.updateWebBrowserSettings"

    def __init__(self, open_external_browser: Any = None, display_close_button: Any = None) -> None:
        self.open_external_browser = open_external_browser
        self.display_close_button = display_close_button

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'open_external_browser', None):
            flags |= (1 << 0)
        if getattr(self, 'display_close_button', None):
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountUploadRingtone(TLRequest[Any]):
    ID = 0X831A83A2
    QUALNAME = "functions.account.uploadRingtone"

    def __init__(self, file: Any = None, file_name: Any = None, mime_type: Any = None) -> None:
        self.file = file
        self.file_name = file_name
        self.mime_type = mime_type

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.file.write() if hasattr(self.file, 'write') else write_bytes(self.file))
        res += write_string(self.file_name)
        res += write_string(self.mime_type)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountUploadTheme(TLRequest[Any]):
    ID = 0X1C3DB333
    QUALNAME = "functions.account.uploadTheme"

    def __init__(self, file: Any = None, thumb: Any = None, file_name: Any = None, mime_type: Any = None) -> None:
        self.file = file
        self.thumb = thumb
        self.file_name = file_name
        self.mime_type = mime_type

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'thumb', None) is not None and getattr(self, 'thumb', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.file.write() if hasattr(self.file, 'write') else write_bytes(self.file))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'thumb', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += write_string(self.file_name)
        res += write_string(self.mime_type)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountUploadWallPaper(TLRequest[Any]):
    ID = 0XE39A8F03
    QUALNAME = "functions.account.uploadWallPaper"

    def __init__(self, for_chat: Any = None, file: Any = None, mime_type: Any = None, settings: Any = None) -> None:
        self.for_chat = for_chat
        self.file = file
        self.mime_type = mime_type
        self.settings = settings

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'for_chat', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.file.write() if hasattr(self.file, 'write') else write_bytes(self.file))
        res += write_string(self.mime_type)
        res += (self.settings.write() if hasattr(self.settings, 'write') else write_bytes(self.settings))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountVerifyEmail(TLRequest[Any]):
    ID = 0X32DA4CF
    QUALNAME = "functions.account.verifyEmail"

    def __init__(self, purpose: Any = None, verification: Any = None) -> None:
        self.purpose = purpose
        self.verification = verification

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.purpose.write() if hasattr(self.purpose, 'write') else write_bytes(self.purpose))
        res += (self.verification.write() if hasattr(self.verification, 'write') else write_bytes(self.verification))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AccountVerifyPhone(TLRequest[Any]):
    ID = 0X4DD3A7F6
    QUALNAME = "functions.account.verifyPhone"

    def __init__(self, phone_number: Any = None, phone_code_hash: Any = None, phone_code: Any = None) -> None:
        self.phone_number = phone_number
        self.phone_code_hash = phone_code_hash
        self.phone_code = phone_code

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.phone_number)
        res += write_string(self.phone_code_hash)
        res += write_string(self.phone_code)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AicomposeCreateTone(TLRequest[Any]):
    ID = 0X4AA83913
    QUALNAME = "functions.aicompose.createTone"

    def __init__(self, display_author: Any = None, emoji_id: Any = None, title: Any = None, prompt: Any = None) -> None:
        self.display_author = display_author
        self.emoji_id = emoji_id
        self.title = title
        self.prompt = prompt

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'display_author', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_long(self.emoji_id)
        res += write_string(self.title)
        res += write_string(self.prompt)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AicomposeDeleteTone(TLRequest[Any]):
    ID = 0XDD39316A
    QUALNAME = "functions.aicompose.deleteTone"

    def __init__(self, tone: Any = None) -> None:
        self.tone = tone

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.tone.write() if hasattr(self.tone, 'write') else write_bytes(self.tone))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AicomposeGetTone(TLRequest[Any]):
    ID = 0XB2E8BA03
    QUALNAME = "functions.aicompose.getTone"

    def __init__(self, tone: Any = None) -> None:
        self.tone = tone

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.tone.write() if hasattr(self.tone, 'write') else write_bytes(self.tone))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AicomposeGetToneExample(TLRequest[Any]):
    ID = 0XD1B4AB14
    QUALNAME = "functions.aicompose.getToneExample"

    def __init__(self, tone: Any = None, num: Any = None) -> None:
        self.tone = tone
        self.num = num

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.tone.write() if hasattr(self.tone, 'write') else write_bytes(self.tone))
        res += write_int(self.num)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AicomposeGetTones(TLRequest[Any]):
    ID = 0XABD59201
    QUALNAME = "functions.aicompose.getTones"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AicomposeSaveTone(TLRequest[Any]):
    ID = 0X1782CBB1
    QUALNAME = "functions.aicompose.saveTone"

    def __init__(self, tone: Any = None, unsave: Any = None) -> None:
        self.tone = tone
        self.unsave = unsave

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.tone.write() if hasattr(self.tone, 'write') else write_bytes(self.tone))
        res += write_bool(self.unsave)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AicomposeUpdateTone(TLRequest[Any]):
    ID = 0X903BCF59
    QUALNAME = "functions.aicompose.updateTone"

    def __init__(self, tone: Any = None, display_author: Any = None, emoji_id: Any = None, title: Any = None, prompt: Any = None) -> None:
        self.tone = tone
        self.display_author = display_author
        self.emoji_id = emoji_id
        self.title = title
        self.prompt = prompt

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'display_author', None) is not None and getattr(self, 'display_author', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'emoji_id', None) is not None and getattr(self, 'emoji_id', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'title', None) is not None and getattr(self, 'title', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'prompt', None) is not None and getattr(self, 'prompt', None) is not False:
            flags |= (1 << 3)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.tone.write() if hasattr(self.tone, 'write') else write_bytes(self.tone))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'display_author', None)
            if v is not None:
                res += write_bool(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'emoji_id', None) or 0
            if v is not None:
                res += write_long(v)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'title', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 3)):
            v = getattr(self, 'prompt', None) or ''
            if v is not None:
                res += write_string(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AuthAcceptLoginToken(TLRequest[Any]):
    ID = 0XE894AD4D
    QUALNAME = "functions.auth.acceptLoginToken"

    def __init__(self, token: Any = None) -> None:
        self.token = token

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_bytes(self.token)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AuthBindTempAuthKey(TLRequest[Any]):
    ID = 0XCDD42A05
    QUALNAME = "functions.auth.bindTempAuthKey"

    def __init__(self, perm_auth_key_id: Any = None, nonce: Any = None, expires_at: Any = None, encrypted_message: Any = None) -> None:
        self.perm_auth_key_id = perm_auth_key_id
        self.nonce = nonce
        self.expires_at = expires_at
        self.encrypted_message = encrypted_message

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.perm_auth_key_id)
        res += write_long(self.nonce)
        res += write_int(self.expires_at)
        res += write_bytes(self.encrypted_message)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AuthCancelCode(TLRequest[Any]):
    ID = 0X1F040578
    QUALNAME = "functions.auth.cancelCode"

    def __init__(self, phone_number: Any = None, phone_code_hash: Any = None) -> None:
        self.phone_number = phone_number
        self.phone_code_hash = phone_code_hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.phone_number)
        res += write_string(self.phone_code_hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AuthCheckPaidAuth(TLRequest[Any]):
    ID = 0X56E59F9C
    QUALNAME = "functions.auth.checkPaidAuth"

    def __init__(self, phone_number: Any = None, phone_code_hash: Any = None, form_id: Any = None) -> None:
        self.phone_number = phone_number
        self.phone_code_hash = phone_code_hash
        self.form_id = form_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.phone_number)
        res += write_string(self.phone_code_hash)
        res += write_long(self.form_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AuthCheckPassword(TLRequest[Any]):
    ID = 0XD18B4D16
    QUALNAME = "functions.auth.checkPassword"

    def __init__(self, password: Any = None) -> None:
        self.password = password

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.password.write() if hasattr(self.password, 'write') else write_bytes(self.password))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AuthCheckRecoveryPassword(TLRequest[Any]):
    ID = 0XD36BF79
    QUALNAME = "functions.auth.checkRecoveryPassword"

    def __init__(self, code: Any = None) -> None:
        self.code = code

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.code)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AuthDropTempAuthKeys(TLRequest[Any]):
    ID = 0X8E48A188
    QUALNAME = "functions.auth.dropTempAuthKeys"

    def __init__(self, except_auth_keys: Any = None) -> None:
        self.except_auth_keys = except_auth_keys

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_vector(self.except_auth_keys, write_long)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AuthExportAuthorization(TLRequest[Any]):
    ID = 0XE5BFFFCD
    QUALNAME = "functions.auth.exportAuthorization"

    def __init__(self, dc_id: Any = None) -> None:
        self.dc_id = dc_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.dc_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AuthExportLoginToken(TLRequest[Any]):
    ID = 0XB7E085FE
    QUALNAME = "functions.auth.exportLoginToken"

    def __init__(self, api_id: Any = None, api_hash: Any = None, except_ids: Any = None) -> None:
        self.api_id = api_id
        self.api_hash = api_hash
        self.except_ids = except_ids

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.api_id)
        res += write_string(self.api_hash)
        res += write_vector(self.except_ids, write_long)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AuthFinishFirebasePnvLogin(TLRequest[Any]):
    ID = 0X2C85094C
    QUALNAME = "functions.auth.finishFirebasePnvLogin"

    def __init__(self, google_token: Any = None) -> None:
        self.google_token = google_token

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.google_token)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AuthFinishPasskeyLogin(TLRequest[Any]):
    ID = 0X9857AD07
    QUALNAME = "functions.auth.finishPasskeyLogin"

    def __init__(self, credential: Any = None, from_dc_id: Any = None, from_auth_key_id: Any = None) -> None:
        self.credential = credential
        self.from_dc_id = from_dc_id
        self.from_auth_key_id = from_auth_key_id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'from_dc_id', None) is not None and getattr(self, 'from_dc_id', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'from_auth_key_id', None) is not None and getattr(self, 'from_auth_key_id', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.credential.write() if hasattr(self.credential, 'write') else write_bytes(self.credential))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'from_dc_id', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'from_auth_key_id', None) or 0
            if v is not None:
                res += write_long(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AuthFirebasePnvSignUp(TLRequest[Any]):
    ID = 0X783F6B56
    QUALNAME = "functions.auth.firebasePnvSignUp"

    def __init__(self, no_joined_notifications: Any = None, first_name: Any = None, last_name: Any = None) -> None:
        self.no_joined_notifications = no_joined_notifications
        self.first_name = first_name
        self.last_name = last_name

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'no_joined_notifications', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_string(self.first_name)
        res += write_string(self.last_name)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AuthImportAuthorization(TLRequest[Any]):
    ID = 0XA57A7DAD
    QUALNAME = "functions.auth.importAuthorization"

    def __init__(self, id: Any = None, bytes: Any = None, bytes_data: Any = None) -> None:
        self.id = id
        b_val = bytes if bytes is not None else bytes_data
        self.bytes = b_val
        self.bytes_data = b_val

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.id)
        res += write_bytes(self.bytes)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AuthImportBotAuthorization(TLRequest[Any]):
    ID = 0X67A3FF2C
    QUALNAME = "functions.auth.importBotAuthorization"

    def __init__(self, flags: Any = None, api_id: Any = None, api_hash: Any = None, bot_auth_token: Any = None) -> None:
        self.flags = flags
        self.api_id = api_id
        self.api_hash = api_hash
        self.bot_auth_token = bot_auth_token

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.flags)
        res += write_int(self.api_id)
        res += write_string(self.api_hash)
        res += write_string(self.bot_auth_token)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AuthImportLoginToken(TLRequest[Any]):
    ID = 0X95AC5CE4
    QUALNAME = "functions.auth.importLoginToken"

    def __init__(self, token: Any = None) -> None:
        self.token = token

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_bytes(self.token)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AuthImportWebTokenAuthorization(TLRequest[Any]):
    ID = 0X2DB873A9
    QUALNAME = "functions.auth.importWebTokenAuthorization"

    def __init__(self, api_id: Any = None, api_hash: Any = None, web_auth_token: Any = None) -> None:
        self.api_id = api_id
        self.api_hash = api_hash
        self.web_auth_token = web_auth_token

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.api_id)
        res += write_string(self.api_hash)
        res += write_string(self.web_auth_token)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AuthInitFirebasePnvLogin(TLRequest[Any]):
    ID = 0X777DF37A
    QUALNAME = "functions.auth.initFirebasePnvLogin"

    def __init__(self, api_id: Any = None, api_hash: Any = None) -> None:
        self.api_id = api_id
        self.api_hash = api_hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.api_id)
        res += write_string(self.api_hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AuthInitPasskeyLogin(TLRequest[Any]):
    ID = 0X518AD0B7
    QUALNAME = "functions.auth.initPasskeyLogin"

    def __init__(self, api_id: Any = None, api_hash: Any = None) -> None:
        self.api_id = api_id
        self.api_hash = api_hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.api_id)
        res += write_string(self.api_hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AuthLogOut(TLRequest[Any]):
    ID = 0X3E72BA19
    QUALNAME = "functions.auth.logOut"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AuthRecoverPassword(TLRequest[Any]):
    ID = 0X37096C70
    QUALNAME = "functions.auth.recoverPassword"

    def __init__(self, code: Any = None, new_settings: Any = None) -> None:
        self.code = code
        self.new_settings = new_settings

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'new_settings', None) is not None and getattr(self, 'new_settings', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_string(self.code)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'new_settings', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AuthReportMissingCode(TLRequest[Any]):
    ID = 0XCB9DEFF6
    QUALNAME = "functions.auth.reportMissingCode"

    def __init__(self, phone_number: Any = None, phone_code_hash: Any = None, mnc: Any = None) -> None:
        self.phone_number = phone_number
        self.phone_code_hash = phone_code_hash
        self.mnc = mnc

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.phone_number)
        res += write_string(self.phone_code_hash)
        res += write_string(self.mnc)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AuthRequestFirebaseSms(TLRequest[Any]):
    ID = 0X8E39261E
    QUALNAME = "functions.auth.requestFirebaseSms"

    def __init__(self, phone_number: Any = None, phone_code_hash: Any = None, safety_net_token: Any = None, play_integrity_token: Any = None, ios_push_secret: Any = None) -> None:
        self.phone_number = phone_number
        self.phone_code_hash = phone_code_hash
        self.safety_net_token = safety_net_token
        self.play_integrity_token = play_integrity_token
        self.ios_push_secret = ios_push_secret

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'safety_net_token', None) is not None and getattr(self, 'safety_net_token', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'play_integrity_token', None) is not None and getattr(self, 'play_integrity_token', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'ios_push_secret', None) is not None and getattr(self, 'ios_push_secret', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_string(self.phone_number)
        res += write_string(self.phone_code_hash)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'safety_net_token', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'play_integrity_token', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'ios_push_secret', None) or ''
            if v is not None:
                res += write_string(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AuthRequestPasswordRecovery(TLRequest[Any]):
    ID = 0XD897BC66
    QUALNAME = "functions.auth.requestPasswordRecovery"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AuthResendCode(TLRequest[Any]):
    ID = 0XCAE47523
    QUALNAME = "functions.auth.resendCode"

    def __init__(self, phone_number: Any = None, phone_code_hash: Any = None, reason: Any = None) -> None:
        self.phone_number = phone_number
        self.phone_code_hash = phone_code_hash
        self.reason = reason

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'reason', None) is not None and getattr(self, 'reason', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_string(self.phone_number)
        res += write_string(self.phone_code_hash)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'reason', None) or ''
            if v is not None:
                res += write_string(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AuthResetAuthorizations(TLRequest[Any]):
    ID = 0X9FAB0D1A
    QUALNAME = "functions.auth.resetAuthorizations"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class AuthResetLoginEmail(TLRequest[Any]):
    ID = 0X7E960193
    QUALNAME = "functions.auth.resetLoginEmail"

    def __init__(self, phone_number: Any = None, phone_code_hash: Any = None) -> None:
        self.phone_number = phone_number
        self.phone_code_hash = phone_code_hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.phone_number)
        res += write_string(self.phone_code_hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AuthSendCode(TLRequest[Any]):
    ID = 0XA677244F
    QUALNAME = "functions.auth.sendCode"

    def __init__(self, phone_number: Any = None, api_id: Any = None, api_hash: Any = None, settings: Any = None) -> None:
        self.phone_number = phone_number
        self.api_id = api_id
        self.api_hash = api_hash
        self.settings = settings

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.phone_number)
        res += write_int(self.api_id)
        res += write_string(self.api_hash)
        res += (self.settings.write() if hasattr(self.settings, 'write') else write_bytes(self.settings))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AuthSignIn(TLRequest[Any]):
    ID = 0X8D52A951
    QUALNAME = "functions.auth.signIn"

    def __init__(self, phone_number: Any = None, phone_code_hash: Any = None, phone_code: Any = None, email_verification: Any = None) -> None:
        self.phone_number = phone_number
        self.phone_code_hash = phone_code_hash
        self.phone_code = phone_code
        self.email_verification = email_verification

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'phone_code', None) is not None and getattr(self, 'phone_code', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'email_verification', None) is not None and getattr(self, 'email_verification', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_string(self.phone_number)
        res += write_string(self.phone_code_hash)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'phone_code', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'email_verification', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class AuthSignUp(TLRequest[Any]):
    ID = 0XAAC7B717
    QUALNAME = "functions.auth.signUp"

    def __init__(self, no_joined_notifications: Any = None, phone_number: Any = None, phone_code_hash: Any = None, first_name: Any = None, last_name: Any = None) -> None:
        self.no_joined_notifications = no_joined_notifications
        self.phone_number = phone_number
        self.phone_code_hash = phone_code_hash
        self.first_name = first_name
        self.last_name = last_name

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'no_joined_notifications', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_string(self.phone_number)
        res += write_string(self.phone_code_hash)
        res += write_string(self.first_name)
        res += write_string(self.last_name)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class BindAuthKeyInner(TLRequest[Any]):
    ID = 0X75A3F765
    QUALNAME = "functions.bind_auth_key_inner"

    def __init__(self, nonce: Any = None, temp_auth_key_id: Any = None, perm_auth_key_id: Any = None, temp_session_id: Any = None, expires_at: Any = None) -> None:
        self.nonce = nonce
        self.temp_auth_key_id = temp_auth_key_id
        self.perm_auth_key_id = perm_auth_key_id
        self.temp_session_id = temp_session_id
        self.expires_at = expires_at

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.nonce)
        res += write_long(self.temp_auth_key_id)
        res += write_long(self.perm_auth_key_id)
        res += write_long(self.temp_session_id)
        res += write_int(self.expires_at)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class BotsAddPreviewMedia(TLRequest[Any]):
    ID = 0X17AEB75A
    QUALNAME = "functions.bots.addPreviewMedia"

    def __init__(self, bot: Any = None, lang_code: Any = None, media: Any = None) -> None:
        self.bot = bot
        self.lang_code = lang_code
        self.media = media

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        res += write_string(self.lang_code)
        res += (self.media.write() if hasattr(self.media, 'write') else write_bytes(self.media))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class BotsAllowSendMessage(TLRequest[Any]):
    ID = 0XF132E3EF
    QUALNAME = "functions.bots.allowSendMessage"

    def __init__(self, bot: Any = None) -> None:
        self.bot = bot

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class BotsAnswerWebhookJsonquery(TLRequest[Any]):
    ID = 0XE6213F4D
    QUALNAME = "functions.bots.answerWebhookJSONQuery"

    def __init__(self, query_id: Any = None, data: Any = None) -> None:
        self.query_id = query_id
        self.data = data

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.query_id)
        res += (self.data.write() if hasattr(self.data, 'write') else write_bytes(self.data))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class BotsCanSendMessage(TLRequest[Any]):
    ID = 0X1359F4E6
    QUALNAME = "functions.bots.canSendMessage"

    def __init__(self, bot: Any = None) -> None:
        self.bot = bot

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class BotsCheckDownloadFileParams(TLRequest[Any]):
    ID = 0X50077589
    QUALNAME = "functions.bots.checkDownloadFileParams"

    def __init__(self, bot: Any = None, file_name: Any = None, url: Any = None) -> None:
        self.bot = bot
        self.file_name = file_name
        self.url = url

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        res += write_string(self.file_name)
        res += write_string(self.url)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class BotsCheckUsername(TLRequest[Any]):
    ID = 0X87F2219B
    QUALNAME = "functions.bots.checkUsername"

    def __init__(self, username: Any = None) -> None:
        self.username = username

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.username)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class BotsCreateBot(TLRequest[Any]):
    ID = 0XE5B17F2B
    QUALNAME = "functions.bots.createBot"

    def __init__(self, via_deeplink: Any = None, name: Any = None, username: Any = None, manager_id: Any = None) -> None:
        self.via_deeplink = via_deeplink
        self.name = name
        self.username = username
        self.manager_id = manager_id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'via_deeplink', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_string(self.name)
        res += write_string(self.username)
        res += (self.manager_id.write() if hasattr(self.manager_id, 'write') else write_bytes(self.manager_id))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class BotsDeletePreviewMedia(TLRequest[Any]):
    ID = 0X2D0135B3
    QUALNAME = "functions.bots.deletePreviewMedia"

    def __init__(self, bot: Any = None, lang_code: Any = None, media: Any = None) -> None:
        self.bot = bot
        self.lang_code = lang_code
        self.media = media

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        res += write_string(self.lang_code)
        res += write_vector(self.media, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class BotsEditAccessSettings(TLRequest[Any]):
    ID = 0X31813CD8
    QUALNAME = "functions.bots.editAccessSettings"

    def __init__(self, restricted: Any = None, bot: Any = None, add_users: Any = None) -> None:
        self.restricted = restricted
        self.bot = bot
        self.add_users = add_users

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'restricted', None):
            flags |= (1 << 0)
        if getattr(self, 'add_users', None) is not None and getattr(self, 'add_users', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        if bool(flags & (1 << 1)):
            v = getattr(self, 'add_users', None) or []
            if v is not None:
                res += write_vector(v, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class BotsEditPreviewMedia(TLRequest[Any]):
    ID = 0X8525606F
    QUALNAME = "functions.bots.editPreviewMedia"

    def __init__(self, bot: Any = None, lang_code: Any = None, media: Any = None, new_media: Any = None) -> None:
        self.bot = bot
        self.lang_code = lang_code
        self.media = media
        self.new_media = new_media

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        res += write_string(self.lang_code)
        res += (self.media.write() if hasattr(self.media, 'write') else write_bytes(self.media))
        res += (self.new_media.write() if hasattr(self.new_media, 'write') else write_bytes(self.new_media))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class BotsExportBotToken(TLRequest[Any]):
    ID = 0XBD0D99EB
    QUALNAME = "functions.bots.exportBotToken"

    def __init__(self, bot: Any = None, revoke: Any = None) -> None:
        self.bot = bot
        self.revoke = revoke

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        res += write_bool(self.revoke)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class BotsGetAccessSettings(TLRequest[Any]):
    ID = 0X213853A3
    QUALNAME = "functions.bots.getAccessSettings"

    def __init__(self, bot: Any = None) -> None:
        self.bot = bot

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class BotsGetAdminedBots(TLRequest[Any]):
    ID = 0XB0711D83
    QUALNAME = "functions.bots.getAdminedBots"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class BotsGetBotCommands(TLRequest[Any]):
    ID = 0XE34C0DD6
    QUALNAME = "functions.bots.getBotCommands"

    def __init__(self, scope: Any = None, lang_code: Any = None) -> None:
        self.scope = scope
        self.lang_code = lang_code

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.scope.write() if hasattr(self.scope, 'write') else write_bytes(self.scope))
        res += write_string(self.lang_code)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class BotsGetBotInfo(TLRequest[Any]):
    ID = 0XDCD914FD
    QUALNAME = "functions.bots.getBotInfo"

    def __init__(self, bot: Any = None, lang_code: Any = None) -> None:
        self.bot = bot
        self.lang_code = lang_code

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'bot', None) is not None and getattr(self, 'bot', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'bot', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += write_string(self.lang_code)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class BotsGetBotMenuButton(TLRequest[Any]):
    ID = 0X9C60EB28
    QUALNAME = "functions.bots.getBotMenuButton"

    def __init__(self, user_id: Any = None) -> None:
        self.user_id = user_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.user_id.write() if hasattr(self.user_id, 'write') else write_bytes(self.user_id))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class BotsGetBotRecommendations(TLRequest[Any]):
    ID = 0XA1B70815
    QUALNAME = "functions.bots.getBotRecommendations"

    def __init__(self, bot: Any = None) -> None:
        self.bot = bot

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class BotsGetPopularAppBots(TLRequest[Any]):
    ID = 0XC2510192
    QUALNAME = "functions.bots.getPopularAppBots"

    def __init__(self, offset: Any = None, limit: Any = None) -> None:
        self.offset = offset
        self.limit = limit

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.offset)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class BotsGetPreviewInfo(TLRequest[Any]):
    ID = 0X423AB3AD
    QUALNAME = "functions.bots.getPreviewInfo"

    def __init__(self, bot: Any = None, lang_code: Any = None) -> None:
        self.bot = bot
        self.lang_code = lang_code

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        res += write_string(self.lang_code)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class BotsGetPreviewMedias(TLRequest[Any]):
    ID = 0XA2A5594D
    QUALNAME = "functions.bots.getPreviewMedias"

    def __init__(self, bot: Any = None) -> None:
        self.bot = bot

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class BotsGetRequestedWebViewButton(TLRequest[Any]):
    ID = 0XBF25B7F3
    QUALNAME = "functions.bots.getRequestedWebViewButton"

    def __init__(self, bot: Any = None, webapp_req_id: Any = None) -> None:
        self.bot = bot
        self.webapp_req_id = webapp_req_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        res += write_string(self.webapp_req_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class BotsInvokeWebViewCustomMethod(TLRequest[Any]):
    ID = 0X87FC5E7
    QUALNAME = "functions.bots.invokeWebViewCustomMethod"

    def __init__(self, bot: Any = None, custom_method: Any = None, params: Any = None) -> None:
        self.bot = bot
        self.custom_method = custom_method
        self.params = params

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        res += write_string(self.custom_method)
        res += (self.params.write() if hasattr(self.params, 'write') else write_bytes(self.params))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class BotsReorderPreviewMedias(TLRequest[Any]):
    ID = 0XB627F3AA
    QUALNAME = "functions.bots.reorderPreviewMedias"

    def __init__(self, bot: Any = None, lang_code: Any = None, order: Any = None) -> None:
        self.bot = bot
        self.lang_code = lang_code
        self.order = order

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        res += write_string(self.lang_code)
        res += write_vector(self.order, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class BotsReorderUsernames(TLRequest[Any]):
    ID = 0X9709B1C2
    QUALNAME = "functions.bots.reorderUsernames"

    def __init__(self, bot: Any = None, order: Any = None) -> None:
        self.bot = bot
        self.order = order

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        res += write_vector(self.order, write_string)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class BotsRequestWebViewButton(TLRequest[Any]):
    ID = 0X31A2A35E
    QUALNAME = "functions.bots.requestWebViewButton"

    def __init__(self, user_id: Any = None, button: Any = None) -> None:
        self.user_id = user_id
        self.button = button

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.user_id.write() if hasattr(self.user_id, 'write') else write_bytes(self.user_id))
        res += (self.button.write() if hasattr(self.button, 'write') else write_bytes(self.button))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class BotsResetBotCommands(TLRequest[Any]):
    ID = 0X3D8DE0F9
    QUALNAME = "functions.bots.resetBotCommands"

    def __init__(self, scope: Any = None, lang_code: Any = None) -> None:
        self.scope = scope
        self.lang_code = lang_code

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.scope.write() if hasattr(self.scope, 'write') else write_bytes(self.scope))
        res += write_string(self.lang_code)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class BotsSendCustomRequest(TLRequest[Any]):
    ID = 0XAA2769ED
    QUALNAME = "functions.bots.sendCustomRequest"

    def __init__(self, custom_method: Any = None, params: Any = None) -> None:
        self.custom_method = custom_method
        self.params = params

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.custom_method)
        res += (self.params.write() if hasattr(self.params, 'write') else write_bytes(self.params))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class BotsSetBotBroadcastDefaultAdminRights(TLRequest[Any]):
    ID = 0X788464E1
    QUALNAME = "functions.bots.setBotBroadcastDefaultAdminRights"

    def __init__(self, admin_rights: Any = None) -> None:
        self.admin_rights = admin_rights

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.admin_rights.write() if hasattr(self.admin_rights, 'write') else write_bytes(self.admin_rights))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class BotsSetBotCommands(TLRequest[Any]):
    ID = 0X517165A
    QUALNAME = "functions.bots.setBotCommands"

    def __init__(self, scope: Any = None, lang_code: Any = None, commands: Any = None) -> None:
        self.scope = scope
        self.lang_code = lang_code
        self.commands = commands

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.scope.write() if hasattr(self.scope, 'write') else write_bytes(self.scope))
        res += write_string(self.lang_code)
        res += write_vector(self.commands, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class BotsSetBotGroupDefaultAdminRights(TLRequest[Any]):
    ID = 0X925EC9EA
    QUALNAME = "functions.bots.setBotGroupDefaultAdminRights"

    def __init__(self, admin_rights: Any = None) -> None:
        self.admin_rights = admin_rights

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.admin_rights.write() if hasattr(self.admin_rights, 'write') else write_bytes(self.admin_rights))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class BotsSetBotInfo(TLRequest[Any]):
    ID = 0X10CF3123
    QUALNAME = "functions.bots.setBotInfo"

    def __init__(self, bot: Any = None, lang_code: Any = None, name: Any = None, about: Any = None, description: Any = None) -> None:
        self.bot = bot
        self.lang_code = lang_code
        self.name = name
        self.about = about
        self.description = description

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'bot', None) is not None and getattr(self, 'bot', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'name', None) is not None and getattr(self, 'name', None) is not False:
            flags |= (1 << 3)
        if getattr(self, 'about', None) is not None and getattr(self, 'about', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'description', None) is not None and getattr(self, 'description', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'bot', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += write_string(self.lang_code)
        if bool(flags & (1 << 3)):
            v = getattr(self, 'name', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'about', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'description', None) or ''
            if v is not None:
                res += write_string(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class BotsSetBotMenuButton(TLRequest[Any]):
    ID = 0X4504D54F
    QUALNAME = "functions.bots.setBotMenuButton"

    def __init__(self, user_id: Any = None, button: Any = None) -> None:
        self.user_id = user_id
        self.button = button

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.user_id.write() if hasattr(self.user_id, 'write') else write_bytes(self.user_id))
        res += (self.button.write() if hasattr(self.button, 'write') else write_bytes(self.button))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class BotsSetCustomVerification(TLRequest[Any]):
    ID = 0X8B89DFBD
    QUALNAME = "functions.bots.setCustomVerification"

    def __init__(self, enabled: Any = None, bot: Any = None, peer: Any = None, custom_description: Any = None) -> None:
        self.enabled = enabled
        self.bot = bot
        self.peer = peer
        self.custom_description = custom_description

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'enabled', None):
            flags |= (1 << 1)
        if getattr(self, 'bot', None) is not None and getattr(self, 'bot', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'custom_description', None) is not None and getattr(self, 'custom_description', None) is not False:
            flags |= (1 << 2)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'bot', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        if bool(flags & (1 << 2)):
            v = getattr(self, 'custom_description', None) or ''
            if v is not None:
                res += write_string(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class BotsSetJoinChatResults(TLRequest[Any]):
    ID = 0XE71A4810
    QUALNAME = "functions.bots.setJoinChatResults"

    def __init__(self, query_id: Any = None, result: Any = None) -> None:
        self.query_id = query_id
        self.result = result

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.query_id)
        res += (self.result.write() if hasattr(self.result, 'write') else write_bytes(self.result))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class BotsToggleUserEmojiStatusPermission(TLRequest[Any]):
    ID = 0X6DE6392
    QUALNAME = "functions.bots.toggleUserEmojiStatusPermission"

    def __init__(self, bot: Any = None, enabled: Any = None) -> None:
        self.bot = bot
        self.enabled = enabled

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        res += write_bool(self.enabled)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class BotsToggleUsername(TLRequest[Any]):
    ID = 0X53CA973
    QUALNAME = "functions.bots.toggleUsername"

    def __init__(self, bot: Any = None, username: Any = None, active: Any = None) -> None:
        self.bot = bot
        self.username = username
        self.active = active

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        res += write_string(self.username)
        res += write_bool(self.active)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class BotsUpdateStarRefProgram(TLRequest[Any]):
    ID = 0X778B5AB3
    QUALNAME = "functions.bots.updateStarRefProgram"

    def __init__(self, bot: Any = None, commission_permille: Any = None, duration_months: Any = None) -> None:
        self.bot = bot
        self.commission_permille = commission_permille
        self.duration_months = duration_months

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'duration_months', None) is not None and getattr(self, 'duration_months', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        res += write_int(self.commission_permille)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'duration_months', None) or 0
            if v is not None:
                res += write_int(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class BotsUpdateUserEmojiStatus(TLRequest[Any]):
    ID = 0XED9F30C5
    QUALNAME = "functions.bots.updateUserEmojiStatus"

    def __init__(self, user_id: Any = None, emoji_status: Any = None) -> None:
        self.user_id = user_id
        self.emoji_status = emoji_status

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.user_id.write() if hasattr(self.user_id, 'write') else write_bytes(self.user_id))
        res += (self.emoji_status.write() if hasattr(self.emoji_status, 'write') else write_bytes(self.emoji_status))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class ChannelsCheckSearchPostsFlood(TLRequest[Any]):
    ID = 0X22567115
    QUALNAME = "functions.channels.checkSearchPostsFlood"

    def __init__(self, query: Any = None) -> None:
        self.query = query

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'query', None) is not None and getattr(self, 'query', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'query', None) or ''
            if v is not None:
                res += write_string(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsCheckUsername(TLRequest[Any]):
    ID = 0X10E6BD2C
    QUALNAME = "functions.channels.checkUsername"

    def __init__(self, channel: Any = None, username: Any = None) -> None:
        self.channel = channel
        self.username = username

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += write_string(self.username)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class ChannelsConvertToGigagroup(TLRequest[Any]):
    ID = 0XB290C69
    QUALNAME = "functions.channels.convertToGigagroup"

    def __init__(self, channel: Any = None) -> None:
        self.channel = channel

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsCreateChannel(TLRequest[Any]):
    ID = 0X91006707
    QUALNAME = "functions.channels.createChannel"

    def __init__(self, broadcast: Any = None, megagroup: Any = None, for_import: Any = None, forum: Any = None, title: Any = None, about: Any = None, geo_point: Any = None, address: Any = None, ttl_period: Any = None) -> None:
        self.broadcast = broadcast
        self.megagroup = megagroup
        self.for_import = for_import
        self.forum = forum
        self.title = title
        self.about = about
        self.geo_point = geo_point
        self.address = address
        self.ttl_period = ttl_period

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'broadcast', None):
            flags |= (1 << 0)
        if getattr(self, 'megagroup', None):
            flags |= (1 << 1)
        if getattr(self, 'for_import', None):
            flags |= (1 << 3)
        if getattr(self, 'forum', None):
            flags |= (1 << 5)
        if getattr(self, 'geo_point', None) is not None and getattr(self, 'geo_point', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'address', None) is not None and getattr(self, 'address', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'ttl_period', None) is not None and getattr(self, 'ttl_period', None) is not False:
            flags |= (1 << 4)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_string(self.title)
        res += write_string(self.about)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'geo_point', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 2)):
            v = getattr(self, 'address', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 4)):
            v = getattr(self, 'ttl_period', None) or 0
            if v is not None:
                res += write_int(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsDeactivateAllUsernames(TLRequest[Any]):
    ID = 0XA245DD3
    QUALNAME = "functions.channels.deactivateAllUsernames"

    def __init__(self, channel: Any = None) -> None:
        self.channel = channel

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class ChannelsDeleteChannel(TLRequest[Any]):
    ID = 0XC0111FE3
    QUALNAME = "functions.channels.deleteChannel"

    def __init__(self, channel: Any = None) -> None:
        self.channel = channel

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsDeleteHistory(TLRequest[Any]):
    ID = 0X9BAA9647
    QUALNAME = "functions.channels.deleteHistory"

    def __init__(self, for_everyone: Any = None, channel: Any = None, max_id: Any = None) -> None:
        self.for_everyone = for_everyone
        self.channel = channel
        self.max_id = max_id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'for_everyone', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += write_int(self.max_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsDeleteMessages(TLRequest[Any]):
    ID = 0X84C1FD4E
    QUALNAME = "functions.channels.deleteMessages"

    def __init__(self, channel: Any = None, id: Any = None) -> None:
        self.channel = channel
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += write_vector(self.id, write_int)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsDeleteParticipantHistory(TLRequest[Any]):
    ID = 0X367544DB
    QUALNAME = "functions.channels.deleteParticipantHistory"

    def __init__(self, channel: Any = None, participant: Any = None) -> None:
        self.channel = channel
        self.participant = participant

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += (self.participant.write() if hasattr(self.participant, 'write') else write_bytes(self.participant))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsEditAdmin(TLRequest[Any]):
    ID = 0X9A98AD68
    QUALNAME = "functions.channels.editAdmin"

    def __init__(self, channel: Any = None, user_id: Any = None, admin_rights: Any = None, rank: Any = None) -> None:
        self.channel = channel
        self.user_id = user_id
        self.admin_rights = admin_rights
        self.rank = rank

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'rank', None) is not None and getattr(self, 'rank', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += (self.user_id.write() if hasattr(self.user_id, 'write') else write_bytes(self.user_id))
        res += (self.admin_rights.write() if hasattr(self.admin_rights, 'write') else write_bytes(self.admin_rights))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'rank', None) or ''
            if v is not None:
                res += write_string(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsEditBanned(TLRequest[Any]):
    ID = 0X96E6CD81
    QUALNAME = "functions.channels.editBanned"

    def __init__(self, channel: Any = None, participant: Any = None, banned_rights: Any = None) -> None:
        self.channel = channel
        self.participant = participant
        self.banned_rights = banned_rights

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += (self.participant.write() if hasattr(self.participant, 'write') else write_bytes(self.participant))
        res += (self.banned_rights.write() if hasattr(self.banned_rights, 'write') else write_bytes(self.banned_rights))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsEditLocation(TLRequest[Any]):
    ID = 0X58E63F6D
    QUALNAME = "functions.channels.editLocation"

    def __init__(self, channel: Any = None, geo_point: Any = None, address: Any = None) -> None:
        self.channel = channel
        self.geo_point = geo_point
        self.address = address

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += (self.geo_point.write() if hasattr(self.geo_point, 'write') else write_bytes(self.geo_point))
        res += write_string(self.address)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class ChannelsEditPhoto(TLRequest[Any]):
    ID = 0XF12E57C9
    QUALNAME = "functions.channels.editPhoto"

    def __init__(self, channel: Any = None, photo: Any = None) -> None:
        self.channel = channel
        self.photo = photo

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += (self.photo.write() if hasattr(self.photo, 'write') else write_bytes(self.photo))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsEditTitle(TLRequest[Any]):
    ID = 0X566DECD0
    QUALNAME = "functions.channels.editTitle"

    def __init__(self, channel: Any = None, title: Any = None) -> None:
        self.channel = channel
        self.title = title

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += write_string(self.title)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsExportMessageLink(TLRequest[Any]):
    ID = 0XE63FADEB
    QUALNAME = "functions.channels.exportMessageLink"

    def __init__(self, grouped: Any = None, thread: Any = None, channel: Any = None, id: Any = None) -> None:
        self.grouped = grouped
        self.thread = thread
        self.channel = channel
        self.id = id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'grouped', None):
            flags |= (1 << 0)
        if getattr(self, 'thread', None):
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += write_int(self.id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsGetAdminLog(TLRequest[Any]):
    ID = 0X33DDF480
    QUALNAME = "functions.channels.getAdminLog"

    def __init__(self, channel: Any = None, q: Any = None, events_filter: Any = None, admins: Any = None, max_id: Any = None, min_id: Any = None, limit: Any = None) -> None:
        self.channel = channel
        self.q = q
        self.events_filter = events_filter
        self.admins = admins
        self.max_id = max_id
        self.min_id = min_id
        self.limit = limit

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'events_filter', None) is not None and getattr(self, 'events_filter', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'admins', None) is not None and getattr(self, 'admins', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += write_string(self.q)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'events_filter', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 1)):
            v = getattr(self, 'admins', None) or []
            if v is not None:
                res += write_vector(v, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        res += write_long(self.max_id)
        res += write_long(self.min_id)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsGetAdminedPublicChannels(TLRequest[Any]):
    ID = 0XF8B036AF
    QUALNAME = "functions.channels.getAdminedPublicChannels"

    def __init__(self, by_location: Any = None, check_limit: Any = None, for_personal: Any = None, for_community_peer: Any = None) -> None:
        self.by_location = by_location
        self.check_limit = check_limit
        self.for_personal = for_personal
        self.for_community_peer = for_community_peer

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'by_location', None):
            flags |= (1 << 0)
        if getattr(self, 'check_limit', None):
            flags |= (1 << 1)
        if getattr(self, 'for_personal', None):
            flags |= (1 << 2)
        if getattr(self, 'for_community_peer', None):
            flags |= (1 << 3)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsGetChannelRecommendations(TLRequest[Any]):
    ID = 0X25A71742
    QUALNAME = "functions.channels.getChannelRecommendations"

    def __init__(self, channel: Any = None) -> None:
        self.channel = channel

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'channel', None) is not None and getattr(self, 'channel', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'channel', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsGetChannels(TLRequest[Any]):
    ID = 0XA7F6BBB
    QUALNAME = "functions.channels.getChannels"

    def __init__(self, id: Any = None) -> None:
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_vector(self.id, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsGetFullChannel(TLRequest[Any]):
    ID = 0X8736A09
    QUALNAME = "functions.channels.getFullChannel"

    def __init__(self, channel: Any = None) -> None:
        self.channel = channel

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsGetGroupsForDiscussion(TLRequest[Any]):
    ID = 0XF5DAD378
    QUALNAME = "functions.channels.getGroupsForDiscussion"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsGetInactiveChannels(TLRequest[Any]):
    ID = 0X11E831EE
    QUALNAME = "functions.channels.getInactiveChannels"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsGetLeftChannels(TLRequest[Any]):
    ID = 0X8341ECC0
    QUALNAME = "functions.channels.getLeftChannels"

    def __init__(self, offset: Any = None) -> None:
        self.offset = offset

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.offset)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsGetMessageAuthor(TLRequest[Any]):
    ID = 0XECE2A0E6
    QUALNAME = "functions.channels.getMessageAuthor"

    def __init__(self, channel: Any = None, id: Any = None) -> None:
        self.channel = channel
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += write_int(self.id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsGetMessages(TLRequest[Any]):
    ID = 0XAD8C9A23
    QUALNAME = "functions.channels.getMessages"

    def __init__(self, channel: Any = None, id: Any = None) -> None:
        self.channel = channel
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += write_vector(self.id, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsGetParticipant(TLRequest[Any]):
    ID = 0XA0AB6CC6
    QUALNAME = "functions.channels.getParticipant"

    def __init__(self, channel: Any = None, participant: Any = None) -> None:
        self.channel = channel
        self.participant = participant

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += (self.participant.write() if hasattr(self.participant, 'write') else write_bytes(self.participant))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsGetParticipants(TLRequest[Any]):
    ID = 0X77CED9D0
    QUALNAME = "functions.channels.getParticipants"

    def __init__(self, channel: Any = None, filter: Any = None, offset: Any = None, limit: Any = None, hash: Any = None) -> None:
        self.channel = channel
        self.filter = filter
        self.offset = offset
        self.limit = limit
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += (self.filter.write() if hasattr(self.filter, 'write') else write_bytes(self.filter))
        res += write_int(self.offset)
        res += write_int(self.limit)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsGetSendAs(TLRequest[Any]):
    ID = 0XE785A43F
    QUALNAME = "functions.channels.getSendAs"

    def __init__(self, for_paid_reactions: Any = None, for_live_stories: Any = None, peer: Any = None) -> None:
        self.for_paid_reactions = for_paid_reactions
        self.for_live_stories = for_live_stories
        self.peer = peer

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'for_paid_reactions', None):
            flags |= (1 << 0)
        if getattr(self, 'for_live_stories', None):
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsInviteToChannel(TLRequest[Any]):
    ID = 0XC9E33D54
    QUALNAME = "functions.channels.inviteToChannel"

    def __init__(self, channel: Any = None, users: Any = None) -> None:
        self.channel = channel
        self.users = users

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += write_vector(self.users, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsJoinChannel(TLRequest[Any]):
    ID = 0X7F6A1E22
    QUALNAME = "functions.channels.joinChannel"

    def __init__(self, channel: Any = None) -> None:
        self.channel = channel

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsLeaveChannel(TLRequest[Any]):
    ID = 0XF836AA95
    QUALNAME = "functions.channels.leaveChannel"

    def __init__(self, channel: Any = None) -> None:
        self.channel = channel

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsReadHistory(TLRequest[Any]):
    ID = 0XCC104937
    QUALNAME = "functions.channels.readHistory"

    def __init__(self, channel: Any = None, max_id: Any = None) -> None:
        self.channel = channel
        self.max_id = max_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += write_int(self.max_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class ChannelsReadMessageContents(TLRequest[Any]):
    ID = 0XEAB5DC38
    QUALNAME = "functions.channels.readMessageContents"

    def __init__(self, channel: Any = None, id: Any = None) -> None:
        self.channel = channel
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += write_vector(self.id, write_int)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class ChannelsReorderUsernames(TLRequest[Any]):
    ID = 0XB45CED1D
    QUALNAME = "functions.channels.reorderUsernames"

    def __init__(self, channel: Any = None, order: Any = None) -> None:
        self.channel = channel
        self.order = order

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += write_vector(self.order, write_string)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class ChannelsReportAntiSpamFalsePositive(TLRequest[Any]):
    ID = 0XA850A693
    QUALNAME = "functions.channels.reportAntiSpamFalsePositive"

    def __init__(self, channel: Any = None, msg_id: Any = None) -> None:
        self.channel = channel
        self.msg_id = msg_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += write_int(self.msg_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class ChannelsReportSpam(TLRequest[Any]):
    ID = 0XF44A8315
    QUALNAME = "functions.channels.reportSpam"

    def __init__(self, channel: Any = None, participant: Any = None, id: Any = None) -> None:
        self.channel = channel
        self.participant = participant
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += (self.participant.write() if hasattr(self.participant, 'write') else write_bytes(self.participant))
        res += write_vector(self.id, write_int)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class ChannelsRestrictSponsoredMessages(TLRequest[Any]):
    ID = 0X9AE91519
    QUALNAME = "functions.channels.restrictSponsoredMessages"

    def __init__(self, channel: Any = None, restricted: Any = None) -> None:
        self.channel = channel
        self.restricted = restricted

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += write_bool(self.restricted)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsSearchPosts(TLRequest[Any]):
    ID = 0XF2C4F24D
    QUALNAME = "functions.channels.searchPosts"

    def __init__(self, hashtag: Any = None, query: Any = None, offset_rate: Any = None, offset_peer: Any = None, offset_id: Any = None, limit: Any = None, allow_paid_stars: Any = None) -> None:
        self.hashtag = hashtag
        self.query = query
        self.offset_rate = offset_rate
        self.offset_peer = offset_peer
        self.offset_id = offset_id
        self.limit = limit
        self.allow_paid_stars = allow_paid_stars

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'hashtag', None) is not None and getattr(self, 'hashtag', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'query', None) is not None and getattr(self, 'query', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'allow_paid_stars', None) is not None and getattr(self, 'allow_paid_stars', None) is not False:
            flags |= (1 << 2)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'hashtag', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'query', None) or ''
            if v is not None:
                res += write_string(v)
        res += write_int(self.offset_rate)
        res += (self.offset_peer.write() if hasattr(self.offset_peer, 'write') else write_bytes(self.offset_peer))
        res += write_int(self.offset_id)
        res += write_int(self.limit)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'allow_paid_stars', None) or 0
            if v is not None:
                res += write_long(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsSetBoostsToUnblockRestrictions(TLRequest[Any]):
    ID = 0XAD399CEE
    QUALNAME = "functions.channels.setBoostsToUnblockRestrictions"

    def __init__(self, channel: Any = None, boosts: Any = None) -> None:
        self.channel = channel
        self.boosts = boosts

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += write_int(self.boosts)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsSetDiscussionGroup(TLRequest[Any]):
    ID = 0X40582BB2
    QUALNAME = "functions.channels.setDiscussionGroup"

    def __init__(self, broadcast: Any = None, group: Any = None) -> None:
        self.broadcast = broadcast
        self.group = group

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.broadcast.write() if hasattr(self.broadcast, 'write') else write_bytes(self.broadcast))
        res += (self.group.write() if hasattr(self.group, 'write') else write_bytes(self.group))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class ChannelsSetEmojiStickers(TLRequest[Any]):
    ID = 0X3CD930B7
    QUALNAME = "functions.channels.setEmojiStickers"

    def __init__(self, channel: Any = None, stickerset: Any = None) -> None:
        self.channel = channel
        self.stickerset = stickerset

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += (self.stickerset.write() if hasattr(self.stickerset, 'write') else write_bytes(self.stickerset))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class ChannelsSetMainProfileTab(TLRequest[Any]):
    ID = 0X3583FCB1
    QUALNAME = "functions.channels.setMainProfileTab"

    def __init__(self, channel: Any = None, tab: Any = None) -> None:
        self.channel = channel
        self.tab = tab

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += (self.tab.write() if hasattr(self.tab, 'write') else write_bytes(self.tab))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class ChannelsSetStickers(TLRequest[Any]):
    ID = 0XEA8CA4F9
    QUALNAME = "functions.channels.setStickers"

    def __init__(self, channel: Any = None, stickerset: Any = None) -> None:
        self.channel = channel
        self.stickerset = stickerset

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += (self.stickerset.write() if hasattr(self.stickerset, 'write') else write_bytes(self.stickerset))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class ChannelsToggleAntiSpam(TLRequest[Any]):
    ID = 0X68F3E4EB
    QUALNAME = "functions.channels.toggleAntiSpam"

    def __init__(self, channel: Any = None, enabled: Any = None) -> None:
        self.channel = channel
        self.enabled = enabled

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += write_bool(self.enabled)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsToggleAutotranslation(TLRequest[Any]):
    ID = 0X167FC0A1
    QUALNAME = "functions.channels.toggleAutotranslation"

    def __init__(self, channel: Any = None, enabled: Any = None) -> None:
        self.channel = channel
        self.enabled = enabled

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += write_bool(self.enabled)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsToggleForum(TLRequest[Any]):
    ID = 0X3FF75734
    QUALNAME = "functions.channels.toggleForum"

    def __init__(self, channel: Any = None, enabled: Any = None, tabs: Any = None) -> None:
        self.channel = channel
        self.enabled = enabled
        self.tabs = tabs

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += write_bool(self.enabled)
        res += write_bool(self.tabs)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsToggleJoinRequest(TLRequest[Any]):
    ID = 0XECC2618
    QUALNAME = "functions.channels.toggleJoinRequest"

    def __init__(self, apply_to_invites: Any = None, channel: Any = None, enabled: Any = None, guard_bot: Any = None) -> None:
        self.apply_to_invites = apply_to_invites
        self.channel = channel
        self.enabled = enabled
        self.guard_bot = guard_bot

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'apply_to_invites', None):
            flags |= (1 << 1)
        if getattr(self, 'guard_bot', None) is not None and getattr(self, 'guard_bot', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += write_bool(self.enabled)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'guard_bot', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsToggleJoinToSend(TLRequest[Any]):
    ID = 0XE4CB9580
    QUALNAME = "functions.channels.toggleJoinToSend"

    def __init__(self, channel: Any = None, enabled: Any = None) -> None:
        self.channel = channel
        self.enabled = enabled

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += write_bool(self.enabled)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsToggleParticipantsHidden(TLRequest[Any]):
    ID = 0X6A6E7854
    QUALNAME = "functions.channels.toggleParticipantsHidden"

    def __init__(self, channel: Any = None, enabled: Any = None) -> None:
        self.channel = channel
        self.enabled = enabled

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += write_bool(self.enabled)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsTogglePreHistoryHidden(TLRequest[Any]):
    ID = 0XEABBB94C
    QUALNAME = "functions.channels.togglePreHistoryHidden"

    def __init__(self, channel: Any = None, enabled: Any = None) -> None:
        self.channel = channel
        self.enabled = enabled

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += write_bool(self.enabled)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsToggleSignatures(TLRequest[Any]):
    ID = 0X418D549C
    QUALNAME = "functions.channels.toggleSignatures"

    def __init__(self, signatures_enabled: Any = None, profiles_enabled: Any = None, channel: Any = None) -> None:
        self.signatures_enabled = signatures_enabled
        self.profiles_enabled = profiles_enabled
        self.channel = channel

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'signatures_enabled', None):
            flags |= (1 << 0)
        if getattr(self, 'profiles_enabled', None):
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsToggleSlowMode(TLRequest[Any]):
    ID = 0XEDD49EF0
    QUALNAME = "functions.channels.toggleSlowMode"

    def __init__(self, channel: Any = None, seconds: Any = None) -> None:
        self.channel = channel
        self.seconds = seconds

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += write_int(self.seconds)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsToggleUsername(TLRequest[Any]):
    ID = 0X50F24105
    QUALNAME = "functions.channels.toggleUsername"

    def __init__(self, channel: Any = None, username: Any = None, active: Any = None) -> None:
        self.channel = channel
        self.username = username
        self.active = active

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += write_string(self.username)
        res += write_bool(self.active)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class ChannelsToggleViewForumAsMessages(TLRequest[Any]):
    ID = 0X9738BB15
    QUALNAME = "functions.channels.toggleViewForumAsMessages"

    def __init__(self, channel: Any = None, enabled: Any = None) -> None:
        self.channel = channel
        self.enabled = enabled

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += write_bool(self.enabled)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsUpdateColor(TLRequest[Any]):
    ID = 0XD8AA3671
    QUALNAME = "functions.channels.updateColor"

    def __init__(self, for_profile: Any = None, channel: Any = None, color: Any = None, background_emoji_id: Any = None) -> None:
        self.for_profile = for_profile
        self.channel = channel
        self.color = color
        self.background_emoji_id = background_emoji_id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'for_profile', None):
            flags |= (1 << 1)
        if getattr(self, 'color', None) is not None and getattr(self, 'color', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'background_emoji_id', None) is not None and getattr(self, 'background_emoji_id', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        if bool(flags & (1 << 2)):
            v = getattr(self, 'color', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'background_emoji_id', None) or 0
            if v is not None:
                res += write_long(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsUpdateEmojiStatus(TLRequest[Any]):
    ID = 0XF0D3E6A8
    QUALNAME = "functions.channels.updateEmojiStatus"

    def __init__(self, channel: Any = None, emoji_status: Any = None) -> None:
        self.channel = channel
        self.emoji_status = emoji_status

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += (self.emoji_status.write() if hasattr(self.emoji_status, 'write') else write_bytes(self.emoji_status))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsUpdatePaidMessagesPrice(TLRequest[Any]):
    ID = 0X4B12327B
    QUALNAME = "functions.channels.updatePaidMessagesPrice"

    def __init__(self, broadcast_messages_allowed: Any = None, channel: Any = None, send_paid_messages_stars: Any = None) -> None:
        self.broadcast_messages_allowed = broadcast_messages_allowed
        self.channel = channel
        self.send_paid_messages_stars = send_paid_messages_stars

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'broadcast_messages_allowed', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += write_long(self.send_paid_messages_stars)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChannelsUpdateUsername(TLRequest[Any]):
    ID = 0X3514B3DE
    QUALNAME = "functions.channels.updateUsername"

    def __init__(self, channel: Any = None, username: Any = None) -> None:
        self.channel = channel
        self.username = username

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += write_string(self.username)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class ChatlistsCheckChatlistInvite(TLRequest[Any]):
    ID = 0X41C10FFF
    QUALNAME = "functions.chatlists.checkChatlistInvite"

    def __init__(self, slug: Any = None) -> None:
        self.slug = slug

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.slug)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChatlistsDeleteExportedInvite(TLRequest[Any]):
    ID = 0X719C5C5E
    QUALNAME = "functions.chatlists.deleteExportedInvite"

    def __init__(self, chatlist: Any = None, slug: Any = None) -> None:
        self.chatlist = chatlist
        self.slug = slug

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.chatlist.write() if hasattr(self.chatlist, 'write') else write_bytes(self.chatlist))
        res += write_string(self.slug)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class ChatlistsEditExportedInvite(TLRequest[Any]):
    ID = 0X653DB63D
    QUALNAME = "functions.chatlists.editExportedInvite"

    def __init__(self, chatlist: Any = None, slug: Any = None, title: Any = None, peers: Any = None) -> None:
        self.chatlist = chatlist
        self.slug = slug
        self.title = title
        self.peers = peers

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'title', None) is not None and getattr(self, 'title', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'peers', None) is not None and getattr(self, 'peers', None) is not False:
            flags |= (1 << 2)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.chatlist.write() if hasattr(self.chatlist, 'write') else write_bytes(self.chatlist))
        res += write_string(self.slug)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'title', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'peers', None) or []
            if v is not None:
                res += write_vector(v, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChatlistsExportChatlistInvite(TLRequest[Any]):
    ID = 0X8472478E
    QUALNAME = "functions.chatlists.exportChatlistInvite"

    def __init__(self, chatlist: Any = None, title: Any = None, peers: Any = None) -> None:
        self.chatlist = chatlist
        self.title = title
        self.peers = peers

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.chatlist.write() if hasattr(self.chatlist, 'write') else write_bytes(self.chatlist))
        res += write_string(self.title)
        res += write_vector(self.peers, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChatlistsGetChatlistUpdates(TLRequest[Any]):
    ID = 0X89419521
    QUALNAME = "functions.chatlists.getChatlistUpdates"

    def __init__(self, chatlist: Any = None) -> None:
        self.chatlist = chatlist

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.chatlist.write() if hasattr(self.chatlist, 'write') else write_bytes(self.chatlist))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChatlistsGetExportedInvites(TLRequest[Any]):
    ID = 0XCE03DA83
    QUALNAME = "functions.chatlists.getExportedInvites"

    def __init__(self, chatlist: Any = None) -> None:
        self.chatlist = chatlist

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.chatlist.write() if hasattr(self.chatlist, 'write') else write_bytes(self.chatlist))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChatlistsGetLeaveChatlistSuggestions(TLRequest[Any]):
    ID = 0XFDBCD714
    QUALNAME = "functions.chatlists.getLeaveChatlistSuggestions"

    def __init__(self, chatlist: Any = None) -> None:
        self.chatlist = chatlist

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.chatlist.write() if hasattr(self.chatlist, 'write') else write_bytes(self.chatlist))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChatlistsHideChatlistUpdates(TLRequest[Any]):
    ID = 0X66E486FB
    QUALNAME = "functions.chatlists.hideChatlistUpdates"

    def __init__(self, chatlist: Any = None) -> None:
        self.chatlist = chatlist

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.chatlist.write() if hasattr(self.chatlist, 'write') else write_bytes(self.chatlist))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class ChatlistsJoinChatlistInvite(TLRequest[Any]):
    ID = 0XA6B1E39A
    QUALNAME = "functions.chatlists.joinChatlistInvite"

    def __init__(self, slug: Any = None, peers: Any = None) -> None:
        self.slug = slug
        self.peers = peers

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.slug)
        res += write_vector(self.peers, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChatlistsJoinChatlistUpdates(TLRequest[Any]):
    ID = 0XE089F8F5
    QUALNAME = "functions.chatlists.joinChatlistUpdates"

    def __init__(self, chatlist: Any = None, peers: Any = None) -> None:
        self.chatlist = chatlist
        self.peers = peers

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.chatlist.write() if hasattr(self.chatlist, 'write') else write_bytes(self.chatlist))
        res += write_vector(self.peers, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ChatlistsLeaveChatlist(TLRequest[Any]):
    ID = 0X74FAE13A
    QUALNAME = "functions.chatlists.leaveChatlist"

    def __init__(self, chatlist: Any = None, peers: Any = None) -> None:
        self.chatlist = chatlist
        self.peers = peers

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.chatlist.write() if hasattr(self.chatlist, 'write') else write_bytes(self.chatlist))
        res += write_vector(self.peers, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ClientDhInnerData(TLRequest[Any]):
    ID = 0X6643B654
    QUALNAME = "functions.client_DH_inner_data"

    def __init__(self, nonce: Any = None, server_nonce: Any = None, retry_id: Any = None, g_b: Any = None) -> None:
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.retry_id = retry_id
        self.g_b = g_b

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int128(self.nonce)
        res += write_int128(self.server_nonce)
        res += write_long(self.retry_id)
        res += write_string(self.g_b)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class CommunitiesCreate(TLRequest[Any]):
    ID = 0XA63859EC
    QUALNAME = "functions.communities.create"

    def __init__(self, hidden: Any = None, title: Any = None, about: Any = None, peer: Any = None) -> None:
        self.hidden = hidden
        self.title = title
        self.about = about
        self.peer = peer

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'hidden', None):
            flags |= (1 << 1)
        if getattr(self, 'about', None) is not None and getattr(self, 'about', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_string(self.title)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'about', None) or ''
            if v is not None:
                res += write_string(v)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class CommunitiesGetJoinedCommunities(TLRequest[Any]):
    ID = 0XA663E830
    QUALNAME = "functions.communities.getJoinedCommunities"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class CommunitiesGetParticipantJoinedChats(TLRequest[Any]):
    ID = 0XF87EABAB
    QUALNAME = "functions.communities.getParticipantJoinedChats"

    def __init__(self, community: Any = None, participant: Any = None) -> None:
        self.community = community
        self.participant = participant

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.community.write() if hasattr(self.community, 'write') else write_bytes(self.community))
        res += (self.participant.write() if hasattr(self.participant, 'write') else write_bytes(self.participant))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class CommunitiesGetPeerLinkRequests(TLRequest[Any]):
    ID = 0X93773344
    QUALNAME = "functions.communities.getPeerLinkRequests"

    def __init__(self, community: Any = None, offset: Any = None, limit: Any = None) -> None:
        self.community = community
        self.offset = offset
        self.limit = limit

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.community.write() if hasattr(self.community, 'write') else write_bytes(self.community))
        res += write_string(self.offset)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class CommunitiesToggleAllPeerLinkRequestApproval(TLRequest[Any]):
    ID = 0XBFE3DD3D
    QUALNAME = "functions.communities.toggleAllPeerLinkRequestApproval"

    def __init__(self, reject: Any = None, community: Any = None) -> None:
        self.reject = reject
        self.community = community

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'reject', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.community.write() if hasattr(self.community, 'write') else write_bytes(self.community))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class CommunitiesToggleCommunityCollapsedInDialogs(TLRequest[Any]):
    ID = 0XD766E3EA
    QUALNAME = "functions.communities.toggleCommunityCollapsedInDialogs"

    def __init__(self, collapsed: Any = None, community: Any = None) -> None:
        self.collapsed = collapsed
        self.community = community

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'collapsed', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.community.write() if hasattr(self.community, 'write') else write_bytes(self.community))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class CommunitiesToggleParticipantBanned(TLRequest[Any]):
    ID = 0X9967AD0F
    QUALNAME = "functions.communities.toggleParticipantBanned"

    def __init__(self, unban: Any = None, community: Any = None, participant: Any = None) -> None:
        self.unban = unban
        self.community = community
        self.participant = participant

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'unban', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.community.write() if hasattr(self.community, 'write') else write_bytes(self.community))
        res += (self.participant.write() if hasattr(self.participant, 'write') else write_bytes(self.participant))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class CommunitiesTogglePeerLink(TLRequest[Any]):
    ID = 0X736DCFEA
    QUALNAME = "functions.communities.togglePeerLink"

    def __init__(self, visible: Any = None, hidden: Any = None, deleted: Any = None, community: Any = None, peer: Any = None) -> None:
        self.visible = visible
        self.hidden = hidden
        self.deleted = deleted
        self.community = community
        self.peer = peer

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'visible', None):
            flags |= (1 << 0)
        if getattr(self, 'hidden', None):
            flags |= (1 << 1)
        if getattr(self, 'deleted', None):
            flags |= (1 << 2)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.community.write() if hasattr(self.community, 'write') else write_bytes(self.community))
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class CommunitiesTogglePeerLinkRequestApproval(TLRequest[Any]):
    ID = 0X8C8219A8
    QUALNAME = "functions.communities.togglePeerLinkRequestApproval"

    def __init__(self, reject: Any = None, community: Any = None, peer: Any = None) -> None:
        self.reject = reject
        self.community = community
        self.peer = peer

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'reject', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.community.write() if hasattr(self.community, 'write') else write_bytes(self.community))
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class ContactsAcceptContact(TLRequest[Any]):
    ID = 0XF831A20F
    QUALNAME = "functions.contacts.acceptContact"

    def __init__(self, id: Any = None) -> None:
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.id.write() if hasattr(self.id, 'write') else write_bytes(self.id))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ContactsAddContact(TLRequest[Any]):
    ID = 0XD9BA2E54
    QUALNAME = "functions.contacts.addContact"

    def __init__(self, add_phone_privacy_exception: Any = None, id: Any = None, first_name: Any = None, last_name: Any = None, phone: Any = None, note: Any = None) -> None:
        self.add_phone_privacy_exception = add_phone_privacy_exception
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.note = note

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'add_phone_privacy_exception', None):
            flags |= (1 << 0)
        if getattr(self, 'note', None) is not None and getattr(self, 'note', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.id.write() if hasattr(self.id, 'write') else write_bytes(self.id))
        res += write_string(self.first_name)
        res += write_string(self.last_name)
        res += write_string(self.phone)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'note', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ContactsBlock(TLRequest[Any]):
    ID = 0X2E2E8734
    QUALNAME = "functions.contacts.block"

    def __init__(self, my_stories_from: Any = None, id: Any = None) -> None:
        self.my_stories_from = my_stories_from
        self.id = id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'my_stories_from', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.id.write() if hasattr(self.id, 'write') else write_bytes(self.id))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class ContactsBlockFromReplies(TLRequest[Any]):
    ID = 0X29A8962C
    QUALNAME = "functions.contacts.blockFromReplies"

    def __init__(self, delete_message: Any = None, delete_history: Any = None, report_spam: Any = None, msg_id: Any = None) -> None:
        self.delete_message = delete_message
        self.delete_history = delete_history
        self.report_spam = report_spam
        self.msg_id = msg_id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'delete_message', None):
            flags |= (1 << 0)
        if getattr(self, 'delete_history', None):
            flags |= (1 << 1)
        if getattr(self, 'report_spam', None):
            flags |= (1 << 2)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_int(self.msg_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ContactsDeleteByPhones(TLRequest[Any]):
    ID = 0X1013FD9E
    QUALNAME = "functions.contacts.deleteByPhones"

    def __init__(self, phones: Any = None) -> None:
        self.phones = phones

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_vector(self.phones, write_string)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class ContactsDeleteContacts(TLRequest[Any]):
    ID = 0X96A0E00
    QUALNAME = "functions.contacts.deleteContacts"

    def __init__(self, id: Any = None) -> None:
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_vector(self.id, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ContactsEditCloseFriends(TLRequest[Any]):
    ID = 0XBA6705F0
    QUALNAME = "functions.contacts.editCloseFriends"

    def __init__(self, id: Any = None) -> None:
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_vector(self.id, write_long)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class ContactsExportContactToken(TLRequest[Any]):
    ID = 0XF8654027
    QUALNAME = "functions.contacts.exportContactToken"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ContactsGetBirthdays(TLRequest[Any]):
    ID = 0XDAEDA864
    QUALNAME = "functions.contacts.getBirthdays"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ContactsGetBlocked(TLRequest[Any]):
    ID = 0X9A868F80
    QUALNAME = "functions.contacts.getBlocked"

    def __init__(self, my_stories_from: Any = None, offset: Any = None, limit: Any = None) -> None:
        self.my_stories_from = my_stories_from
        self.offset = offset
        self.limit = limit

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'my_stories_from', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_int(self.offset)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ContactsGetContactIds(TLRequest[Any]):
    ID = 0X7ADC669D
    QUALNAME = "functions.contacts.getContactIDs"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x1CB5C415:
            return read_vector(b, read_int)
        return read_tl_object(b)

class ContactsGetContacts(TLRequest[Any]):
    ID = 0X5DD69E12
    QUALNAME = "functions.contacts.getContacts"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ContactsGetLocated(TLRequest[Any]):
    ID = 0XD348BC44
    QUALNAME = "functions.contacts.getLocated"

    def __init__(self, background: Any = None, geo_point: Any = None, self_expires: Any = None) -> None:
        self.background = background
        self.geo_point = geo_point
        self.self_expires = self_expires

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'background', None):
            flags |= (1 << 1)
        if getattr(self, 'self_expires', None) is not None and getattr(self, 'self_expires', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.geo_point.write() if hasattr(self.geo_point, 'write') else write_bytes(self.geo_point))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'self_expires', None) or 0
            if v is not None:
                res += write_int(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ContactsGetSaved(TLRequest[Any]):
    ID = 0X82F1E39F
    QUALNAME = "functions.contacts.getSaved"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ContactsGetSponsoredPeers(TLRequest[Any]):
    ID = 0XB6C8C393
    QUALNAME = "functions.contacts.getSponsoredPeers"

    def __init__(self, q: Any = None) -> None:
        self.q = q

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.q)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ContactsGetStatuses(TLRequest[Any]):
    ID = 0XC4A353EE
    QUALNAME = "functions.contacts.getStatuses"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ContactsGetTopPeers(TLRequest[Any]):
    ID = 0X973478B6
    QUALNAME = "functions.contacts.getTopPeers"

    def __init__(self, correspondents: Any = None, bots_pm: Any = None, bots_inline: Any = None, phone_calls: Any = None, forward_users: Any = None, forward_chats: Any = None, groups: Any = None, channels: Any = None, bots_app: Any = None, bots_guestchat: Any = None, offset: Any = None, limit: Any = None, hash: Any = None) -> None:
        self.correspondents = correspondents
        self.bots_pm = bots_pm
        self.bots_inline = bots_inline
        self.phone_calls = phone_calls
        self.forward_users = forward_users
        self.forward_chats = forward_chats
        self.groups = groups
        self.channels = channels
        self.bots_app = bots_app
        self.bots_guestchat = bots_guestchat
        self.offset = offset
        self.limit = limit
        self.hash = hash

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'correspondents', None):
            flags |= (1 << 0)
        if getattr(self, 'bots_pm', None):
            flags |= (1 << 1)
        if getattr(self, 'bots_inline', None):
            flags |= (1 << 2)
        if getattr(self, 'phone_calls', None):
            flags |= (1 << 3)
        if getattr(self, 'forward_users', None):
            flags |= (1 << 4)
        if getattr(self, 'forward_chats', None):
            flags |= (1 << 5)
        if getattr(self, 'groups', None):
            flags |= (1 << 10)
        if getattr(self, 'channels', None):
            flags |= (1 << 15)
        if getattr(self, 'bots_app', None):
            flags |= (1 << 16)
        if getattr(self, 'bots_guestchat', None):
            flags |= (1 << 17)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_int(self.offset)
        res += write_int(self.limit)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ContactsImportContactToken(TLRequest[Any]):
    ID = 0X13005788
    QUALNAME = "functions.contacts.importContactToken"

    def __init__(self, token: Any = None) -> None:
        self.token = token

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.token)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ContactsImportContacts(TLRequest[Any]):
    ID = 0X2C800BE5
    QUALNAME = "functions.contacts.importContacts"

    def __init__(self, contacts: Any = None) -> None:
        self.contacts = contacts

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_vector(self.contacts, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ContactsResetSaved(TLRequest[Any]):
    ID = 0X879537F1
    QUALNAME = "functions.contacts.resetSaved"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class ContactsResetTopPeerRating(TLRequest[Any]):
    ID = 0X1AE373AC
    QUALNAME = "functions.contacts.resetTopPeerRating"

    def __init__(self, category: Any = None, peer: Any = None) -> None:
        self.category = category
        self.peer = peer

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.category.write() if hasattr(self.category, 'write') else write_bytes(self.category))
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class ContactsResolvePhone(TLRequest[Any]):
    ID = 0X8AF94344
    QUALNAME = "functions.contacts.resolvePhone"

    def __init__(self, phone: Any = None) -> None:
        self.phone = phone

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.phone)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ContactsResolveUsername(TLRequest[Any]):
    ID = 0X725AFBBC
    QUALNAME = "functions.contacts.resolveUsername"

    def __init__(self, username: Any = None, referer: Any = None) -> None:
        self.username = username
        self.referer = referer

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'referer', None) is not None and getattr(self, 'referer', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_string(self.username)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'referer', None) or ''
            if v is not None:
                res += write_string(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ContactsSearch(TLRequest[Any]):
    ID = 0X5F58D0F
    QUALNAME = "functions.contacts.search"

    def __init__(self, broadcasts: Any = None, bots: Any = None, q: Any = None, limit: Any = None) -> None:
        self.broadcasts = broadcasts
        self.bots = bots
        self.q = q
        self.limit = limit

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'broadcasts', None):
            flags |= (1 << 0)
        if getattr(self, 'bots', None):
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_string(self.q)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ContactsSetBlocked(TLRequest[Any]):
    ID = 0X94C65C76
    QUALNAME = "functions.contacts.setBlocked"

    def __init__(self, my_stories_from: Any = None, id: Any = None, limit: Any = None) -> None:
        self.my_stories_from = my_stories_from
        self.id = id
        self.limit = limit

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'my_stories_from', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_vector(self.id, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class ContactsToggleTopPeers(TLRequest[Any]):
    ID = 0X8514BDDA
    QUALNAME = "functions.contacts.toggleTopPeers"

    def __init__(self, enabled: Any = None) -> None:
        self.enabled = enabled

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_bool(self.enabled)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class ContactsUnblock(TLRequest[Any]):
    ID = 0XB550D328
    QUALNAME = "functions.contacts.unblock"

    def __init__(self, my_stories_from: Any = None, id: Any = None) -> None:
        self.my_stories_from = my_stories_from
        self.id = id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'my_stories_from', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.id.write() if hasattr(self.id, 'write') else write_bytes(self.id))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class ContactsUpdateContactNote(TLRequest[Any]):
    ID = 0X139F63FB
    QUALNAME = "functions.contacts.updateContactNote"

    def __init__(self, id: Any = None, note: Any = None) -> None:
        self.id = id
        self.note = note

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.id.write() if hasattr(self.id, 'write') else write_bytes(self.id))
        res += (self.note.write() if hasattr(self.note, 'write') else write_bytes(self.note))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class DestroyAuthKey(TLRequest[Any]):
    ID = 0XD1435160
    QUALNAME = "functions.destroy_auth_key"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class DestroyAuthKeyFail(TLRequest[Any]):
    ID = 0XEA109B13
    QUALNAME = "functions.destroy_auth_key_fail"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class DestroyAuthKeyNone(TLRequest[Any]):
    ID = 0XA9F2259
    QUALNAME = "functions.destroy_auth_key_none"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class DestroyAuthKeyOk(TLRequest[Any]):
    ID = 0XF660E1D4
    QUALNAME = "functions.destroy_auth_key_ok"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class DestroySession(TLRequest[Any]):
    ID = 0XE7512126
    QUALNAME = "functions.destroy_session"

    def __init__(self, session_id: Any = None) -> None:
        self.session_id = session_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.session_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class DhGenFail(TLRequest[Any]):
    ID = 0XA69DAE02
    QUALNAME = "functions.dh_gen_fail"

    def __init__(self, nonce: Any = None, server_nonce: Any = None, new_nonce_hash3: Any = None) -> None:
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.new_nonce_hash3 = new_nonce_hash3

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int128(self.nonce)
        res += write_int128(self.server_nonce)
        res += write_int128(self.new_nonce_hash3)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class DhGenOk(TLRequest[Any]):
    ID = 0X3BCBF734
    QUALNAME = "functions.dh_gen_ok"

    def __init__(self, nonce: Any = None, server_nonce: Any = None, new_nonce_hash1: Any = None) -> None:
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.new_nonce_hash1 = new_nonce_hash1

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int128(self.nonce)
        res += write_int128(self.server_nonce)
        res += write_int128(self.new_nonce_hash1)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class DhGenRetry(TLRequest[Any]):
    ID = 0X46DC1FB9
    QUALNAME = "functions.dh_gen_retry"

    def __init__(self, nonce: Any = None, server_nonce: Any = None, new_nonce_hash2: Any = None) -> None:
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.new_nonce_hash2 = new_nonce_hash2

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int128(self.nonce)
        res += write_int128(self.server_nonce)
        res += write_int128(self.new_nonce_hash2)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class EphemeralDeleteAllWelcomeMessages(TLRequest[Any]):
    ID = 0X734F9721
    QUALNAME = "functions.ephemeral.deleteAllWelcomeMessages"

    def __init__(self, peer: Any = None) -> None:
        self.peer = peer

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class EphemeralDeleteMessage(TLRequest[Any]):
    ID = 0X92F6E797
    QUALNAME = "functions.ephemeral.deleteMessage"

    def __init__(self, peer: Any = None, receiver_id: Any = None, id: Any = None) -> None:
        self.peer = peer
        self.receiver_id = receiver_id
        self.id = id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'peer', None) is not None and getattr(self, 'peer', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'peer', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += (self.receiver_id.write() if hasattr(self.receiver_id, 'write') else write_bytes(self.receiver_id))
        res += write_int(self.id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class EphemeralDeleteWelcomeMessage(TLRequest[Any]):
    ID = 0XE882A9E1
    QUALNAME = "functions.ephemeral.deleteWelcomeMessage"

    def __init__(self, peer: Any = None, id: Any = None) -> None:
        self.peer = peer
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class EphemeralEditMessage(TLRequest[Any]):
    ID = 0XCF9C725B
    QUALNAME = "functions.ephemeral.editMessage"

    def __init__(self, invert_media: Any = None, welcome: Any = None, peer: Any = None, receiver_id: Any = None, id: Any = None, message: Any = None, media: Any = None, entities: Any = None, reply_markup: Any = None, rich_message: Any = None) -> None:
        self.invert_media = invert_media
        self.welcome = welcome
        self.peer = peer
        self.receiver_id = receiver_id
        self.id = id
        self.message = message
        self.media = media
        self.entities = entities
        self.reply_markup = reply_markup
        self.rich_message = rich_message

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'invert_media', None):
            flags |= (1 << 5)
        if getattr(self, 'welcome', None):
            flags |= (1 << 6)
        if getattr(self, 'peer', None) is not None and getattr(self, 'peer', None) is not False:
            flags |= (1 << 7)
        if getattr(self, 'message', None) is not None and getattr(self, 'message', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'media', None) is not None and getattr(self, 'media', None) is not False:
            flags |= (1 << 3)
        if getattr(self, 'entities', None) is not None and getattr(self, 'entities', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'reply_markup', None) is not None and getattr(self, 'reply_markup', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'rich_message', None) is not None and getattr(self, 'rich_message', None) is not False:
            flags |= (1 << 4)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 7)):
            v = getattr(self, 'peer', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += (self.receiver_id.write() if hasattr(self.receiver_id, 'write') else write_bytes(self.receiver_id))
        res += write_int(self.id)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'message', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 3)):
            v = getattr(self, 'media', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 1)):
            v = getattr(self, 'entities', None) or []
            if v is not None:
                res += write_vector(v, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        if bool(flags & (1 << 2)):
            v = getattr(self, 'reply_markup', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 4)):
            v = getattr(self, 'rich_message', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class EphemeralGetCallbackAnswer(TLRequest[Any]):
    ID = 0X3FA464C8
    QUALNAME = "functions.ephemeral.getCallbackAnswer"

    def __init__(self, peer: Any = None, id: Any = None, data: Any = None) -> None:
        self.peer = peer
        self.id = id
        self.data = data

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'data', None) is not None and getattr(self, 'data', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.id)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'data', None) or b''
            if v is not None:
                res += write_bytes(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class EphemeralGetWelcomeMessages(TLRequest[Any]):
    ID = 0XDB9AC18D
    QUALNAME = "functions.ephemeral.getWelcomeMessages"

    def __init__(self, peer: Any = None, hash: Any = None) -> None:
        self.peer = peer
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class EphemeralReportMessage(TLRequest[Any]):
    ID = 0X8704F2BF
    QUALNAME = "functions.ephemeral.reportMessage"

    def __init__(self, peer: Any = None, id: Any = None, option: Any = None, message: Any = None) -> None:
        self.peer = peer
        self.id = id
        self.option = option
        self.message = message

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.id)
        res += write_bytes(self.option)
        res += write_string(self.message)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class EphemeralSendMessage(TLRequest[Any]):
    ID = 0XBA8D5F35
    QUALNAME = "functions.ephemeral.sendMessage"

    def __init__(self, invert_media: Any = None, welcome: Any = None, anchor: Any = None, noforwards: Any = None, peer: Any = None, receiver_id: Any = None, query_id: Any = None, message: Any = None, entities: Any = None, media: Any = None, reply_markup: Any = None, rich_message: Any = None, random_id: Any = None, reply_to: Any = None) -> None:
        self.invert_media = invert_media
        self.welcome = welcome
        self.anchor = anchor
        self.noforwards = noforwards
        self.peer = peer
        self.receiver_id = receiver_id
        self.query_id = query_id
        self.message = message
        self.entities = entities
        self.media = media
        self.reply_markup = reply_markup
        self.rich_message = rich_message
        self.random_id = random_id
        self.reply_to = reply_to

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'invert_media', None):
            flags |= (1 << 6)
        if getattr(self, 'welcome', None):
            flags |= (1 << 7)
        if getattr(self, 'anchor', None):
            flags |= (1 << 9)
        if getattr(self, 'noforwards', None):
            flags |= (1 << 10)
        if getattr(self, 'peer', None) is not None and getattr(self, 'peer', None) is not False:
            flags |= (1 << 8)
        if getattr(self, 'query_id', None) is not None and getattr(self, 'query_id', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'entities', None) is not None and getattr(self, 'entities', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'media', None) is not None and getattr(self, 'media', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'reply_markup', None) is not None and getattr(self, 'reply_markup', None) is not False:
            flags |= (1 << 3)
        if getattr(self, 'rich_message', None) is not None and getattr(self, 'rich_message', None) is not False:
            flags |= (1 << 4)
        if getattr(self, 'reply_to', None) is not None and getattr(self, 'reply_to', None) is not False:
            flags |= (1 << 5)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 8)):
            v = getattr(self, 'peer', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += (self.receiver_id.write() if hasattr(self.receiver_id, 'write') else write_bytes(self.receiver_id))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'query_id', None) or 0
            if v is not None:
                res += write_long(v)
        res += write_string(self.message)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'entities', None) or []
            if v is not None:
                res += write_vector(v, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        if bool(flags & (1 << 2)):
            v = getattr(self, 'media', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 3)):
            v = getattr(self, 'reply_markup', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 4)):
            v = getattr(self, 'rich_message', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += write_long(self.random_id)
        if bool(flags & (1 << 5)):
            v = getattr(self, 'reply_to', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class FoldersEditPeerFolders(TLRequest[Any]):
    ID = 0X6847D0AB
    QUALNAME = "functions.folders.editPeerFolders"

    def __init__(self, folder_peers: Any = None) -> None:
        self.folder_peers = folder_peers

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_vector(self.folder_peers, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class FragmentGetCollectibleInfo(TLRequest[Any]):
    ID = 0XBE1E85BA
    QUALNAME = "functions.fragment.getCollectibleInfo"

    def __init__(self, collectible: Any = None) -> None:
        self.collectible = collectible

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.collectible.write() if hasattr(self.collectible, 'write') else write_bytes(self.collectible))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class GetFutureSalts(TLRequest[Any]):
    ID = 0XB921BD04
    QUALNAME = "functions.get_future_salts"

    def __init__(self, num: Any = None) -> None:
        self.num = num

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.num)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class HelpAcceptTermsOfService(TLRequest[Any]):
    ID = 0XEE72F79A
    QUALNAME = "functions.help.acceptTermsOfService"

    def __init__(self, id: Any = None) -> None:
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.id.write() if hasattr(self.id, 'write') else write_bytes(self.id))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class HelpDismissSuggestion(TLRequest[Any]):
    ID = 0XF50DBAA1
    QUALNAME = "functions.help.dismissSuggestion"

    def __init__(self, peer: Any = None, suggestion: Any = None) -> None:
        self.peer = peer
        self.suggestion = suggestion

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_string(self.suggestion)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class HelpEditUserInfo(TLRequest[Any]):
    ID = 0X66B91B70
    QUALNAME = "functions.help.editUserInfo"

    def __init__(self, user_id: Any = None, message: Any = None, entities: Any = None) -> None:
        self.user_id = user_id
        self.message = message
        self.entities = entities

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.user_id.write() if hasattr(self.user_id, 'write') else write_bytes(self.user_id))
        res += write_string(self.message)
        res += write_vector(self.entities, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class HelpGetAppConfig(TLRequest[Any]):
    ID = 0X61E3F854
    QUALNAME = "functions.help.getAppConfig"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class HelpGetAppUpdate(TLRequest[Any]):
    ID = 0X522D5A7D
    QUALNAME = "functions.help.getAppUpdate"

    def __init__(self, source: Any = None) -> None:
        self.source = source

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.source)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class HelpGetCdnConfig(TLRequest[Any]):
    ID = 0X52029342
    QUALNAME = "functions.help.getCdnConfig"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class HelpGetConfig(TLRequest[Any]):
    ID = 0XC4F9186B
    QUALNAME = "functions.help.getConfig"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class HelpGetCountriesList(TLRequest[Any]):
    ID = 0X735787A8
    QUALNAME = "functions.help.getCountriesList"

    def __init__(self, lang_code: Any = None, hash: Any = None) -> None:
        self.lang_code = lang_code
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.lang_code)
        res += write_int(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class HelpGetDeepLinkInfo(TLRequest[Any]):
    ID = 0X3FEDC75F
    QUALNAME = "functions.help.getDeepLinkInfo"

    def __init__(self, path: Any = None) -> None:
        self.path = path

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.path)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class HelpGetInviteText(TLRequest[Any]):
    ID = 0X4D392343
    QUALNAME = "functions.help.getInviteText"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class HelpGetNearestDc(TLRequest[Any]):
    ID = 0X1FB33026
    QUALNAME = "functions.help.getNearestDc"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class HelpGetPassportConfig(TLRequest[Any]):
    ID = 0XC661AD08
    QUALNAME = "functions.help.getPassportConfig"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class HelpGetPeerColors(TLRequest[Any]):
    ID = 0XDA80F42F
    QUALNAME = "functions.help.getPeerColors"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class HelpGetPeerProfileColors(TLRequest[Any]):
    ID = 0XABCFA9FD
    QUALNAME = "functions.help.getPeerProfileColors"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class HelpGetPremiumPromo(TLRequest[Any]):
    ID = 0XB81B93D4
    QUALNAME = "functions.help.getPremiumPromo"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class HelpGetPromoData(TLRequest[Any]):
    ID = 0XC0977421
    QUALNAME = "functions.help.getPromoData"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class HelpGetRecentMeUrls(TLRequest[Any]):
    ID = 0X3DC0F114
    QUALNAME = "functions.help.getRecentMeUrls"

    def __init__(self, referer: Any = None) -> None:
        self.referer = referer

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.referer)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class HelpGetSupport(TLRequest[Any]):
    ID = 0X9CDF08CD
    QUALNAME = "functions.help.getSupport"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class HelpGetSupportName(TLRequest[Any]):
    ID = 0XD360E72C
    QUALNAME = "functions.help.getSupportName"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class HelpGetTermsOfServiceUpdate(TLRequest[Any]):
    ID = 0X2CA51FD1
    QUALNAME = "functions.help.getTermsOfServiceUpdate"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class HelpGetTimezonesList(TLRequest[Any]):
    ID = 0X49B30240
    QUALNAME = "functions.help.getTimezonesList"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class HelpGetUserInfo(TLRequest[Any]):
    ID = 0X38A08D3
    QUALNAME = "functions.help.getUserInfo"

    def __init__(self, user_id: Any = None) -> None:
        self.user_id = user_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.user_id.write() if hasattr(self.user_id, 'write') else write_bytes(self.user_id))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class HelpHidePromoData(TLRequest[Any]):
    ID = 0X1E251C95
    QUALNAME = "functions.help.hidePromoData"

    def __init__(self, peer: Any = None) -> None:
        self.peer = peer

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class HelpSaveAppLog(TLRequest[Any]):
    ID = 0X6F02F748
    QUALNAME = "functions.help.saveAppLog"

    def __init__(self, events: Any = None) -> None:
        self.events = events

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_vector(self.events, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class HelpSetBotUpdatesStatus(TLRequest[Any]):
    ID = 0XEC22CFCD
    QUALNAME = "functions.help.setBotUpdatesStatus"

    def __init__(self, pending_updates_count: Any = None, message: Any = None) -> None:
        self.pending_updates_count = pending_updates_count
        self.message = message

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.pending_updates_count)
        res += write_string(self.message)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class InitConnection(TLRequest[Any]):
    ID = 0XC1CD5EA9
    QUALNAME = "functions.initConnection"

    def __init__(self, api_id: Any = None, device_model: Any = None, system_version: Any = None, app_version: Any = None, system_lang_code: Any = None, lang_pack: Any = None, lang_code: Any = None, proxy: Any = None, params: Any = None, query: Any = None) -> None:
        self.api_id = api_id
        self.device_model = device_model
        self.system_version = system_version
        self.app_version = app_version
        self.system_lang_code = system_lang_code
        self.lang_pack = lang_pack
        self.lang_code = lang_code
        self.proxy = proxy
        self.params = params
        self.query = query

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'proxy', None) is not None and getattr(self, 'proxy', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'params', None) is not None and getattr(self, 'params', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_int(self.api_id)
        res += write_string(self.device_model)
        res += write_string(self.system_version)
        res += write_string(self.app_version)
        res += write_string(self.system_lang_code)
        res += write_string(self.lang_pack)
        res += write_string(self.lang_code)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'proxy', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 1)):
            v = getattr(self, 'params', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += (self.query.write() if hasattr(self.query, 'write') else write_bytes(self.query))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class Int128(TLRequest[Any]):
    ID = 0X36DEC32
    QUALNAME = "functions.int128"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class Int256(TLRequest[Any]):
    ID = 0XE9BE1E6B
    QUALNAME = "functions.int256"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class InvokeAfterMsg(TLRequest[Any]):
    ID = 0XCB9F372D
    QUALNAME = "functions.invokeAfterMsg"

    def __init__(self, msg_id: Any = None, query: Any = None) -> None:
        self.msg_id = msg_id
        self.query = query

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.msg_id)
        res += (self.query.write() if hasattr(self.query, 'write') else write_bytes(self.query))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class InvokeAfterMsgs(TLRequest[Any]):
    ID = 0X3DC4B4F0
    QUALNAME = "functions.invokeAfterMsgs"

    def __init__(self, msg_ids: Any = None, query: Any = None) -> None:
        self.msg_ids = msg_ids
        self.query = query

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_vector(self.msg_ids, write_long)
        res += (self.query.write() if hasattr(self.query, 'write') else write_bytes(self.query))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class InvokeWithApnsSecret(TLRequest[Any]):
    ID = 0XDAE54F8
    QUALNAME = "functions.invokeWithApnsSecret"

    def __init__(self, nonce: Any = None, secret: Any = None, query: Any = None) -> None:
        self.nonce = nonce
        self.secret = secret
        self.query = query

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.nonce)
        res += write_string(self.secret)
        res += (self.query.write() if hasattr(self.query, 'write') else write_bytes(self.query))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class InvokeWithBusinessConnection(TLRequest[Any]):
    ID = 0XDD289F8E
    QUALNAME = "functions.invokeWithBusinessConnection"

    def __init__(self, connection_id: Any = None, query: Any = None) -> None:
        self.connection_id = connection_id
        self.query = query

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.connection_id)
        res += (self.query.write() if hasattr(self.query, 'write') else write_bytes(self.query))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class InvokeWithGooglePlayIntegrity(TLRequest[Any]):
    ID = 0X1DF92984
    QUALNAME = "functions.invokeWithGooglePlayIntegrity"

    def __init__(self, nonce: Any = None, token: Any = None, query: Any = None) -> None:
        self.nonce = nonce
        self.token = token
        self.query = query

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.nonce)
        res += write_string(self.token)
        res += (self.query.write() if hasattr(self.query, 'write') else write_bytes(self.query))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class InvokeWithLayer(TLRequest[Any]):
    ID = 0XDA9B0D0D
    QUALNAME = "functions.invokeWithLayer"

    def __init__(self, layer: Any = None, query: Any = None) -> None:
        self.layer = layer
        self.query = query

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.layer)
        res += (self.query.write() if hasattr(self.query, 'write') else write_bytes(self.query))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class InvokeWithMessagesRange(TLRequest[Any]):
    ID = 0X365275F2
    QUALNAME = "functions.invokeWithMessagesRange"

    def __init__(self, range: Any = None, query: Any = None) -> None:
        self.range = range
        self.query = query

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.range.write() if hasattr(self.range, 'write') else write_bytes(self.range))
        res += (self.query.write() if hasattr(self.query, 'write') else write_bytes(self.query))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class InvokeWithReCaptcha(TLRequest[Any]):
    ID = 0XADBB0F94
    QUALNAME = "functions.invokeWithReCaptcha"

    def __init__(self, token: Any = None, query: Any = None) -> None:
        self.token = token
        self.query = query

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.token)
        res += (self.query.write() if hasattr(self.query, 'write') else write_bytes(self.query))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class InvokeWithTakeout(TLRequest[Any]):
    ID = 0XACA9FD2E
    QUALNAME = "functions.invokeWithTakeout"

    def __init__(self, takeout_id: Any = None, query: Any = None) -> None:
        self.takeout_id = takeout_id
        self.query = query

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.takeout_id)
        res += (self.query.write() if hasattr(self.query, 'write') else write_bytes(self.query))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class InvokeWithoutUpdates(TLRequest[Any]):
    ID = 0XBF9459B7
    QUALNAME = "functions.invokeWithoutUpdates"

    def __init__(self, query: Any = None) -> None:
        self.query = query

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.query.write() if hasattr(self.query, 'write') else write_bytes(self.query))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class LangpackGetDifference(TLRequest[Any]):
    ID = 0XCD984AA5
    QUALNAME = "functions.langpack.getDifference"

    def __init__(self, lang_pack: Any = None, lang_code: Any = None, from_version: Any = None) -> None:
        self.lang_pack = lang_pack
        self.lang_code = lang_code
        self.from_version = from_version

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.lang_pack)
        res += write_string(self.lang_code)
        res += write_int(self.from_version)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class LangpackGetLangPack(TLRequest[Any]):
    ID = 0XF2F2330A
    QUALNAME = "functions.langpack.getLangPack"

    def __init__(self, lang_pack: Any = None, lang_code: Any = None) -> None:
        self.lang_pack = lang_pack
        self.lang_code = lang_code

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.lang_pack)
        res += write_string(self.lang_code)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class LangpackGetLanguage(TLRequest[Any]):
    ID = 0X6A596502
    QUALNAME = "functions.langpack.getLanguage"

    def __init__(self, lang_pack: Any = None, lang_code: Any = None) -> None:
        self.lang_pack = lang_pack
        self.lang_code = lang_code

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.lang_pack)
        res += write_string(self.lang_code)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class LangpackGetLanguages(TLRequest[Any]):
    ID = 0X42C6978F
    QUALNAME = "functions.langpack.getLanguages"

    def __init__(self, lang_pack: Any = None) -> None:
        self.lang_pack = lang_pack

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.lang_pack)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class LangpackGetStrings(TLRequest[Any]):
    ID = 0XEFEA3803
    QUALNAME = "functions.langpack.getStrings"

    def __init__(self, lang_pack: Any = None, lang_code: Any = None, keys: Any = None) -> None:
        self.lang_pack = lang_pack
        self.lang_code = lang_code
        self.keys = keys

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.lang_pack)
        res += write_string(self.lang_code)
        res += write_vector(self.keys, write_string)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesAcceptEncryption(TLRequest[Any]):
    ID = 0X3DBC0415
    QUALNAME = "functions.messages.acceptEncryption"

    def __init__(self, peer: Any = None, g_b: Any = None, key_fingerprint: Any = None) -> None:
        self.peer = peer
        self.g_b = g_b
        self.key_fingerprint = key_fingerprint

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_bytes(self.g_b)
        res += write_long(self.key_fingerprint)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesAcceptUrlAuth(TLRequest[Any]):
    ID = 0X67A3F0DE
    QUALNAME = "functions.messages.acceptUrlAuth"

    def __init__(self, write_allowed: Any = None, share_phone_number: Any = None, peer: Any = None, msg_id: Any = None, button_id: Any = None, url: Any = None, match_code: Any = None) -> None:
        self.write_allowed = write_allowed
        self.share_phone_number = share_phone_number
        self.peer = peer
        self.msg_id = msg_id
        self.button_id = button_id
        self.url = url
        self.match_code = match_code

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'write_allowed', None):
            flags |= (1 << 0)
        if getattr(self, 'share_phone_number', None):
            flags |= (1 << 3)
        if getattr(self, 'peer', None) is not None and getattr(self, 'peer', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'msg_id', None) is not None and getattr(self, 'msg_id', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'button_id', None) is not None and getattr(self, 'button_id', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'url', None) is not None and getattr(self, 'url', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'match_code', None) is not None and getattr(self, 'match_code', None) is not False:
            flags |= (1 << 4)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'peer', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 1)):
            v = getattr(self, 'msg_id', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'button_id', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'url', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 4)):
            v = getattr(self, 'match_code', None) or ''
            if v is not None:
                res += write_string(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesAddChatUser(TLRequest[Any]):
    ID = 0XCBC6D107
    QUALNAME = "functions.messages.addChatUser"

    def __init__(self, chat_id: Any = None, user_id: Any = None, fwd_limit: Any = None) -> None:
        self.chat_id = chat_id
        self.user_id = user_id
        self.fwd_limit = fwd_limit

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.chat_id)
        res += (self.user_id.write() if hasattr(self.user_id, 'write') else write_bytes(self.user_id))
        res += write_int(self.fwd_limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesAddPollAnswer(TLRequest[Any]):
    ID = 0X19BC4B6D
    QUALNAME = "functions.messages.addPollAnswer"

    def __init__(self, peer: Any = None, msg_id: Any = None, answer: Any = None) -> None:
        self.peer = peer
        self.msg_id = msg_id
        self.answer = answer

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.msg_id)
        res += (self.answer.write() if hasattr(self.answer, 'write') else write_bytes(self.answer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesAppendTodoList(TLRequest[Any]):
    ID = 0X21A61057
    QUALNAME = "functions.messages.appendTodoList"

    def __init__(self, peer: Any = None, msg_id: Any = None, list: Any = None) -> None:
        self.peer = peer
        self.msg_id = msg_id
        self.list = list

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.msg_id)
        res += write_vector(self.list, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesCheckChatInvite(TLRequest[Any]):
    ID = 0X3EADB1BB
    QUALNAME = "functions.messages.checkChatInvite"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesCheckHistoryImport(TLRequest[Any]):
    ID = 0X43FE19F3
    QUALNAME = "functions.messages.checkHistoryImport"

    def __init__(self, import_head: Any = None) -> None:
        self.import_head = import_head

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.import_head)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesCheckHistoryImportPeer(TLRequest[Any]):
    ID = 0X5DC60F03
    QUALNAME = "functions.messages.checkHistoryImportPeer"

    def __init__(self, peer: Any = None) -> None:
        self.peer = peer

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesCheckQuickReplyShortcut(TLRequest[Any]):
    ID = 0XF1D0FBD3
    QUALNAME = "functions.messages.checkQuickReplyShortcut"

    def __init__(self, shortcut: Any = None) -> None:
        self.shortcut = shortcut

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.shortcut)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesCheckUrlAuthMatchCode(TLRequest[Any]):
    ID = 0XC9A47B0B
    QUALNAME = "functions.messages.checkUrlAuthMatchCode"

    def __init__(self, url: Any = None, match_code: Any = None) -> None:
        self.url = url
        self.match_code = match_code

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.url)
        res += write_string(self.match_code)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesClearAllDrafts(TLRequest[Any]):
    ID = 0X7E58EE9C
    QUALNAME = "functions.messages.clearAllDrafts"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesClearRecentReactions(TLRequest[Any]):
    ID = 0X9DFEEFB4
    QUALNAME = "functions.messages.clearRecentReactions"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesClearRecentStickers(TLRequest[Any]):
    ID = 0X8999602D
    QUALNAME = "functions.messages.clearRecentStickers"

    def __init__(self, attached: Any = None) -> None:
        self.attached = attached

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'attached', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesClickSponsoredMessage(TLRequest[Any]):
    ID = 0X8235057E
    QUALNAME = "functions.messages.clickSponsoredMessage"

    def __init__(self, media: Any = None, fullscreen: Any = None, random_id: Any = None) -> None:
        self.media = media
        self.fullscreen = fullscreen
        self.random_id = random_id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'media', None):
            flags |= (1 << 0)
        if getattr(self, 'fullscreen', None):
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_bytes(self.random_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesComposeMessageWithAi(TLRequest[Any]):
    ID = 0XDAECC589
    QUALNAME = "functions.messages.composeMessageWithAI"

    def __init__(self, proofread: Any = None, emojify: Any = None, text: Any = None, translate_to_lang: Any = None, tone: Any = None) -> None:
        self.proofread = proofread
        self.emojify = emojify
        self.text = text
        self.translate_to_lang = translate_to_lang
        self.tone = tone

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'proofread', None):
            flags |= (1 << 0)
        if getattr(self, 'emojify', None):
            flags |= (1 << 3)
        if getattr(self, 'translate_to_lang', None) is not None and getattr(self, 'translate_to_lang', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'tone', None) is not None and getattr(self, 'tone', None) is not False:
            flags |= (1 << 2)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.text.write() if hasattr(self.text, 'write') else write_bytes(self.text))
        if bool(flags & (1 << 1)):
            v = getattr(self, 'translate_to_lang', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'tone', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesComposeRichMessageWithAi(TLRequest[Any]):
    ID = 0X8D7AE6AF
    QUALNAME = "functions.messages.composeRichMessageWithAI"

    def __init__(self, proofread: Any = None, emojify: Any = None, text: Any = None, translate_to_lang: Any = None, tone: Any = None) -> None:
        self.proofread = proofread
        self.emojify = emojify
        self.text = text
        self.translate_to_lang = translate_to_lang
        self.tone = tone

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'proofread', None):
            flags |= (1 << 0)
        if getattr(self, 'emojify', None):
            flags |= (1 << 3)
        if getattr(self, 'text', None) is not None and getattr(self, 'text', None) is not False:
            flags |= (1 << 4)
        if getattr(self, 'translate_to_lang', None) is not None and getattr(self, 'translate_to_lang', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'tone', None) is not None and getattr(self, 'tone', None) is not False:
            flags |= (1 << 2)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 4)):
            v = getattr(self, 'text', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 1)):
            v = getattr(self, 'translate_to_lang', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'tone', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesCreateChat(TLRequest[Any]):
    ID = 0X92CEDDD4
    QUALNAME = "functions.messages.createChat"

    def __init__(self, users: Any = None, title: Any = None, ttl_period: Any = None) -> None:
        self.users = users
        self.title = title
        self.ttl_period = ttl_period

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'ttl_period', None) is not None and getattr(self, 'ttl_period', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_vector(self.users, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        res += write_string(self.title)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'ttl_period', None) or 0
            if v is not None:
                res += write_int(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesCreateForumTopic(TLRequest[Any]):
    ID = 0X2F98C3D5
    QUALNAME = "functions.messages.createForumTopic"

    def __init__(self, title_missing: Any = None, peer: Any = None, title: Any = None, icon_color: Any = None, icon_emoji_id: Any = None, random_id: Any = None, send_as: Any = None) -> None:
        self.title_missing = title_missing
        self.peer = peer
        self.title = title
        self.icon_color = icon_color
        self.icon_emoji_id = icon_emoji_id
        self.random_id = random_id
        self.send_as = send_as

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'title_missing', None):
            flags |= (1 << 4)
        if getattr(self, 'icon_color', None) is not None and getattr(self, 'icon_color', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'icon_emoji_id', None) is not None and getattr(self, 'icon_emoji_id', None) is not False:
            flags |= (1 << 3)
        if getattr(self, 'send_as', None) is not None and getattr(self, 'send_as', None) is not False:
            flags |= (1 << 2)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_string(self.title)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'icon_color', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 3)):
            v = getattr(self, 'icon_emoji_id', None) or 0
            if v is not None:
                res += write_long(v)
        res += write_long(self.random_id)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'send_as', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesDeclineUrlAuth(TLRequest[Any]):
    ID = 0X35436BBC
    QUALNAME = "functions.messages.declineUrlAuth"

    def __init__(self, url: Any = None) -> None:
        self.url = url

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.url)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesDeleteChat(TLRequest[Any]):
    ID = 0X5BD0EE50
    QUALNAME = "functions.messages.deleteChat"

    def __init__(self, chat_id: Any = None) -> None:
        self.chat_id = chat_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.chat_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesDeleteChatUser(TLRequest[Any]):
    ID = 0XA2185CAB
    QUALNAME = "functions.messages.deleteChatUser"

    def __init__(self, revoke_history: Any = None, chat_id: Any = None, user_id: Any = None) -> None:
        self.revoke_history = revoke_history
        self.chat_id = chat_id
        self.user_id = user_id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'revoke_history', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_long(self.chat_id)
        res += (self.user_id.write() if hasattr(self.user_id, 'write') else write_bytes(self.user_id))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesDeleteExportedChatInvite(TLRequest[Any]):
    ID = 0XD464A42B
    QUALNAME = "functions.messages.deleteExportedChatInvite"

    def __init__(self, peer: Any = None, link: Any = None) -> None:
        self.peer = peer
        self.link = link

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_string(self.link)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesDeleteFactCheck(TLRequest[Any]):
    ID = 0XD1DA940C
    QUALNAME = "functions.messages.deleteFactCheck"

    def __init__(self, peer: Any = None, msg_id: Any = None) -> None:
        self.peer = peer
        self.msg_id = msg_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.msg_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesDeleteHistory(TLRequest[Any]):
    ID = 0XB08F922A
    QUALNAME = "functions.messages.deleteHistory"

    def __init__(self, just_clear: Any = None, revoke: Any = None, peer: Any = None, max_id: Any = None, min_date: Any = None, max_date: Any = None) -> None:
        self.just_clear = just_clear
        self.revoke = revoke
        self.peer = peer
        self.max_id = max_id
        self.min_date = min_date
        self.max_date = max_date

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'just_clear', None):
            flags |= (1 << 0)
        if getattr(self, 'revoke', None):
            flags |= (1 << 1)
        if getattr(self, 'min_date', None) is not None and getattr(self, 'min_date', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'max_date', None) is not None and getattr(self, 'max_date', None) is not False:
            flags |= (1 << 3)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.max_id)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'min_date', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 3)):
            v = getattr(self, 'max_date', None) or 0
            if v is not None:
                res += write_int(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesDeleteMessages(TLRequest[Any]):
    ID = 0XE58E95D2
    QUALNAME = "functions.messages.deleteMessages"

    def __init__(self, revoke: Any = None, id: Any = None) -> None:
        self.revoke = revoke
        self.id = id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'revoke', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_vector(self.id, write_int)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesDeleteParticipantReaction(TLRequest[Any]):
    ID = 0XE3B7F82C
    QUALNAME = "functions.messages.deleteParticipantReaction"

    def __init__(self, peer: Any = None, msg_id: Any = None, participant: Any = None) -> None:
        self.peer = peer
        self.msg_id = msg_id
        self.participant = participant

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.msg_id)
        res += (self.participant.write() if hasattr(self.participant, 'write') else write_bytes(self.participant))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesDeleteParticipantReactions(TLRequest[Any]):
    ID = 0XA0B80CF8
    QUALNAME = "functions.messages.deleteParticipantReactions"

    def __init__(self, peer: Any = None, participant: Any = None) -> None:
        self.peer = peer
        self.participant = participant

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += (self.participant.write() if hasattr(self.participant, 'write') else write_bytes(self.participant))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesDeletePhoneCallHistory(TLRequest[Any]):
    ID = 0XF9CBE409
    QUALNAME = "functions.messages.deletePhoneCallHistory"

    def __init__(self, revoke: Any = None) -> None:
        self.revoke = revoke

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'revoke', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesDeletePollAnswer(TLRequest[Any]):
    ID = 0XAC8505A5
    QUALNAME = "functions.messages.deletePollAnswer"

    def __init__(self, peer: Any = None, msg_id: Any = None, option: Any = None) -> None:
        self.peer = peer
        self.msg_id = msg_id
        self.option = option

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.msg_id)
        res += write_bytes(self.option)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesDeleteQuickReplyMessages(TLRequest[Any]):
    ID = 0XE105E910
    QUALNAME = "functions.messages.deleteQuickReplyMessages"

    def __init__(self, shortcut_id: Any = None, id: Any = None) -> None:
        self.shortcut_id = shortcut_id
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.shortcut_id)
        res += write_vector(self.id, write_int)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesDeleteQuickReplyShortcut(TLRequest[Any]):
    ID = 0X3CC04740
    QUALNAME = "functions.messages.deleteQuickReplyShortcut"

    def __init__(self, shortcut_id: Any = None) -> None:
        self.shortcut_id = shortcut_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.shortcut_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesDeleteRevokedExportedChatInvites(TLRequest[Any]):
    ID = 0X56987BD5
    QUALNAME = "functions.messages.deleteRevokedExportedChatInvites"

    def __init__(self, peer: Any = None, admin_id: Any = None) -> None:
        self.peer = peer
        self.admin_id = admin_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += (self.admin_id.write() if hasattr(self.admin_id, 'write') else write_bytes(self.admin_id))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesDeleteSavedHistory(TLRequest[Any]):
    ID = 0X4DC5085F
    QUALNAME = "functions.messages.deleteSavedHistory"

    def __init__(self, parent_peer: Any = None, peer: Any = None, max_id: Any = None, min_date: Any = None, max_date: Any = None) -> None:
        self.parent_peer = parent_peer
        self.peer = peer
        self.max_id = max_id
        self.min_date = min_date
        self.max_date = max_date

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'parent_peer', None) is not None and getattr(self, 'parent_peer', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'min_date', None) is not None and getattr(self, 'min_date', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'max_date', None) is not None and getattr(self, 'max_date', None) is not False:
            flags |= (1 << 3)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'parent_peer', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.max_id)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'min_date', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 3)):
            v = getattr(self, 'max_date', None) or 0
            if v is not None:
                res += write_int(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesDeleteScheduledMessages(TLRequest[Any]):
    ID = 0X59AE2B16
    QUALNAME = "functions.messages.deleteScheduledMessages"

    def __init__(self, peer: Any = None, id: Any = None) -> None:
        self.peer = peer
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_vector(self.id, write_int)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesDeleteTopicHistory(TLRequest[Any]):
    ID = 0XD2816F10
    QUALNAME = "functions.messages.deleteTopicHistory"

    def __init__(self, peer: Any = None, top_msg_id: Any = None) -> None:
        self.peer = peer
        self.top_msg_id = top_msg_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.top_msg_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesDiscardEncryption(TLRequest[Any]):
    ID = 0XF393AEA0
    QUALNAME = "functions.messages.discardEncryption"

    def __init__(self, delete_history: Any = None, chat_id: Any = None) -> None:
        self.delete_history = delete_history
        self.chat_id = chat_id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'delete_history', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_int(self.chat_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesEditChatAbout(TLRequest[Any]):
    ID = 0XDEF60797
    QUALNAME = "functions.messages.editChatAbout"

    def __init__(self, peer: Any = None, about: Any = None) -> None:
        self.peer = peer
        self.about = about

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_string(self.about)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesEditChatAdmin(TLRequest[Any]):
    ID = 0XA85BD1C2
    QUALNAME = "functions.messages.editChatAdmin"

    def __init__(self, chat_id: Any = None, user_id: Any = None, is_admin: Any = None) -> None:
        self.chat_id = chat_id
        self.user_id = user_id
        self.is_admin = is_admin

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.chat_id)
        res += (self.user_id.write() if hasattr(self.user_id, 'write') else write_bytes(self.user_id))
        res += write_bool(self.is_admin)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesEditChatCreator(TLRequest[Any]):
    ID = 0XF743B857
    QUALNAME = "functions.messages.editChatCreator"

    def __init__(self, peer: Any = None, user_id: Any = None, password: Any = None) -> None:
        self.peer = peer
        self.user_id = user_id
        self.password = password

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += (self.user_id.write() if hasattr(self.user_id, 'write') else write_bytes(self.user_id))
        res += (self.password.write() if hasattr(self.password, 'write') else write_bytes(self.password))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesEditChatDefaultBannedRights(TLRequest[Any]):
    ID = 0XA5866B41
    QUALNAME = "functions.messages.editChatDefaultBannedRights"

    def __init__(self, peer: Any = None, banned_rights: Any = None) -> None:
        self.peer = peer
        self.banned_rights = banned_rights

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += (self.banned_rights.write() if hasattr(self.banned_rights, 'write') else write_bytes(self.banned_rights))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesEditChatParticipantRank(TLRequest[Any]):
    ID = 0XA00F32B0
    QUALNAME = "functions.messages.editChatParticipantRank"

    def __init__(self, peer: Any = None, participant: Any = None, rank: Any = None) -> None:
        self.peer = peer
        self.participant = participant
        self.rank = rank

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += (self.participant.write() if hasattr(self.participant, 'write') else write_bytes(self.participant))
        res += write_string(self.rank)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesEditChatPhoto(TLRequest[Any]):
    ID = 0X35DDD674
    QUALNAME = "functions.messages.editChatPhoto"

    def __init__(self, chat_id: Any = None, photo: Any = None) -> None:
        self.chat_id = chat_id
        self.photo = photo

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.chat_id)
        res += (self.photo.write() if hasattr(self.photo, 'write') else write_bytes(self.photo))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesEditChatTitle(TLRequest[Any]):
    ID = 0X73783FFD
    QUALNAME = "functions.messages.editChatTitle"

    def __init__(self, chat_id: Any = None, title: Any = None) -> None:
        self.chat_id = chat_id
        self.title = title

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.chat_id)
        res += write_string(self.title)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesEditExportedChatInvite(TLRequest[Any]):
    ID = 0XBDCA2F75
    QUALNAME = "functions.messages.editExportedChatInvite"

    def __init__(self, revoked: Any = None, peer: Any = None, link: Any = None, expire_date: Any = None, usage_limit: Any = None, request_needed: Any = None, title: Any = None) -> None:
        self.revoked = revoked
        self.peer = peer
        self.link = link
        self.expire_date = expire_date
        self.usage_limit = usage_limit
        self.request_needed = request_needed
        self.title = title

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'revoked', None):
            flags |= (1 << 2)
        if getattr(self, 'expire_date', None) is not None and getattr(self, 'expire_date', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'usage_limit', None) is not None and getattr(self, 'usage_limit', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'request_needed', None) is not None and getattr(self, 'request_needed', None) is not False:
            flags |= (1 << 3)
        if getattr(self, 'title', None) is not None and getattr(self, 'title', None) is not False:
            flags |= (1 << 4)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_string(self.link)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'expire_date', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'usage_limit', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 3)):
            v = getattr(self, 'request_needed', None)
            if v is not None:
                res += write_bool(v)
        if bool(flags & (1 << 4)):
            v = getattr(self, 'title', None) or ''
            if v is not None:
                res += write_string(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesEditFactCheck(TLRequest[Any]):
    ID = 0X589EE75
    QUALNAME = "functions.messages.editFactCheck"

    def __init__(self, peer: Any = None, msg_id: Any = None, text: Any = None) -> None:
        self.peer = peer
        self.msg_id = msg_id
        self.text = text

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.msg_id)
        res += (self.text.write() if hasattr(self.text, 'write') else write_bytes(self.text))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesEditForumTopic(TLRequest[Any]):
    ID = 0XCECC1134
    QUALNAME = "functions.messages.editForumTopic"

    def __init__(self, peer: Any = None, topic_id: Any = None, title: Any = None, icon_emoji_id: Any = None, closed: Any = None, hidden: Any = None) -> None:
        self.peer = peer
        self.topic_id = topic_id
        self.title = title
        self.icon_emoji_id = icon_emoji_id
        self.closed = closed
        self.hidden = hidden

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'title', None) is not None and getattr(self, 'title', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'icon_emoji_id', None) is not None and getattr(self, 'icon_emoji_id', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'closed', None) is not None and getattr(self, 'closed', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'hidden', None) is not None and getattr(self, 'hidden', None) is not False:
            flags |= (1 << 3)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.topic_id)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'title', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'icon_emoji_id', None) or 0
            if v is not None:
                res += write_long(v)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'closed', None)
            if v is not None:
                res += write_bool(v)
        if bool(flags & (1 << 3)):
            v = getattr(self, 'hidden', None)
            if v is not None:
                res += write_bool(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesEditInlineBotMessage(TLRequest[Any]):
    ID = 0XA423BB51
    QUALNAME = "functions.messages.editInlineBotMessage"

    def __init__(self, no_webpage: Any = None, invert_media: Any = None, id: Any = None, message: Any = None, media: Any = None, reply_markup: Any = None, entities: Any = None, rich_message: Any = None) -> None:
        self.no_webpage = no_webpage
        self.invert_media = invert_media
        self.id = id
        self.message = message
        self.media = media
        self.reply_markup = reply_markup
        self.entities = entities
        self.rich_message = rich_message

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'no_webpage', None):
            flags |= (1 << 1)
        if getattr(self, 'invert_media', None):
            flags |= (1 << 16)
        if getattr(self, 'message', None) is not None and getattr(self, 'message', None) is not False:
            flags |= (1 << 11)
        if getattr(self, 'media', None) is not None and getattr(self, 'media', None) is not False:
            flags |= (1 << 14)
        if getattr(self, 'reply_markup', None) is not None and getattr(self, 'reply_markup', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'entities', None) is not None and getattr(self, 'entities', None) is not False:
            flags |= (1 << 3)
        if getattr(self, 'rich_message', None) is not None and getattr(self, 'rich_message', None) is not False:
            flags |= (1 << 23)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.id.write() if hasattr(self.id, 'write') else write_bytes(self.id))
        if bool(flags & (1 << 11)):
            v = getattr(self, 'message', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 14)):
            v = getattr(self, 'media', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 2)):
            v = getattr(self, 'reply_markup', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 3)):
            v = getattr(self, 'entities', None) or []
            if v is not None:
                res += write_vector(v, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        if bool(flags & (1 << 23)):
            v = getattr(self, 'rich_message', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesEditMessage(TLRequest[Any]):
    ID = 0XB106E66C
    QUALNAME = "functions.messages.editMessage"

    def __init__(self, no_webpage: Any = None, invert_media: Any = None, peer: Any = None, id: Any = None, message: Any = None, media: Any = None, reply_markup: Any = None, entities: Any = None, schedule_date: Any = None, schedule_repeat_period: Any = None, quick_reply_shortcut_id: Any = None, rich_message: Any = None) -> None:
        self.no_webpage = no_webpage
        self.invert_media = invert_media
        self.peer = peer
        self.id = id
        self.message = message
        self.media = media
        self.reply_markup = reply_markup
        self.entities = entities
        self.schedule_date = schedule_date
        self.schedule_repeat_period = schedule_repeat_period
        self.quick_reply_shortcut_id = quick_reply_shortcut_id
        self.rich_message = rich_message

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'no_webpage', None):
            flags |= (1 << 1)
        if getattr(self, 'invert_media', None):
            flags |= (1 << 16)
        if getattr(self, 'message', None) is not None and getattr(self, 'message', None) is not False:
            flags |= (1 << 11)
        if getattr(self, 'media', None) is not None and getattr(self, 'media', None) is not False:
            flags |= (1 << 14)
        if getattr(self, 'reply_markup', None) is not None and getattr(self, 'reply_markup', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'entities', None) is not None and getattr(self, 'entities', None) is not False:
            flags |= (1 << 3)
        if getattr(self, 'schedule_date', None) is not None and getattr(self, 'schedule_date', None) is not False:
            flags |= (1 << 15)
        if getattr(self, 'schedule_repeat_period', None) is not None and getattr(self, 'schedule_repeat_period', None) is not False:
            flags |= (1 << 18)
        if getattr(self, 'quick_reply_shortcut_id', None) is not None and getattr(self, 'quick_reply_shortcut_id', None) is not False:
            flags |= (1 << 17)
        if getattr(self, 'rich_message', None) is not None and getattr(self, 'rich_message', None) is not False:
            flags |= (1 << 23)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.id)
        if bool(flags & (1 << 11)):
            v = getattr(self, 'message', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 14)):
            v = getattr(self, 'media', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 2)):
            v = getattr(self, 'reply_markup', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 3)):
            v = getattr(self, 'entities', None) or []
            if v is not None:
                res += write_vector(v, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        if bool(flags & (1 << 15)):
            v = getattr(self, 'schedule_date', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 18)):
            v = getattr(self, 'schedule_repeat_period', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 17)):
            v = getattr(self, 'quick_reply_shortcut_id', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 23)):
            v = getattr(self, 'rich_message', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesEditQuickReplyShortcut(TLRequest[Any]):
    ID = 0X5C003CEF
    QUALNAME = "functions.messages.editQuickReplyShortcut"

    def __init__(self, shortcut_id: Any = None, shortcut: Any = None) -> None:
        self.shortcut_id = shortcut_id
        self.shortcut = shortcut

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.shortcut_id)
        res += write_string(self.shortcut)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesExportChatInvite(TLRequest[Any]):
    ID = 0XA455DE90
    QUALNAME = "functions.messages.exportChatInvite"

    def __init__(self, legacy_revoke_permanent: Any = None, request_needed: Any = None, peer: Any = None, expire_date: Any = None, usage_limit: Any = None, title: Any = None, subscription_pricing: Any = None) -> None:
        self.legacy_revoke_permanent = legacy_revoke_permanent
        self.request_needed = request_needed
        self.peer = peer
        self.expire_date = expire_date
        self.usage_limit = usage_limit
        self.title = title
        self.subscription_pricing = subscription_pricing

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'legacy_revoke_permanent', None):
            flags |= (1 << 2)
        if getattr(self, 'request_needed', None):
            flags |= (1 << 3)
        if getattr(self, 'expire_date', None) is not None and getattr(self, 'expire_date', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'usage_limit', None) is not None and getattr(self, 'usage_limit', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'title', None) is not None and getattr(self, 'title', None) is not False:
            flags |= (1 << 4)
        if getattr(self, 'subscription_pricing', None) is not None and getattr(self, 'subscription_pricing', None) is not False:
            flags |= (1 << 5)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'expire_date', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'usage_limit', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 4)):
            v = getattr(self, 'title', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 5)):
            v = getattr(self, 'subscription_pricing', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesFaveSticker(TLRequest[Any]):
    ID = 0XB9FFC55B
    QUALNAME = "functions.messages.faveSticker"

    def __init__(self, id: Any = None, unfave: Any = None) -> None:
        self.id = id
        self.unfave = unfave

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.id.write() if hasattr(self.id, 'write') else write_bytes(self.id))
        res += write_bool(self.unfave)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesForwardMessages(TLRequest[Any]):
    ID = 0X13704A7C
    QUALNAME = "functions.messages.forwardMessages"

    def __init__(self, silent: Any = None, background: Any = None, with_my_score: Any = None, drop_author: Any = None, drop_media_captions: Any = None, noforwards: Any = None, allow_paid_floodskip: Any = None, from_ephemeral: Any = None, from_peer: Any = None, id: Any = None, random_id: Any = None, to_peer: Any = None, top_msg_id: Any = None, reply_to: Any = None, schedule_date: Any = None, schedule_repeat_period: Any = None, send_as: Any = None, quick_reply_shortcut: Any = None, effect: Any = None, video_timestamp: Any = None, allow_paid_stars: Any = None, suggested_post: Any = None) -> None:
        self.silent = silent
        self.background = background
        self.with_my_score = with_my_score
        self.drop_author = drop_author
        self.drop_media_captions = drop_media_captions
        self.noforwards = noforwards
        self.allow_paid_floodskip = allow_paid_floodskip
        self.from_ephemeral = from_ephemeral
        self.from_peer = from_peer
        self.id = id
        self.random_id = random_id
        self.to_peer = to_peer
        self.top_msg_id = top_msg_id
        self.reply_to = reply_to
        self.schedule_date = schedule_date
        self.schedule_repeat_period = schedule_repeat_period
        self.send_as = send_as
        self.quick_reply_shortcut = quick_reply_shortcut
        self.effect = effect
        self.video_timestamp = video_timestamp
        self.allow_paid_stars = allow_paid_stars
        self.suggested_post = suggested_post

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'silent', None):
            flags |= (1 << 5)
        if getattr(self, 'background', None):
            flags |= (1 << 6)
        if getattr(self, 'with_my_score', None):
            flags |= (1 << 8)
        if getattr(self, 'drop_author', None):
            flags |= (1 << 11)
        if getattr(self, 'drop_media_captions', None):
            flags |= (1 << 12)
        if getattr(self, 'noforwards', None):
            flags |= (1 << 14)
        if getattr(self, 'allow_paid_floodskip', None):
            flags |= (1 << 19)
        if getattr(self, 'from_ephemeral', None):
            flags |= (1 << 25)
        if getattr(self, 'top_msg_id', None) is not None and getattr(self, 'top_msg_id', None) is not False:
            flags |= (1 << 9)
        if getattr(self, 'reply_to', None) is not None and getattr(self, 'reply_to', None) is not False:
            flags |= (1 << 22)
        if getattr(self, 'schedule_date', None) is not None and getattr(self, 'schedule_date', None) is not False:
            flags |= (1 << 10)
        if getattr(self, 'schedule_repeat_period', None) is not None and getattr(self, 'schedule_repeat_period', None) is not False:
            flags |= (1 << 24)
        if getattr(self, 'send_as', None) is not None and getattr(self, 'send_as', None) is not False:
            flags |= (1 << 13)
        if getattr(self, 'quick_reply_shortcut', None) is not None and getattr(self, 'quick_reply_shortcut', None) is not False:
            flags |= (1 << 17)
        if getattr(self, 'effect', None) is not None and getattr(self, 'effect', None) is not False:
            flags |= (1 << 18)
        if getattr(self, 'video_timestamp', None) is not None and getattr(self, 'video_timestamp', None) is not False:
            flags |= (1 << 20)
        if getattr(self, 'allow_paid_stars', None) is not None and getattr(self, 'allow_paid_stars', None) is not False:
            flags |= (1 << 21)
        if getattr(self, 'suggested_post', None) is not None and getattr(self, 'suggested_post', None) is not False:
            flags |= (1 << 23)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.from_peer.write() if hasattr(self.from_peer, 'write') else write_bytes(self.from_peer))
        res += write_vector(self.id, write_int)
        res += write_vector(self.random_id, write_long)
        res += (self.to_peer.write() if hasattr(self.to_peer, 'write') else write_bytes(self.to_peer))
        if bool(flags & (1 << 9)):
            v = getattr(self, 'top_msg_id', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 22)):
            v = getattr(self, 'reply_to', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 10)):
            v = getattr(self, 'schedule_date', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 24)):
            v = getattr(self, 'schedule_repeat_period', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 13)):
            v = getattr(self, 'send_as', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 17)):
            v = getattr(self, 'quick_reply_shortcut', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 18)):
            v = getattr(self, 'effect', None) or 0
            if v is not None:
                res += write_long(v)
        if bool(flags & (1 << 20)):
            v = getattr(self, 'video_timestamp', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 21)):
            v = getattr(self, 'allow_paid_stars', None) or 0
            if v is not None:
                res += write_long(v)
        if bool(flags & (1 << 23)):
            v = getattr(self, 'suggested_post', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetAdminsWithInvites(TLRequest[Any]):
    ID = 0X3920E6EF
    QUALNAME = "functions.messages.getAdminsWithInvites"

    def __init__(self, peer: Any = None) -> None:
        self.peer = peer

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetAllDrafts(TLRequest[Any]):
    ID = 0X6A3F8D65
    QUALNAME = "functions.messages.getAllDrafts"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetAllStickers(TLRequest[Any]):
    ID = 0XB8A0A1A8
    QUALNAME = "functions.messages.getAllStickers"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetArchivedStickers(TLRequest[Any]):
    ID = 0X57F17692
    QUALNAME = "functions.messages.getArchivedStickers"

    def __init__(self, masks: Any = None, emojis: Any = None, offset_id: Any = None, limit: Any = None) -> None:
        self.masks = masks
        self.emojis = emojis
        self.offset_id = offset_id
        self.limit = limit

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'masks', None):
            flags |= (1 << 0)
        if getattr(self, 'emojis', None):
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_long(self.offset_id)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetAttachMenuBot(TLRequest[Any]):
    ID = 0X77216192
    QUALNAME = "functions.messages.getAttachMenuBot"

    def __init__(self, bot: Any = None) -> None:
        self.bot = bot

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetAttachMenuBots(TLRequest[Any]):
    ID = 0X16FCC2CB
    QUALNAME = "functions.messages.getAttachMenuBots"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetAttachedStickers(TLRequest[Any]):
    ID = 0XCC5B67CC
    QUALNAME = "functions.messages.getAttachedStickers"

    def __init__(self, media: Any = None) -> None:
        self.media = media

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.media.write() if hasattr(self.media, 'write') else write_bytes(self.media))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetAvailableEffects(TLRequest[Any]):
    ID = 0XDEA20A39
    QUALNAME = "functions.messages.getAvailableEffects"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetAvailableReactions(TLRequest[Any]):
    ID = 0X18DEA0AC
    QUALNAME = "functions.messages.getAvailableReactions"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetBotApp(TLRequest[Any]):
    ID = 0X34FDC5C3
    QUALNAME = "functions.messages.getBotApp"

    def __init__(self, app: Any = None, hash: Any = None) -> None:
        self.app = app
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.app.write() if hasattr(self.app, 'write') else write_bytes(self.app))
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetBotCallbackAnswer(TLRequest[Any]):
    ID = 0X9342CA07
    QUALNAME = "functions.messages.getBotCallbackAnswer"

    def __init__(self, game: Any = None, peer: Any = None, msg_id: Any = None, data: Any = None, password: Any = None) -> None:
        self.game = game
        self.peer = peer
        self.msg_id = msg_id
        self.data = data
        self.password = password

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'game', None):
            flags |= (1 << 1)
        if getattr(self, 'data', None) is not None and getattr(self, 'data', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'password', None) is not None and getattr(self, 'password', None) is not False:
            flags |= (1 << 2)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.msg_id)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'data', None) or b''
            if v is not None:
                res += write_bytes(v)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'password', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetChatInviteImporters(TLRequest[Any]):
    ID = 0XDF04DD4E
    QUALNAME = "functions.messages.getChatInviteImporters"

    def __init__(self, requested: Any = None, subscription_expired: Any = None, peer: Any = None, link: Any = None, q: Any = None, offset_date: Any = None, offset_user: Any = None, limit: Any = None) -> None:
        self.requested = requested
        self.subscription_expired = subscription_expired
        self.peer = peer
        self.link = link
        self.q = q
        self.offset_date = offset_date
        self.offset_user = offset_user
        self.limit = limit

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'requested', None):
            flags |= (1 << 0)
        if getattr(self, 'subscription_expired', None):
            flags |= (1 << 3)
        if getattr(self, 'link', None) is not None and getattr(self, 'link', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'q', None) is not None and getattr(self, 'q', None) is not False:
            flags |= (1 << 2)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        if bool(flags & (1 << 1)):
            v = getattr(self, 'link', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'q', None) or ''
            if v is not None:
                res += write_string(v)
        res += write_int(self.offset_date)
        res += (self.offset_user.write() if hasattr(self.offset_user, 'write') else write_bytes(self.offset_user))
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetChats(TLRequest[Any]):
    ID = 0X49E9528F
    QUALNAME = "functions.messages.getChats"

    def __init__(self, id: Any = None) -> None:
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_vector(self.id, write_long)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetCommonChats(TLRequest[Any]):
    ID = 0XE40CA104
    QUALNAME = "functions.messages.getCommonChats"

    def __init__(self, user_id: Any = None, max_id: Any = None, limit: Any = None) -> None:
        self.user_id = user_id
        self.max_id = max_id
        self.limit = limit

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.user_id.write() if hasattr(self.user_id, 'write') else write_bytes(self.user_id))
        res += write_long(self.max_id)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetCustomEmojiDocuments(TLRequest[Any]):
    ID = 0XD9AB0F54
    QUALNAME = "functions.messages.getCustomEmojiDocuments"

    def __init__(self, document_id: Any = None) -> None:
        self.document_id = document_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_vector(self.document_id, write_long)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetDefaultHistoryTtl(TLRequest[Any]):
    ID = 0X658B7188
    QUALNAME = "functions.messages.getDefaultHistoryTTL"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetDefaultTagReactions(TLRequest[Any]):
    ID = 0XBDF93428
    QUALNAME = "functions.messages.getDefaultTagReactions"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetDhConfig(TLRequest[Any]):
    ID = 0X26CF8950
    QUALNAME = "functions.messages.getDhConfig"

    def __init__(self, version: Any = None, random_length: Any = None) -> None:
        self.version = version
        self.random_length = random_length

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.version)
        res += write_int(self.random_length)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetDialogFilters(TLRequest[Any]):
    ID = 0XEFD48C89
    QUALNAME = "functions.messages.getDialogFilters"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetDialogUnreadMarks(TLRequest[Any]):
    ID = 0X21202222
    QUALNAME = "functions.messages.getDialogUnreadMarks"

    def __init__(self, parent_peer: Any = None) -> None:
        self.parent_peer = parent_peer

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'parent_peer', None) is not None and getattr(self, 'parent_peer', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'parent_peer', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetDialogs(TLRequest[Any]):
    ID = 0XA0F4CB4F
    QUALNAME = "functions.messages.getDialogs"

    def __init__(self, exclude_pinned: Any = None, folder_id: Any = None, offset_date: Any = None, offset_id: Any = None, offset_peer: Any = None, limit: Any = None, hash: Any = None) -> None:
        self.exclude_pinned = exclude_pinned
        self.folder_id = folder_id
        self.offset_date = offset_date
        self.offset_id = offset_id
        self.offset_peer = offset_peer
        self.limit = limit
        self.hash = hash

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'exclude_pinned', None):
            flags |= (1 << 0)
        if getattr(self, 'folder_id', None) is not None and getattr(self, 'folder_id', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'folder_id', None) or 0
            if v is not None:
                res += write_int(v)
        res += write_int(self.offset_date)
        res += write_int(self.offset_id)
        res += (self.offset_peer.write() if hasattr(self.offset_peer, 'write') else write_bytes(self.offset_peer))
        res += write_int(self.limit)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetDiscussionMessage(TLRequest[Any]):
    ID = 0X446972FD
    QUALNAME = "functions.messages.getDiscussionMessage"

    def __init__(self, peer: Any = None, msg_id: Any = None) -> None:
        self.peer = peer
        self.msg_id = msg_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.msg_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetDocumentByHash(TLRequest[Any]):
    ID = 0XB1F2061F
    QUALNAME = "functions.messages.getDocumentByHash"

    def __init__(self, sha256: Any = None, size: Any = None, mime_type: Any = None) -> None:
        self.sha256 = sha256
        self.size = size
        self.mime_type = mime_type

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_bytes(self.sha256)
        res += write_long(self.size)
        res += write_string(self.mime_type)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetEmojiGameInfo(TLRequest[Any]):
    ID = 0XFB7E8CA7
    QUALNAME = "functions.messages.getEmojiGameInfo"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetEmojiGroups(TLRequest[Any]):
    ID = 0X7488CE5B
    QUALNAME = "functions.messages.getEmojiGroups"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetEmojiKeywords(TLRequest[Any]):
    ID = 0X35A0E062
    QUALNAME = "functions.messages.getEmojiKeywords"

    def __init__(self, lang_code: Any = None) -> None:
        self.lang_code = lang_code

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.lang_code)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetEmojiKeywordsDifference(TLRequest[Any]):
    ID = 0X1508B6AF
    QUALNAME = "functions.messages.getEmojiKeywordsDifference"

    def __init__(self, lang_code: Any = None, from_version: Any = None) -> None:
        self.lang_code = lang_code
        self.from_version = from_version

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.lang_code)
        res += write_int(self.from_version)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetEmojiKeywordsLanguages(TLRequest[Any]):
    ID = 0X4E9963B2
    QUALNAME = "functions.messages.getEmojiKeywordsLanguages"

    def __init__(self, lang_codes: Any = None) -> None:
        self.lang_codes = lang_codes

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_vector(self.lang_codes, write_string)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetEmojiProfilePhotoGroups(TLRequest[Any]):
    ID = 0X21A548F3
    QUALNAME = "functions.messages.getEmojiProfilePhotoGroups"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetEmojiStatusGroups(TLRequest[Any]):
    ID = 0X2ECD56CD
    QUALNAME = "functions.messages.getEmojiStatusGroups"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetEmojiStickerGroups(TLRequest[Any]):
    ID = 0X1DD840F5
    QUALNAME = "functions.messages.getEmojiStickerGroups"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetEmojiStickers(TLRequest[Any]):
    ID = 0XFBFCA18F
    QUALNAME = "functions.messages.getEmojiStickers"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetEmojiUrl(TLRequest[Any]):
    ID = 0XD5B10C26
    QUALNAME = "functions.messages.getEmojiURL"

    def __init__(self, lang_code: Any = None) -> None:
        self.lang_code = lang_code

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.lang_code)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetExportedChatInvite(TLRequest[Any]):
    ID = 0X73746F5C
    QUALNAME = "functions.messages.getExportedChatInvite"

    def __init__(self, peer: Any = None, link: Any = None) -> None:
        self.peer = peer
        self.link = link

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_string(self.link)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetExportedChatInvites(TLRequest[Any]):
    ID = 0XA2B5A3F6
    QUALNAME = "functions.messages.getExportedChatInvites"

    def __init__(self, revoked: Any = None, peer: Any = None, admin_id: Any = None, offset_date: Any = None, offset_link: Any = None, limit: Any = None) -> None:
        self.revoked = revoked
        self.peer = peer
        self.admin_id = admin_id
        self.offset_date = offset_date
        self.offset_link = offset_link
        self.limit = limit

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'revoked', None):
            flags |= (1 << 3)
        if getattr(self, 'offset_date', None) is not None and getattr(self, 'offset_date', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'offset_link', None) is not None and getattr(self, 'offset_link', None) is not False:
            flags |= (1 << 2)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += (self.admin_id.write() if hasattr(self.admin_id, 'write') else write_bytes(self.admin_id))
        if bool(flags & (1 << 2)):
            v = getattr(self, 'offset_date', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'offset_link', None) or ''
            if v is not None:
                res += write_string(v)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetExtendedMedia(TLRequest[Any]):
    ID = 0X84F80814
    QUALNAME = "functions.messages.getExtendedMedia"

    def __init__(self, peer: Any = None, id: Any = None) -> None:
        self.peer = peer
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_vector(self.id, write_int)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetFactCheck(TLRequest[Any]):
    ID = 0XB9CDC5EE
    QUALNAME = "functions.messages.getFactCheck"

    def __init__(self, peer: Any = None, msg_id: Any = None) -> None:
        self.peer = peer
        self.msg_id = msg_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_vector(self.msg_id, write_int)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetFavedStickers(TLRequest[Any]):
    ID = 0X4F1AAA9
    QUALNAME = "functions.messages.getFavedStickers"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetFeaturedEmojiStickers(TLRequest[Any]):
    ID = 0XECF6736
    QUALNAME = "functions.messages.getFeaturedEmojiStickers"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetFeaturedStickers(TLRequest[Any]):
    ID = 0X64780B14
    QUALNAME = "functions.messages.getFeaturedStickers"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetForumTopics(TLRequest[Any]):
    ID = 0X3BA47BFF
    QUALNAME = "functions.messages.getForumTopics"

    def __init__(self, peer: Any = None, q: Any = None, offset_date: Any = None, offset_id: Any = None, offset_topic: Any = None, limit: Any = None) -> None:
        self.peer = peer
        self.q = q
        self.offset_date = offset_date
        self.offset_id = offset_id
        self.offset_topic = offset_topic
        self.limit = limit

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'q', None) is not None and getattr(self, 'q', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'q', None) or ''
            if v is not None:
                res += write_string(v)
        res += write_int(self.offset_date)
        res += write_int(self.offset_id)
        res += write_int(self.offset_topic)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetForumTopicsById(TLRequest[Any]):
    ID = 0XAF0A4A08
    QUALNAME = "functions.messages.getForumTopicsByID"

    def __init__(self, peer: Any = None, topics: Any = None) -> None:
        self.peer = peer
        self.topics = topics

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_vector(self.topics, write_int)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetFullChat(TLRequest[Any]):
    ID = 0XAEB00B34
    QUALNAME = "functions.messages.getFullChat"

    def __init__(self, chat_id: Any = None) -> None:
        self.chat_id = chat_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.chat_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetFutureChatCreatorAfterLeave(TLRequest[Any]):
    ID = 0X3B7D0EA6
    QUALNAME = "functions.messages.getFutureChatCreatorAfterLeave"

    def __init__(self, peer: Any = None) -> None:
        self.peer = peer

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetGameHighScores(TLRequest[Any]):
    ID = 0XE822649D
    QUALNAME = "functions.messages.getGameHighScores"

    def __init__(self, peer: Any = None, id: Any = None, user_id: Any = None) -> None:
        self.peer = peer
        self.id = id
        self.user_id = user_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.id)
        res += (self.user_id.write() if hasattr(self.user_id, 'write') else write_bytes(self.user_id))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetHistory(TLRequest[Any]):
    ID = 0X4423E6C5
    QUALNAME = "functions.messages.getHistory"

    def __init__(self, peer: Any = None, offset_id: Any = None, offset_date: Any = None, add_offset: Any = None, limit: Any = None, max_id: Any = None, min_id: Any = None, hash: Any = None) -> None:
        self.peer = peer
        self.offset_id = offset_id
        self.offset_date = offset_date
        self.add_offset = add_offset
        self.limit = limit
        self.max_id = max_id
        self.min_id = min_id
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.offset_id)
        res += write_int(self.offset_date)
        res += write_int(self.add_offset)
        res += write_int(self.limit)
        res += write_int(self.max_id)
        res += write_int(self.min_id)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetInlineBotResults(TLRequest[Any]):
    ID = 0X514E999D
    QUALNAME = "functions.messages.getInlineBotResults"

    def __init__(self, bot: Any = None, peer: Any = None, geo_point: Any = None, query: Any = None, offset: Any = None) -> None:
        self.bot = bot
        self.peer = peer
        self.geo_point = geo_point
        self.query = query
        self.offset = offset

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'geo_point', None) is not None and getattr(self, 'geo_point', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'geo_point', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += write_string(self.query)
        res += write_string(self.offset)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetInlineGameHighScores(TLRequest[Any]):
    ID = 0XF635E1B
    QUALNAME = "functions.messages.getInlineGameHighScores"

    def __init__(self, id: Any = None, user_id: Any = None) -> None:
        self.id = id
        self.user_id = user_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.id.write() if hasattr(self.id, 'write') else write_bytes(self.id))
        res += (self.user_id.write() if hasattr(self.user_id, 'write') else write_bytes(self.user_id))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetMaskStickers(TLRequest[Any]):
    ID = 0X640F82B8
    QUALNAME = "functions.messages.getMaskStickers"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetMessageEditData(TLRequest[Any]):
    ID = 0XFDA68D36
    QUALNAME = "functions.messages.getMessageEditData"

    def __init__(self, peer: Any = None, id: Any = None) -> None:
        self.peer = peer
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetMessageReactionsList(TLRequest[Any]):
    ID = 0X461B3F48
    QUALNAME = "functions.messages.getMessageReactionsList"

    def __init__(self, peer: Any = None, id: Any = None, reaction: Any = None, offset: Any = None, limit: Any = None) -> None:
        self.peer = peer
        self.id = id
        self.reaction = reaction
        self.offset = offset
        self.limit = limit

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'reaction', None) is not None and getattr(self, 'reaction', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'offset', None) is not None and getattr(self, 'offset', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.id)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'reaction', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 1)):
            v = getattr(self, 'offset', None) or ''
            if v is not None:
                res += write_string(v)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetMessageReadParticipants(TLRequest[Any]):
    ID = 0X31C1C44F
    QUALNAME = "functions.messages.getMessageReadParticipants"

    def __init__(self, peer: Any = None, msg_id: Any = None) -> None:
        self.peer = peer
        self.msg_id = msg_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.msg_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetMessages(TLRequest[Any]):
    ID = 0X63C66506
    QUALNAME = "functions.messages.getMessages"

    def __init__(self, id: Any = None) -> None:
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_vector(self.id, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetMessagesReactions(TLRequest[Any]):
    ID = 0X8BBA90E6
    QUALNAME = "functions.messages.getMessagesReactions"

    def __init__(self, peer: Any = None, id: Any = None) -> None:
        self.peer = peer
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_vector(self.id, write_int)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetMessagesViews(TLRequest[Any]):
    ID = 0X5784D3E1
    QUALNAME = "functions.messages.getMessagesViews"

    def __init__(self, peer: Any = None, id: Any = None, increment: Any = None) -> None:
        self.peer = peer
        self.id = id
        self.increment = increment

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_vector(self.id, write_int)
        res += write_bool(self.increment)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetMyStickers(TLRequest[Any]):
    ID = 0XD0B5E1FC
    QUALNAME = "functions.messages.getMyStickers"

    def __init__(self, offset_id: Any = None, limit: Any = None) -> None:
        self.offset_id = offset_id
        self.limit = limit

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.offset_id)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetOldFeaturedStickers(TLRequest[Any]):
    ID = 0X7ED094A1
    QUALNAME = "functions.messages.getOldFeaturedStickers"

    def __init__(self, offset: Any = None, limit: Any = None, hash: Any = None) -> None:
        self.offset = offset
        self.limit = limit
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.offset)
        res += write_int(self.limit)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetOnlines(TLRequest[Any]):
    ID = 0X6E2BE050
    QUALNAME = "functions.messages.getOnlines"

    def __init__(self, peer: Any = None) -> None:
        self.peer = peer

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetOutboxReadDate(TLRequest[Any]):
    ID = 0X8C4BFE5D
    QUALNAME = "functions.messages.getOutboxReadDate"

    def __init__(self, peer: Any = None, msg_id: Any = None) -> None:
        self.peer = peer
        self.msg_id = msg_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.msg_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetPaidReactionPrivacy(TLRequest[Any]):
    ID = 0X472455AA
    QUALNAME = "functions.messages.getPaidReactionPrivacy"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetPeerDialogs(TLRequest[Any]):
    ID = 0XE470BCFD
    QUALNAME = "functions.messages.getPeerDialogs"

    def __init__(self, peers: Any = None) -> None:
        self.peers = peers

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_vector(self.peers, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetPeerSettings(TLRequest[Any]):
    ID = 0XEFD9A6A2
    QUALNAME = "functions.messages.getPeerSettings"

    def __init__(self, peer: Any = None) -> None:
        self.peer = peer

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetPersonalChannelHistory(TLRequest[Any]):
    ID = 0X55FB0996
    QUALNAME = "functions.messages.getPersonalChannelHistory"

    def __init__(self, user_id: Any = None, limit: Any = None, max_id: Any = None, min_id: Any = None, hash: Any = None) -> None:
        self.user_id = user_id
        self.limit = limit
        self.max_id = max_id
        self.min_id = min_id
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.user_id.write() if hasattr(self.user_id, 'write') else write_bytes(self.user_id))
        res += write_int(self.limit)
        res += write_int(self.max_id)
        res += write_int(self.min_id)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetPinnedDialogs(TLRequest[Any]):
    ID = 0XD6B94DF2
    QUALNAME = "functions.messages.getPinnedDialogs"

    def __init__(self, folder_id: Any = None) -> None:
        self.folder_id = folder_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.folder_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetPinnedSavedDialogs(TLRequest[Any]):
    ID = 0XD63D94E0
    QUALNAME = "functions.messages.getPinnedSavedDialogs"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetPollResults(TLRequest[Any]):
    ID = 0XEDA3E33B
    QUALNAME = "functions.messages.getPollResults"

    def __init__(self, peer: Any = None, msg_id: Any = None, poll_hash: Any = None) -> None:
        self.peer = peer
        self.msg_id = msg_id
        self.poll_hash = poll_hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.msg_id)
        res += write_long(self.poll_hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetPollVotes(TLRequest[Any]):
    ID = 0XB86E380E
    QUALNAME = "functions.messages.getPollVotes"

    def __init__(self, peer: Any = None, id: Any = None, option: Any = None, offset: Any = None, limit: Any = None) -> None:
        self.peer = peer
        self.id = id
        self.option = option
        self.offset = offset
        self.limit = limit

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'option', None) is not None and getattr(self, 'option', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'offset', None) is not None and getattr(self, 'offset', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.id)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'option', None) or b''
            if v is not None:
                res += write_bytes(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'offset', None) or ''
            if v is not None:
                res += write_string(v)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetPreparedInlineMessage(TLRequest[Any]):
    ID = 0X857EBDB8
    QUALNAME = "functions.messages.getPreparedInlineMessage"

    def __init__(self, bot: Any = None, id: Any = None) -> None:
        self.bot = bot
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        res += write_string(self.id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetQuickReplies(TLRequest[Any]):
    ID = 0XD483F2A8
    QUALNAME = "functions.messages.getQuickReplies"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetQuickReplyMessages(TLRequest[Any]):
    ID = 0X94A495C3
    QUALNAME = "functions.messages.getQuickReplyMessages"

    def __init__(self, shortcut_id: Any = None, id: Any = None, hash: Any = None) -> None:
        self.shortcut_id = shortcut_id
        self.id = id
        self.hash = hash

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'id', None) is not None and getattr(self, 'id', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_int(self.shortcut_id)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'id', None) or []
            if v is not None:
                res += write_vector(v, write_int)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetRecentLocations(TLRequest[Any]):
    ID = 0X702A40E0
    QUALNAME = "functions.messages.getRecentLocations"

    def __init__(self, peer: Any = None, limit: Any = None, hash: Any = None) -> None:
        self.peer = peer
        self.limit = limit
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.limit)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetRecentReactions(TLRequest[Any]):
    ID = 0X39461DB2
    QUALNAME = "functions.messages.getRecentReactions"

    def __init__(self, limit: Any = None, hash: Any = None) -> None:
        self.limit = limit
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.limit)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetRecentStickers(TLRequest[Any]):
    ID = 0X9DA9403B
    QUALNAME = "functions.messages.getRecentStickers"

    def __init__(self, attached: Any = None, hash: Any = None) -> None:
        self.attached = attached
        self.hash = hash

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'attached', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetReplies(TLRequest[Any]):
    ID = 0X22DDD30C
    QUALNAME = "functions.messages.getReplies"

    def __init__(self, peer: Any = None, msg_id: Any = None, offset_id: Any = None, offset_date: Any = None, add_offset: Any = None, limit: Any = None, max_id: Any = None, min_id: Any = None, hash: Any = None) -> None:
        self.peer = peer
        self.msg_id = msg_id
        self.offset_id = offset_id
        self.offset_date = offset_date
        self.add_offset = add_offset
        self.limit = limit
        self.max_id = max_id
        self.min_id = min_id
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.msg_id)
        res += write_int(self.offset_id)
        res += write_int(self.offset_date)
        res += write_int(self.add_offset)
        res += write_int(self.limit)
        res += write_int(self.max_id)
        res += write_int(self.min_id)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetRichMessage(TLRequest[Any]):
    ID = 0X501569CF
    QUALNAME = "functions.messages.getRichMessage"

    def __init__(self, peer: Any = None, id: Any = None) -> None:
        self.peer = peer
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetSavedDialogs(TLRequest[Any]):
    ID = 0X1E91FC99
    QUALNAME = "functions.messages.getSavedDialogs"

    def __init__(self, exclude_pinned: Any = None, parent_peer: Any = None, offset_date: Any = None, offset_id: Any = None, offset_peer: Any = None, limit: Any = None, hash: Any = None) -> None:
        self.exclude_pinned = exclude_pinned
        self.parent_peer = parent_peer
        self.offset_date = offset_date
        self.offset_id = offset_id
        self.offset_peer = offset_peer
        self.limit = limit
        self.hash = hash

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'exclude_pinned', None):
            flags |= (1 << 0)
        if getattr(self, 'parent_peer', None) is not None and getattr(self, 'parent_peer', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'parent_peer', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += write_int(self.offset_date)
        res += write_int(self.offset_id)
        res += (self.offset_peer.write() if hasattr(self.offset_peer, 'write') else write_bytes(self.offset_peer))
        res += write_int(self.limit)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetSavedDialogsById(TLRequest[Any]):
    ID = 0X6F6F9C96
    QUALNAME = "functions.messages.getSavedDialogsByID"

    def __init__(self, parent_peer: Any = None, ids: Any = None) -> None:
        self.parent_peer = parent_peer
        self.ids = ids

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'parent_peer', None) is not None and getattr(self, 'parent_peer', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'parent_peer', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += write_vector(self.ids, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetSavedGifs(TLRequest[Any]):
    ID = 0X5CF09635
    QUALNAME = "functions.messages.getSavedGifs"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetSavedHistory(TLRequest[Any]):
    ID = 0X998AB009
    QUALNAME = "functions.messages.getSavedHistory"

    def __init__(self, parent_peer: Any = None, peer: Any = None, offset_id: Any = None, offset_date: Any = None, add_offset: Any = None, limit: Any = None, max_id: Any = None, min_id: Any = None, hash: Any = None) -> None:
        self.parent_peer = parent_peer
        self.peer = peer
        self.offset_id = offset_id
        self.offset_date = offset_date
        self.add_offset = add_offset
        self.limit = limit
        self.max_id = max_id
        self.min_id = min_id
        self.hash = hash

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'parent_peer', None) is not None and getattr(self, 'parent_peer', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'parent_peer', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.offset_id)
        res += write_int(self.offset_date)
        res += write_int(self.add_offset)
        res += write_int(self.limit)
        res += write_int(self.max_id)
        res += write_int(self.min_id)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetSavedReactionTags(TLRequest[Any]):
    ID = 0X3637E05B
    QUALNAME = "functions.messages.getSavedReactionTags"

    def __init__(self, peer: Any = None, hash: Any = None) -> None:
        self.peer = peer
        self.hash = hash

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'peer', None) is not None and getattr(self, 'peer', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'peer', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetScheduledHistory(TLRequest[Any]):
    ID = 0XF516760B
    QUALNAME = "functions.messages.getScheduledHistory"

    def __init__(self, peer: Any = None, hash: Any = None) -> None:
        self.peer = peer
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetScheduledMessages(TLRequest[Any]):
    ID = 0XBDBB0464
    QUALNAME = "functions.messages.getScheduledMessages"

    def __init__(self, peer: Any = None, id: Any = None) -> None:
        self.peer = peer
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_vector(self.id, write_int)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetSearchCounters(TLRequest[Any]):
    ID = 0X1BBCF300
    QUALNAME = "functions.messages.getSearchCounters"

    def __init__(self, peer: Any = None, saved_peer_id: Any = None, top_msg_id: Any = None, filters: Any = None) -> None:
        self.peer = peer
        self.saved_peer_id = saved_peer_id
        self.top_msg_id = top_msg_id
        self.filters = filters

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'saved_peer_id', None) is not None and getattr(self, 'saved_peer_id', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'top_msg_id', None) is not None and getattr(self, 'top_msg_id', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        if bool(flags & (1 << 2)):
            v = getattr(self, 'saved_peer_id', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'top_msg_id', None) or 0
            if v is not None:
                res += write_int(v)
        res += write_vector(self.filters, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetSearchResultsCalendar(TLRequest[Any]):
    ID = 0X6AA3F6BD
    QUALNAME = "functions.messages.getSearchResultsCalendar"

    def __init__(self, peer: Any = None, saved_peer_id: Any = None, filter: Any = None, offset_id: Any = None, offset_date: Any = None) -> None:
        self.peer = peer
        self.saved_peer_id = saved_peer_id
        self.filter = filter
        self.offset_id = offset_id
        self.offset_date = offset_date

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'saved_peer_id', None) is not None and getattr(self, 'saved_peer_id', None) is not False:
            flags |= (1 << 2)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        if bool(flags & (1 << 2)):
            v = getattr(self, 'saved_peer_id', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += (self.filter.write() if hasattr(self.filter, 'write') else write_bytes(self.filter))
        res += write_int(self.offset_id)
        res += write_int(self.offset_date)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetSearchResultsPositions(TLRequest[Any]):
    ID = 0X9C7F2F10
    QUALNAME = "functions.messages.getSearchResultsPositions"

    def __init__(self, peer: Any = None, saved_peer_id: Any = None, filter: Any = None, offset_id: Any = None, limit: Any = None) -> None:
        self.peer = peer
        self.saved_peer_id = saved_peer_id
        self.filter = filter
        self.offset_id = offset_id
        self.limit = limit

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'saved_peer_id', None) is not None and getattr(self, 'saved_peer_id', None) is not False:
            flags |= (1 << 2)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        if bool(flags & (1 << 2)):
            v = getattr(self, 'saved_peer_id', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += (self.filter.write() if hasattr(self.filter, 'write') else write_bytes(self.filter))
        res += write_int(self.offset_id)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetSplitRanges(TLRequest[Any]):
    ID = 0X1CFF7E08
    QUALNAME = "functions.messages.getSplitRanges"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetSponsoredMessages(TLRequest[Any]):
    ID = 0X3D6CE850
    QUALNAME = "functions.messages.getSponsoredMessages"

    def __init__(self, peer: Any = None, msg_id: Any = None) -> None:
        self.peer = peer
        self.msg_id = msg_id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'msg_id', None) is not None and getattr(self, 'msg_id', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'msg_id', None) or 0
            if v is not None:
                res += write_int(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetStickerSet(TLRequest[Any]):
    ID = 0XC8A0EC74
    QUALNAME = "functions.messages.getStickerSet"

    def __init__(self, stickerset: Any = None, hash: Any = None) -> None:
        self.stickerset = stickerset
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.stickerset.write() if hasattr(self.stickerset, 'write') else write_bytes(self.stickerset))
        res += write_int(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetStickers(TLRequest[Any]):
    ID = 0XD5A5D3A1
    QUALNAME = "functions.messages.getStickers"

    def __init__(self, emoticon: Any = None, hash: Any = None) -> None:
        self.emoticon = emoticon
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.emoticon)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetSuggestedDialogFilters(TLRequest[Any]):
    ID = 0XA29CD42C
    QUALNAME = "functions.messages.getSuggestedDialogFilters"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetTopReactions(TLRequest[Any]):
    ID = 0XBB8125BA
    QUALNAME = "functions.messages.getTopReactions"

    def __init__(self, limit: Any = None, hash: Any = None) -> None:
        self.limit = limit
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.limit)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetUnreadMentions(TLRequest[Any]):
    ID = 0XF107E790
    QUALNAME = "functions.messages.getUnreadMentions"

    def __init__(self, peer: Any = None, top_msg_id: Any = None, offset_id: Any = None, add_offset: Any = None, limit: Any = None, max_id: Any = None, min_id: Any = None) -> None:
        self.peer = peer
        self.top_msg_id = top_msg_id
        self.offset_id = offset_id
        self.add_offset = add_offset
        self.limit = limit
        self.max_id = max_id
        self.min_id = min_id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'top_msg_id', None) is not None and getattr(self, 'top_msg_id', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'top_msg_id', None) or 0
            if v is not None:
                res += write_int(v)
        res += write_int(self.offset_id)
        res += write_int(self.add_offset)
        res += write_int(self.limit)
        res += write_int(self.max_id)
        res += write_int(self.min_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetUnreadPollVotes(TLRequest[Any]):
    ID = 0X43286CF2
    QUALNAME = "functions.messages.getUnreadPollVotes"

    def __init__(self, peer: Any = None, top_msg_id: Any = None, offset_id: Any = None, add_offset: Any = None, limit: Any = None, max_id: Any = None, min_id: Any = None) -> None:
        self.peer = peer
        self.top_msg_id = top_msg_id
        self.offset_id = offset_id
        self.add_offset = add_offset
        self.limit = limit
        self.max_id = max_id
        self.min_id = min_id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'top_msg_id', None) is not None and getattr(self, 'top_msg_id', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'top_msg_id', None) or 0
            if v is not None:
                res += write_int(v)
        res += write_int(self.offset_id)
        res += write_int(self.add_offset)
        res += write_int(self.limit)
        res += write_int(self.max_id)
        res += write_int(self.min_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetUnreadReactions(TLRequest[Any]):
    ID = 0XBD7F90AC
    QUALNAME = "functions.messages.getUnreadReactions"

    def __init__(self, peer: Any = None, top_msg_id: Any = None, saved_peer_id: Any = None, offset_id: Any = None, add_offset: Any = None, limit: Any = None, max_id: Any = None, min_id: Any = None) -> None:
        self.peer = peer
        self.top_msg_id = top_msg_id
        self.saved_peer_id = saved_peer_id
        self.offset_id = offset_id
        self.add_offset = add_offset
        self.limit = limit
        self.max_id = max_id
        self.min_id = min_id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'top_msg_id', None) is not None and getattr(self, 'top_msg_id', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'saved_peer_id', None) is not None and getattr(self, 'saved_peer_id', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'top_msg_id', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'saved_peer_id', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += write_int(self.offset_id)
        res += write_int(self.add_offset)
        res += write_int(self.limit)
        res += write_int(self.max_id)
        res += write_int(self.min_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetWebPage(TLRequest[Any]):
    ID = 0X8D9692A3
    QUALNAME = "functions.messages.getWebPage"

    def __init__(self, url: Any = None, hash: Any = None) -> None:
        self.url = url
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.url)
        res += write_int(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesGetWebPagePreview(TLRequest[Any]):
    ID = 0X570D6F6F
    QUALNAME = "functions.messages.getWebPagePreview"

    def __init__(self, message: Any = None, entities: Any = None) -> None:
        self.message = message
        self.entities = entities

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'entities', None) is not None and getattr(self, 'entities', None) is not False:
            flags |= (1 << 3)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_string(self.message)
        if bool(flags & (1 << 3)):
            v = getattr(self, 'entities', None) or []
            if v is not None:
                res += write_vector(v, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesHideAllChatJoinRequests(TLRequest[Any]):
    ID = 0XE085F4EA
    QUALNAME = "functions.messages.hideAllChatJoinRequests"

    def __init__(self, approved: Any = None, peer: Any = None, link: Any = None) -> None:
        self.approved = approved
        self.peer = peer
        self.link = link

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'approved', None):
            flags |= (1 << 0)
        if getattr(self, 'link', None) is not None and getattr(self, 'link', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        if bool(flags & (1 << 1)):
            v = getattr(self, 'link', None) or ''
            if v is not None:
                res += write_string(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesHideChatJoinRequest(TLRequest[Any]):
    ID = 0X7FE7E815
    QUALNAME = "functions.messages.hideChatJoinRequest"

    def __init__(self, approved: Any = None, peer: Any = None, user_id: Any = None) -> None:
        self.approved = approved
        self.peer = peer
        self.user_id = user_id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'approved', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += (self.user_id.write() if hasattr(self.user_id, 'write') else write_bytes(self.user_id))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesHidePeerSettingsBar(TLRequest[Any]):
    ID = 0X4FACB138
    QUALNAME = "functions.messages.hidePeerSettingsBar"

    def __init__(self, peer: Any = None) -> None:
        self.peer = peer

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesImportChatInvite(TLRequest[Any]):
    ID = 0XDE91436E
    QUALNAME = "functions.messages.importChatInvite"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesInitHistoryImport(TLRequest[Any]):
    ID = 0X34090C3B
    QUALNAME = "functions.messages.initHistoryImport"

    def __init__(self, peer: Any = None, file: Any = None, media_count: Any = None) -> None:
        self.peer = peer
        self.file = file
        self.media_count = media_count

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += (self.file.write() if hasattr(self.file, 'write') else write_bytes(self.file))
        res += write_int(self.media_count)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesInstallStickerSet(TLRequest[Any]):
    ID = 0XC78FE460
    QUALNAME = "functions.messages.installStickerSet"

    def __init__(self, stickerset: Any = None, archived: Any = None) -> None:
        self.stickerset = stickerset
        self.archived = archived

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.stickerset.write() if hasattr(self.stickerset, 'write') else write_bytes(self.stickerset))
        res += write_bool(self.archived)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesMarkDialogUnread(TLRequest[Any]):
    ID = 0X8C5006F8
    QUALNAME = "functions.messages.markDialogUnread"

    def __init__(self, unread: Any = None, parent_peer: Any = None, peer: Any = None) -> None:
        self.unread = unread
        self.parent_peer = parent_peer
        self.peer = peer

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'unread', None):
            flags |= (1 << 0)
        if getattr(self, 'parent_peer', None) is not None and getattr(self, 'parent_peer', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'parent_peer', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesMigrateChat(TLRequest[Any]):
    ID = 0XA2875319
    QUALNAME = "functions.messages.migrateChat"

    def __init__(self, chat_id: Any = None) -> None:
        self.chat_id = chat_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.chat_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesProlongWebView(TLRequest[Any]):
    ID = 0XB0D81A83
    QUALNAME = "functions.messages.prolongWebView"

    def __init__(self, silent: Any = None, peer: Any = None, bot: Any = None, query_id: Any = None, reply_to: Any = None, send_as: Any = None) -> None:
        self.silent = silent
        self.peer = peer
        self.bot = bot
        self.query_id = query_id
        self.reply_to = reply_to
        self.send_as = send_as

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'silent', None):
            flags |= (1 << 5)
        if getattr(self, 'reply_to', None) is not None and getattr(self, 'reply_to', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'send_as', None) is not None and getattr(self, 'send_as', None) is not False:
            flags |= (1 << 13)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        res += write_long(self.query_id)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'reply_to', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 13)):
            v = getattr(self, 'send_as', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesRateTranscribedAudio(TLRequest[Any]):
    ID = 0X7F1D072F
    QUALNAME = "functions.messages.rateTranscribedAudio"

    def __init__(self, peer: Any = None, msg_id: Any = None, transcription_id: Any = None, good: Any = None) -> None:
        self.peer = peer
        self.msg_id = msg_id
        self.transcription_id = transcription_id
        self.good = good

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.msg_id)
        res += write_long(self.transcription_id)
        res += write_bool(self.good)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesReadDiscussion(TLRequest[Any]):
    ID = 0XF731A9F4
    QUALNAME = "functions.messages.readDiscussion"

    def __init__(self, peer: Any = None, msg_id: Any = None, read_max_id: Any = None) -> None:
        self.peer = peer
        self.msg_id = msg_id
        self.read_max_id = read_max_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.msg_id)
        res += write_int(self.read_max_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesReadEncryptedHistory(TLRequest[Any]):
    ID = 0X7F4B690A
    QUALNAME = "functions.messages.readEncryptedHistory"

    def __init__(self, peer: Any = None, max_date: Any = None) -> None:
        self.peer = peer
        self.max_date = max_date

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.max_date)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesReadFeaturedStickers(TLRequest[Any]):
    ID = 0X5B118126
    QUALNAME = "functions.messages.readFeaturedStickers"

    def __init__(self, id: Any = None) -> None:
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_vector(self.id, write_long)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesReadHistory(TLRequest[Any]):
    ID = 0XE306D3A
    QUALNAME = "functions.messages.readHistory"

    def __init__(self, peer: Any = None, max_id: Any = None) -> None:
        self.peer = peer
        self.max_id = max_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.max_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesReadMentions(TLRequest[Any]):
    ID = 0X36E5BF4D
    QUALNAME = "functions.messages.readMentions"

    def __init__(self, peer: Any = None, top_msg_id: Any = None) -> None:
        self.peer = peer
        self.top_msg_id = top_msg_id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'top_msg_id', None) is not None and getattr(self, 'top_msg_id', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'top_msg_id', None) or 0
            if v is not None:
                res += write_int(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesReadMessageContents(TLRequest[Any]):
    ID = 0X36A73F77
    QUALNAME = "functions.messages.readMessageContents"

    def __init__(self, id: Any = None) -> None:
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_vector(self.id, write_int)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesReadPollVotes(TLRequest[Any]):
    ID = 0X1720B4D8
    QUALNAME = "functions.messages.readPollVotes"

    def __init__(self, peer: Any = None, top_msg_id: Any = None) -> None:
        self.peer = peer
        self.top_msg_id = top_msg_id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'top_msg_id', None) is not None and getattr(self, 'top_msg_id', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'top_msg_id', None) or 0
            if v is not None:
                res += write_int(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesReadReactions(TLRequest[Any]):
    ID = 0X9EC44F93
    QUALNAME = "functions.messages.readReactions"

    def __init__(self, peer: Any = None, top_msg_id: Any = None, saved_peer_id: Any = None) -> None:
        self.peer = peer
        self.top_msg_id = top_msg_id
        self.saved_peer_id = saved_peer_id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'top_msg_id', None) is not None and getattr(self, 'top_msg_id', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'saved_peer_id', None) is not None and getattr(self, 'saved_peer_id', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'top_msg_id', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'saved_peer_id', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesReadSavedHistory(TLRequest[Any]):
    ID = 0XBA4A3B5B
    QUALNAME = "functions.messages.readSavedHistory"

    def __init__(self, parent_peer: Any = None, peer: Any = None, max_id: Any = None) -> None:
        self.parent_peer = parent_peer
        self.peer = peer
        self.max_id = max_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.parent_peer.write() if hasattr(self.parent_peer, 'write') else write_bytes(self.parent_peer))
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.max_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesReceivedMessages(TLRequest[Any]):
    ID = 0X5A954C0
    QUALNAME = "functions.messages.receivedMessages"

    def __init__(self, max_id: Any = None) -> None:
        self.max_id = max_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.max_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesReceivedQueue(TLRequest[Any]):
    ID = 0X55A5BB66
    QUALNAME = "functions.messages.receivedQueue"

    def __init__(self, max_qts: Any = None) -> None:
        self.max_qts = max_qts

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.max_qts)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x1CB5C415:
            return read_vector(b, read_long)
        return read_tl_object(b)

class MessagesReorderPinnedDialogs(TLRequest[Any]):
    ID = 0X3B1ADF37
    QUALNAME = "functions.messages.reorderPinnedDialogs"

    def __init__(self, force: Any = None, folder_id: Any = None, order: Any = None) -> None:
        self.force = force
        self.folder_id = folder_id
        self.order = order

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'force', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_int(self.folder_id)
        res += write_vector(self.order, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesReorderPinnedForumTopics(TLRequest[Any]):
    ID = 0XE7841F0
    QUALNAME = "functions.messages.reorderPinnedForumTopics"

    def __init__(self, force: Any = None, peer: Any = None, order: Any = None) -> None:
        self.force = force
        self.peer = peer
        self.order = order

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'force', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_vector(self.order, write_int)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesReorderPinnedSavedDialogs(TLRequest[Any]):
    ID = 0X8B716587
    QUALNAME = "functions.messages.reorderPinnedSavedDialogs"

    def __init__(self, force: Any = None, order: Any = None) -> None:
        self.force = force
        self.order = order

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'force', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_vector(self.order, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesReorderQuickReplies(TLRequest[Any]):
    ID = 0X60331907
    QUALNAME = "functions.messages.reorderQuickReplies"

    def __init__(self, order: Any = None) -> None:
        self.order = order

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_vector(self.order, write_int)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesReorderStickerSets(TLRequest[Any]):
    ID = 0X78337739
    QUALNAME = "functions.messages.reorderStickerSets"

    def __init__(self, masks: Any = None, emojis: Any = None, order: Any = None) -> None:
        self.masks = masks
        self.emojis = emojis
        self.order = order

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'masks', None):
            flags |= (1 << 0)
        if getattr(self, 'emojis', None):
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_vector(self.order, write_long)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesReport(TLRequest[Any]):
    ID = 0XFC78AF9B
    QUALNAME = "functions.messages.report"

    def __init__(self, peer: Any = None, id: Any = None, option: Any = None, message: Any = None) -> None:
        self.peer = peer
        self.id = id
        self.option = option
        self.message = message

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_vector(self.id, write_int)
        res += write_bytes(self.option)
        res += write_string(self.message)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesReportEncryptedSpam(TLRequest[Any]):
    ID = 0X4B0C8C0F
    QUALNAME = "functions.messages.reportEncryptedSpam"

    def __init__(self, peer: Any = None) -> None:
        self.peer = peer

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesReportMessagesDelivery(TLRequest[Any]):
    ID = 0X5A6D7395
    QUALNAME = "functions.messages.reportMessagesDelivery"

    def __init__(self, push: Any = None, peer: Any = None, id: Any = None) -> None:
        self.push = push
        self.peer = peer
        self.id = id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'push', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_vector(self.id, write_int)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesReportMusicListen(TLRequest[Any]):
    ID = 0XDDBCD819
    QUALNAME = "functions.messages.reportMusicListen"

    def __init__(self, id: Any = None, listened_duration: Any = None) -> None:
        self.id = id
        self.listened_duration = listened_duration

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.id.write() if hasattr(self.id, 'write') else write_bytes(self.id))
        res += write_int(self.listened_duration)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesReportReaction(TLRequest[Any]):
    ID = 0X3F64C076
    QUALNAME = "functions.messages.reportReaction"

    def __init__(self, peer: Any = None, id: Any = None, reaction_peer: Any = None) -> None:
        self.peer = peer
        self.id = id
        self.reaction_peer = reaction_peer

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.id)
        res += (self.reaction_peer.write() if hasattr(self.reaction_peer, 'write') else write_bytes(self.reaction_peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesReportReadMetrics(TLRequest[Any]):
    ID = 0X4067C5E6
    QUALNAME = "functions.messages.reportReadMetrics"

    def __init__(self, peer: Any = None, metrics: Any = None) -> None:
        self.peer = peer
        self.metrics = metrics

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_vector(self.metrics, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesReportSpam(TLRequest[Any]):
    ID = 0XCF1592DB
    QUALNAME = "functions.messages.reportSpam"

    def __init__(self, peer: Any = None) -> None:
        self.peer = peer

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesReportSponsoredMessage(TLRequest[Any]):
    ID = 0X12CBF0C4
    QUALNAME = "functions.messages.reportSponsoredMessage"

    def __init__(self, random_id: Any = None, option: Any = None) -> None:
        self.random_id = random_id
        self.option = option

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_bytes(self.random_id)
        res += write_bytes(self.option)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesRequestAppWebView(TLRequest[Any]):
    ID = 0X53618BCE
    QUALNAME = "functions.messages.requestAppWebView"

    def __init__(self, write_allowed: Any = None, compact: Any = None, fullscreen: Any = None, peer: Any = None, app: Any = None, start_param: Any = None, theme_params: Any = None, platform: Any = None) -> None:
        self.write_allowed = write_allowed
        self.compact = compact
        self.fullscreen = fullscreen
        self.peer = peer
        self.app = app
        self.start_param = start_param
        self.theme_params = theme_params
        self.platform = platform

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'write_allowed', None):
            flags |= (1 << 0)
        if getattr(self, 'compact', None):
            flags |= (1 << 7)
        if getattr(self, 'fullscreen', None):
            flags |= (1 << 8)
        if getattr(self, 'start_param', None) is not None and getattr(self, 'start_param', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'theme_params', None) is not None and getattr(self, 'theme_params', None) is not False:
            flags |= (1 << 2)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += (self.app.write() if hasattr(self.app, 'write') else write_bytes(self.app))
        if bool(flags & (1 << 1)):
            v = getattr(self, 'start_param', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'theme_params', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += write_string(self.platform)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesRequestChatJoinWebView(TLRequest[Any]):
    ID = 0XBA9EE679
    QUALNAME = "functions.messages.requestChatJoinWebView"

    def __init__(self, query_id: Any = None, theme_params: Any = None, platform: Any = None) -> None:
        self.query_id = query_id
        self.theme_params = theme_params
        self.platform = platform

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'theme_params', None) is not None and getattr(self, 'theme_params', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_long(self.query_id)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'theme_params', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += write_string(self.platform)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesRequestEncryption(TLRequest[Any]):
    ID = 0XF64DAF43
    QUALNAME = "functions.messages.requestEncryption"

    def __init__(self, user_id: Any = None, random_id: Any = None, g_a: Any = None) -> None:
        self.user_id = user_id
        self.random_id = random_id
        self.g_a = g_a

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.user_id.write() if hasattr(self.user_id, 'write') else write_bytes(self.user_id))
        res += write_int(self.random_id)
        res += write_bytes(self.g_a)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesRequestMainWebView(TLRequest[Any]):
    ID = 0XC9E01E7B
    QUALNAME = "functions.messages.requestMainWebView"

    def __init__(self, compact: Any = None, fullscreen: Any = None, peer: Any = None, bot: Any = None, start_param: Any = None, theme_params: Any = None, platform: Any = None) -> None:
        self.compact = compact
        self.fullscreen = fullscreen
        self.peer = peer
        self.bot = bot
        self.start_param = start_param
        self.theme_params = theme_params
        self.platform = platform

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'compact', None):
            flags |= (1 << 7)
        if getattr(self, 'fullscreen', None):
            flags |= (1 << 8)
        if getattr(self, 'start_param', None) is not None and getattr(self, 'start_param', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'theme_params', None) is not None and getattr(self, 'theme_params', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        if bool(flags & (1 << 1)):
            v = getattr(self, 'start_param', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'theme_params', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += write_string(self.platform)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesRequestSimpleWebView(TLRequest[Any]):
    ID = 0X413A3E73
    QUALNAME = "functions.messages.requestSimpleWebView"

    def __init__(self, from_switch_webview: Any = None, from_side_menu: Any = None, compact: Any = None, fullscreen: Any = None, bot: Any = None, url: Any = None, start_param: Any = None, theme_params: Any = None, platform: Any = None) -> None:
        self.from_switch_webview = from_switch_webview
        self.from_side_menu = from_side_menu
        self.compact = compact
        self.fullscreen = fullscreen
        self.bot = bot
        self.url = url
        self.start_param = start_param
        self.theme_params = theme_params
        self.platform = platform

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'from_switch_webview', None):
            flags |= (1 << 1)
        if getattr(self, 'from_side_menu', None):
            flags |= (1 << 2)
        if getattr(self, 'compact', None):
            flags |= (1 << 7)
        if getattr(self, 'fullscreen', None):
            flags |= (1 << 8)
        if getattr(self, 'url', None) is not None and getattr(self, 'url', None) is not False:
            flags |= (1 << 3)
        if getattr(self, 'start_param', None) is not None and getattr(self, 'start_param', None) is not False:
            flags |= (1 << 4)
        if getattr(self, 'theme_params', None) is not None and getattr(self, 'theme_params', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        if bool(flags & (1 << 3)):
            v = getattr(self, 'url', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 4)):
            v = getattr(self, 'start_param', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'theme_params', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += write_string(self.platform)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesRequestUrlAuth(TLRequest[Any]):
    ID = 0X894CC99C
    QUALNAME = "functions.messages.requestUrlAuth"

    def __init__(self, peer: Any = None, msg_id: Any = None, button_id: Any = None, url: Any = None, in_app_origin: Any = None) -> None:
        self.peer = peer
        self.msg_id = msg_id
        self.button_id = button_id
        self.url = url
        self.in_app_origin = in_app_origin

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'peer', None) is not None and getattr(self, 'peer', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'msg_id', None) is not None and getattr(self, 'msg_id', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'button_id', None) is not None and getattr(self, 'button_id', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'url', None) is not None and getattr(self, 'url', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'in_app_origin', None) is not None and getattr(self, 'in_app_origin', None) is not False:
            flags |= (1 << 3)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'peer', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 1)):
            v = getattr(self, 'msg_id', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'button_id', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'url', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 3)):
            v = getattr(self, 'in_app_origin', None) or ''
            if v is not None:
                res += write_string(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesRequestWebView(TLRequest[Any]):
    ID = 0X269DC2C1
    QUALNAME = "functions.messages.requestWebView"

    def __init__(self, from_bot_menu: Any = None, silent: Any = None, compact: Any = None, fullscreen: Any = None, peer: Any = None, bot: Any = None, url: Any = None, start_param: Any = None, theme_params: Any = None, platform: Any = None, reply_to: Any = None, send_as: Any = None) -> None:
        self.from_bot_menu = from_bot_menu
        self.silent = silent
        self.compact = compact
        self.fullscreen = fullscreen
        self.peer = peer
        self.bot = bot
        self.url = url
        self.start_param = start_param
        self.theme_params = theme_params
        self.platform = platform
        self.reply_to = reply_to
        self.send_as = send_as

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'from_bot_menu', None):
            flags |= (1 << 4)
        if getattr(self, 'silent', None):
            flags |= (1 << 5)
        if getattr(self, 'compact', None):
            flags |= (1 << 7)
        if getattr(self, 'fullscreen', None):
            flags |= (1 << 8)
        if getattr(self, 'url', None) is not None and getattr(self, 'url', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'start_param', None) is not None and getattr(self, 'start_param', None) is not False:
            flags |= (1 << 3)
        if getattr(self, 'theme_params', None) is not None and getattr(self, 'theme_params', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'reply_to', None) is not None and getattr(self, 'reply_to', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'send_as', None) is not None and getattr(self, 'send_as', None) is not False:
            flags |= (1 << 13)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        if bool(flags & (1 << 1)):
            v = getattr(self, 'url', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 3)):
            v = getattr(self, 'start_param', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'theme_params', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += write_string(self.platform)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'reply_to', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 13)):
            v = getattr(self, 'send_as', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSaveDefaultSendAs(TLRequest[Any]):
    ID = 0XCCFDDF96
    QUALNAME = "functions.messages.saveDefaultSendAs"

    def __init__(self, peer: Any = None, send_as: Any = None) -> None:
        self.peer = peer
        self.send_as = send_as

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += (self.send_as.write() if hasattr(self.send_as, 'write') else write_bytes(self.send_as))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesSaveDraft(TLRequest[Any]):
    ID = 0XAD0FA15C
    QUALNAME = "functions.messages.saveDraft"

    def __init__(self, no_webpage: Any = None, invert_media: Any = None, reply_to: Any = None, peer: Any = None, message: Any = None, entities: Any = None, media: Any = None, effect: Any = None, suggested_post: Any = None, rich_message: Any = None) -> None:
        self.no_webpage = no_webpage
        self.invert_media = invert_media
        self.reply_to = reply_to
        self.peer = peer
        self.message = message
        self.entities = entities
        self.media = media
        self.effect = effect
        self.suggested_post = suggested_post
        self.rich_message = rich_message

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'no_webpage', None):
            flags |= (1 << 1)
        if getattr(self, 'invert_media', None):
            flags |= (1 << 6)
        if getattr(self, 'reply_to', None) is not None and getattr(self, 'reply_to', None) is not False:
            flags |= (1 << 4)
        if getattr(self, 'entities', None) is not None and getattr(self, 'entities', None) is not False:
            flags |= (1 << 3)
        if getattr(self, 'media', None) is not None and getattr(self, 'media', None) is not False:
            flags |= (1 << 5)
        if getattr(self, 'effect', None) is not None and getattr(self, 'effect', None) is not False:
            flags |= (1 << 7)
        if getattr(self, 'suggested_post', None) is not None and getattr(self, 'suggested_post', None) is not False:
            flags |= (1 << 8)
        if getattr(self, 'rich_message', None) is not None and getattr(self, 'rich_message', None) is not False:
            flags |= (1 << 9)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 4)):
            v = getattr(self, 'reply_to', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_string(self.message)
        if bool(flags & (1 << 3)):
            v = getattr(self, 'entities', None) or []
            if v is not None:
                res += write_vector(v, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        if bool(flags & (1 << 5)):
            v = getattr(self, 'media', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 7)):
            v = getattr(self, 'effect', None) or 0
            if v is not None:
                res += write_long(v)
        if bool(flags & (1 << 8)):
            v = getattr(self, 'suggested_post', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 9)):
            v = getattr(self, 'rich_message', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesSaveGif(TLRequest[Any]):
    ID = 0X327A30CB
    QUALNAME = "functions.messages.saveGif"

    def __init__(self, id: Any = None, unsave: Any = None) -> None:
        self.id = id
        self.unsave = unsave

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.id.write() if hasattr(self.id, 'write') else write_bytes(self.id))
        res += write_bool(self.unsave)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesSavePreparedInlineMessage(TLRequest[Any]):
    ID = 0XF21F7F2F
    QUALNAME = "functions.messages.savePreparedInlineMessage"

    def __init__(self, result: Any = None, user_id: Any = None, peer_types: Any = None) -> None:
        self.result = result
        self.user_id = user_id
        self.peer_types = peer_types

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'peer_types', None) is not None and getattr(self, 'peer_types', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.result.write() if hasattr(self.result, 'write') else write_bytes(self.result))
        res += (self.user_id.write() if hasattr(self.user_id, 'write') else write_bytes(self.user_id))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'peer_types', None) or []
            if v is not None:
                res += write_vector(v, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSaveRecentSticker(TLRequest[Any]):
    ID = 0X392718F8
    QUALNAME = "functions.messages.saveRecentSticker"

    def __init__(self, attached: Any = None, id: Any = None, unsave: Any = None) -> None:
        self.attached = attached
        self.id = id
        self.unsave = unsave

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'attached', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.id.write() if hasattr(self.id, 'write') else write_bytes(self.id))
        res += write_bool(self.unsave)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesSearch(TLRequest[Any]):
    ID = 0X29EE847A
    QUALNAME = "functions.messages.search"

    def __init__(self, peer: Any = None, q: Any = None, from_id: Any = None, saved_peer_id: Any = None, saved_reaction: Any = None, top_msg_id: Any = None, filter: Any = None, min_date: Any = None, max_date: Any = None, offset_id: Any = None, add_offset: Any = None, limit: Any = None, max_id: Any = None, min_id: Any = None, hash: Any = None) -> None:
        self.peer = peer
        self.q = q
        self.from_id = from_id
        self.saved_peer_id = saved_peer_id
        self.saved_reaction = saved_reaction
        self.top_msg_id = top_msg_id
        self.filter = filter
        self.min_date = min_date
        self.max_date = max_date
        self.offset_id = offset_id
        self.add_offset = add_offset
        self.limit = limit
        self.max_id = max_id
        self.min_id = min_id
        self.hash = hash

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'from_id', None) is not None and getattr(self, 'from_id', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'saved_peer_id', None) is not None and getattr(self, 'saved_peer_id', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'saved_reaction', None) is not None and getattr(self, 'saved_reaction', None) is not False:
            flags |= (1 << 3)
        if getattr(self, 'top_msg_id', None) is not None and getattr(self, 'top_msg_id', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_string(self.q)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'from_id', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 2)):
            v = getattr(self, 'saved_peer_id', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 3)):
            v = getattr(self, 'saved_reaction', None) or []
            if v is not None:
                res += write_vector(v, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        if bool(flags & (1 << 1)):
            v = getattr(self, 'top_msg_id', None) or 0
            if v is not None:
                res += write_int(v)
        res += (self.filter.write() if hasattr(self.filter, 'write') else write_bytes(self.filter))
        res += write_int(self.min_date)
        res += write_int(self.max_date)
        res += write_int(self.offset_id)
        res += write_int(self.add_offset)
        res += write_int(self.limit)
        res += write_int(self.max_id)
        res += write_int(self.min_id)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSearchCustomEmoji(TLRequest[Any]):
    ID = 0X2C11C0D7
    QUALNAME = "functions.messages.searchCustomEmoji"

    def __init__(self, emoticon: Any = None, hash: Any = None) -> None:
        self.emoticon = emoticon
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.emoticon)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSearchEmojiStickerSets(TLRequest[Any]):
    ID = 0X92B4494C
    QUALNAME = "functions.messages.searchEmojiStickerSets"

    def __init__(self, exclude_featured: Any = None, q: Any = None, hash: Any = None) -> None:
        self.exclude_featured = exclude_featured
        self.q = q
        self.hash = hash

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'exclude_featured', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_string(self.q)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSearchGlobal(TLRequest[Any]):
    ID = 0X6126A43C
    QUALNAME = "functions.messages.searchGlobal"

    def __init__(self, broadcasts_only: Any = None, groups_only: Any = None, users_only: Any = None, folder_id: Any = None, community: Any = None, q: Any = None, filter: Any = None, min_date: Any = None, max_date: Any = None, offset_rate: Any = None, offset_peer: Any = None, offset_id: Any = None, limit: Any = None) -> None:
        self.broadcasts_only = broadcasts_only
        self.groups_only = groups_only
        self.users_only = users_only
        self.folder_id = folder_id
        self.community = community
        self.q = q
        self.filter = filter
        self.min_date = min_date
        self.max_date = max_date
        self.offset_rate = offset_rate
        self.offset_peer = offset_peer
        self.offset_id = offset_id
        self.limit = limit

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'broadcasts_only', None):
            flags |= (1 << 1)
        if getattr(self, 'groups_only', None):
            flags |= (1 << 2)
        if getattr(self, 'users_only', None):
            flags |= (1 << 3)
        if getattr(self, 'folder_id', None) is not None and getattr(self, 'folder_id', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'community', None) is not None and getattr(self, 'community', None) is not False:
            flags |= (1 << 4)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'folder_id', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 4)):
            v = getattr(self, 'community', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += write_string(self.q)
        res += (self.filter.write() if hasattr(self.filter, 'write') else write_bytes(self.filter))
        res += write_int(self.min_date)
        res += write_int(self.max_date)
        res += write_int(self.offset_rate)
        res += (self.offset_peer.write() if hasattr(self.offset_peer, 'write') else write_bytes(self.offset_peer))
        res += write_int(self.offset_id)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSearchSentMedia(TLRequest[Any]):
    ID = 0X107E31A0
    QUALNAME = "functions.messages.searchSentMedia"

    def __init__(self, q: Any = None, filter: Any = None, limit: Any = None) -> None:
        self.q = q
        self.filter = filter
        self.limit = limit

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.q)
        res += (self.filter.write() if hasattr(self.filter, 'write') else write_bytes(self.filter))
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSearchStickerSets(TLRequest[Any]):
    ID = 0X35705B8A
    QUALNAME = "functions.messages.searchStickerSets"

    def __init__(self, exclude_featured: Any = None, q: Any = None, hash: Any = None) -> None:
        self.exclude_featured = exclude_featured
        self.q = q
        self.hash = hash

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'exclude_featured', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_string(self.q)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSearchStickers(TLRequest[Any]):
    ID = 0X29B1C66A
    QUALNAME = "functions.messages.searchStickers"

    def __init__(self, emojis: Any = None, q: Any = None, emoticon: Any = None, lang_code: Any = None, offset: Any = None, limit: Any = None, hash: Any = None) -> None:
        self.emojis = emojis
        self.q = q
        self.emoticon = emoticon
        self.lang_code = lang_code
        self.offset = offset
        self.limit = limit
        self.hash = hash

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'emojis', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_string(self.q)
        res += write_string(self.emoticon)
        res += write_vector(self.lang_code, write_string)
        res += write_int(self.offset)
        res += write_int(self.limit)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSendBotRequestedPeer(TLRequest[Any]):
    ID = 0X6C5CF2A7
    QUALNAME = "functions.messages.sendBotRequestedPeer"

    def __init__(self, peer: Any = None, msg_id: Any = None, webapp_req_id: Any = None, button_id: Any = None, requested_peers: Any = None) -> None:
        self.peer = peer
        self.msg_id = msg_id
        self.webapp_req_id = webapp_req_id
        self.button_id = button_id
        self.requested_peers = requested_peers

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'msg_id', None) is not None and getattr(self, 'msg_id', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'webapp_req_id', None) is not None and getattr(self, 'webapp_req_id', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'msg_id', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'webapp_req_id', None) or ''
            if v is not None:
                res += write_string(v)
        res += write_int(self.button_id)
        res += write_vector(self.requested_peers, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSendEncrypted(TLRequest[Any]):
    ID = 0X44FA7A15
    QUALNAME = "functions.messages.sendEncrypted"

    def __init__(self, silent: Any = None, peer: Any = None, random_id: Any = None, data: Any = None) -> None:
        self.silent = silent
        self.peer = peer
        self.random_id = random_id
        self.data = data

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'silent', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_long(self.random_id)
        res += write_bytes(self.data)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSendEncryptedFile(TLRequest[Any]):
    ID = 0X5559481D
    QUALNAME = "functions.messages.sendEncryptedFile"

    def __init__(self, silent: Any = None, peer: Any = None, random_id: Any = None, data: Any = None, file: Any = None) -> None:
        self.silent = silent
        self.peer = peer
        self.random_id = random_id
        self.data = data
        self.file = file

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'silent', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_long(self.random_id)
        res += write_bytes(self.data)
        res += (self.file.write() if hasattr(self.file, 'write') else write_bytes(self.file))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSendEncryptedService(TLRequest[Any]):
    ID = 0X32D439A4
    QUALNAME = "functions.messages.sendEncryptedService"

    def __init__(self, peer: Any = None, random_id: Any = None, data: Any = None) -> None:
        self.peer = peer
        self.random_id = random_id
        self.data = data

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_long(self.random_id)
        res += write_bytes(self.data)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSendInlineBotResult(TLRequest[Any]):
    ID = 0XC0CF7646
    QUALNAME = "functions.messages.sendInlineBotResult"

    def __init__(self, silent: Any = None, background: Any = None, clear_draft: Any = None, hide_via: Any = None, peer: Any = None, reply_to: Any = None, random_id: Any = None, query_id: Any = None, id: Any = None, schedule_date: Any = None, send_as: Any = None, quick_reply_shortcut: Any = None, allow_paid_stars: Any = None) -> None:
        self.silent = silent
        self.background = background
        self.clear_draft = clear_draft
        self.hide_via = hide_via
        self.peer = peer
        self.reply_to = reply_to
        self.random_id = random_id
        self.query_id = query_id
        self.id = id
        self.schedule_date = schedule_date
        self.send_as = send_as
        self.quick_reply_shortcut = quick_reply_shortcut
        self.allow_paid_stars = allow_paid_stars

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'silent', None):
            flags |= (1 << 5)
        if getattr(self, 'background', None):
            flags |= (1 << 6)
        if getattr(self, 'clear_draft', None):
            flags |= (1 << 7)
        if getattr(self, 'hide_via', None):
            flags |= (1 << 11)
        if getattr(self, 'reply_to', None) is not None and getattr(self, 'reply_to', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'schedule_date', None) is not None and getattr(self, 'schedule_date', None) is not False:
            flags |= (1 << 10)
        if getattr(self, 'send_as', None) is not None and getattr(self, 'send_as', None) is not False:
            flags |= (1 << 13)
        if getattr(self, 'quick_reply_shortcut', None) is not None and getattr(self, 'quick_reply_shortcut', None) is not False:
            flags |= (1 << 17)
        if getattr(self, 'allow_paid_stars', None) is not None and getattr(self, 'allow_paid_stars', None) is not False:
            flags |= (1 << 21)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'reply_to', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += write_long(self.random_id)
        res += write_long(self.query_id)
        res += write_string(self.id)
        if bool(flags & (1 << 10)):
            v = getattr(self, 'schedule_date', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 13)):
            v = getattr(self, 'send_as', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 17)):
            v = getattr(self, 'quick_reply_shortcut', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 21)):
            v = getattr(self, 'allow_paid_stars', None) or 0
            if v is not None:
                res += write_long(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSendMedia(TLRequest[Any]):
    ID = 0X330E77F
    QUALNAME = "functions.messages.sendMedia"

    def __init__(self, silent: Any = None, background: Any = None, clear_draft: Any = None, noforwards: Any = None, update_stickersets_order: Any = None, invert_media: Any = None, allow_paid_floodskip: Any = None, peer: Any = None, reply_to: Any = None, media: Any = None, message: Any = None, random_id: Any = None, reply_markup: Any = None, entities: Any = None, schedule_date: Any = None, schedule_repeat_period: Any = None, send_as: Any = None, quick_reply_shortcut: Any = None, effect: Any = None, allow_paid_stars: Any = None, suggested_post: Any = None) -> None:
        self.silent = silent
        self.background = background
        self.clear_draft = clear_draft
        self.noforwards = noforwards
        self.update_stickersets_order = update_stickersets_order
        self.invert_media = invert_media
        self.allow_paid_floodskip = allow_paid_floodskip
        self.peer = peer
        self.reply_to = reply_to
        self.media = media
        self.message = message
        self.random_id = random_id
        self.reply_markup = reply_markup
        self.entities = entities
        self.schedule_date = schedule_date
        self.schedule_repeat_period = schedule_repeat_period
        self.send_as = send_as
        self.quick_reply_shortcut = quick_reply_shortcut
        self.effect = effect
        self.allow_paid_stars = allow_paid_stars
        self.suggested_post = suggested_post

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'silent', None):
            flags |= (1 << 5)
        if getattr(self, 'background', None):
            flags |= (1 << 6)
        if getattr(self, 'clear_draft', None):
            flags |= (1 << 7)
        if getattr(self, 'noforwards', None):
            flags |= (1 << 14)
        if getattr(self, 'update_stickersets_order', None):
            flags |= (1 << 15)
        if getattr(self, 'invert_media', None):
            flags |= (1 << 16)
        if getattr(self, 'allow_paid_floodskip', None):
            flags |= (1 << 19)
        if getattr(self, 'reply_to', None) is not None and getattr(self, 'reply_to', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'reply_markup', None) is not None and getattr(self, 'reply_markup', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'entities', None) is not None and getattr(self, 'entities', None) is not False:
            flags |= (1 << 3)
        if getattr(self, 'schedule_date', None) is not None and getattr(self, 'schedule_date', None) is not False:
            flags |= (1 << 10)
        if getattr(self, 'schedule_repeat_period', None) is not None and getattr(self, 'schedule_repeat_period', None) is not False:
            flags |= (1 << 24)
        if getattr(self, 'send_as', None) is not None and getattr(self, 'send_as', None) is not False:
            flags |= (1 << 13)
        if getattr(self, 'quick_reply_shortcut', None) is not None and getattr(self, 'quick_reply_shortcut', None) is not False:
            flags |= (1 << 17)
        if getattr(self, 'effect', None) is not None and getattr(self, 'effect', None) is not False:
            flags |= (1 << 18)
        if getattr(self, 'allow_paid_stars', None) is not None and getattr(self, 'allow_paid_stars', None) is not False:
            flags |= (1 << 21)
        if getattr(self, 'suggested_post', None) is not None and getattr(self, 'suggested_post', None) is not False:
            flags |= (1 << 22)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'reply_to', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += (self.media.write() if hasattr(self.media, 'write') else write_bytes(self.media))
        res += write_string(self.message)
        res += write_long(self.random_id)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'reply_markup', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 3)):
            v = getattr(self, 'entities', None) or []
            if v is not None:
                res += write_vector(v, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        if bool(flags & (1 << 10)):
            v = getattr(self, 'schedule_date', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 24)):
            v = getattr(self, 'schedule_repeat_period', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 13)):
            v = getattr(self, 'send_as', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 17)):
            v = getattr(self, 'quick_reply_shortcut', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 18)):
            v = getattr(self, 'effect', None) or 0
            if v is not None:
                res += write_long(v)
        if bool(flags & (1 << 21)):
            v = getattr(self, 'allow_paid_stars', None) or 0
            if v is not None:
                res += write_long(v)
        if bool(flags & (1 << 22)):
            v = getattr(self, 'suggested_post', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSendMessage(TLRequest[Any]):
    ID = 0XFEF48F62
    QUALNAME = "functions.messages.sendMessage"

    def __init__(self, no_webpage: Any = None, silent: Any = None, background: Any = None, clear_draft: Any = None, noforwards: Any = None, update_stickersets_order: Any = None, invert_media: Any = None, allow_paid_floodskip: Any = None, peer: Any = None, reply_to: Any = None, message: Any = None, random_id: Any = None, reply_markup: Any = None, entities: Any = None, schedule_date: Any = None, schedule_repeat_period: Any = None, send_as: Any = None, quick_reply_shortcut: Any = None, effect: Any = None, allow_paid_stars: Any = None, suggested_post: Any = None, rich_message: Any = None) -> None:
        self.no_webpage = no_webpage
        self.silent = silent
        self.background = background
        self.clear_draft = clear_draft
        self.noforwards = noforwards
        self.update_stickersets_order = update_stickersets_order
        self.invert_media = invert_media
        self.allow_paid_floodskip = allow_paid_floodskip
        self.peer = peer
        self.reply_to = reply_to
        self.message = message
        self.random_id = random_id
        self.reply_markup = reply_markup
        self.entities = entities
        self.schedule_date = schedule_date
        self.schedule_repeat_period = schedule_repeat_period
        self.send_as = send_as
        self.quick_reply_shortcut = quick_reply_shortcut
        self.effect = effect
        self.allow_paid_stars = allow_paid_stars
        self.suggested_post = suggested_post
        self.rich_message = rich_message

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'no_webpage', None):
            flags |= (1 << 1)
        if getattr(self, 'silent', None):
            flags |= (1 << 5)
        if getattr(self, 'background', None):
            flags |= (1 << 6)
        if getattr(self, 'clear_draft', None):
            flags |= (1 << 7)
        if getattr(self, 'noforwards', None):
            flags |= (1 << 14)
        if getattr(self, 'update_stickersets_order', None):
            flags |= (1 << 15)
        if getattr(self, 'invert_media', None):
            flags |= (1 << 16)
        if getattr(self, 'allow_paid_floodskip', None):
            flags |= (1 << 19)
        if getattr(self, 'reply_to', None) is not None and getattr(self, 'reply_to', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'reply_markup', None) is not None and getattr(self, 'reply_markup', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'entities', None) is not None and getattr(self, 'entities', None) is not False:
            flags |= (1 << 3)
        if getattr(self, 'schedule_date', None) is not None and getattr(self, 'schedule_date', None) is not False:
            flags |= (1 << 10)
        if getattr(self, 'schedule_repeat_period', None) is not None and getattr(self, 'schedule_repeat_period', None) is not False:
            flags |= (1 << 24)
        if getattr(self, 'send_as', None) is not None and getattr(self, 'send_as', None) is not False:
            flags |= (1 << 13)
        if getattr(self, 'quick_reply_shortcut', None) is not None and getattr(self, 'quick_reply_shortcut', None) is not False:
            flags |= (1 << 17)
        if getattr(self, 'effect', None) is not None and getattr(self, 'effect', None) is not False:
            flags |= (1 << 18)
        if getattr(self, 'allow_paid_stars', None) is not None and getattr(self, 'allow_paid_stars', None) is not False:
            flags |= (1 << 21)
        if getattr(self, 'suggested_post', None) is not None and getattr(self, 'suggested_post', None) is not False:
            flags |= (1 << 22)
        if getattr(self, 'rich_message', None) is not None and getattr(self, 'rich_message', None) is not False:
            flags |= (1 << 23)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'reply_to', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += write_string(self.message)
        res += write_long(self.random_id)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'reply_markup', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 3)):
            v = getattr(self, 'entities', None) or []
            if v is not None:
                res += write_vector(v, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        if bool(flags & (1 << 10)):
            v = getattr(self, 'schedule_date', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 24)):
            v = getattr(self, 'schedule_repeat_period', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 13)):
            v = getattr(self, 'send_as', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 17)):
            v = getattr(self, 'quick_reply_shortcut', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 18)):
            v = getattr(self, 'effect', None) or 0
            if v is not None:
                res += write_long(v)
        if bool(flags & (1 << 21)):
            v = getattr(self, 'allow_paid_stars', None) or 0
            if v is not None:
                res += write_long(v)
        if bool(flags & (1 << 22)):
            v = getattr(self, 'suggested_post', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 23)):
            v = getattr(self, 'rich_message', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSendMultiMedia(TLRequest[Any]):
    ID = 0X1BF89D74
    QUALNAME = "functions.messages.sendMultiMedia"

    def __init__(self, silent: Any = None, background: Any = None, clear_draft: Any = None, noforwards: Any = None, update_stickersets_order: Any = None, invert_media: Any = None, allow_paid_floodskip: Any = None, peer: Any = None, reply_to: Any = None, multi_media: Any = None, schedule_date: Any = None, send_as: Any = None, quick_reply_shortcut: Any = None, effect: Any = None, allow_paid_stars: Any = None) -> None:
        self.silent = silent
        self.background = background
        self.clear_draft = clear_draft
        self.noforwards = noforwards
        self.update_stickersets_order = update_stickersets_order
        self.invert_media = invert_media
        self.allow_paid_floodskip = allow_paid_floodskip
        self.peer = peer
        self.reply_to = reply_to
        self.multi_media = multi_media
        self.schedule_date = schedule_date
        self.send_as = send_as
        self.quick_reply_shortcut = quick_reply_shortcut
        self.effect = effect
        self.allow_paid_stars = allow_paid_stars

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'silent', None):
            flags |= (1 << 5)
        if getattr(self, 'background', None):
            flags |= (1 << 6)
        if getattr(self, 'clear_draft', None):
            flags |= (1 << 7)
        if getattr(self, 'noforwards', None):
            flags |= (1 << 14)
        if getattr(self, 'update_stickersets_order', None):
            flags |= (1 << 15)
        if getattr(self, 'invert_media', None):
            flags |= (1 << 16)
        if getattr(self, 'allow_paid_floodskip', None):
            flags |= (1 << 19)
        if getattr(self, 'reply_to', None) is not None and getattr(self, 'reply_to', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'schedule_date', None) is not None and getattr(self, 'schedule_date', None) is not False:
            flags |= (1 << 10)
        if getattr(self, 'send_as', None) is not None and getattr(self, 'send_as', None) is not False:
            flags |= (1 << 13)
        if getattr(self, 'quick_reply_shortcut', None) is not None and getattr(self, 'quick_reply_shortcut', None) is not False:
            flags |= (1 << 17)
        if getattr(self, 'effect', None) is not None and getattr(self, 'effect', None) is not False:
            flags |= (1 << 18)
        if getattr(self, 'allow_paid_stars', None) is not None and getattr(self, 'allow_paid_stars', None) is not False:
            flags |= (1 << 21)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'reply_to', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += write_vector(self.multi_media, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        if bool(flags & (1 << 10)):
            v = getattr(self, 'schedule_date', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 13)):
            v = getattr(self, 'send_as', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 17)):
            v = getattr(self, 'quick_reply_shortcut', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 18)):
            v = getattr(self, 'effect', None) or 0
            if v is not None:
                res += write_long(v)
        if bool(flags & (1 << 21)):
            v = getattr(self, 'allow_paid_stars', None) or 0
            if v is not None:
                res += write_long(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSendPaidReaction(TLRequest[Any]):
    ID = 0X58BBCB50
    QUALNAME = "functions.messages.sendPaidReaction"

    def __init__(self, peer: Any = None, msg_id: Any = None, count: Any = None, random_id: Any = None, private: Any = None) -> None:
        self.peer = peer
        self.msg_id = msg_id
        self.count = count
        self.random_id = random_id
        self.private = private

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'private', None) is not None and getattr(self, 'private', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.msg_id)
        res += write_int(self.count)
        res += write_long(self.random_id)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'private', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSendQuickReplyMessages(TLRequest[Any]):
    ID = 0X6C750DE1
    QUALNAME = "functions.messages.sendQuickReplyMessages"

    def __init__(self, peer: Any = None, shortcut_id: Any = None, id: Any = None, random_id: Any = None) -> None:
        self.peer = peer
        self.shortcut_id = shortcut_id
        self.id = id
        self.random_id = random_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.shortcut_id)
        res += write_vector(self.id, write_int)
        res += write_vector(self.random_id, write_long)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSendReaction(TLRequest[Any]):
    ID = 0XD30D78D4
    QUALNAME = "functions.messages.sendReaction"

    def __init__(self, big: Any = None, add_to_recent: Any = None, peer: Any = None, msg_id: Any = None, reaction: Any = None) -> None:
        self.big = big
        self.add_to_recent = add_to_recent
        self.peer = peer
        self.msg_id = msg_id
        self.reaction = reaction

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'big', None):
            flags |= (1 << 1)
        if getattr(self, 'add_to_recent', None):
            flags |= (1 << 2)
        if getattr(self, 'reaction', None) is not None and getattr(self, 'reaction', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.msg_id)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'reaction', None) or []
            if v is not None:
                res += write_vector(v, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSendScheduledMessages(TLRequest[Any]):
    ID = 0XBD38850A
    QUALNAME = "functions.messages.sendScheduledMessages"

    def __init__(self, peer: Any = None, id: Any = None) -> None:
        self.peer = peer
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_vector(self.id, write_int)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSendScreenshotNotification(TLRequest[Any]):
    ID = 0XA1405817
    QUALNAME = "functions.messages.sendScreenshotNotification"

    def __init__(self, peer: Any = None, reply_to: Any = None, random_id: Any = None) -> None:
        self.peer = peer
        self.reply_to = reply_to
        self.random_id = random_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += (self.reply_to.write() if hasattr(self.reply_to, 'write') else write_bytes(self.reply_to))
        res += write_long(self.random_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSendVote(TLRequest[Any]):
    ID = 0X10EA6184
    QUALNAME = "functions.messages.sendVote"

    def __init__(self, peer: Any = None, msg_id: Any = None, options: Any = None) -> None:
        self.peer = peer
        self.msg_id = msg_id
        self.options = options

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.msg_id)
        res += write_vector(self.options, write_bytes)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSendWebViewData(TLRequest[Any]):
    ID = 0XDC0242C8
    QUALNAME = "functions.messages.sendWebViewData"

    def __init__(self, bot: Any = None, random_id: Any = None, button_text: Any = None, data: Any = None) -> None:
        self.bot = bot
        self.random_id = random_id
        self.button_text = button_text
        self.data = data

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        res += write_long(self.random_id)
        res += write_string(self.button_text)
        res += write_string(self.data)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSendWebViewResultMessage(TLRequest[Any]):
    ID = 0XA4314F5
    QUALNAME = "functions.messages.sendWebViewResultMessage"

    def __init__(self, bot_query_id: Any = None, result: Any = None) -> None:
        self.bot_query_id = bot_query_id
        self.result = result

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.bot_query_id)
        res += (self.result.write() if hasattr(self.result, 'write') else write_bytes(self.result))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSetBotCallbackAnswer(TLRequest[Any]):
    ID = 0XD58F130A
    QUALNAME = "functions.messages.setBotCallbackAnswer"

    def __init__(self, alert: Any = None, query_id: Any = None, message: Any = None, url: Any = None, cache_time: Any = None) -> None:
        self.alert = alert
        self.query_id = query_id
        self.message = message
        self.url = url
        self.cache_time = cache_time

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'alert', None):
            flags |= (1 << 1)
        if getattr(self, 'message', None) is not None and getattr(self, 'message', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'url', None) is not None and getattr(self, 'url', None) is not False:
            flags |= (1 << 2)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_long(self.query_id)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'message', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'url', None) or ''
            if v is not None:
                res += write_string(v)
        res += write_int(self.cache_time)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesSetBotGuestChatResult(TLRequest[Any]):
    ID = 0XB8F106E3
    QUALNAME = "functions.messages.setBotGuestChatResult"

    def __init__(self, query_id: Any = None, result: Any = None) -> None:
        self.query_id = query_id
        self.result = result

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.query_id)
        res += (self.result.write() if hasattr(self.result, 'write') else write_bytes(self.result))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSetBotPrecheckoutResults(TLRequest[Any]):
    ID = 0X9C2DD95
    QUALNAME = "functions.messages.setBotPrecheckoutResults"

    def __init__(self, success: Any = None, query_id: Any = None, error: Any = None) -> None:
        self.success = success
        self.query_id = query_id
        self.error = error

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'success', None):
            flags |= (1 << 1)
        if getattr(self, 'error', None) is not None and getattr(self, 'error', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_long(self.query_id)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'error', None) or ''
            if v is not None:
                res += write_string(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesSetBotShippingResults(TLRequest[Any]):
    ID = 0XE5F672FA
    QUALNAME = "functions.messages.setBotShippingResults"

    def __init__(self, query_id: Any = None, error: Any = None, shipping_options: Any = None) -> None:
        self.query_id = query_id
        self.error = error
        self.shipping_options = shipping_options

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'error', None) is not None and getattr(self, 'error', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'shipping_options', None) is not None and getattr(self, 'shipping_options', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_long(self.query_id)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'error', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'shipping_options', None) or []
            if v is not None:
                res += write_vector(v, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesSetChatAvailableReactions(TLRequest[Any]):
    ID = 0X864B2581
    QUALNAME = "functions.messages.setChatAvailableReactions"

    def __init__(self, peer: Any = None, available_reactions: Any = None, reactions_limit: Any = None, paid_enabled: Any = None) -> None:
        self.peer = peer
        self.available_reactions = available_reactions
        self.reactions_limit = reactions_limit
        self.paid_enabled = paid_enabled

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'reactions_limit', None) is not None and getattr(self, 'reactions_limit', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'paid_enabled', None) is not None and getattr(self, 'paid_enabled', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += (self.available_reactions.write() if hasattr(self.available_reactions, 'write') else write_bytes(self.available_reactions))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'reactions_limit', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'paid_enabled', None)
            if v is not None:
                res += write_bool(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSetChatTheme(TLRequest[Any]):
    ID = 0X81202C9
    QUALNAME = "functions.messages.setChatTheme"

    def __init__(self, peer: Any = None, theme: Any = None) -> None:
        self.peer = peer
        self.theme = theme

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += (self.theme.write() if hasattr(self.theme, 'write') else write_bytes(self.theme))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSetChatWallPaper(TLRequest[Any]):
    ID = 0X8FFACAE1
    QUALNAME = "functions.messages.setChatWallPaper"

    def __init__(self, for_both: Any = None, revert: Any = None, peer: Any = None, wallpaper: Any = None, settings: Any = None, id: Any = None) -> None:
        self.for_both = for_both
        self.revert = revert
        self.peer = peer
        self.wallpaper = wallpaper
        self.settings = settings
        self.id = id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'for_both', None):
            flags |= (1 << 3)
        if getattr(self, 'revert', None):
            flags |= (1 << 4)
        if getattr(self, 'wallpaper', None) is not None and getattr(self, 'wallpaper', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'settings', None) is not None and getattr(self, 'settings', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'id', None) is not None and getattr(self, 'id', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'wallpaper', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 2)):
            v = getattr(self, 'settings', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 1)):
            v = getattr(self, 'id', None) or 0
            if v is not None:
                res += write_int(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSetDefaultHistoryTtl(TLRequest[Any]):
    ID = 0X9EB51445
    QUALNAME = "functions.messages.setDefaultHistoryTTL"

    def __init__(self, period: Any = None) -> None:
        self.period = period

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.period)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesSetDefaultReaction(TLRequest[Any]):
    ID = 0X4F47A016
    QUALNAME = "functions.messages.setDefaultReaction"

    def __init__(self, reaction: Any = None) -> None:
        self.reaction = reaction

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.reaction.write() if hasattr(self.reaction, 'write') else write_bytes(self.reaction))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesSetEncryptedTyping(TLRequest[Any]):
    ID = 0X791451ED
    QUALNAME = "functions.messages.setEncryptedTyping"

    def __init__(self, peer: Any = None, typing: Any = None) -> None:
        self.peer = peer
        self.typing = typing

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_bool(self.typing)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesSetGameScore(TLRequest[Any]):
    ID = 0X8EF8ECC0
    QUALNAME = "functions.messages.setGameScore"

    def __init__(self, edit_message: Any = None, force: Any = None, peer: Any = None, id: Any = None, user_id: Any = None, score: Any = None) -> None:
        self.edit_message = edit_message
        self.force = force
        self.peer = peer
        self.id = id
        self.user_id = user_id
        self.score = score

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'edit_message', None):
            flags |= (1 << 0)
        if getattr(self, 'force', None):
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.id)
        res += (self.user_id.write() if hasattr(self.user_id, 'write') else write_bytes(self.user_id))
        res += write_int(self.score)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSetHistoryTtl(TLRequest[Any]):
    ID = 0XB80E5FE4
    QUALNAME = "functions.messages.setHistoryTTL"

    def __init__(self, peer: Any = None, period: Any = None) -> None:
        self.peer = peer
        self.period = period

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.period)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesSetInlineBotResults(TLRequest[Any]):
    ID = 0XBB12A419
    QUALNAME = "functions.messages.setInlineBotResults"

    def __init__(self, gallery: Any = None, private: Any = None, query_id: Any = None, results: Any = None, cache_time: Any = None, next_offset: Any = None, switch_pm: Any = None, switch_webview: Any = None) -> None:
        self.gallery = gallery
        self.private = private
        self.query_id = query_id
        self.results = results
        self.cache_time = cache_time
        self.next_offset = next_offset
        self.switch_pm = switch_pm
        self.switch_webview = switch_webview

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'gallery', None):
            flags |= (1 << 0)
        if getattr(self, 'private', None):
            flags |= (1 << 1)
        if getattr(self, 'next_offset', None) is not None and getattr(self, 'next_offset', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'switch_pm', None) is not None and getattr(self, 'switch_pm', None) is not False:
            flags |= (1 << 3)
        if getattr(self, 'switch_webview', None) is not None and getattr(self, 'switch_webview', None) is not False:
            flags |= (1 << 4)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_long(self.query_id)
        res += write_vector(self.results, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        res += write_int(self.cache_time)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'next_offset', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 3)):
            v = getattr(self, 'switch_pm', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 4)):
            v = getattr(self, 'switch_webview', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesSetInlineGameScore(TLRequest[Any]):
    ID = 0X15AD9F64
    QUALNAME = "functions.messages.setInlineGameScore"

    def __init__(self, edit_message: Any = None, force: Any = None, id: Any = None, user_id: Any = None, score: Any = None) -> None:
        self.edit_message = edit_message
        self.force = force
        self.id = id
        self.user_id = user_id
        self.score = score

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'edit_message', None):
            flags |= (1 << 0)
        if getattr(self, 'force', None):
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.id.write() if hasattr(self.id, 'write') else write_bytes(self.id))
        res += (self.user_id.write() if hasattr(self.user_id, 'write') else write_bytes(self.user_id))
        res += write_int(self.score)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesSetTyping(TLRequest[Any]):
    ID = 0X58943EE2
    QUALNAME = "functions.messages.setTyping"

    def __init__(self, peer: Any = None, top_msg_id: Any = None, action: Any = None) -> None:
        self.peer = peer
        self.top_msg_id = top_msg_id
        self.action = action

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'top_msg_id', None) is not None and getattr(self, 'top_msg_id', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'top_msg_id', None) or 0
            if v is not None:
                res += write_int(v)
        res += (self.action.write() if hasattr(self.action, 'write') else write_bytes(self.action))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesStartBot(TLRequest[Any]):
    ID = 0XE6DF7378
    QUALNAME = "functions.messages.startBot"

    def __init__(self, bot: Any = None, peer: Any = None, random_id: Any = None, start_param: Any = None) -> None:
        self.bot = bot
        self.peer = peer
        self.random_id = random_id
        self.start_param = start_param

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_long(self.random_id)
        res += write_string(self.start_param)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesStartHistoryImport(TLRequest[Any]):
    ID = 0XB43DF344
    QUALNAME = "functions.messages.startHistoryImport"

    def __init__(self, peer: Any = None, import_id: Any = None) -> None:
        self.peer = peer
        self.import_id = import_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_long(self.import_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesSummarizeText(TLRequest[Any]):
    ID = 0XABBBD346
    QUALNAME = "functions.messages.summarizeText"

    def __init__(self, peer: Any = None, id: Any = None, to_lang: Any = None, tone: Any = None) -> None:
        self.peer = peer
        self.id = id
        self.to_lang = to_lang
        self.tone = tone

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'to_lang', None) is not None and getattr(self, 'to_lang', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'tone', None) is not None and getattr(self, 'tone', None) is not False:
            flags |= (1 << 2)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.id)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'to_lang', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'tone', None) or ''
            if v is not None:
                res += write_string(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesToggleBotInAttachMenu(TLRequest[Any]):
    ID = 0X69F59D69
    QUALNAME = "functions.messages.toggleBotInAttachMenu"

    def __init__(self, write_allowed: Any = None, bot: Any = None, enabled: Any = None) -> None:
        self.write_allowed = write_allowed
        self.bot = bot
        self.enabled = enabled

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'write_allowed', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        res += write_bool(self.enabled)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesToggleDialogFilterTags(TLRequest[Any]):
    ID = 0XFD2DDA49
    QUALNAME = "functions.messages.toggleDialogFilterTags"

    def __init__(self, enabled: Any = None) -> None:
        self.enabled = enabled

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_bool(self.enabled)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesToggleDialogPin(TLRequest[Any]):
    ID = 0XA731E257
    QUALNAME = "functions.messages.toggleDialogPin"

    def __init__(self, pinned: Any = None, peer: Any = None) -> None:
        self.pinned = pinned
        self.peer = peer

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'pinned', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesToggleNoForwards(TLRequest[Any]):
    ID = 0XB2081A35
    QUALNAME = "functions.messages.toggleNoForwards"

    def __init__(self, peer: Any = None, enabled: Any = None, request_msg_id: Any = None) -> None:
        self.peer = peer
        self.enabled = enabled
        self.request_msg_id = request_msg_id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'request_msg_id', None) is not None and getattr(self, 'request_msg_id', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_bool(self.enabled)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'request_msg_id', None) or 0
            if v is not None:
                res += write_int(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesTogglePaidReactionPrivacy(TLRequest[Any]):
    ID = 0X435885B5
    QUALNAME = "functions.messages.togglePaidReactionPrivacy"

    def __init__(self, peer: Any = None, msg_id: Any = None, private: Any = None) -> None:
        self.peer = peer
        self.msg_id = msg_id
        self.private = private

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.msg_id)
        res += (self.private.write() if hasattr(self.private, 'write') else write_bytes(self.private))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesTogglePeerTranslations(TLRequest[Any]):
    ID = 0XE47CB579
    QUALNAME = "functions.messages.togglePeerTranslations"

    def __init__(self, disabled: Any = None, peer: Any = None) -> None:
        self.disabled = disabled
        self.peer = peer

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'disabled', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesToggleSavedDialogPin(TLRequest[Any]):
    ID = 0XAC81BBDE
    QUALNAME = "functions.messages.toggleSavedDialogPin"

    def __init__(self, pinned: Any = None, peer: Any = None) -> None:
        self.pinned = pinned
        self.peer = peer

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'pinned', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesToggleStickerSets(TLRequest[Any]):
    ID = 0XB5052FEA
    QUALNAME = "functions.messages.toggleStickerSets"

    def __init__(self, uninstall: Any = None, archive: Any = None, unarchive: Any = None, stickersets: Any = None) -> None:
        self.uninstall = uninstall
        self.archive = archive
        self.unarchive = unarchive
        self.stickersets = stickersets

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'uninstall', None):
            flags |= (1 << 0)
        if getattr(self, 'archive', None):
            flags |= (1 << 1)
        if getattr(self, 'unarchive', None):
            flags |= (1 << 2)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_vector(self.stickersets, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesToggleSuggestedPostApproval(TLRequest[Any]):
    ID = 0X8107455C
    QUALNAME = "functions.messages.toggleSuggestedPostApproval"

    def __init__(self, reject: Any = None, peer: Any = None, msg_id: Any = None, schedule_date: Any = None, reject_comment: Any = None) -> None:
        self.reject = reject
        self.peer = peer
        self.msg_id = msg_id
        self.schedule_date = schedule_date
        self.reject_comment = reject_comment

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'reject', None):
            flags |= (1 << 1)
        if getattr(self, 'schedule_date', None) is not None and getattr(self, 'schedule_date', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'reject_comment', None) is not None and getattr(self, 'reject_comment', None) is not False:
            flags |= (1 << 2)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.msg_id)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'schedule_date', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'reject_comment', None) or ''
            if v is not None:
                res += write_string(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesToggleTodoCompleted(TLRequest[Any]):
    ID = 0XD3E03124
    QUALNAME = "functions.messages.toggleTodoCompleted"

    def __init__(self, peer: Any = None, msg_id: Any = None, completed: Any = None, incompleted: Any = None) -> None:
        self.peer = peer
        self.msg_id = msg_id
        self.completed = completed
        self.incompleted = incompleted

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.msg_id)
        res += write_vector(self.completed, write_int)
        res += write_vector(self.incompleted, write_int)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesTranscribeAudio(TLRequest[Any]):
    ID = 0X269E9A49
    QUALNAME = "functions.messages.transcribeAudio"

    def __init__(self, peer: Any = None, msg_id: Any = None) -> None:
        self.peer = peer
        self.msg_id = msg_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.msg_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesTranslateRichMessage(TLRequest[Any]):
    ID = 0X1A542004
    QUALNAME = "functions.messages.translateRichMessage"

    def __init__(self, peer: Any = None, id: Any = None, text: Any = None, to_lang: Any = None, tone: Any = None) -> None:
        self.peer = peer
        self.id = id
        self.text = text
        self.to_lang = to_lang
        self.tone = tone

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'peer', None) is not None and getattr(self, 'peer', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'id', None) is not None and getattr(self, 'id', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'text', None) is not None and getattr(self, 'text', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'tone', None) is not None and getattr(self, 'tone', None) is not False:
            flags |= (1 << 2)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'peer', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'id', None) or []
            if v is not None:
                res += write_vector(v, write_int)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'text', None) or []
            if v is not None:
                res += write_vector(v, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        res += write_string(self.to_lang)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'tone', None) or ''
            if v is not None:
                res += write_string(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesTranslateText(TLRequest[Any]):
    ID = 0XA5EEC345
    QUALNAME = "functions.messages.translateText"

    def __init__(self, peer: Any = None, id: Any = None, text: Any = None, to_lang: Any = None, tone: Any = None) -> None:
        self.peer = peer
        self.id = id
        self.text = text
        self.to_lang = to_lang
        self.tone = tone

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'peer', None) is not None and getattr(self, 'peer', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'id', None) is not None and getattr(self, 'id', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'text', None) is not None and getattr(self, 'text', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'tone', None) is not None and getattr(self, 'tone', None) is not False:
            flags |= (1 << 2)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'peer', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'id', None) or []
            if v is not None:
                res += write_vector(v, write_int)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'text', None) or []
            if v is not None:
                res += write_vector(v, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        res += write_string(self.to_lang)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'tone', None) or ''
            if v is not None:
                res += write_string(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesUninstallStickerSet(TLRequest[Any]):
    ID = 0XF96E55DE
    QUALNAME = "functions.messages.uninstallStickerSet"

    def __init__(self, stickerset: Any = None) -> None:
        self.stickerset = stickerset

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.stickerset.write() if hasattr(self.stickerset, 'write') else write_bytes(self.stickerset))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesUnpinAllMessages(TLRequest[Any]):
    ID = 0X62DD747
    QUALNAME = "functions.messages.unpinAllMessages"

    def __init__(self, peer: Any = None, top_msg_id: Any = None, saved_peer_id: Any = None) -> None:
        self.peer = peer
        self.top_msg_id = top_msg_id
        self.saved_peer_id = saved_peer_id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'top_msg_id', None) is not None and getattr(self, 'top_msg_id', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'saved_peer_id', None) is not None and getattr(self, 'saved_peer_id', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'top_msg_id', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'saved_peer_id', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesUpdateDialogFilter(TLRequest[Any]):
    ID = 0X1AD4A04A
    QUALNAME = "functions.messages.updateDialogFilter"

    def __init__(self, id: Any = None, filter: Any = None) -> None:
        self.id = id
        self.filter = filter

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'filter', None) is not None and getattr(self, 'filter', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_int(self.id)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'filter', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesUpdateDialogFiltersOrder(TLRequest[Any]):
    ID = 0XC563C1E4
    QUALNAME = "functions.messages.updateDialogFiltersOrder"

    def __init__(self, order: Any = None) -> None:
        self.order = order

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_vector(self.order, write_int)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesUpdatePinnedForumTopic(TLRequest[Any]):
    ID = 0X175DF251
    QUALNAME = "functions.messages.updatePinnedForumTopic"

    def __init__(self, peer: Any = None, topic_id: Any = None, pinned: Any = None) -> None:
        self.peer = peer
        self.topic_id = topic_id
        self.pinned = pinned

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.topic_id)
        res += write_bool(self.pinned)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesUpdatePinnedMessage(TLRequest[Any]):
    ID = 0XD2AAF7EC
    QUALNAME = "functions.messages.updatePinnedMessage"

    def __init__(self, silent: Any = None, unpin: Any = None, pm_oneside: Any = None, peer: Any = None, id: Any = None) -> None:
        self.silent = silent
        self.unpin = unpin
        self.pm_oneside = pm_oneside
        self.peer = peer
        self.id = id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'silent', None):
            flags |= (1 << 0)
        if getattr(self, 'unpin', None):
            flags |= (1 << 1)
        if getattr(self, 'pm_oneside', None):
            flags |= (1 << 2)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesUpdateSavedReactionTag(TLRequest[Any]):
    ID = 0X60297DEC
    QUALNAME = "functions.messages.updateSavedReactionTag"

    def __init__(self, reaction: Any = None, title: Any = None) -> None:
        self.reaction = reaction
        self.title = title

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'title', None) is not None and getattr(self, 'title', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.reaction.write() if hasattr(self.reaction, 'write') else write_bytes(self.reaction))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'title', None) or ''
            if v is not None:
                res += write_string(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class MessagesUploadEncryptedFile(TLRequest[Any]):
    ID = 0X5057C497
    QUALNAME = "functions.messages.uploadEncryptedFile"

    def __init__(self, peer: Any = None, file: Any = None) -> None:
        self.peer = peer
        self.file = file

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += (self.file.write() if hasattr(self.file, 'write') else write_bytes(self.file))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesUploadImportedMedia(TLRequest[Any]):
    ID = 0X2A862092
    QUALNAME = "functions.messages.uploadImportedMedia"

    def __init__(self, peer: Any = None, import_id: Any = None, file_name: Any = None, media: Any = None) -> None:
        self.peer = peer
        self.import_id = import_id
        self.file_name = file_name
        self.media = media

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_long(self.import_id)
        res += write_string(self.file_name)
        res += (self.media.write() if hasattr(self.media, 'write') else write_bytes(self.media))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesUploadMedia(TLRequest[Any]):
    ID = 0X14967978
    QUALNAME = "functions.messages.uploadMedia"

    def __init__(self, business_connection_id: Any = None, peer: Any = None, media: Any = None) -> None:
        self.business_connection_id = business_connection_id
        self.peer = peer
        self.media = media

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'business_connection_id', None) is not None and getattr(self, 'business_connection_id', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'business_connection_id', None) or ''
            if v is not None:
                res += write_string(v)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += (self.media.write() if hasattr(self.media, 'write') else write_bytes(self.media))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class MessagesViewSponsoredMessage(TLRequest[Any]):
    ID = 0X269E3643
    QUALNAME = "functions.messages.viewSponsoredMessage"

    def __init__(self, random_id: Any = None) -> None:
        self.random_id = random_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_bytes(self.random_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class PQInnerData(TLRequest[Any]):
    ID = 0X83C95AEC
    QUALNAME = "functions.p_q_inner_data"

    def __init__(self, pq: Any = None, p: Any = None, q: Any = None, nonce: Any = None, server_nonce: Any = None, new_nonce: Any = None) -> None:
        self.pq = pq
        self.p = p
        self.q = q
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.new_nonce = new_nonce

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.pq)
        res += write_string(self.p)
        res += write_string(self.q)
        res += write_int128(self.nonce)
        res += write_int128(self.server_nonce)
        res += write_int256(self.new_nonce)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PQInnerDataDc(TLRequest[Any]):
    ID = 0XA9F55F95
    QUALNAME = "functions.p_q_inner_data_dc"

    def __init__(self, pq: Any = None, p: Any = None, q: Any = None, nonce: Any = None, server_nonce: Any = None, new_nonce: Any = None, dc: Any = None) -> None:
        self.pq = pq
        self.p = p
        self.q = q
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.new_nonce = new_nonce
        self.dc = dc

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.pq)
        res += write_string(self.p)
        res += write_string(self.q)
        res += write_int128(self.nonce)
        res += write_int128(self.server_nonce)
        res += write_int256(self.new_nonce)
        res += write_int(self.dc)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PQInnerDataTemp(TLRequest[Any]):
    ID = 0X3C6A84D4
    QUALNAME = "functions.p_q_inner_data_temp"

    def __init__(self, pq: Any = None, p: Any = None, q: Any = None, nonce: Any = None, server_nonce: Any = None, new_nonce: Any = None, expires_in: Any = None) -> None:
        self.pq = pq
        self.p = p
        self.q = q
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.new_nonce = new_nonce
        self.expires_in = expires_in

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.pq)
        res += write_string(self.p)
        res += write_string(self.q)
        res += write_int128(self.nonce)
        res += write_int128(self.server_nonce)
        res += write_int256(self.new_nonce)
        res += write_int(self.expires_in)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PQInnerDataTempDc(TLRequest[Any]):
    ID = 0X56FDDF88
    QUALNAME = "functions.p_q_inner_data_temp_dc"

    def __init__(self, pq: Any = None, p: Any = None, q: Any = None, nonce: Any = None, server_nonce: Any = None, new_nonce: Any = None, dc: Any = None, expires_in: Any = None) -> None:
        self.pq = pq
        self.p = p
        self.q = q
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.new_nonce = new_nonce
        self.dc = dc
        self.expires_in = expires_in

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.pq)
        res += write_string(self.p)
        res += write_string(self.q)
        res += write_int128(self.nonce)
        res += write_int128(self.server_nonce)
        res += write_int256(self.new_nonce)
        res += write_int(self.dc)
        res += write_int(self.expires_in)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsApplyGiftCode(TLRequest[Any]):
    ID = 0XF6E26854
    QUALNAME = "functions.payments.applyGiftCode"

    def __init__(self, slug: Any = None) -> None:
        self.slug = slug

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.slug)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsAssignAppStoreTransaction(TLRequest[Any]):
    ID = 0X80ED747D
    QUALNAME = "functions.payments.assignAppStoreTransaction"

    def __init__(self, receipt: Any = None, purpose: Any = None) -> None:
        self.receipt = receipt
        self.purpose = purpose

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_bytes(self.receipt)
        res += (self.purpose.write() if hasattr(self.purpose, 'write') else write_bytes(self.purpose))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsAssignPlayMarketTransaction(TLRequest[Any]):
    ID = 0XDFFD50D3
    QUALNAME = "functions.payments.assignPlayMarketTransaction"

    def __init__(self, receipt: Any = None, purpose: Any = None) -> None:
        self.receipt = receipt
        self.purpose = purpose

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.receipt.write() if hasattr(self.receipt, 'write') else write_bytes(self.receipt))
        res += (self.purpose.write() if hasattr(self.purpose, 'write') else write_bytes(self.purpose))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsBotCancelStarsSubscription(TLRequest[Any]):
    ID = 0X6DFA0622
    QUALNAME = "functions.payments.botCancelStarsSubscription"

    def __init__(self, restore: Any = None, user_id: Any = None, charge_id: Any = None) -> None:
        self.restore = restore
        self.user_id = user_id
        self.charge_id = charge_id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'restore', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.user_id.write() if hasattr(self.user_id, 'write') else write_bytes(self.user_id))
        res += write_string(self.charge_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class PaymentsCanPurchaseStore(TLRequest[Any]):
    ID = 0X4FDC5EA7
    QUALNAME = "functions.payments.canPurchaseStore"

    def __init__(self, purpose: Any = None) -> None:
        self.purpose = purpose

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.purpose.write() if hasattr(self.purpose, 'write') else write_bytes(self.purpose))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class PaymentsChangeStarsSubscription(TLRequest[Any]):
    ID = 0XC7770878
    QUALNAME = "functions.payments.changeStarsSubscription"

    def __init__(self, peer: Any = None, subscription_id: Any = None, canceled: Any = None) -> None:
        self.peer = peer
        self.subscription_id = subscription_id
        self.canceled = canceled

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'canceled', None) is not None and getattr(self, 'canceled', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_string(self.subscription_id)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'canceled', None)
            if v is not None:
                res += write_bool(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class PaymentsCheckCanSendGift(TLRequest[Any]):
    ID = 0XC0C4EDC9
    QUALNAME = "functions.payments.checkCanSendGift"

    def __init__(self, gift_id: Any = None) -> None:
        self.gift_id = gift_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.gift_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsCheckGiftCode(TLRequest[Any]):
    ID = 0X8E51B4C1
    QUALNAME = "functions.payments.checkGiftCode"

    def __init__(self, slug: Any = None) -> None:
        self.slug = slug

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.slug)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsClearSavedInfo(TLRequest[Any]):
    ID = 0XD83D70C1
    QUALNAME = "functions.payments.clearSavedInfo"

    def __init__(self, credentials: Any = None, info: Any = None) -> None:
        self.credentials = credentials
        self.info = info

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'credentials', None):
            flags |= (1 << 0)
        if getattr(self, 'info', None):
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class PaymentsConnectStarRefBot(TLRequest[Any]):
    ID = 0X7ED5348A
    QUALNAME = "functions.payments.connectStarRefBot"

    def __init__(self, peer: Any = None, bot: Any = None) -> None:
        self.peer = peer
        self.bot = bot

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsConvertStarGift(TLRequest[Any]):
    ID = 0X74BF076B
    QUALNAME = "functions.payments.convertStarGift"

    def __init__(self, stargift: Any = None) -> None:
        self.stargift = stargift

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.stargift.write() if hasattr(self.stargift, 'write') else write_bytes(self.stargift))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class PaymentsCraftStarGift(TLRequest[Any]):
    ID = 0XB0F9684F
    QUALNAME = "functions.payments.craftStarGift"

    def __init__(self, stargift: Any = None) -> None:
        self.stargift = stargift

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_vector(self.stargift, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsCreateStarGiftCollection(TLRequest[Any]):
    ID = 0X1F4A0E87
    QUALNAME = "functions.payments.createStarGiftCollection"

    def __init__(self, peer: Any = None, title: Any = None, stargift: Any = None) -> None:
        self.peer = peer
        self.title = title
        self.stargift = stargift

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_string(self.title)
        res += write_vector(self.stargift, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsDeleteStarGiftCollection(TLRequest[Any]):
    ID = 0XAD5648E8
    QUALNAME = "functions.payments.deleteStarGiftCollection"

    def __init__(self, peer: Any = None, collection_id: Any = None) -> None:
        self.peer = peer
        self.collection_id = collection_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.collection_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class PaymentsEditConnectedStarRefBot(TLRequest[Any]):
    ID = 0XE4FCA4A3
    QUALNAME = "functions.payments.editConnectedStarRefBot"

    def __init__(self, revoked: Any = None, peer: Any = None, link: Any = None) -> None:
        self.revoked = revoked
        self.peer = peer
        self.link = link

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'revoked', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_string(self.link)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsExportInvoice(TLRequest[Any]):
    ID = 0XF91B065
    QUALNAME = "functions.payments.exportInvoice"

    def __init__(self, invoice_media: Any = None) -> None:
        self.invoice_media = invoice_media

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.invoice_media.write() if hasattr(self.invoice_media, 'write') else write_bytes(self.invoice_media))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsFulfillStarsSubscription(TLRequest[Any]):
    ID = 0XCC5BEBB3
    QUALNAME = "functions.payments.fulfillStarsSubscription"

    def __init__(self, peer: Any = None, subscription_id: Any = None) -> None:
        self.peer = peer
        self.subscription_id = subscription_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_string(self.subscription_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class PaymentsGetBankCardData(TLRequest[Any]):
    ID = 0X2E79D779
    QUALNAME = "functions.payments.getBankCardData"

    def __init__(self, number: Any = None) -> None:
        self.number = number

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.number)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetConnectedStarRefBot(TLRequest[Any]):
    ID = 0XB7D998F0
    QUALNAME = "functions.payments.getConnectedStarRefBot"

    def __init__(self, peer: Any = None, bot: Any = None) -> None:
        self.peer = peer
        self.bot = bot

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += (self.bot.write() if hasattr(self.bot, 'write') else write_bytes(self.bot))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetConnectedStarRefBots(TLRequest[Any]):
    ID = 0X5869A553
    QUALNAME = "functions.payments.getConnectedStarRefBots"

    def __init__(self, peer: Any = None, offset_date: Any = None, offset_link: Any = None, limit: Any = None) -> None:
        self.peer = peer
        self.offset_date = offset_date
        self.offset_link = offset_link
        self.limit = limit

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'offset_date', None) is not None and getattr(self, 'offset_date', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'offset_link', None) is not None and getattr(self, 'offset_link', None) is not False:
            flags |= (1 << 2)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        if bool(flags & (1 << 2)):
            v = getattr(self, 'offset_date', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'offset_link', None) or ''
            if v is not None:
                res += write_string(v)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetCraftStarGifts(TLRequest[Any]):
    ID = 0XFD05DD00
    QUALNAME = "functions.payments.getCraftStarGifts"

    def __init__(self, gift_id: Any = None, offset: Any = None, limit: Any = None) -> None:
        self.gift_id = gift_id
        self.offset = offset
        self.limit = limit

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.gift_id)
        res += write_string(self.offset)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetGiveawayInfo(TLRequest[Any]):
    ID = 0XF4239425
    QUALNAME = "functions.payments.getGiveawayInfo"

    def __init__(self, peer: Any = None, msg_id: Any = None) -> None:
        self.peer = peer
        self.msg_id = msg_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.msg_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetPaymentForm(TLRequest[Any]):
    ID = 0X37148DBB
    QUALNAME = "functions.payments.getPaymentForm"

    def __init__(self, invoice: Any = None, theme_params: Any = None) -> None:
        self.invoice = invoice
        self.theme_params = theme_params

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'theme_params', None) is not None and getattr(self, 'theme_params', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.invoice.write() if hasattr(self.invoice, 'write') else write_bytes(self.invoice))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'theme_params', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetPaymentReceipt(TLRequest[Any]):
    ID = 0X2478D1CC
    QUALNAME = "functions.payments.getPaymentReceipt"

    def __init__(self, peer: Any = None, msg_id: Any = None) -> None:
        self.peer = peer
        self.msg_id = msg_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.msg_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetPremiumGiftCodeOptions(TLRequest[Any]):
    ID = 0X2757BA54
    QUALNAME = "functions.payments.getPremiumGiftCodeOptions"

    def __init__(self, boost_peer: Any = None) -> None:
        self.boost_peer = boost_peer

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'boost_peer', None) is not None and getattr(self, 'boost_peer', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'boost_peer', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetResaleStarGifts(TLRequest[Any]):
    ID = 0X7A5FA236
    QUALNAME = "functions.payments.getResaleStarGifts"

    def __init__(self, sort_by_price: Any = None, sort_by_num: Any = None, for_craft: Any = None, stars_only: Any = None, attributes_hash: Any = None, gift_id: Any = None, attributes: Any = None, offset: Any = None, limit: Any = None) -> None:
        self.sort_by_price = sort_by_price
        self.sort_by_num = sort_by_num
        self.for_craft = for_craft
        self.stars_only = stars_only
        self.attributes_hash = attributes_hash
        self.gift_id = gift_id
        self.attributes = attributes
        self.offset = offset
        self.limit = limit

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'sort_by_price', None):
            flags |= (1 << 1)
        if getattr(self, 'sort_by_num', None):
            flags |= (1 << 2)
        if getattr(self, 'for_craft', None):
            flags |= (1 << 4)
        if getattr(self, 'stars_only', None):
            flags |= (1 << 5)
        if getattr(self, 'attributes_hash', None) is not None and getattr(self, 'attributes_hash', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'attributes', None) is not None and getattr(self, 'attributes', None) is not False:
            flags |= (1 << 3)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'attributes_hash', None) or 0
            if v is not None:
                res += write_long(v)
        res += write_long(self.gift_id)
        if bool(flags & (1 << 3)):
            v = getattr(self, 'attributes', None) or []
            if v is not None:
                res += write_vector(v, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        res += write_string(self.offset)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetSavedInfo(TLRequest[Any]):
    ID = 0X227D824B
    QUALNAME = "functions.payments.getSavedInfo"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetSavedStarGift(TLRequest[Any]):
    ID = 0XB455A106
    QUALNAME = "functions.payments.getSavedStarGift"

    def __init__(self, stargift: Any = None) -> None:
        self.stargift = stargift

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_vector(self.stargift, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetSavedStarGifts(TLRequest[Any]):
    ID = 0XA319E569
    QUALNAME = "functions.payments.getSavedStarGifts"

    def __init__(self, exclude_unsaved: Any = None, exclude_saved: Any = None, exclude_unlimited: Any = None, exclude_unique: Any = None, sort_by_value: Any = None, exclude_upgradable: Any = None, exclude_unupgradable: Any = None, peer_color_available: Any = None, exclude_hosted: Any = None, peer: Any = None, collection_id: Any = None, offset: Any = None, limit: Any = None) -> None:
        self.exclude_unsaved = exclude_unsaved
        self.exclude_saved = exclude_saved
        self.exclude_unlimited = exclude_unlimited
        self.exclude_unique = exclude_unique
        self.sort_by_value = sort_by_value
        self.exclude_upgradable = exclude_upgradable
        self.exclude_unupgradable = exclude_unupgradable
        self.peer_color_available = peer_color_available
        self.exclude_hosted = exclude_hosted
        self.peer = peer
        self.collection_id = collection_id
        self.offset = offset
        self.limit = limit

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'exclude_unsaved', None):
            flags |= (1 << 0)
        if getattr(self, 'exclude_saved', None):
            flags |= (1 << 1)
        if getattr(self, 'exclude_unlimited', None):
            flags |= (1 << 2)
        if getattr(self, 'exclude_unique', None):
            flags |= (1 << 4)
        if getattr(self, 'sort_by_value', None):
            flags |= (1 << 5)
        if getattr(self, 'exclude_upgradable', None):
            flags |= (1 << 7)
        if getattr(self, 'exclude_unupgradable', None):
            flags |= (1 << 8)
        if getattr(self, 'peer_color_available', None):
            flags |= (1 << 9)
        if getattr(self, 'exclude_hosted', None):
            flags |= (1 << 10)
        if getattr(self, 'collection_id', None) is not None and getattr(self, 'collection_id', None) is not False:
            flags |= (1 << 6)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        if bool(flags & (1 << 6)):
            v = getattr(self, 'collection_id', None) or 0
            if v is not None:
                res += write_int(v)
        res += write_string(self.offset)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetStarGiftActiveAuctions(TLRequest[Any]):
    ID = 0XA5D0514D
    QUALNAME = "functions.payments.getStarGiftActiveAuctions"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetStarGiftAuctionAcquiredGifts(TLRequest[Any]):
    ID = 0X6BA2CBEC
    QUALNAME = "functions.payments.getStarGiftAuctionAcquiredGifts"

    def __init__(self, gift_id: Any = None) -> None:
        self.gift_id = gift_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.gift_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetStarGiftAuctionState(TLRequest[Any]):
    ID = 0X5C9FF4D6
    QUALNAME = "functions.payments.getStarGiftAuctionState"

    def __init__(self, auction: Any = None, version: Any = None) -> None:
        self.auction = auction
        self.version = version

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.auction.write() if hasattr(self.auction, 'write') else write_bytes(self.auction))
        res += write_int(self.version)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetStarGiftCollections(TLRequest[Any]):
    ID = 0X981B91DD
    QUALNAME = "functions.payments.getStarGiftCollections"

    def __init__(self, peer: Any = None, hash: Any = None) -> None:
        self.peer = peer
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetStarGiftUpgradeAttributes(TLRequest[Any]):
    ID = 0X6D038B58
    QUALNAME = "functions.payments.getStarGiftUpgradeAttributes"

    def __init__(self, gift_id: Any = None) -> None:
        self.gift_id = gift_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.gift_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetStarGiftUpgradePreview(TLRequest[Any]):
    ID = 0X9C9ABCB1
    QUALNAME = "functions.payments.getStarGiftUpgradePreview"

    def __init__(self, gift_id: Any = None) -> None:
        self.gift_id = gift_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.gift_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetStarGiftWithdrawalUrl(TLRequest[Any]):
    ID = 0XD06E93A8
    QUALNAME = "functions.payments.getStarGiftWithdrawalUrl"

    def __init__(self, stargift: Any = None, password: Any = None) -> None:
        self.stargift = stargift
        self.password = password

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.stargift.write() if hasattr(self.stargift, 'write') else write_bytes(self.stargift))
        res += (self.password.write() if hasattr(self.password, 'write') else write_bytes(self.password))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetStarGifts(TLRequest[Any]):
    ID = 0XC4563590
    QUALNAME = "functions.payments.getStarGifts"

    def __init__(self, hash: Any = None) -> None:
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetStarsGiftOptions(TLRequest[Any]):
    ID = 0XD3C96BC8
    QUALNAME = "functions.payments.getStarsGiftOptions"

    def __init__(self, user_id: Any = None) -> None:
        self.user_id = user_id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'user_id', None) is not None and getattr(self, 'user_id', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'user_id', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetStarsGiveawayOptions(TLRequest[Any]):
    ID = 0XBD1EFD3E
    QUALNAME = "functions.payments.getStarsGiveawayOptions"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetStarsRevenueAdsAccountUrl(TLRequest[Any]):
    ID = 0XD1D7EFC5
    QUALNAME = "functions.payments.getStarsRevenueAdsAccountUrl"

    def __init__(self, peer: Any = None) -> None:
        self.peer = peer

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetStarsRevenueStats(TLRequest[Any]):
    ID = 0XD91FFAD6
    QUALNAME = "functions.payments.getStarsRevenueStats"

    def __init__(self, dark: Any = None, ton: Any = None, peer: Any = None) -> None:
        self.dark = dark
        self.ton = ton
        self.peer = peer

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'dark', None):
            flags |= (1 << 0)
        if getattr(self, 'ton', None):
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetStarsRevenueWithdrawalUrl(TLRequest[Any]):
    ID = 0X2433DC92
    QUALNAME = "functions.payments.getStarsRevenueWithdrawalUrl"

    def __init__(self, ton: Any = None, peer: Any = None, amount: Any = None, password: Any = None) -> None:
        self.ton = ton
        self.peer = peer
        self.amount = amount
        self.password = password

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'ton', None):
            flags |= (1 << 0)
        if getattr(self, 'amount', None) is not None and getattr(self, 'amount', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        if bool(flags & (1 << 1)):
            v = getattr(self, 'amount', None) or 0
            if v is not None:
                res += write_long(v)
        res += (self.password.write() if hasattr(self.password, 'write') else write_bytes(self.password))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetStarsStatus(TLRequest[Any]):
    ID = 0X4EA9B3BF
    QUALNAME = "functions.payments.getStarsStatus"

    def __init__(self, ton: Any = None, peer: Any = None) -> None:
        self.ton = ton
        self.peer = peer

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'ton', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetStarsSubscriptions(TLRequest[Any]):
    ID = 0X32512C5
    QUALNAME = "functions.payments.getStarsSubscriptions"

    def __init__(self, missing_balance: Any = None, peer: Any = None, offset: Any = None) -> None:
        self.missing_balance = missing_balance
        self.peer = peer
        self.offset = offset

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'missing_balance', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_string(self.offset)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetStarsTopupOptions(TLRequest[Any]):
    ID = 0XC00EC7D3
    QUALNAME = "functions.payments.getStarsTopupOptions"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetStarsTransactions(TLRequest[Any]):
    ID = 0X69DA4557
    QUALNAME = "functions.payments.getStarsTransactions"

    def __init__(self, inbound: Any = None, outbound: Any = None, ascending: Any = None, ton: Any = None, subscription_id: Any = None, peer: Any = None, offset: Any = None, limit: Any = None) -> None:
        self.inbound = inbound
        self.outbound = outbound
        self.ascending = ascending
        self.ton = ton
        self.subscription_id = subscription_id
        self.peer = peer
        self.offset = offset
        self.limit = limit

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'inbound', None):
            flags |= (1 << 0)
        if getattr(self, 'outbound', None):
            flags |= (1 << 1)
        if getattr(self, 'ascending', None):
            flags |= (1 << 2)
        if getattr(self, 'ton', None):
            flags |= (1 << 4)
        if getattr(self, 'subscription_id', None) is not None and getattr(self, 'subscription_id', None) is not False:
            flags |= (1 << 3)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 3)):
            v = getattr(self, 'subscription_id', None) or ''
            if v is not None:
                res += write_string(v)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_string(self.offset)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetStarsTransactionsById(TLRequest[Any]):
    ID = 0X2DCA16B8
    QUALNAME = "functions.payments.getStarsTransactionsByID"

    def __init__(self, ton: Any = None, peer: Any = None, id: Any = None) -> None:
        self.ton = ton
        self.peer = peer
        self.id = id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'ton', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_vector(self.id, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetSuggestedStarRefBots(TLRequest[Any]):
    ID = 0XD6B48F7
    QUALNAME = "functions.payments.getSuggestedStarRefBots"

    def __init__(self, order_by_revenue: Any = None, order_by_date: Any = None, peer: Any = None, offset: Any = None, limit: Any = None) -> None:
        self.order_by_revenue = order_by_revenue
        self.order_by_date = order_by_date
        self.peer = peer
        self.offset = offset
        self.limit = limit

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'order_by_revenue', None):
            flags |= (1 << 0)
        if getattr(self, 'order_by_date', None):
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_string(self.offset)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetUniqueStarGift(TLRequest[Any]):
    ID = 0XA1974D72
    QUALNAME = "functions.payments.getUniqueStarGift"

    def __init__(self, slug: Any = None) -> None:
        self.slug = slug

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.slug)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsGetUniqueStarGiftValueInfo(TLRequest[Any]):
    ID = 0X4365AF6B
    QUALNAME = "functions.payments.getUniqueStarGiftValueInfo"

    def __init__(self, slug: Any = None) -> None:
        self.slug = slug

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.slug)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsLaunchPrepaidGiveaway(TLRequest[Any]):
    ID = 0X5FF58F20
    QUALNAME = "functions.payments.launchPrepaidGiveaway"

    def __init__(self, peer: Any = None, giveaway_id: Any = None, purpose: Any = None) -> None:
        self.peer = peer
        self.giveaway_id = giveaway_id
        self.purpose = purpose

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_long(self.giveaway_id)
        res += (self.purpose.write() if hasattr(self.purpose, 'write') else write_bytes(self.purpose))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsRefundStarsCharge(TLRequest[Any]):
    ID = 0X25AE8F4A
    QUALNAME = "functions.payments.refundStarsCharge"

    def __init__(self, user_id: Any = None, charge_id: Any = None) -> None:
        self.user_id = user_id
        self.charge_id = charge_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.user_id.write() if hasattr(self.user_id, 'write') else write_bytes(self.user_id))
        res += write_string(self.charge_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsReorderStarGiftCollections(TLRequest[Any]):
    ID = 0XC32AF4CC
    QUALNAME = "functions.payments.reorderStarGiftCollections"

    def __init__(self, peer: Any = None, order: Any = None) -> None:
        self.peer = peer
        self.order = order

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_vector(self.order, write_int)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class PaymentsResolveStarGiftOffer(TLRequest[Any]):
    ID = 0XE9CE781C
    QUALNAME = "functions.payments.resolveStarGiftOffer"

    def __init__(self, decline: Any = None, offer_msg_id: Any = None) -> None:
        self.decline = decline
        self.offer_msg_id = offer_msg_id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'decline', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_int(self.offer_msg_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsSaveStarGift(TLRequest[Any]):
    ID = 0X2A2A697C
    QUALNAME = "functions.payments.saveStarGift"

    def __init__(self, unsave: Any = None, stargift: Any = None) -> None:
        self.unsave = unsave
        self.stargift = stargift

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'unsave', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.stargift.write() if hasattr(self.stargift, 'write') else write_bytes(self.stargift))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class PaymentsSendPaymentForm(TLRequest[Any]):
    ID = 0X2D03522F
    QUALNAME = "functions.payments.sendPaymentForm"

    def __init__(self, form_id: Any = None, invoice: Any = None, requested_info_id: Any = None, shipping_option_id: Any = None, credentials: Any = None, tip_amount: Any = None) -> None:
        self.form_id = form_id
        self.invoice = invoice
        self.requested_info_id = requested_info_id
        self.shipping_option_id = shipping_option_id
        self.credentials = credentials
        self.tip_amount = tip_amount

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'requested_info_id', None) is not None and getattr(self, 'requested_info_id', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'shipping_option_id', None) is not None and getattr(self, 'shipping_option_id', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'tip_amount', None) is not None and getattr(self, 'tip_amount', None) is not False:
            flags |= (1 << 2)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_long(self.form_id)
        res += (self.invoice.write() if hasattr(self.invoice, 'write') else write_bytes(self.invoice))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'requested_info_id', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'shipping_option_id', None) or ''
            if v is not None:
                res += write_string(v)
        res += (self.credentials.write() if hasattr(self.credentials, 'write') else write_bytes(self.credentials))
        if bool(flags & (1 << 2)):
            v = getattr(self, 'tip_amount', None) or 0
            if v is not None:
                res += write_long(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsSendStarGiftOffer(TLRequest[Any]):
    ID = 0X8FB86B41
    QUALNAME = "functions.payments.sendStarGiftOffer"

    def __init__(self, peer: Any = None, slug: Any = None, price: Any = None, duration: Any = None, random_id: Any = None, allow_paid_stars: Any = None) -> None:
        self.peer = peer
        self.slug = slug
        self.price = price
        self.duration = duration
        self.random_id = random_id
        self.allow_paid_stars = allow_paid_stars

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'allow_paid_stars', None) is not None and getattr(self, 'allow_paid_stars', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_string(self.slug)
        res += (self.price.write() if hasattr(self.price, 'write') else write_bytes(self.price))
        res += write_int(self.duration)
        res += write_long(self.random_id)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'allow_paid_stars', None) or 0
            if v is not None:
                res += write_long(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsSendStarsForm(TLRequest[Any]):
    ID = 0X7998C914
    QUALNAME = "functions.payments.sendStarsForm"

    def __init__(self, form_id: Any = None, invoice: Any = None) -> None:
        self.form_id = form_id
        self.invoice = invoice

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.form_id)
        res += (self.invoice.write() if hasattr(self.invoice, 'write') else write_bytes(self.invoice))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsToggleChatStarGiftNotifications(TLRequest[Any]):
    ID = 0X60EAEFA1
    QUALNAME = "functions.payments.toggleChatStarGiftNotifications"

    def __init__(self, enabled: Any = None, peer: Any = None) -> None:
        self.enabled = enabled
        self.peer = peer

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'enabled', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class PaymentsToggleStarGiftsPinnedToTop(TLRequest[Any]):
    ID = 0X1513E7B0
    QUALNAME = "functions.payments.toggleStarGiftsPinnedToTop"

    def __init__(self, peer: Any = None, stargift: Any = None) -> None:
        self.peer = peer
        self.stargift = stargift

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_vector(self.stargift, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class PaymentsTransferStarGift(TLRequest[Any]):
    ID = 0X7F18176A
    QUALNAME = "functions.payments.transferStarGift"

    def __init__(self, stargift: Any = None, to_id: Any = None) -> None:
        self.stargift = stargift
        self.to_id = to_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.stargift.write() if hasattr(self.stargift, 'write') else write_bytes(self.stargift))
        res += (self.to_id.write() if hasattr(self.to_id, 'write') else write_bytes(self.to_id))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsUpdateStarGiftCollection(TLRequest[Any]):
    ID = 0X4FDDBEE7
    QUALNAME = "functions.payments.updateStarGiftCollection"

    def __init__(self, peer: Any = None, collection_id: Any = None, title: Any = None, delete_stargift: Any = None, add_stargift: Any = None, order: Any = None) -> None:
        self.peer = peer
        self.collection_id = collection_id
        self.title = title
        self.delete_stargift = delete_stargift
        self.add_stargift = add_stargift
        self.order = order

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'title', None) is not None and getattr(self, 'title', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'delete_stargift', None) is not None and getattr(self, 'delete_stargift', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'add_stargift', None) is not None and getattr(self, 'add_stargift', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'order', None) is not None and getattr(self, 'order', None) is not False:
            flags |= (1 << 3)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.collection_id)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'title', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'delete_stargift', None) or []
            if v is not None:
                res += write_vector(v, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        if bool(flags & (1 << 2)):
            v = getattr(self, 'add_stargift', None) or []
            if v is not None:
                res += write_vector(v, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        if bool(flags & (1 << 3)):
            v = getattr(self, 'order', None) or []
            if v is not None:
                res += write_vector(v, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsUpdateStarGiftPrice(TLRequest[Any]):
    ID = 0XEDBE6CCB
    QUALNAME = "functions.payments.updateStarGiftPrice"

    def __init__(self, stargift: Any = None, resell_amount: Any = None) -> None:
        self.stargift = stargift
        self.resell_amount = resell_amount

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.stargift.write() if hasattr(self.stargift, 'write') else write_bytes(self.stargift))
        res += (self.resell_amount.write() if hasattr(self.resell_amount, 'write') else write_bytes(self.resell_amount))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsUpgradeStarGift(TLRequest[Any]):
    ID = 0XAED6E4F5
    QUALNAME = "functions.payments.upgradeStarGift"

    def __init__(self, keep_original_details: Any = None, stargift: Any = None) -> None:
        self.keep_original_details = keep_original_details
        self.stargift = stargift

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'keep_original_details', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.stargift.write() if hasattr(self.stargift, 'write') else write_bytes(self.stargift))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PaymentsValidateRequestedInfo(TLRequest[Any]):
    ID = 0XB6C8F12B
    QUALNAME = "functions.payments.validateRequestedInfo"

    def __init__(self, save: Any = None, invoice: Any = None, info: Any = None) -> None:
        self.save = save
        self.invoice = invoice
        self.info = info

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'save', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.invoice.write() if hasattr(self.invoice, 'write') else write_bytes(self.invoice))
        res += (self.info.write() if hasattr(self.info, 'write') else write_bytes(self.info))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneAcceptCall(TLRequest[Any]):
    ID = 0X3BD2B4A0
    QUALNAME = "functions.phone.acceptCall"

    def __init__(self, peer: Any = None, g_b: Any = None, protocol: Any = None) -> None:
        self.peer = peer
        self.g_b = g_b
        self.protocol = protocol

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_bytes(self.g_b)
        res += (self.protocol.write() if hasattr(self.protocol, 'write') else write_bytes(self.protocol))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneCheckGroupCall(TLRequest[Any]):
    ID = 0XB59CF977
    QUALNAME = "functions.phone.checkGroupCall"

    def __init__(self, call: Any = None, sources: Any = None) -> None:
        self.call = call
        self.sources = sources

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.call.write() if hasattr(self.call, 'write') else write_bytes(self.call))
        res += write_vector(self.sources, write_int)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x1CB5C415:
            return read_vector(b, read_int)
        return read_tl_object(b)

class PhoneConfirmCall(TLRequest[Any]):
    ID = 0X2EFE1722
    QUALNAME = "functions.phone.confirmCall"

    def __init__(self, peer: Any = None, g_a: Any = None, key_fingerprint: Any = None, protocol: Any = None) -> None:
        self.peer = peer
        self.g_a = g_a
        self.key_fingerprint = key_fingerprint
        self.protocol = protocol

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_bytes(self.g_a)
        res += write_long(self.key_fingerprint)
        res += (self.protocol.write() if hasattr(self.protocol, 'write') else write_bytes(self.protocol))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneCreateConferenceCall(TLRequest[Any]):
    ID = 0X7D0444BB
    QUALNAME = "functions.phone.createConferenceCall"

    def __init__(self, muted: Any = None, video_stopped: Any = None, join: Any = None, random_id: Any = None, public_key: Any = None, block: Any = None, params: Any = None) -> None:
        self.muted = muted
        self.video_stopped = video_stopped
        self.join = join
        self.random_id = random_id
        self.public_key = public_key
        self.block = block
        self.params = params

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'muted', None):
            flags |= (1 << 0)
        if getattr(self, 'video_stopped', None):
            flags |= (1 << 2)
        if getattr(self, 'join', None):
            flags |= (1 << 3)
        if getattr(self, 'public_key', None) is not None and getattr(self, 'public_key', None) is not False:
            flags |= (1 << 3)
        if getattr(self, 'block', None) is not None and getattr(self, 'block', None) is not False:
            flags |= (1 << 3)
        if getattr(self, 'params', None) is not None and getattr(self, 'params', None) is not False:
            flags |= (1 << 3)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_int(self.random_id)
        if bool(flags & (1 << 3)):
            v = getattr(self, 'public_key', None)
            if v is not None:
                res += write_int256(v)
        if bool(flags & (1 << 3)):
            v = getattr(self, 'block', None) or b''
            if v is not None:
                res += write_bytes(v)
        if bool(flags & (1 << 3)):
            v = getattr(self, 'params', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneCreateGroupCall(TLRequest[Any]):
    ID = 0X48CDC6D8
    QUALNAME = "functions.phone.createGroupCall"

    def __init__(self, rtmp_stream: Any = None, peer: Any = None, random_id: Any = None, title: Any = None, schedule_date: Any = None) -> None:
        self.rtmp_stream = rtmp_stream
        self.peer = peer
        self.random_id = random_id
        self.title = title
        self.schedule_date = schedule_date

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'rtmp_stream', None):
            flags |= (1 << 2)
        if getattr(self, 'title', None) is not None and getattr(self, 'title', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'schedule_date', None) is not None and getattr(self, 'schedule_date', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.random_id)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'title', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'schedule_date', None) or 0
            if v is not None:
                res += write_int(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneDeclineConferenceCallInvite(TLRequest[Any]):
    ID = 0X3C479971
    QUALNAME = "functions.phone.declineConferenceCallInvite"

    def __init__(self, msg_id: Any = None) -> None:
        self.msg_id = msg_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int(self.msg_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneDeleteConferenceCallParticipants(TLRequest[Any]):
    ID = 0X8CA60525
    QUALNAME = "functions.phone.deleteConferenceCallParticipants"

    def __init__(self, only_left: Any = None, kick: Any = None, call: Any = None, ids: Any = None, block: Any = None) -> None:
        self.only_left = only_left
        self.kick = kick
        self.call = call
        self.ids = ids
        self.block = block

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'only_left', None):
            flags |= (1 << 0)
        if getattr(self, 'kick', None):
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.call.write() if hasattr(self.call, 'write') else write_bytes(self.call))
        res += write_vector(self.ids, write_long)
        res += write_bytes(self.block)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneDeleteGroupCallMessages(TLRequest[Any]):
    ID = 0XF64F54F7
    QUALNAME = "functions.phone.deleteGroupCallMessages"

    def __init__(self, report_spam: Any = None, call: Any = None, messages: Any = None) -> None:
        self.report_spam = report_spam
        self.call = call
        self.messages = messages

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'report_spam', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.call.write() if hasattr(self.call, 'write') else write_bytes(self.call))
        res += write_vector(self.messages, write_int)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneDeleteGroupCallParticipantMessages(TLRequest[Any]):
    ID = 0X1DBFECA0
    QUALNAME = "functions.phone.deleteGroupCallParticipantMessages"

    def __init__(self, report_spam: Any = None, call: Any = None, participant: Any = None) -> None:
        self.report_spam = report_spam
        self.call = call
        self.participant = participant

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'report_spam', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.call.write() if hasattr(self.call, 'write') else write_bytes(self.call))
        res += (self.participant.write() if hasattr(self.participant, 'write') else write_bytes(self.participant))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneDiscardCall(TLRequest[Any]):
    ID = 0XB2CBC1C0
    QUALNAME = "functions.phone.discardCall"

    def __init__(self, video: Any = None, peer: Any = None, duration: Any = None, reason: Any = None, connection_id: Any = None) -> None:
        self.video = video
        self.peer = peer
        self.duration = duration
        self.reason = reason
        self.connection_id = connection_id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'video', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.duration)
        res += (self.reason.write() if hasattr(self.reason, 'write') else write_bytes(self.reason))
        res += write_long(self.connection_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneDiscardGroupCall(TLRequest[Any]):
    ID = 0X7A777135
    QUALNAME = "functions.phone.discardGroupCall"

    def __init__(self, call: Any = None) -> None:
        self.call = call

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.call.write() if hasattr(self.call, 'write') else write_bytes(self.call))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneEditGroupCallParticipant(TLRequest[Any]):
    ID = 0XA5273ABF
    QUALNAME = "functions.phone.editGroupCallParticipant"

    def __init__(self, call: Any = None, participant: Any = None, muted: Any = None, volume: Any = None, raise_hand: Any = None, video_stopped: Any = None, video_paused: Any = None, presentation_paused: Any = None) -> None:
        self.call = call
        self.participant = participant
        self.muted = muted
        self.volume = volume
        self.raise_hand = raise_hand
        self.video_stopped = video_stopped
        self.video_paused = video_paused
        self.presentation_paused = presentation_paused

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'muted', None) is not None and getattr(self, 'muted', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'volume', None) is not None and getattr(self, 'volume', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'raise_hand', None) is not None and getattr(self, 'raise_hand', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'video_stopped', None) is not None and getattr(self, 'video_stopped', None) is not False:
            flags |= (1 << 3)
        if getattr(self, 'video_paused', None) is not None and getattr(self, 'video_paused', None) is not False:
            flags |= (1 << 4)
        if getattr(self, 'presentation_paused', None) is not None and getattr(self, 'presentation_paused', None) is not False:
            flags |= (1 << 5)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.call.write() if hasattr(self.call, 'write') else write_bytes(self.call))
        res += (self.participant.write() if hasattr(self.participant, 'write') else write_bytes(self.participant))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'muted', None)
            if v is not None:
                res += write_bool(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'volume', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'raise_hand', None)
            if v is not None:
                res += write_bool(v)
        if bool(flags & (1 << 3)):
            v = getattr(self, 'video_stopped', None)
            if v is not None:
                res += write_bool(v)
        if bool(flags & (1 << 4)):
            v = getattr(self, 'video_paused', None)
            if v is not None:
                res += write_bool(v)
        if bool(flags & (1 << 5)):
            v = getattr(self, 'presentation_paused', None)
            if v is not None:
                res += write_bool(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneEditGroupCallTitle(TLRequest[Any]):
    ID = 0X1CA6AC0A
    QUALNAME = "functions.phone.editGroupCallTitle"

    def __init__(self, call: Any = None, title: Any = None) -> None:
        self.call = call
        self.title = title

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.call.write() if hasattr(self.call, 'write') else write_bytes(self.call))
        res += write_string(self.title)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneExportGroupCallInvite(TLRequest[Any]):
    ID = 0XE6AA647F
    QUALNAME = "functions.phone.exportGroupCallInvite"

    def __init__(self, can_self_unmute: Any = None, call: Any = None) -> None:
        self.can_self_unmute = can_self_unmute
        self.call = call

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'can_self_unmute', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.call.write() if hasattr(self.call, 'write') else write_bytes(self.call))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneGetCallConfig(TLRequest[Any]):
    ID = 0X55451FA9
    QUALNAME = "functions.phone.getCallConfig"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneGetGroupCall(TLRequest[Any]):
    ID = 0X41845DB
    QUALNAME = "functions.phone.getGroupCall"

    def __init__(self, call: Any = None, limit: Any = None) -> None:
        self.call = call
        self.limit = limit

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.call.write() if hasattr(self.call, 'write') else write_bytes(self.call))
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneGetGroupCallChainBlocks(TLRequest[Any]):
    ID = 0XEE9F88A6
    QUALNAME = "functions.phone.getGroupCallChainBlocks"

    def __init__(self, call: Any = None, sub_chain_id: Any = None, offset: Any = None, limit: Any = None) -> None:
        self.call = call
        self.sub_chain_id = sub_chain_id
        self.offset = offset
        self.limit = limit

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.call.write() if hasattr(self.call, 'write') else write_bytes(self.call))
        res += write_int(self.sub_chain_id)
        res += write_int(self.offset)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneGetGroupCallJoinAs(TLRequest[Any]):
    ID = 0XEF7C213A
    QUALNAME = "functions.phone.getGroupCallJoinAs"

    def __init__(self, peer: Any = None) -> None:
        self.peer = peer

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneGetGroupCallStars(TLRequest[Any]):
    ID = 0X6F636302
    QUALNAME = "functions.phone.getGroupCallStars"

    def __init__(self, call: Any = None) -> None:
        self.call = call

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.call.write() if hasattr(self.call, 'write') else write_bytes(self.call))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneGetGroupCallStreamChannels(TLRequest[Any]):
    ID = 0X1AB21940
    QUALNAME = "functions.phone.getGroupCallStreamChannels"

    def __init__(self, call: Any = None) -> None:
        self.call = call

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.call.write() if hasattr(self.call, 'write') else write_bytes(self.call))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneGetGroupCallStreamRtmpUrl(TLRequest[Any]):
    ID = 0X5AF4C73A
    QUALNAME = "functions.phone.getGroupCallStreamRtmpUrl"

    def __init__(self, live_story: Any = None, peer: Any = None, revoke: Any = None) -> None:
        self.live_story = live_story
        self.peer = peer
        self.revoke = revoke

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'live_story', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_bool(self.revoke)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneGetGroupParticipants(TLRequest[Any]):
    ID = 0XC558D8AB
    QUALNAME = "functions.phone.getGroupParticipants"

    def __init__(self, call: Any = None, ids: Any = None, sources: Any = None, offset: Any = None, limit: Any = None) -> None:
        self.call = call
        self.ids = ids
        self.sources = sources
        self.offset = offset
        self.limit = limit

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.call.write() if hasattr(self.call, 'write') else write_bytes(self.call))
        res += write_vector(self.ids, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        res += write_vector(self.sources, write_int)
        res += write_string(self.offset)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneInviteConferenceCallParticipant(TLRequest[Any]):
    ID = 0XBCF22685
    QUALNAME = "functions.phone.inviteConferenceCallParticipant"

    def __init__(self, video: Any = None, call: Any = None, user_id: Any = None) -> None:
        self.video = video
        self.call = call
        self.user_id = user_id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'video', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.call.write() if hasattr(self.call, 'write') else write_bytes(self.call))
        res += (self.user_id.write() if hasattr(self.user_id, 'write') else write_bytes(self.user_id))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneInviteToGroupCall(TLRequest[Any]):
    ID = 0X7B393160
    QUALNAME = "functions.phone.inviteToGroupCall"

    def __init__(self, call: Any = None, users: Any = None) -> None:
        self.call = call
        self.users = users

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.call.write() if hasattr(self.call, 'write') else write_bytes(self.call))
        res += write_vector(self.users, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneJoinGroupCall(TLRequest[Any]):
    ID = 0X8FB53057
    QUALNAME = "functions.phone.joinGroupCall"

    def __init__(self, muted: Any = None, video_stopped: Any = None, call: Any = None, join_as: Any = None, invite_hash: Any = None, public_key: Any = None, block: Any = None, params: Any = None) -> None:
        self.muted = muted
        self.video_stopped = video_stopped
        self.call = call
        self.join_as = join_as
        self.invite_hash = invite_hash
        self.public_key = public_key
        self.block = block
        self.params = params

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'muted', None):
            flags |= (1 << 0)
        if getattr(self, 'video_stopped', None):
            flags |= (1 << 2)
        if getattr(self, 'invite_hash', None) is not None and getattr(self, 'invite_hash', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'public_key', None) is not None and getattr(self, 'public_key', None) is not False:
            flags |= (1 << 3)
        if getattr(self, 'block', None) is not None and getattr(self, 'block', None) is not False:
            flags |= (1 << 3)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.call.write() if hasattr(self.call, 'write') else write_bytes(self.call))
        res += (self.join_as.write() if hasattr(self.join_as, 'write') else write_bytes(self.join_as))
        if bool(flags & (1 << 1)):
            v = getattr(self, 'invite_hash', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 3)):
            v = getattr(self, 'public_key', None)
            if v is not None:
                res += write_int256(v)
        if bool(flags & (1 << 3)):
            v = getattr(self, 'block', None) or b''
            if v is not None:
                res += write_bytes(v)
        res += (self.params.write() if hasattr(self.params, 'write') else write_bytes(self.params))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneJoinGroupCallPresentation(TLRequest[Any]):
    ID = 0XCBEA6BC4
    QUALNAME = "functions.phone.joinGroupCallPresentation"

    def __init__(self, call: Any = None, params: Any = None) -> None:
        self.call = call
        self.params = params

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.call.write() if hasattr(self.call, 'write') else write_bytes(self.call))
        res += (self.params.write() if hasattr(self.params, 'write') else write_bytes(self.params))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneLeaveGroupCall(TLRequest[Any]):
    ID = 0X500377F9
    QUALNAME = "functions.phone.leaveGroupCall"

    def __init__(self, call: Any = None, source: Any = None) -> None:
        self.call = call
        self.source = source

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.call.write() if hasattr(self.call, 'write') else write_bytes(self.call))
        res += write_int(self.source)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneLeaveGroupCallPresentation(TLRequest[Any]):
    ID = 0X1C50D144
    QUALNAME = "functions.phone.leaveGroupCallPresentation"

    def __init__(self, call: Any = None) -> None:
        self.call = call

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.call.write() if hasattr(self.call, 'write') else write_bytes(self.call))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneReceivedCall(TLRequest[Any]):
    ID = 0X17D54F61
    QUALNAME = "functions.phone.receivedCall"

    def __init__(self, peer: Any = None) -> None:
        self.peer = peer

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class PhoneRequestCall(TLRequest[Any]):
    ID = 0X42FF96ED
    QUALNAME = "functions.phone.requestCall"

    def __init__(self, video: Any = None, user_id: Any = None, random_id: Any = None, g_a_hash: Any = None, protocol: Any = None) -> None:
        self.video = video
        self.user_id = user_id
        self.random_id = random_id
        self.g_a_hash = g_a_hash
        self.protocol = protocol

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'video', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.user_id.write() if hasattr(self.user_id, 'write') else write_bytes(self.user_id))
        res += write_int(self.random_id)
        res += write_bytes(self.g_a_hash)
        res += (self.protocol.write() if hasattr(self.protocol, 'write') else write_bytes(self.protocol))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneSaveCallDebug(TLRequest[Any]):
    ID = 0X277ADD7E
    QUALNAME = "functions.phone.saveCallDebug"

    def __init__(self, peer: Any = None, debug: Any = None) -> None:
        self.peer = peer
        self.debug = debug

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += (self.debug.write() if hasattr(self.debug, 'write') else write_bytes(self.debug))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class PhoneSaveCallLog(TLRequest[Any]):
    ID = 0X41248786
    QUALNAME = "functions.phone.saveCallLog"

    def __init__(self, peer: Any = None, file: Any = None) -> None:
        self.peer = peer
        self.file = file

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += (self.file.write() if hasattr(self.file, 'write') else write_bytes(self.file))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class PhoneSaveDefaultGroupCallJoinAs(TLRequest[Any]):
    ID = 0X575E1F8C
    QUALNAME = "functions.phone.saveDefaultGroupCallJoinAs"

    def __init__(self, peer: Any = None, join_as: Any = None) -> None:
        self.peer = peer
        self.join_as = join_as

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += (self.join_as.write() if hasattr(self.join_as, 'write') else write_bytes(self.join_as))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class PhoneSaveDefaultSendAs(TLRequest[Any]):
    ID = 0X4167ADD1
    QUALNAME = "functions.phone.saveDefaultSendAs"

    def __init__(self, call: Any = None, send_as: Any = None) -> None:
        self.call = call
        self.send_as = send_as

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.call.write() if hasattr(self.call, 'write') else write_bytes(self.call))
        res += (self.send_as.write() if hasattr(self.send_as, 'write') else write_bytes(self.send_as))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class PhoneSendConferenceCallBroadcast(TLRequest[Any]):
    ID = 0XC6701900
    QUALNAME = "functions.phone.sendConferenceCallBroadcast"

    def __init__(self, call: Any = None, block: Any = None) -> None:
        self.call = call
        self.block = block

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.call.write() if hasattr(self.call, 'write') else write_bytes(self.call))
        res += write_bytes(self.block)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneSendGroupCallEncryptedMessage(TLRequest[Any]):
    ID = 0XE5AFA56D
    QUALNAME = "functions.phone.sendGroupCallEncryptedMessage"

    def __init__(self, call: Any = None, encrypted_message: Any = None) -> None:
        self.call = call
        self.encrypted_message = encrypted_message

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.call.write() if hasattr(self.call, 'write') else write_bytes(self.call))
        res += write_bytes(self.encrypted_message)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class PhoneSendGroupCallMessage(TLRequest[Any]):
    ID = 0XB1D11410
    QUALNAME = "functions.phone.sendGroupCallMessage"

    def __init__(self, call: Any = None, random_id: Any = None, message: Any = None, allow_paid_stars: Any = None, send_as: Any = None) -> None:
        self.call = call
        self.random_id = random_id
        self.message = message
        self.allow_paid_stars = allow_paid_stars
        self.send_as = send_as

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'allow_paid_stars', None) is not None and getattr(self, 'allow_paid_stars', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'send_as', None) is not None and getattr(self, 'send_as', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.call.write() if hasattr(self.call, 'write') else write_bytes(self.call))
        res += write_long(self.random_id)
        res += (self.message.write() if hasattr(self.message, 'write') else write_bytes(self.message))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'allow_paid_stars', None) or 0
            if v is not None:
                res += write_long(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'send_as', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneSendSignalingData(TLRequest[Any]):
    ID = 0XFF7A9383
    QUALNAME = "functions.phone.sendSignalingData"

    def __init__(self, peer: Any = None, data: Any = None) -> None:
        self.peer = peer
        self.data = data

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_bytes(self.data)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class PhoneSetCallRating(TLRequest[Any]):
    ID = 0X59EAD627
    QUALNAME = "functions.phone.setCallRating"

    def __init__(self, user_initiative: Any = None, peer: Any = None, rating: Any = None, comment: Any = None) -> None:
        self.user_initiative = user_initiative
        self.peer = peer
        self.rating = rating
        self.comment = comment

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'user_initiative', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.rating)
        res += write_string(self.comment)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneStartScheduledGroupCall(TLRequest[Any]):
    ID = 0X5680E342
    QUALNAME = "functions.phone.startScheduledGroupCall"

    def __init__(self, call: Any = None) -> None:
        self.call = call

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.call.write() if hasattr(self.call, 'write') else write_bytes(self.call))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneToggleGroupCallRecord(TLRequest[Any]):
    ID = 0XF128C708
    QUALNAME = "functions.phone.toggleGroupCallRecord"

    def __init__(self, start: Any = None, video: Any = None, call: Any = None, title: Any = None, video_portrait: Any = None) -> None:
        self.start = start
        self.video = video
        self.call = call
        self.title = title
        self.video_portrait = video_portrait

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'start', None):
            flags |= (1 << 0)
        if getattr(self, 'video', None):
            flags |= (1 << 2)
        if getattr(self, 'title', None) is not None and getattr(self, 'title', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'video_portrait', None) is not None and getattr(self, 'video_portrait', None) is not False:
            flags |= (1 << 2)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.call.write() if hasattr(self.call, 'write') else write_bytes(self.call))
        if bool(flags & (1 << 1)):
            v = getattr(self, 'title', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'video_portrait', None)
            if v is not None:
                res += write_bool(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneToggleGroupCallSettings(TLRequest[Any]):
    ID = 0X974392F2
    QUALNAME = "functions.phone.toggleGroupCallSettings"

    def __init__(self, reset_invite_hash: Any = None, call: Any = None, join_muted: Any = None, messages_enabled: Any = None, send_paid_messages_stars: Any = None) -> None:
        self.reset_invite_hash = reset_invite_hash
        self.call = call
        self.join_muted = join_muted
        self.messages_enabled = messages_enabled
        self.send_paid_messages_stars = send_paid_messages_stars

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'reset_invite_hash', None):
            flags |= (1 << 1)
        if getattr(self, 'join_muted', None) is not None and getattr(self, 'join_muted', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'messages_enabled', None) is not None and getattr(self, 'messages_enabled', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'send_paid_messages_stars', None) is not None and getattr(self, 'send_paid_messages_stars', None) is not False:
            flags |= (1 << 3)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.call.write() if hasattr(self.call, 'write') else write_bytes(self.call))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'join_muted', None)
            if v is not None:
                res += write_bool(v)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'messages_enabled', None)
            if v is not None:
                res += write_bool(v)
        if bool(flags & (1 << 3)):
            v = getattr(self, 'send_paid_messages_stars', None) or 0
            if v is not None:
                res += write_long(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhoneToggleGroupCallStartSubscription(TLRequest[Any]):
    ID = 0X219C34E6
    QUALNAME = "functions.phone.toggleGroupCallStartSubscription"

    def __init__(self, call: Any = None, subscribed: Any = None) -> None:
        self.call = call
        self.subscribed = subscribed

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.call.write() if hasattr(self.call, 'write') else write_bytes(self.call))
        res += write_bool(self.subscribed)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhotosDeletePhotos(TLRequest[Any]):
    ID = 0X87CF7F2F
    QUALNAME = "functions.photos.deletePhotos"

    def __init__(self, id: Any = None) -> None:
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_vector(self.id, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x1CB5C415:
            return read_vector(b, read_long)
        return read_tl_object(b)

class PhotosGetUserPhotos(TLRequest[Any]):
    ID = 0X91CD32A8
    QUALNAME = "functions.photos.getUserPhotos"

    def __init__(self, user_id: Any = None, offset: Any = None, max_id: Any = None, limit: Any = None) -> None:
        self.user_id = user_id
        self.offset = offset
        self.max_id = max_id
        self.limit = limit

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.user_id.write() if hasattr(self.user_id, 'write') else write_bytes(self.user_id))
        res += write_int(self.offset)
        res += write_long(self.max_id)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhotosUpdateProfilePhoto(TLRequest[Any]):
    ID = 0X9E82039
    QUALNAME = "functions.photos.updateProfilePhoto"

    def __init__(self, fallback: Any = None, bot: Any = None, id: Any = None) -> None:
        self.fallback = fallback
        self.bot = bot
        self.id = id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'fallback', None):
            flags |= (1 << 0)
        if getattr(self, 'bot', None) is not None and getattr(self, 'bot', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'bot', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += (self.id.write() if hasattr(self.id, 'write') else write_bytes(self.id))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhotosUploadContactProfilePhoto(TLRequest[Any]):
    ID = 0XE14C4A71
    QUALNAME = "functions.photos.uploadContactProfilePhoto"

    def __init__(self, suggest: Any = None, save: Any = None, user_id: Any = None, file: Any = None, video: Any = None, video_start_ts: Any = None, video_emoji_markup: Any = None) -> None:
        self.suggest = suggest
        self.save = save
        self.user_id = user_id
        self.file = file
        self.video = video
        self.video_start_ts = video_start_ts
        self.video_emoji_markup = video_emoji_markup

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'suggest', None):
            flags |= (1 << 3)
        if getattr(self, 'save', None):
            flags |= (1 << 4)
        if getattr(self, 'file', None) is not None and getattr(self, 'file', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'video', None) is not None and getattr(self, 'video', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'video_start_ts', None) is not None and getattr(self, 'video_start_ts', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'video_emoji_markup', None) is not None and getattr(self, 'video_emoji_markup', None) is not False:
            flags |= (1 << 5)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.user_id.write() if hasattr(self.user_id, 'write') else write_bytes(self.user_id))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'file', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 1)):
            v = getattr(self, 'video', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 2)):
            v = getattr(self, 'video_start_ts', None) or 0
            if v is not None:
                res += write_double(v)
        if bool(flags & (1 << 5)):
            v = getattr(self, 'video_emoji_markup', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PhotosUploadProfilePhoto(TLRequest[Any]):
    ID = 0X388A3B5
    QUALNAME = "functions.photos.uploadProfilePhoto"

    def __init__(self, fallback: Any = None, bot: Any = None, file: Any = None, video: Any = None, video_start_ts: Any = None, video_emoji_markup: Any = None) -> None:
        self.fallback = fallback
        self.bot = bot
        self.file = file
        self.video = video
        self.video_start_ts = video_start_ts
        self.video_emoji_markup = video_emoji_markup

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'fallback', None):
            flags |= (1 << 3)
        if getattr(self, 'bot', None) is not None and getattr(self, 'bot', None) is not False:
            flags |= (1 << 5)
        if getattr(self, 'file', None) is not None and getattr(self, 'file', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'video', None) is not None and getattr(self, 'video', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'video_start_ts', None) is not None and getattr(self, 'video_start_ts', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'video_emoji_markup', None) is not None and getattr(self, 'video_emoji_markup', None) is not False:
            flags |= (1 << 4)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 5)):
            v = getattr(self, 'bot', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'file', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 1)):
            v = getattr(self, 'video', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 2)):
            v = getattr(self, 'video_start_ts', None) or 0
            if v is not None:
                res += write_double(v)
        if bool(flags & (1 << 4)):
            v = getattr(self, 'video_emoji_markup', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class Ping(TLRequest[Any]):
    ID = 0X7ABE77EC
    QUALNAME = "functions.ping"

    def __init__(self, ping_id: Any = None) -> None:
        self.ping_id = ping_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.ping_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PingDelayDisconnect(TLRequest[Any]):
    ID = 0XF3427B8C
    QUALNAME = "functions.ping_delay_disconnect"

    def __init__(self, ping_id: Any = None, disconnect_delay: Any = None) -> None:
        self.ping_id = ping_id
        self.disconnect_delay = disconnect_delay

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.ping_id)
        res += write_int(self.disconnect_delay)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PremiumApplyBoost(TLRequest[Any]):
    ID = 0X6B7DA746
    QUALNAME = "functions.premium.applyBoost"

    def __init__(self, slots: Any = None, peer: Any = None) -> None:
        self.slots = slots
        self.peer = peer

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'slots', None) is not None and getattr(self, 'slots', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'slots', None) or []
            if v is not None:
                res += write_vector(v, write_int)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PremiumGetBoostsList(TLRequest[Any]):
    ID = 0X60F67660
    QUALNAME = "functions.premium.getBoostsList"

    def __init__(self, gifts: Any = None, peer: Any = None, offset: Any = None, limit: Any = None) -> None:
        self.gifts = gifts
        self.peer = peer
        self.offset = offset
        self.limit = limit

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'gifts', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_string(self.offset)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PremiumGetBoostsStatus(TLRequest[Any]):
    ID = 0X42F1F61
    QUALNAME = "functions.premium.getBoostsStatus"

    def __init__(self, peer: Any = None) -> None:
        self.peer = peer

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PremiumGetMyBoosts(TLRequest[Any]):
    ID = 0XBE77B4A
    QUALNAME = "functions.premium.getMyBoosts"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class PremiumGetUserBoosts(TLRequest[Any]):
    ID = 0X39854D1F
    QUALNAME = "functions.premium.getUserBoosts"

    def __init__(self, peer: Any = None, user_id: Any = None) -> None:
        self.peer = peer
        self.user_id = user_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += (self.user_id.write() if hasattr(self.user_id, 'write') else write_bytes(self.user_id))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ReqDhParams(TLRequest[Any]):
    ID = 0XD712E4BE
    QUALNAME = "functions.req_DH_params"

    def __init__(self, nonce: Any = None, server_nonce: Any = None, p: Any = None, q: Any = None, public_key_fingerprint: Any = None, encrypted_data: Any = None) -> None:
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.p = p
        self.q = q
        self.public_key_fingerprint = public_key_fingerprint
        self.encrypted_data = encrypted_data

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int128(self.nonce)
        res += write_int128(self.server_nonce)
        res += write_string(self.p)
        res += write_string(self.q)
        res += write_long(self.public_key_fingerprint)
        res += write_string(self.encrypted_data)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ReqPq(TLRequest[Any]):
    ID = 0X60469778
    QUALNAME = "functions.req_pq"

    def __init__(self, nonce: Any = None) -> None:
        self.nonce = nonce

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int128(self.nonce)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ReqPqMulti(TLRequest[Any]):
    ID = 0XBE7E8EF1
    QUALNAME = "functions.req_pq_multi"

    def __init__(self, nonce: Any = None) -> None:
        self.nonce = nonce

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int128(self.nonce)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ResPq(TLRequest[Any]):
    ID = 0X5162463
    QUALNAME = "functions.resPQ"

    def __init__(self, nonce: Any = None, server_nonce: Any = None, pq: Any = None, server_public_key_fingerprints: Any = None) -> None:
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.pq = pq
        self.server_public_key_fingerprints = server_public_key_fingerprints

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int128(self.nonce)
        res += write_int128(self.server_nonce)
        res += write_string(self.pq)
        res += write_vector(self.server_public_key_fingerprints, write_long)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class RpcDropAnswer(TLRequest[Any]):
    ID = 0X58E4A740
    QUALNAME = "functions.rpc_drop_answer"

    def __init__(self, req_msg_id: Any = None) -> None:
        self.req_msg_id = req_msg_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.req_msg_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ServerDhInnerData(TLRequest[Any]):
    ID = 0XB5890DBA
    QUALNAME = "functions.server_DH_inner_data"

    def __init__(self, nonce: Any = None, server_nonce: Any = None, g: Any = None, dh_prime: Any = None, g_a: Any = None, server_time: Any = None) -> None:
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.g = g
        self.dh_prime = dh_prime
        self.g_a = g_a
        self.server_time = server_time

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int128(self.nonce)
        res += write_int128(self.server_nonce)
        res += write_int(self.g)
        res += write_string(self.dh_prime)
        res += write_string(self.g_a)
        res += write_int(self.server_time)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ServerDhParamsFail(TLRequest[Any]):
    ID = 0X79CB045D
    QUALNAME = "functions.server_DH_params_fail"

    def __init__(self, nonce: Any = None, server_nonce: Any = None, new_nonce_hash: Any = None) -> None:
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.new_nonce_hash = new_nonce_hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int128(self.nonce)
        res += write_int128(self.server_nonce)
        res += write_int128(self.new_nonce_hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class ServerDhParamsOk(TLRequest[Any]):
    ID = 0XD0E8075C
    QUALNAME = "functions.server_DH_params_ok"

    def __init__(self, nonce: Any = None, server_nonce: Any = None, encrypted_answer: Any = None) -> None:
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.encrypted_answer = encrypted_answer

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int128(self.nonce)
        res += write_int128(self.server_nonce)
        res += write_string(self.encrypted_answer)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class SetClientDhParams(TLRequest[Any]):
    ID = 0XF5045F1F
    QUALNAME = "functions.set_client_DH_params"

    def __init__(self, nonce: Any = None, server_nonce: Any = None, encrypted_data: Any = None) -> None:
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.encrypted_data = encrypted_data

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_int128(self.nonce)
        res += write_int128(self.server_nonce)
        res += write_string(self.encrypted_data)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class SmsjobsFinishJob(TLRequest[Any]):
    ID = 0X4F1EBF24
    QUALNAME = "functions.smsjobs.finishJob"

    def __init__(self, job_id: Any = None, error: Any = None) -> None:
        self.job_id = job_id
        self.error = error

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'error', None) is not None and getattr(self, 'error', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_string(self.job_id)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'error', None) or ''
            if v is not None:
                res += write_string(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class SmsjobsGetSmsJob(TLRequest[Any]):
    ID = 0X778D902F
    QUALNAME = "functions.smsjobs.getSmsJob"

    def __init__(self, job_id: Any = None) -> None:
        self.job_id = job_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.job_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class SmsjobsGetStatus(TLRequest[Any]):
    ID = 0X10A698E8
    QUALNAME = "functions.smsjobs.getStatus"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class SmsjobsIsEligibleToJoin(TLRequest[Any]):
    ID = 0XEDC39D0
    QUALNAME = "functions.smsjobs.isEligibleToJoin"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class SmsjobsJoin(TLRequest[Any]):
    ID = 0XA74ECE2D
    QUALNAME = "functions.smsjobs.join"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class SmsjobsLeave(TLRequest[Any]):
    ID = 0X9898AD73
    QUALNAME = "functions.smsjobs.leave"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class SmsjobsUpdateSettings(TLRequest[Any]):
    ID = 0X93FA0BF
    QUALNAME = "functions.smsjobs.updateSettings"

    def __init__(self, allow_international: Any = None) -> None:
        self.allow_international = allow_international

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'allow_international', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class StatsGetBroadcastStats(TLRequest[Any]):
    ID = 0XAB42441A
    QUALNAME = "functions.stats.getBroadcastStats"

    def __init__(self, dark: Any = None, channel: Any = None) -> None:
        self.dark = dark
        self.channel = channel

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'dark', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StatsGetMegagroupStats(TLRequest[Any]):
    ID = 0XDCDF8607
    QUALNAME = "functions.stats.getMegagroupStats"

    def __init__(self, dark: Any = None, channel: Any = None) -> None:
        self.dark = dark
        self.channel = channel

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'dark', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StatsGetMessagePublicForwards(TLRequest[Any]):
    ID = 0X5F150144
    QUALNAME = "functions.stats.getMessagePublicForwards"

    def __init__(self, channel: Any = None, msg_id: Any = None, offset: Any = None, limit: Any = None) -> None:
        self.channel = channel
        self.msg_id = msg_id
        self.offset = offset
        self.limit = limit

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += write_int(self.msg_id)
        res += write_string(self.offset)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StatsGetMessageStats(TLRequest[Any]):
    ID = 0XB6E0A3F5
    QUALNAME = "functions.stats.getMessageStats"

    def __init__(self, dark: Any = None, channel: Any = None, msg_id: Any = None) -> None:
        self.dark = dark
        self.channel = channel
        self.msg_id = msg_id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'dark', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += write_int(self.msg_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StatsGetPollStats(TLRequest[Any]):
    ID = 0XC27DFA68
    QUALNAME = "functions.stats.getPollStats"

    def __init__(self, dark: Any = None, peer: Any = None, msg_id: Any = None) -> None:
        self.dark = dark
        self.peer = peer
        self.msg_id = msg_id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'dark', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.msg_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StatsGetStoryPublicForwards(TLRequest[Any]):
    ID = 0XA6437EF6
    QUALNAME = "functions.stats.getStoryPublicForwards"

    def __init__(self, peer: Any = None, id: Any = None, offset: Any = None, limit: Any = None) -> None:
        self.peer = peer
        self.id = id
        self.offset = offset
        self.limit = limit

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.id)
        res += write_string(self.offset)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StatsGetStoryStats(TLRequest[Any]):
    ID = 0X374FEF40
    QUALNAME = "functions.stats.getStoryStats"

    def __init__(self, dark: Any = None, peer: Any = None, id: Any = None) -> None:
        self.dark = dark
        self.peer = peer
        self.id = id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'dark', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StatsLoadAsyncGraph(TLRequest[Any]):
    ID = 0X621D5FA0
    QUALNAME = "functions.stats.loadAsyncGraph"

    def __init__(self, token: Any = None, x: Any = None) -> None:
        self.token = token
        self.x = x

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'x', None) is not None and getattr(self, 'x', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_string(self.token)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'x', None) or 0
            if v is not None:
                res += write_long(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StickersAddStickerToSet(TLRequest[Any]):
    ID = 0X8653FEBE
    QUALNAME = "functions.stickers.addStickerToSet"

    def __init__(self, stickerset: Any = None, sticker: Any = None) -> None:
        self.stickerset = stickerset
        self.sticker = sticker

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.stickerset.write() if hasattr(self.stickerset, 'write') else write_bytes(self.stickerset))
        res += (self.sticker.write() if hasattr(self.sticker, 'write') else write_bytes(self.sticker))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StickersChangeSticker(TLRequest[Any]):
    ID = 0XF5537EBC
    QUALNAME = "functions.stickers.changeSticker"

    def __init__(self, sticker: Any = None, emoji: Any = None, mask_coords: Any = None, keywords: Any = None) -> None:
        self.sticker = sticker
        self.emoji = emoji
        self.mask_coords = mask_coords
        self.keywords = keywords

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'emoji', None) is not None and getattr(self, 'emoji', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'mask_coords', None) is not None and getattr(self, 'mask_coords', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'keywords', None) is not None and getattr(self, 'keywords', None) is not False:
            flags |= (1 << 2)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.sticker.write() if hasattr(self.sticker, 'write') else write_bytes(self.sticker))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'emoji', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'mask_coords', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 2)):
            v = getattr(self, 'keywords', None) or ''
            if v is not None:
                res += write_string(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StickersChangeStickerPosition(TLRequest[Any]):
    ID = 0XFFB6D4CA
    QUALNAME = "functions.stickers.changeStickerPosition"

    def __init__(self, sticker: Any = None, position: Any = None) -> None:
        self.sticker = sticker
        self.position = position

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.sticker.write() if hasattr(self.sticker, 'write') else write_bytes(self.sticker))
        res += write_int(self.position)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StickersCheckShortName(TLRequest[Any]):
    ID = 0X284B3639
    QUALNAME = "functions.stickers.checkShortName"

    def __init__(self, short_name: Any = None) -> None:
        self.short_name = short_name

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.short_name)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class StickersCreateStickerSet(TLRequest[Any]):
    ID = 0X9021AB67
    QUALNAME = "functions.stickers.createStickerSet"

    def __init__(self, masks: Any = None, emojis: Any = None, text_color: Any = None, user_id: Any = None, title: Any = None, short_name: Any = None, thumb: Any = None, stickers: Any = None, software: Any = None) -> None:
        self.masks = masks
        self.emojis = emojis
        self.text_color = text_color
        self.user_id = user_id
        self.title = title
        self.short_name = short_name
        self.thumb = thumb
        self.stickers = stickers
        self.software = software

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'masks', None):
            flags |= (1 << 0)
        if getattr(self, 'emojis', None):
            flags |= (1 << 5)
        if getattr(self, 'text_color', None):
            flags |= (1 << 6)
        if getattr(self, 'thumb', None) is not None and getattr(self, 'thumb', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'software', None) is not None and getattr(self, 'software', None) is not False:
            flags |= (1 << 3)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.user_id.write() if hasattr(self.user_id, 'write') else write_bytes(self.user_id))
        res += write_string(self.title)
        res += write_string(self.short_name)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'thumb', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += write_vector(self.stickers, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        if bool(flags & (1 << 3)):
            v = getattr(self, 'software', None) or ''
            if v is not None:
                res += write_string(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StickersDeleteStickerSet(TLRequest[Any]):
    ID = 0X87704394
    QUALNAME = "functions.stickers.deleteStickerSet"

    def __init__(self, stickerset: Any = None) -> None:
        self.stickerset = stickerset

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.stickerset.write() if hasattr(self.stickerset, 'write') else write_bytes(self.stickerset))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class StickersRemoveStickerFromSet(TLRequest[Any]):
    ID = 0XF7760F51
    QUALNAME = "functions.stickers.removeStickerFromSet"

    def __init__(self, sticker: Any = None) -> None:
        self.sticker = sticker

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.sticker.write() if hasattr(self.sticker, 'write') else write_bytes(self.sticker))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StickersRenameStickerSet(TLRequest[Any]):
    ID = 0X124B1C00
    QUALNAME = "functions.stickers.renameStickerSet"

    def __init__(self, stickerset: Any = None, title: Any = None) -> None:
        self.stickerset = stickerset
        self.title = title

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.stickerset.write() if hasattr(self.stickerset, 'write') else write_bytes(self.stickerset))
        res += write_string(self.title)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StickersReplaceSticker(TLRequest[Any]):
    ID = 0X4696459A
    QUALNAME = "functions.stickers.replaceSticker"

    def __init__(self, sticker: Any = None, new_sticker: Any = None) -> None:
        self.sticker = sticker
        self.new_sticker = new_sticker

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.sticker.write() if hasattr(self.sticker, 'write') else write_bytes(self.sticker))
        res += (self.new_sticker.write() if hasattr(self.new_sticker, 'write') else write_bytes(self.new_sticker))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StickersSetStickerSetThumb(TLRequest[Any]):
    ID = 0XA76A5392
    QUALNAME = "functions.stickers.setStickerSetThumb"

    def __init__(self, stickerset: Any = None, thumb: Any = None, thumb_document_id: Any = None) -> None:
        self.stickerset = stickerset
        self.thumb = thumb
        self.thumb_document_id = thumb_document_id

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'thumb', None) is not None and getattr(self, 'thumb', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'thumb_document_id', None) is not None and getattr(self, 'thumb_document_id', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.stickerset.write() if hasattr(self.stickerset, 'write') else write_bytes(self.stickerset))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'thumb', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 1)):
            v = getattr(self, 'thumb_document_id', None) or 0
            if v is not None:
                res += write_long(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StickersSuggestShortName(TLRequest[Any]):
    ID = 0X4DAFC503
    QUALNAME = "functions.stickers.suggestShortName"

    def __init__(self, title: Any = None) -> None:
        self.title = title

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_string(self.title)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StoriesActivateStealthMode(TLRequest[Any]):
    ID = 0X57BBD166
    QUALNAME = "functions.stories.activateStealthMode"

    def __init__(self, past: Any = None, future: Any = None) -> None:
        self.past = past
        self.future = future

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'past', None):
            flags |= (1 << 0)
        if getattr(self, 'future', None):
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StoriesCanSendStory(TLRequest[Any]):
    ID = 0X30EB63F0
    QUALNAME = "functions.stories.canSendStory"

    def __init__(self, peer: Any = None) -> None:
        self.peer = peer

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StoriesCreateAlbum(TLRequest[Any]):
    ID = 0XA36396E5
    QUALNAME = "functions.stories.createAlbum"

    def __init__(self, peer: Any = None, title: Any = None, stories: Any = None) -> None:
        self.peer = peer
        self.title = title
        self.stories = stories

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_string(self.title)
        res += write_vector(self.stories, write_int)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StoriesDeleteAlbum(TLRequest[Any]):
    ID = 0X8D3456D0
    QUALNAME = "functions.stories.deleteAlbum"

    def __init__(self, peer: Any = None, album_id: Any = None) -> None:
        self.peer = peer
        self.album_id = album_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.album_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class StoriesDeleteStories(TLRequest[Any]):
    ID = 0XAE59DB5F
    QUALNAME = "functions.stories.deleteStories"

    def __init__(self, peer: Any = None, id: Any = None) -> None:
        self.peer = peer
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_vector(self.id, write_int)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x1CB5C415:
            return read_vector(b, read_int)
        return read_tl_object(b)

class StoriesEditStory(TLRequest[Any]):
    ID = 0X2C63A72B
    QUALNAME = "functions.stories.editStory"

    def __init__(self, peer: Any = None, id: Any = None, media: Any = None, media_areas: Any = None, caption: Any = None, entities: Any = None, privacy_rules: Any = None, music: Any = None) -> None:
        self.peer = peer
        self.id = id
        self.media = media
        self.media_areas = media_areas
        self.caption = caption
        self.entities = entities
        self.privacy_rules = privacy_rules
        self.music = music

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'media', None) is not None and getattr(self, 'media', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'media_areas', None) is not None and getattr(self, 'media_areas', None) is not False:
            flags |= (1 << 3)
        if getattr(self, 'caption', None) is not None and getattr(self, 'caption', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'entities', None) is not None and getattr(self, 'entities', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'privacy_rules', None) is not None and getattr(self, 'privacy_rules', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'music', None) is not None and getattr(self, 'music', None) is not False:
            flags |= (1 << 4)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.id)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'media', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 3)):
            v = getattr(self, 'media_areas', None) or []
            if v is not None:
                res += write_vector(v, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        if bool(flags & (1 << 1)):
            v = getattr(self, 'caption', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'entities', None) or []
            if v is not None:
                res += write_vector(v, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        if bool(flags & (1 << 2)):
            v = getattr(self, 'privacy_rules', None) or []
            if v is not None:
                res += write_vector(v, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        if bool(flags & (1 << 4)):
            v = getattr(self, 'music', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StoriesExportStoryLink(TLRequest[Any]):
    ID = 0X7B8DEF20
    QUALNAME = "functions.stories.exportStoryLink"

    def __init__(self, peer: Any = None, id: Any = None) -> None:
        self.peer = peer
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StoriesGetAlbumStories(TLRequest[Any]):
    ID = 0XAC806D61
    QUALNAME = "functions.stories.getAlbumStories"

    def __init__(self, peer: Any = None, album_id: Any = None, offset: Any = None, limit: Any = None) -> None:
        self.peer = peer
        self.album_id = album_id
        self.offset = offset
        self.limit = limit

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.album_id)
        res += write_int(self.offset)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StoriesGetAlbums(TLRequest[Any]):
    ID = 0X25B3EAC7
    QUALNAME = "functions.stories.getAlbums"

    def __init__(self, peer: Any = None, hash: Any = None) -> None:
        self.peer = peer
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StoriesGetAllReadPeerStories(TLRequest[Any]):
    ID = 0X9B5AE7F9
    QUALNAME = "functions.stories.getAllReadPeerStories"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StoriesGetAllStories(TLRequest[Any]):
    ID = 0XEEB0D625
    QUALNAME = "functions.stories.getAllStories"

    def __init__(self, next: Any = None, hidden: Any = None, state: Any = None) -> None:
        self.next = next
        self.hidden = hidden
        self.state = state

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'next', None):
            flags |= (1 << 1)
        if getattr(self, 'hidden', None):
            flags |= (1 << 2)
        if getattr(self, 'state', None) is not None and getattr(self, 'state', None) is not False:
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'state', None) or ''
            if v is not None:
                res += write_string(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StoriesGetChatsToSend(TLRequest[Any]):
    ID = 0XA56A8B60
    QUALNAME = "functions.stories.getChatsToSend"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StoriesGetPeerMaxIds(TLRequest[Any]):
    ID = 0X78499170
    QUALNAME = "functions.stories.getPeerMaxIDs"

    def __init__(self, id: Any = None) -> None:
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_vector(self.id, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StoriesGetPeerStories(TLRequest[Any]):
    ID = 0X2C4ADA50
    QUALNAME = "functions.stories.getPeerStories"

    def __init__(self, peer: Any = None) -> None:
        self.peer = peer

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StoriesGetPinnedStories(TLRequest[Any]):
    ID = 0X5821A5DC
    QUALNAME = "functions.stories.getPinnedStories"

    def __init__(self, peer: Any = None, offset_id: Any = None, limit: Any = None) -> None:
        self.peer = peer
        self.offset_id = offset_id
        self.limit = limit

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.offset_id)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StoriesGetStoriesArchive(TLRequest[Any]):
    ID = 0XB4352016
    QUALNAME = "functions.stories.getStoriesArchive"

    def __init__(self, peer: Any = None, offset_id: Any = None, limit: Any = None) -> None:
        self.peer = peer
        self.offset_id = offset_id
        self.limit = limit

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.offset_id)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StoriesGetStoriesById(TLRequest[Any]):
    ID = 0X5774CA74
    QUALNAME = "functions.stories.getStoriesByID"

    def __init__(self, peer: Any = None, id: Any = None) -> None:
        self.peer = peer
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_vector(self.id, write_int)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StoriesGetStoriesViews(TLRequest[Any]):
    ID = 0X28E16CC8
    QUALNAME = "functions.stories.getStoriesViews"

    def __init__(self, peer: Any = None, id: Any = None) -> None:
        self.peer = peer
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_vector(self.id, write_int)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StoriesGetStoryReactionsList(TLRequest[Any]):
    ID = 0XB9B2881F
    QUALNAME = "functions.stories.getStoryReactionsList"

    def __init__(self, forwards_first: Any = None, peer: Any = None, id: Any = None, reaction: Any = None, offset: Any = None, limit: Any = None) -> None:
        self.forwards_first = forwards_first
        self.peer = peer
        self.id = id
        self.reaction = reaction
        self.offset = offset
        self.limit = limit

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'forwards_first', None):
            flags |= (1 << 2)
        if getattr(self, 'reaction', None) is not None and getattr(self, 'reaction', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'offset', None) is not None and getattr(self, 'offset', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.id)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'reaction', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 1)):
            v = getattr(self, 'offset', None) or ''
            if v is not None:
                res += write_string(v)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StoriesGetStoryViewsList(TLRequest[Any]):
    ID = 0X7ED23C57
    QUALNAME = "functions.stories.getStoryViewsList"

    def __init__(self, just_contacts: Any = None, reactions_first: Any = None, forwards_first: Any = None, peer: Any = None, q: Any = None, id: Any = None, offset: Any = None, limit: Any = None) -> None:
        self.just_contacts = just_contacts
        self.reactions_first = reactions_first
        self.forwards_first = forwards_first
        self.peer = peer
        self.q = q
        self.id = id
        self.offset = offset
        self.limit = limit

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'just_contacts', None):
            flags |= (1 << 0)
        if getattr(self, 'reactions_first', None):
            flags |= (1 << 2)
        if getattr(self, 'forwards_first', None):
            flags |= (1 << 3)
        if getattr(self, 'q', None) is not None and getattr(self, 'q', None) is not False:
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        if bool(flags & (1 << 1)):
            v = getattr(self, 'q', None) or ''
            if v is not None:
                res += write_string(v)
        res += write_int(self.id)
        res += write_string(self.offset)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StoriesIncrementStoryViews(TLRequest[Any]):
    ID = 0XB2028AFB
    QUALNAME = "functions.stories.incrementStoryViews"

    def __init__(self, peer: Any = None, id: Any = None) -> None:
        self.peer = peer
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_vector(self.id, write_int)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class StoriesReadStories(TLRequest[Any]):
    ID = 0XA556DAC8
    QUALNAME = "functions.stories.readStories"

    def __init__(self, peer: Any = None, max_id: Any = None) -> None:
        self.peer = peer
        self.max_id = max_id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.max_id)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x1CB5C415:
            return read_vector(b, read_int)
        return read_tl_object(b)

class StoriesReorderAlbums(TLRequest[Any]):
    ID = 0X8535FBD9
    QUALNAME = "functions.stories.reorderAlbums"

    def __init__(self, peer: Any = None, order: Any = None) -> None:
        self.peer = peer
        self.order = order

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_vector(self.order, write_int)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class StoriesReport(TLRequest[Any]):
    ID = 0X19D8EB45
    QUALNAME = "functions.stories.report"

    def __init__(self, peer: Any = None, id: Any = None, option: Any = None, message: Any = None) -> None:
        self.peer = peer
        self.id = id
        self.option = option
        self.message = message

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_vector(self.id, write_int)
        res += write_bytes(self.option)
        res += write_string(self.message)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StoriesSearchPosts(TLRequest[Any]):
    ID = 0XD1810907
    QUALNAME = "functions.stories.searchPosts"

    def __init__(self, hashtag: Any = None, area: Any = None, peer: Any = None, offset: Any = None, limit: Any = None) -> None:
        self.hashtag = hashtag
        self.area = area
        self.peer = peer
        self.offset = offset
        self.limit = limit

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'hashtag', None) is not None and getattr(self, 'hashtag', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'area', None) is not None and getattr(self, 'area', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'peer', None) is not None and getattr(self, 'peer', None) is not False:
            flags |= (1 << 2)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'hashtag', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'area', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 2)):
            v = getattr(self, 'peer', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        res += write_string(self.offset)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StoriesSendReaction(TLRequest[Any]):
    ID = 0X7FD736B2
    QUALNAME = "functions.stories.sendReaction"

    def __init__(self, add_to_recent: Any = None, peer: Any = None, story_id: Any = None, reaction: Any = None) -> None:
        self.add_to_recent = add_to_recent
        self.peer = peer
        self.story_id = story_id
        self.reaction = reaction

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'add_to_recent', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.story_id)
        res += (self.reaction.write() if hasattr(self.reaction, 'write') else write_bytes(self.reaction))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StoriesSendStory(TLRequest[Any]):
    ID = 0X8F9E6898
    QUALNAME = "functions.stories.sendStory"

    def __init__(self, pinned: Any = None, noforwards: Any = None, fwd_modified: Any = None, peer: Any = None, media: Any = None, media_areas: Any = None, caption: Any = None, entities: Any = None, privacy_rules: Any = None, random_id: Any = None, period: Any = None, fwd_from_id: Any = None, fwd_from_story: Any = None, albums: Any = None, music: Any = None) -> None:
        self.pinned = pinned
        self.noforwards = noforwards
        self.fwd_modified = fwd_modified
        self.peer = peer
        self.media = media
        self.media_areas = media_areas
        self.caption = caption
        self.entities = entities
        self.privacy_rules = privacy_rules
        self.random_id = random_id
        self.period = period
        self.fwd_from_id = fwd_from_id
        self.fwd_from_story = fwd_from_story
        self.albums = albums
        self.music = music

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'pinned', None):
            flags |= (1 << 2)
        if getattr(self, 'noforwards', None):
            flags |= (1 << 4)
        if getattr(self, 'fwd_modified', None):
            flags |= (1 << 7)
        if getattr(self, 'media_areas', None) is not None and getattr(self, 'media_areas', None) is not False:
            flags |= (1 << 5)
        if getattr(self, 'caption', None) is not None and getattr(self, 'caption', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'entities', None) is not None and getattr(self, 'entities', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'period', None) is not None and getattr(self, 'period', None) is not False:
            flags |= (1 << 3)
        if getattr(self, 'fwd_from_id', None) is not None and getattr(self, 'fwd_from_id', None) is not False:
            flags |= (1 << 6)
        if getattr(self, 'fwd_from_story', None) is not None and getattr(self, 'fwd_from_story', None) is not False:
            flags |= (1 << 6)
        if getattr(self, 'albums', None) is not None and getattr(self, 'albums', None) is not False:
            flags |= (1 << 8)
        if getattr(self, 'music', None) is not None and getattr(self, 'music', None) is not False:
            flags |= (1 << 9)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += (self.media.write() if hasattr(self.media, 'write') else write_bytes(self.media))
        if bool(flags & (1 << 5)):
            v = getattr(self, 'media_areas', None) or []
            if v is not None:
                res += write_vector(v, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'caption', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'entities', None) or []
            if v is not None:
                res += write_vector(v, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        res += write_vector(self.privacy_rules, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        res += write_long(self.random_id)
        if bool(flags & (1 << 3)):
            v = getattr(self, 'period', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 6)):
            v = getattr(self, 'fwd_from_id', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        if bool(flags & (1 << 6)):
            v = getattr(self, 'fwd_from_story', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 8)):
            v = getattr(self, 'albums', None) or []
            if v is not None:
                res += write_vector(v, write_int)
        if bool(flags & (1 << 9)):
            v = getattr(self, 'music', None)
            if v is not None:
                res += (v.write() if hasattr(v, 'write') else write_bytes(v))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StoriesStartLive(TLRequest[Any]):
    ID = 0XD069CCDE
    QUALNAME = "functions.stories.startLive"

    def __init__(self, pinned: Any = None, noforwards: Any = None, rtmp_stream: Any = None, peer: Any = None, caption: Any = None, entities: Any = None, privacy_rules: Any = None, random_id: Any = None, messages_enabled: Any = None, send_paid_messages_stars: Any = None) -> None:
        self.pinned = pinned
        self.noforwards = noforwards
        self.rtmp_stream = rtmp_stream
        self.peer = peer
        self.caption = caption
        self.entities = entities
        self.privacy_rules = privacy_rules
        self.random_id = random_id
        self.messages_enabled = messages_enabled
        self.send_paid_messages_stars = send_paid_messages_stars

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'pinned', None):
            flags |= (1 << 2)
        if getattr(self, 'noforwards', None):
            flags |= (1 << 4)
        if getattr(self, 'rtmp_stream', None):
            flags |= (1 << 5)
        if getattr(self, 'caption', None) is not None and getattr(self, 'caption', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'entities', None) is not None and getattr(self, 'entities', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'messages_enabled', None) is not None and getattr(self, 'messages_enabled', None) is not False:
            flags |= (1 << 6)
        if getattr(self, 'send_paid_messages_stars', None) is not None and getattr(self, 'send_paid_messages_stars', None) is not False:
            flags |= (1 << 7)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        if bool(flags & (1 << 0)):
            v = getattr(self, 'caption', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'entities', None) or []
            if v is not None:
                res += write_vector(v, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        res += write_vector(self.privacy_rules, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        res += write_long(self.random_id)
        if bool(flags & (1 << 6)):
            v = getattr(self, 'messages_enabled', None)
            if v is not None:
                res += write_bool(v)
        if bool(flags & (1 << 7)):
            v = getattr(self, 'send_paid_messages_stars', None) or 0
            if v is not None:
                res += write_long(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class StoriesToggleAllStoriesHidden(TLRequest[Any]):
    ID = 0X7C2557C4
    QUALNAME = "functions.stories.toggleAllStoriesHidden"

    def __init__(self, hidden: Any = None) -> None:
        self.hidden = hidden

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_bool(self.hidden)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class StoriesTogglePeerStoriesHidden(TLRequest[Any]):
    ID = 0XBD0415C4
    QUALNAME = "functions.stories.togglePeerStoriesHidden"

    def __init__(self, peer: Any = None, hidden: Any = None) -> None:
        self.peer = peer
        self.hidden = hidden

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_bool(self.hidden)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class StoriesTogglePinned(TLRequest[Any]):
    ID = 0X9A75A1EF
    QUALNAME = "functions.stories.togglePinned"

    def __init__(self, peer: Any = None, id: Any = None, pinned: Any = None) -> None:
        self.peer = peer
        self.id = id
        self.pinned = pinned

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_vector(self.id, write_int)
        res += write_bool(self.pinned)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x1CB5C415:
            return read_vector(b, read_int)
        return read_tl_object(b)

class StoriesTogglePinnedToTop(TLRequest[Any]):
    ID = 0XB297E9B
    QUALNAME = "functions.stories.togglePinnedToTop"

    def __init__(self, peer: Any = None, id: Any = None) -> None:
        self.peer = peer
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_vector(self.id, write_int)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class StoriesUpdateAlbum(TLRequest[Any]):
    ID = 0X5E5259B6
    QUALNAME = "functions.stories.updateAlbum"

    def __init__(self, peer: Any = None, album_id: Any = None, title: Any = None, delete_stories: Any = None, add_stories: Any = None, order: Any = None) -> None:
        self.peer = peer
        self.album_id = album_id
        self.title = title
        self.delete_stories = delete_stories
        self.add_stories = add_stories
        self.order = order

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'title', None) is not None and getattr(self, 'title', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'delete_stories', None) is not None and getattr(self, 'delete_stories', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'add_stories', None) is not None and getattr(self, 'add_stories', None) is not False:
            flags |= (1 << 2)
        if getattr(self, 'order', None) is not None and getattr(self, 'order', None) is not False:
            flags |= (1 << 3)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.peer.write() if hasattr(self.peer, 'write') else write_bytes(self.peer))
        res += write_int(self.album_id)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'title', None) or ''
            if v is not None:
                res += write_string(v)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'delete_stories', None) or []
            if v is not None:
                res += write_vector(v, write_int)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'add_stories', None) or []
            if v is not None:
                res += write_vector(v, write_int)
        if bool(flags & (1 << 3)):
            v = getattr(self, 'order', None) or []
            if v is not None:
                res += write_vector(v, write_int)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class UpdatesGetChannelDifference(TLRequest[Any]):
    ID = 0X3173D78
    QUALNAME = "functions.updates.getChannelDifference"

    def __init__(self, force: Any = None, channel: Any = None, filter: Any = None, pts: Any = None, limit: Any = None) -> None:
        self.force = force
        self.channel = channel
        self.filter = filter
        self.pts = pts
        self.limit = limit

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'force', None):
            flags |= (1 << 0)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.channel.write() if hasattr(self.channel, 'write') else write_bytes(self.channel))
        res += (self.filter.write() if hasattr(self.filter, 'write') else write_bytes(self.filter))
        res += write_int(self.pts)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class UpdatesGetDifference(TLRequest[Any]):
    ID = 0X19C2F763
    QUALNAME = "functions.updates.getDifference"

    def __init__(self, pts: Any = None, pts_limit: Any = None, pts_total_limit: Any = None, date: Any = None, qts: Any = None, qts_limit: Any = None) -> None:
        self.pts = pts
        self.pts_limit = pts_limit
        self.pts_total_limit = pts_total_limit
        self.date = date
        self.qts = qts
        self.qts_limit = qts_limit

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'pts_limit', None) is not None and getattr(self, 'pts_limit', None) is not False:
            flags |= (1 << 1)
        if getattr(self, 'pts_total_limit', None) is not None and getattr(self, 'pts_total_limit', None) is not False:
            flags |= (1 << 0)
        if getattr(self, 'qts_limit', None) is not None and getattr(self, 'qts_limit', None) is not False:
            flags |= (1 << 2)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += write_int(self.pts)
        if bool(flags & (1 << 1)):
            v = getattr(self, 'pts_limit', None) or 0
            if v is not None:
                res += write_int(v)
        if bool(flags & (1 << 0)):
            v = getattr(self, 'pts_total_limit', None) or 0
            if v is not None:
                res += write_int(v)
        res += write_int(self.date)
        res += write_int(self.qts)
        if bool(flags & (1 << 2)):
            v = getattr(self, 'qts_limit', None) or 0
            if v is not None:
                res += write_int(v)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class UpdatesGetState(TLRequest[Any]):
    ID = 0XEDD4882A
    QUALNAME = "functions.updates.getState"

    def __init__(self) -> None:
        pass

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class UploadGetCdnFile(TLRequest[Any]):
    ID = 0X395F69DA
    QUALNAME = "functions.upload.getCdnFile"

    def __init__(self, file_token: Any = None, offset: Any = None, limit: Any = None) -> None:
        self.file_token = file_token
        self.offset = offset
        self.limit = limit

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_bytes(self.file_token)
        res += write_long(self.offset)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class UploadGetCdnFileHashes(TLRequest[Any]):
    ID = 0X91DC3F31
    QUALNAME = "functions.upload.getCdnFileHashes"

    def __init__(self, file_token: Any = None, offset: Any = None) -> None:
        self.file_token = file_token
        self.offset = offset

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_bytes(self.file_token)
        res += write_long(self.offset)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class UploadGetFile(TLRequest[Any]):
    ID = 0XBE5335BE
    QUALNAME = "functions.upload.getFile"

    def __init__(self, precise: Any = None, cdn_supported: Any = None, location: Any = None, offset: Any = None, limit: Any = None) -> None:
        self.precise = precise
        self.cdn_supported = cdn_supported
        self.location = location
        self.offset = offset
        self.limit = limit

    def write(self) -> bytes:
        flags = 0
        if getattr(self, 'precise', None):
            flags |= (1 << 0)
        if getattr(self, 'cdn_supported', None):
            flags |= (1 << 1)
        res = struct.pack('<I', self.ID)
        res += write_int(flags)
        res += (self.location.write() if hasattr(self.location, 'write') else write_bytes(self.location))
        res += write_long(self.offset)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class UploadGetFileHashes(TLRequest[Any]):
    ID = 0X9156982A
    QUALNAME = "functions.upload.getFileHashes"

    def __init__(self, location: Any = None, offset: Any = None) -> None:
        self.location = location
        self.offset = offset

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.location.write() if hasattr(self.location, 'write') else write_bytes(self.location))
        res += write_long(self.offset)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class UploadGetWebFile(TLRequest[Any]):
    ID = 0X24E6818D
    QUALNAME = "functions.upload.getWebFile"

    def __init__(self, location: Any = None, offset: Any = None, limit: Any = None) -> None:
        self.location = location
        self.offset = offset
        self.limit = limit

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.location.write() if hasattr(self.location, 'write') else write_bytes(self.location))
        res += write_int(self.offset)
        res += write_int(self.limit)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class UploadReuploadCdnFile(TLRequest[Any]):
    ID = 0X9B2754A8
    QUALNAME = "functions.upload.reuploadCdnFile"

    def __init__(self, file_token: Any = None, request_token: Any = None) -> None:
        self.file_token = file_token
        self.request_token = request_token

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_bytes(self.file_token)
        res += write_bytes(self.request_token)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class UploadSaveBigFilePart(TLRequest[Any]):
    ID = 0XDE7B673D
    QUALNAME = "functions.upload.saveBigFilePart"

    def __init__(self, file_id: Any = None, file_part: Any = None, file_total_parts: Any = None, bytes: Any = None, bytes_data: Any = None) -> None:
        self.file_id = file_id
        self.file_part = file_part
        self.file_total_parts = file_total_parts
        b_val = bytes if bytes is not None else bytes_data
        self.bytes = b_val
        self.bytes_data = b_val

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.file_id)
        res += write_int(self.file_part)
        res += write_int(self.file_total_parts)
        res += write_bytes(self.bytes)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class UploadSaveFilePart(TLRequest[Any]):
    ID = 0XB304A621
    QUALNAME = "functions.upload.saveFilePart"

    def __init__(self, file_id: Any = None, file_part: Any = None, bytes: Any = None, bytes_data: Any = None) -> None:
        self.file_id = file_id
        self.file_part = file_part
        b_val = bytes if bytes is not None else bytes_data
        self.bytes = b_val
        self.bytes_data = b_val

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_long(self.file_id)
        res += write_int(self.file_part)
        res += write_bytes(self.bytes)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class UsersGetFullUser(TLRequest[Any]):
    ID = 0XB60F5918
    QUALNAME = "functions.users.getFullUser"

    def __init__(self, id: Any = None) -> None:
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.id.write() if hasattr(self.id, 'write') else write_bytes(self.id))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class UsersGetRequirementsToContact(TLRequest[Any]):
    ID = 0XD89A83A3
    QUALNAME = "functions.users.getRequirementsToContact"

    def __init__(self, id: Any = None) -> None:
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_vector(self.id, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class UsersGetSavedMusic(TLRequest[Any]):
    ID = 0X788D7FE3
    QUALNAME = "functions.users.getSavedMusic"

    def __init__(self, id: Any = None, offset: Any = None, limit: Any = None, hash: Any = None) -> None:
        self.id = id
        self.offset = offset
        self.limit = limit
        self.hash = hash

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.id.write() if hasattr(self.id, 'write') else write_bytes(self.id))
        res += write_int(self.offset)
        res += write_int(self.limit)
        res += write_long(self.hash)
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class UsersGetSavedMusicById(TLRequest[Any]):
    ID = 0X7573A4E9
    QUALNAME = "functions.users.getSavedMusicByID"

    def __init__(self, id: Any = None, documents: Any = None) -> None:
        self.id = id
        self.documents = documents

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.id.write() if hasattr(self.id, 'write') else write_bytes(self.id))
        res += write_vector(self.documents, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class UsersGetUsers(TLRequest[Any]):
    ID = 0XD91A548
    QUALNAME = "functions.users.getUsers"

    def __init__(self, id: Any = None) -> None:
        self.id = id

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += write_vector(self.id, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

class UsersSetSecureValueErrors(TLRequest[Any]):
    ID = 0X90C894B5
    QUALNAME = "functions.users.setSecureValueErrors"

    def __init__(self, id: Any = None, errors: Any = None) -> None:
        self.id = id
        self.errors = errors

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.id.write() if hasattr(self.id, 'write') else write_bytes(self.id))
        res += write_vector(self.errors, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        c_id = read_uint(b)
        b.seek(b.tell() - 4)
        if c_id == 0x997275B5:
            read_uint(b)
            return True
        if c_id == 0xBC799737:
            read_uint(b)
            return False
        return read_tl_object(b)

class UsersSuggestBirthday(TLRequest[Any]):
    ID = 0XFC533372
    QUALNAME = "functions.users.suggestBirthday"

    def __init__(self, id: Any = None, birthday: Any = None) -> None:
        self.id = id
        self.birthday = birthday

    def write(self) -> bytes:
        res = struct.pack('<I', self.ID)
        res += (self.id.write() if hasattr(self.id, 'write') else write_bytes(self.id))
        res += (self.birthday.write() if hasattr(self.birthday, 'write') else write_bytes(self.birthday))
        return res

    def read_result(self, b: BinaryIO) -> Any:
        from aiogram.raw.all import read_tl_object
        return read_tl_object(b)

SendMessage = MessagesSendMessage
SendMedia = MessagesSendMedia
GetHistory = MessagesGetHistory
GetFile = UploadGetFile
SaveFilePart = UploadSaveFilePart
SaveBigFilePart = UploadSaveBigFilePart
ResolveUsername = ContactsResolveUsername
GetNearestDc = HelpGetNearestDc
SendCode = AuthSendCode
ResendCode = AuthResendCode
CancelCode = AuthCancelCode
SignIn = AuthSignIn
SignUp = AuthSignUp
CheckPassword = AuthCheckPassword
ImportBotAuthorization = AuthImportBotAuthorization
ExportAuthorization = AuthExportAuthorization
ImportAuthorization = AuthImportAuthorization
LogOut = AuthLogOut
GetPassword = AccountGetPassword
GetUsers = UsersGetUsers
GetFullUser = UsersGetFullUser
EditMessage = MessagesEditMessage
DeleteMessages = MessagesDeleteMessages
ForwardMessages = MessagesForwardMessages

class account:
    AcceptAuthorization = AccountAcceptAuthorization
    CancelPasswordEmail = AccountCancelPasswordEmail
    ChangeAuthorizationSettings = AccountChangeAuthorizationSettings
    ChangePhone = AccountChangePhone
    CheckUsername = AccountCheckUsername
    ClearRecentEmojiStatuses = AccountClearRecentEmojiStatuses
    ConfirmBotConnection = AccountConfirmBotConnection
    ConfirmPasswordEmail = AccountConfirmPasswordEmail
    ConfirmPhone = AccountConfirmPhone
    CreateBusinessChatLink = AccountCreateBusinessChatLink
    CreateTheme = AccountCreateTheme
    DeclinePasswordReset = AccountDeclinePasswordReset
    DeleteAccount = AccountDeleteAccount
    DeleteAutoSaveExceptions = AccountDeleteAutoSaveExceptions
    DeleteBusinessChatLink = AccountDeleteBusinessChatLink
    DeletePasskey = AccountDeletePasskey
    DeleteSecureValue = AccountDeleteSecureValue
    DeleteWebBrowserSettingsExceptions = AccountDeleteWebBrowserSettingsExceptions
    DisablePeerConnectedBot = AccountDisablePeerConnectedBot
    EditBusinessChatLink = AccountEditBusinessChatLink
    FinishTakeoutSession = AccountFinishTakeoutSession
    GetAccountTtl = AccountGetAccountTtl
    GetAllSecureValues = AccountGetAllSecureValues
    GetAuthorizationForm = AccountGetAuthorizationForm
    GetAuthorizations = AccountGetAuthorizations
    GetAutoDownloadSettings = AccountGetAutoDownloadSettings
    GetAutoSaveSettings = AccountGetAutoSaveSettings
    GetBotBusinessConnection = AccountGetBotBusinessConnection
    GetBusinessChatLinks = AccountGetBusinessChatLinks
    GetChannelDefaultEmojiStatuses = AccountGetChannelDefaultEmojiStatuses
    GetChannelRestrictedStatusEmojis = AccountGetChannelRestrictedStatusEmojis
    GetChatThemes = AccountGetChatThemes
    GetCollectibleEmojiStatuses = AccountGetCollectibleEmojiStatuses
    GetConnectedBots = AccountGetConnectedBots
    GetContactSignUpNotification = AccountGetContactSignUpNotification
    GetContentSettings = AccountGetContentSettings
    GetDefaultBackgroundEmojis = AccountGetDefaultBackgroundEmojis
    GetDefaultEmojiStatuses = AccountGetDefaultEmojiStatuses
    GetDefaultGroupPhotoEmojis = AccountGetDefaultGroupPhotoEmojis
    GetDefaultProfilePhotoEmojis = AccountGetDefaultProfilePhotoEmojis
    GetGlobalPrivacySettings = AccountGetGlobalPrivacySettings
    GetMultiWallPapers = AccountGetMultiWallPapers
    GetNotifyExceptions = AccountGetNotifyExceptions
    GetNotifySettings = AccountGetNotifySettings
    GetPaidMessagesRevenue = AccountGetPaidMessagesRevenue
    GetPasskeys = AccountGetPasskeys
    GetPassword = AccountGetPassword
    GetPasswordSettings = AccountGetPasswordSettings
    GetPrivacy = AccountGetPrivacy
    GetReactionsNotifySettings = AccountGetReactionsNotifySettings
    GetRecentEmojiStatuses = AccountGetRecentEmojiStatuses
    GetSavedMusicIds = AccountGetSavedMusicIds
    GetSavedRingtones = AccountGetSavedRingtones
    GetSecureValue = AccountGetSecureValue
    GetTheme = AccountGetTheme
    GetThemes = AccountGetThemes
    GetTmpPassword = AccountGetTmpPassword
    GetUniqueGiftChatThemes = AccountGetUniqueGiftChatThemes
    GetWallPaper = AccountGetWallPaper
    GetWallPapers = AccountGetWallPapers
    GetWebAuthorizations = AccountGetWebAuthorizations
    GetWebBrowserSettings = AccountGetWebBrowserSettings
    InitPasskeyRegistration = AccountInitPasskeyRegistration
    InitTakeoutSession = AccountInitTakeoutSession
    InstallTheme = AccountInstallTheme
    InstallWallPaper = AccountInstallWallPaper
    InvalidateSignInCodes = AccountInvalidateSignInCodes
    RegisterDevice = AccountRegisterDevice
    RegisterPasskey = AccountRegisterPasskey
    ReorderUsernames = AccountReorderUsernames
    ReportPeer = AccountReportPeer
    ReportProfilePhoto = AccountReportProfilePhoto
    ResendPasswordEmail = AccountResendPasswordEmail
    ResetAuthorization = AccountResetAuthorization
    ResetNotifySettings = AccountResetNotifySettings
    ResetPassword = AccountResetPassword
    ResetWallPapers = AccountResetWallPapers
    ResetWebAuthorization = AccountResetWebAuthorization
    ResetWebAuthorizations = AccountResetWebAuthorizations
    ResolveBusinessChatLink = AccountResolveBusinessChatLink
    SaveAutoDownloadSettings = AccountSaveAutoDownloadSettings
    SaveAutoSaveSettings = AccountSaveAutoSaveSettings
    SaveMusic = AccountSaveMusic
    SaveRingtone = AccountSaveRingtone
    SaveSecureValue = AccountSaveSecureValue
    SaveTheme = AccountSaveTheme
    SaveWallPaper = AccountSaveWallPaper
    SendChangePhoneCode = AccountSendChangePhoneCode
    SendConfirmPhoneCode = AccountSendConfirmPhoneCode
    SendVerifyEmailCode = AccountSendVerifyEmailCode
    SendVerifyPhoneCode = AccountSendVerifyPhoneCode
    SetAccountTtl = AccountSetAccountTtl
    SetAuthorizationTtl = AccountSetAuthorizationTtl
    SetContactSignUpNotification = AccountSetContactSignUpNotification
    SetContentSettings = AccountSetContentSettings
    SetGlobalPrivacySettings = AccountSetGlobalPrivacySettings
    SetMainProfileTab = AccountSetMainProfileTab
    SetPrivacy = AccountSetPrivacy
    SetReactionsNotifySettings = AccountSetReactionsNotifySettings
    ToggleConnectedBotPaused = AccountToggleConnectedBotPaused
    ToggleNoPaidMessagesException = AccountToggleNoPaidMessagesException
    ToggleSponsoredMessages = AccountToggleSponsoredMessages
    ToggleUsername = AccountToggleUsername
    ToggleWebBrowserSettingsException = AccountToggleWebBrowserSettingsException
    UnregisterDevice = AccountUnregisterDevice
    UpdateBirthday = AccountUpdateBirthday
    UpdateBusinessAwayMessage = AccountUpdateBusinessAwayMessage
    UpdateBusinessGreetingMessage = AccountUpdateBusinessGreetingMessage
    UpdateBusinessIntro = AccountUpdateBusinessIntro
    UpdateBusinessLocation = AccountUpdateBusinessLocation
    UpdateBusinessWorkHours = AccountUpdateBusinessWorkHours
    UpdateColor = AccountUpdateColor
    UpdateConnectedBot = AccountUpdateConnectedBot
    UpdateDeviceLocked = AccountUpdateDeviceLocked
    UpdateEmojiStatus = AccountUpdateEmojiStatus
    UpdateNotifySettings = AccountUpdateNotifySettings
    UpdatePasswordSettings = AccountUpdatePasswordSettings
    UpdatePersonalChannel = AccountUpdatePersonalChannel
    UpdateProfile = AccountUpdateProfile
    UpdateStatus = AccountUpdateStatus
    UpdateTheme = AccountUpdateTheme
    UpdateUsername = AccountUpdateUsername
    UpdateWebBrowserSettings = AccountUpdateWebBrowserSettings
    UploadRingtone = AccountUploadRingtone
    UploadTheme = AccountUploadTheme
    UploadWallPaper = AccountUploadWallPaper
    VerifyEmail = AccountVerifyEmail
    VerifyPhone = AccountVerifyPhone

class aicompose:
    CreateTone = AicomposeCreateTone
    DeleteTone = AicomposeDeleteTone
    GetTone = AicomposeGetTone
    GetToneExample = AicomposeGetToneExample
    GetTones = AicomposeGetTones
    SaveTone = AicomposeSaveTone
    UpdateTone = AicomposeUpdateTone

class auth:
    AcceptLoginToken = AuthAcceptLoginToken
    BindTempAuthKey = AuthBindTempAuthKey
    CancelCode = AuthCancelCode
    CheckPaidAuth = AuthCheckPaidAuth
    CheckPassword = AuthCheckPassword
    CheckRecoveryPassword = AuthCheckRecoveryPassword
    DropTempAuthKeys = AuthDropTempAuthKeys
    ExportAuthorization = AuthExportAuthorization
    ExportLoginToken = AuthExportLoginToken
    FinishFirebasePnvLogin = AuthFinishFirebasePnvLogin
    FinishPasskeyLogin = AuthFinishPasskeyLogin
    FirebasePnvSignUp = AuthFirebasePnvSignUp
    ImportAuthorization = AuthImportAuthorization
    ImportBotAuthorization = AuthImportBotAuthorization
    ImportLoginToken = AuthImportLoginToken
    ImportWebTokenAuthorization = AuthImportWebTokenAuthorization
    InitFirebasePnvLogin = AuthInitFirebasePnvLogin
    InitPasskeyLogin = AuthInitPasskeyLogin
    LogOut = AuthLogOut
    RecoverPassword = AuthRecoverPassword
    ReportMissingCode = AuthReportMissingCode
    RequestFirebaseSms = AuthRequestFirebaseSms
    RequestPasswordRecovery = AuthRequestPasswordRecovery
    ResendCode = AuthResendCode
    ResetAuthorizations = AuthResetAuthorizations
    ResetLoginEmail = AuthResetLoginEmail
    SendCode = AuthSendCode
    SignIn = AuthSignIn
    SignUp = AuthSignUp

class bots:
    AddPreviewMedia = BotsAddPreviewMedia
    AllowSendMessage = BotsAllowSendMessage
    AnswerWebhookJsonquery = BotsAnswerWebhookJsonquery
    CanSendMessage = BotsCanSendMessage
    CheckDownloadFileParams = BotsCheckDownloadFileParams
    CheckUsername = BotsCheckUsername
    CreateBot = BotsCreateBot
    DeletePreviewMedia = BotsDeletePreviewMedia
    EditAccessSettings = BotsEditAccessSettings
    EditPreviewMedia = BotsEditPreviewMedia
    ExportBotToken = BotsExportBotToken
    GetAccessSettings = BotsGetAccessSettings
    GetAdminedBots = BotsGetAdminedBots
    GetBotCommands = BotsGetBotCommands
    GetBotInfo = BotsGetBotInfo
    GetBotMenuButton = BotsGetBotMenuButton
    GetBotRecommendations = BotsGetBotRecommendations
    GetPopularAppBots = BotsGetPopularAppBots
    GetPreviewInfo = BotsGetPreviewInfo
    GetPreviewMedias = BotsGetPreviewMedias
    GetRequestedWebViewButton = BotsGetRequestedWebViewButton
    InvokeWebViewCustomMethod = BotsInvokeWebViewCustomMethod
    ReorderPreviewMedias = BotsReorderPreviewMedias
    ReorderUsernames = BotsReorderUsernames
    RequestWebViewButton = BotsRequestWebViewButton
    ResetBotCommands = BotsResetBotCommands
    SendCustomRequest = BotsSendCustomRequest
    SetBotBroadcastDefaultAdminRights = BotsSetBotBroadcastDefaultAdminRights
    SetBotCommands = BotsSetBotCommands
    SetBotGroupDefaultAdminRights = BotsSetBotGroupDefaultAdminRights
    SetBotInfo = BotsSetBotInfo
    SetBotMenuButton = BotsSetBotMenuButton
    SetCustomVerification = BotsSetCustomVerification
    SetJoinChatResults = BotsSetJoinChatResults
    ToggleUserEmojiStatusPermission = BotsToggleUserEmojiStatusPermission
    ToggleUsername = BotsToggleUsername
    UpdateStarRefProgram = BotsUpdateStarRefProgram
    UpdateUserEmojiStatus = BotsUpdateUserEmojiStatus

class channels:
    CheckSearchPostsFlood = ChannelsCheckSearchPostsFlood
    CheckUsername = ChannelsCheckUsername
    ConvertToGigagroup = ChannelsConvertToGigagroup
    CreateChannel = ChannelsCreateChannel
    DeactivateAllUsernames = ChannelsDeactivateAllUsernames
    DeleteChannel = ChannelsDeleteChannel
    DeleteHistory = ChannelsDeleteHistory
    DeleteMessages = ChannelsDeleteMessages
    DeleteParticipantHistory = ChannelsDeleteParticipantHistory
    EditAdmin = ChannelsEditAdmin
    EditBanned = ChannelsEditBanned
    EditLocation = ChannelsEditLocation
    EditPhoto = ChannelsEditPhoto
    EditTitle = ChannelsEditTitle
    ExportMessageLink = ChannelsExportMessageLink
    GetAdminLog = ChannelsGetAdminLog
    GetAdminedPublicChannels = ChannelsGetAdminedPublicChannels
    GetChannelRecommendations = ChannelsGetChannelRecommendations
    GetChannels = ChannelsGetChannels
    GetFullChannel = ChannelsGetFullChannel
    GetGroupsForDiscussion = ChannelsGetGroupsForDiscussion
    GetInactiveChannels = ChannelsGetInactiveChannels
    GetLeftChannels = ChannelsGetLeftChannels
    GetMessageAuthor = ChannelsGetMessageAuthor
    GetMessages = ChannelsGetMessages
    GetParticipant = ChannelsGetParticipant
    GetParticipants = ChannelsGetParticipants
    GetSendAs = ChannelsGetSendAs
    InviteToChannel = ChannelsInviteToChannel
    JoinChannel = ChannelsJoinChannel
    LeaveChannel = ChannelsLeaveChannel
    ReadHistory = ChannelsReadHistory
    ReadMessageContents = ChannelsReadMessageContents
    ReorderUsernames = ChannelsReorderUsernames
    ReportAntiSpamFalsePositive = ChannelsReportAntiSpamFalsePositive
    ReportSpam = ChannelsReportSpam
    RestrictSponsoredMessages = ChannelsRestrictSponsoredMessages
    SearchPosts = ChannelsSearchPosts
    SetBoostsToUnblockRestrictions = ChannelsSetBoostsToUnblockRestrictions
    SetDiscussionGroup = ChannelsSetDiscussionGroup
    SetEmojiStickers = ChannelsSetEmojiStickers
    SetMainProfileTab = ChannelsSetMainProfileTab
    SetStickers = ChannelsSetStickers
    ToggleAntiSpam = ChannelsToggleAntiSpam
    ToggleAutotranslation = ChannelsToggleAutotranslation
    ToggleForum = ChannelsToggleForum
    ToggleJoinRequest = ChannelsToggleJoinRequest
    ToggleJoinToSend = ChannelsToggleJoinToSend
    ToggleParticipantsHidden = ChannelsToggleParticipantsHidden
    TogglePreHistoryHidden = ChannelsTogglePreHistoryHidden
    ToggleSignatures = ChannelsToggleSignatures
    ToggleSlowMode = ChannelsToggleSlowMode
    ToggleUsername = ChannelsToggleUsername
    ToggleViewForumAsMessages = ChannelsToggleViewForumAsMessages
    UpdateColor = ChannelsUpdateColor
    UpdateEmojiStatus = ChannelsUpdateEmojiStatus
    UpdatePaidMessagesPrice = ChannelsUpdatePaidMessagesPrice
    UpdateUsername = ChannelsUpdateUsername

class chatlists:
    CheckChatlistInvite = ChatlistsCheckChatlistInvite
    DeleteExportedInvite = ChatlistsDeleteExportedInvite
    EditExportedInvite = ChatlistsEditExportedInvite
    ExportChatlistInvite = ChatlistsExportChatlistInvite
    GetChatlistUpdates = ChatlistsGetChatlistUpdates
    GetExportedInvites = ChatlistsGetExportedInvites
    GetLeaveChatlistSuggestions = ChatlistsGetLeaveChatlistSuggestions
    HideChatlistUpdates = ChatlistsHideChatlistUpdates
    JoinChatlistInvite = ChatlistsJoinChatlistInvite
    JoinChatlistUpdates = ChatlistsJoinChatlistUpdates
    LeaveChatlist = ChatlistsLeaveChatlist

class communities:
    Create = CommunitiesCreate
    GetJoinedCommunities = CommunitiesGetJoinedCommunities
    GetParticipantJoinedChats = CommunitiesGetParticipantJoinedChats
    GetPeerLinkRequests = CommunitiesGetPeerLinkRequests
    ToggleAllPeerLinkRequestApproval = CommunitiesToggleAllPeerLinkRequestApproval
    ToggleCommunityCollapsedInDialogs = CommunitiesToggleCommunityCollapsedInDialogs
    ToggleParticipantBanned = CommunitiesToggleParticipantBanned
    TogglePeerLink = CommunitiesTogglePeerLink
    TogglePeerLinkRequestApproval = CommunitiesTogglePeerLinkRequestApproval

class contacts:
    AcceptContact = ContactsAcceptContact
    AddContact = ContactsAddContact
    Block = ContactsBlock
    BlockFromReplies = ContactsBlockFromReplies
    DeleteByPhones = ContactsDeleteByPhones
    DeleteContacts = ContactsDeleteContacts
    EditCloseFriends = ContactsEditCloseFriends
    ExportContactToken = ContactsExportContactToken
    GetBirthdays = ContactsGetBirthdays
    GetBlocked = ContactsGetBlocked
    GetContactIds = ContactsGetContactIds
    GetContacts = ContactsGetContacts
    GetLocated = ContactsGetLocated
    GetSaved = ContactsGetSaved
    GetSponsoredPeers = ContactsGetSponsoredPeers
    GetStatuses = ContactsGetStatuses
    GetTopPeers = ContactsGetTopPeers
    ImportContactToken = ContactsImportContactToken
    ImportContacts = ContactsImportContacts
    ResetSaved = ContactsResetSaved
    ResetTopPeerRating = ContactsResetTopPeerRating
    ResolvePhone = ContactsResolvePhone
    ResolveUsername = ContactsResolveUsername
    Search = ContactsSearch
    SetBlocked = ContactsSetBlocked
    ToggleTopPeers = ContactsToggleTopPeers
    Unblock = ContactsUnblock
    UpdateContactNote = ContactsUpdateContactNote

class ephemeral:
    DeleteAllWelcomeMessages = EphemeralDeleteAllWelcomeMessages
    DeleteMessage = EphemeralDeleteMessage
    DeleteWelcomeMessage = EphemeralDeleteWelcomeMessage
    EditMessage = EphemeralEditMessage
    GetCallbackAnswer = EphemeralGetCallbackAnswer
    GetWelcomeMessages = EphemeralGetWelcomeMessages
    ReportMessage = EphemeralReportMessage
    SendMessage = EphemeralSendMessage

class folders:
    EditPeerFolders = FoldersEditPeerFolders

class fragment:
    GetCollectibleInfo = FragmentGetCollectibleInfo

class help:
    AcceptTermsOfService = HelpAcceptTermsOfService
    DismissSuggestion = HelpDismissSuggestion
    EditUserInfo = HelpEditUserInfo
    GetAppConfig = HelpGetAppConfig
    GetAppUpdate = HelpGetAppUpdate
    GetCdnConfig = HelpGetCdnConfig
    GetConfig = HelpGetConfig
    GetCountriesList = HelpGetCountriesList
    GetDeepLinkInfo = HelpGetDeepLinkInfo
    GetInviteText = HelpGetInviteText
    GetNearestDc = HelpGetNearestDc
    GetPassportConfig = HelpGetPassportConfig
    GetPeerColors = HelpGetPeerColors
    GetPeerProfileColors = HelpGetPeerProfileColors
    GetPremiumPromo = HelpGetPremiumPromo
    GetPromoData = HelpGetPromoData
    GetRecentMeUrls = HelpGetRecentMeUrls
    GetSupport = HelpGetSupport
    GetSupportName = HelpGetSupportName
    GetTermsOfServiceUpdate = HelpGetTermsOfServiceUpdate
    GetTimezonesList = HelpGetTimezonesList
    GetUserInfo = HelpGetUserInfo
    HidePromoData = HelpHidePromoData
    SaveAppLog = HelpSaveAppLog
    SetBotUpdatesStatus = HelpSetBotUpdatesStatus

class langpack:
    GetDifference = LangpackGetDifference
    GetLangPack = LangpackGetLangPack
    GetLanguage = LangpackGetLanguage
    GetLanguages = LangpackGetLanguages
    GetStrings = LangpackGetStrings

class messages:
    AcceptEncryption = MessagesAcceptEncryption
    AcceptUrlAuth = MessagesAcceptUrlAuth
    AddChatUser = MessagesAddChatUser
    AddPollAnswer = MessagesAddPollAnswer
    AppendTodoList = MessagesAppendTodoList
    CheckChatInvite = MessagesCheckChatInvite
    CheckHistoryImport = MessagesCheckHistoryImport
    CheckHistoryImportPeer = MessagesCheckHistoryImportPeer
    CheckQuickReplyShortcut = MessagesCheckQuickReplyShortcut
    CheckUrlAuthMatchCode = MessagesCheckUrlAuthMatchCode
    ClearAllDrafts = MessagesClearAllDrafts
    ClearRecentReactions = MessagesClearRecentReactions
    ClearRecentStickers = MessagesClearRecentStickers
    ClickSponsoredMessage = MessagesClickSponsoredMessage
    ComposeMessageWithAi = MessagesComposeMessageWithAi
    ComposeRichMessageWithAi = MessagesComposeRichMessageWithAi
    CreateChat = MessagesCreateChat
    CreateForumTopic = MessagesCreateForumTopic
    DeclineUrlAuth = MessagesDeclineUrlAuth
    DeleteChat = MessagesDeleteChat
    DeleteChatUser = MessagesDeleteChatUser
    DeleteExportedChatInvite = MessagesDeleteExportedChatInvite
    DeleteFactCheck = MessagesDeleteFactCheck
    DeleteHistory = MessagesDeleteHistory
    DeleteMessages = MessagesDeleteMessages
    DeleteParticipantReaction = MessagesDeleteParticipantReaction
    DeleteParticipantReactions = MessagesDeleteParticipantReactions
    DeletePhoneCallHistory = MessagesDeletePhoneCallHistory
    DeletePollAnswer = MessagesDeletePollAnswer
    DeleteQuickReplyMessages = MessagesDeleteQuickReplyMessages
    DeleteQuickReplyShortcut = MessagesDeleteQuickReplyShortcut
    DeleteRevokedExportedChatInvites = MessagesDeleteRevokedExportedChatInvites
    DeleteSavedHistory = MessagesDeleteSavedHistory
    DeleteScheduledMessages = MessagesDeleteScheduledMessages
    DeleteTopicHistory = MessagesDeleteTopicHistory
    DiscardEncryption = MessagesDiscardEncryption
    EditChatAbout = MessagesEditChatAbout
    EditChatAdmin = MessagesEditChatAdmin
    EditChatCreator = MessagesEditChatCreator
    EditChatDefaultBannedRights = MessagesEditChatDefaultBannedRights
    EditChatParticipantRank = MessagesEditChatParticipantRank
    EditChatPhoto = MessagesEditChatPhoto
    EditChatTitle = MessagesEditChatTitle
    EditExportedChatInvite = MessagesEditExportedChatInvite
    EditFactCheck = MessagesEditFactCheck
    EditForumTopic = MessagesEditForumTopic
    EditInlineBotMessage = MessagesEditInlineBotMessage
    EditMessage = MessagesEditMessage
    EditQuickReplyShortcut = MessagesEditQuickReplyShortcut
    ExportChatInvite = MessagesExportChatInvite
    FaveSticker = MessagesFaveSticker
    ForwardMessages = MessagesForwardMessages
    GetAdminsWithInvites = MessagesGetAdminsWithInvites
    GetAllDrafts = MessagesGetAllDrafts
    GetAllStickers = MessagesGetAllStickers
    GetArchivedStickers = MessagesGetArchivedStickers
    GetAttachMenuBot = MessagesGetAttachMenuBot
    GetAttachMenuBots = MessagesGetAttachMenuBots
    GetAttachedStickers = MessagesGetAttachedStickers
    GetAvailableEffects = MessagesGetAvailableEffects
    GetAvailableReactions = MessagesGetAvailableReactions
    GetBotApp = MessagesGetBotApp
    GetBotCallbackAnswer = MessagesGetBotCallbackAnswer
    GetChatInviteImporters = MessagesGetChatInviteImporters
    GetChats = MessagesGetChats
    GetCommonChats = MessagesGetCommonChats
    GetCustomEmojiDocuments = MessagesGetCustomEmojiDocuments
    GetDefaultHistoryTtl = MessagesGetDefaultHistoryTtl
    GetDefaultTagReactions = MessagesGetDefaultTagReactions
    GetDhConfig = MessagesGetDhConfig
    GetDialogFilters = MessagesGetDialogFilters
    GetDialogUnreadMarks = MessagesGetDialogUnreadMarks
    GetDialogs = MessagesGetDialogs
    GetDiscussionMessage = MessagesGetDiscussionMessage
    GetDocumentByHash = MessagesGetDocumentByHash
    GetEmojiGameInfo = MessagesGetEmojiGameInfo
    GetEmojiGroups = MessagesGetEmojiGroups
    GetEmojiKeywords = MessagesGetEmojiKeywords
    GetEmojiKeywordsDifference = MessagesGetEmojiKeywordsDifference
    GetEmojiKeywordsLanguages = MessagesGetEmojiKeywordsLanguages
    GetEmojiProfilePhotoGroups = MessagesGetEmojiProfilePhotoGroups
    GetEmojiStatusGroups = MessagesGetEmojiStatusGroups
    GetEmojiStickerGroups = MessagesGetEmojiStickerGroups
    GetEmojiStickers = MessagesGetEmojiStickers
    GetEmojiUrl = MessagesGetEmojiUrl
    GetExportedChatInvite = MessagesGetExportedChatInvite
    GetExportedChatInvites = MessagesGetExportedChatInvites
    GetExtendedMedia = MessagesGetExtendedMedia
    GetFactCheck = MessagesGetFactCheck
    GetFavedStickers = MessagesGetFavedStickers
    GetFeaturedEmojiStickers = MessagesGetFeaturedEmojiStickers
    GetFeaturedStickers = MessagesGetFeaturedStickers
    GetForumTopics = MessagesGetForumTopics
    GetForumTopicsById = MessagesGetForumTopicsById
    GetFullChat = MessagesGetFullChat
    GetFutureChatCreatorAfterLeave = MessagesGetFutureChatCreatorAfterLeave
    GetGameHighScores = MessagesGetGameHighScores
    GetHistory = MessagesGetHistory
    GetInlineBotResults = MessagesGetInlineBotResults
    GetInlineGameHighScores = MessagesGetInlineGameHighScores
    GetMaskStickers = MessagesGetMaskStickers
    GetMessageEditData = MessagesGetMessageEditData
    GetMessageReactionsList = MessagesGetMessageReactionsList
    GetMessageReadParticipants = MessagesGetMessageReadParticipants
    GetMessages = MessagesGetMessages
    GetMessagesReactions = MessagesGetMessagesReactions
    GetMessagesViews = MessagesGetMessagesViews
    GetMyStickers = MessagesGetMyStickers
    GetOldFeaturedStickers = MessagesGetOldFeaturedStickers
    GetOnlines = MessagesGetOnlines
    GetOutboxReadDate = MessagesGetOutboxReadDate
    GetPaidReactionPrivacy = MessagesGetPaidReactionPrivacy
    GetPeerDialogs = MessagesGetPeerDialogs
    GetPeerSettings = MessagesGetPeerSettings
    GetPersonalChannelHistory = MessagesGetPersonalChannelHistory
    GetPinnedDialogs = MessagesGetPinnedDialogs
    GetPinnedSavedDialogs = MessagesGetPinnedSavedDialogs
    GetPollResults = MessagesGetPollResults
    GetPollVotes = MessagesGetPollVotes
    GetPreparedInlineMessage = MessagesGetPreparedInlineMessage
    GetQuickReplies = MessagesGetQuickReplies
    GetQuickReplyMessages = MessagesGetQuickReplyMessages
    GetRecentLocations = MessagesGetRecentLocations
    GetRecentReactions = MessagesGetRecentReactions
    GetRecentStickers = MessagesGetRecentStickers
    GetReplies = MessagesGetReplies
    GetRichMessage = MessagesGetRichMessage
    GetSavedDialogs = MessagesGetSavedDialogs
    GetSavedDialogsById = MessagesGetSavedDialogsById
    GetSavedGifs = MessagesGetSavedGifs
    GetSavedHistory = MessagesGetSavedHistory
    GetSavedReactionTags = MessagesGetSavedReactionTags
    GetScheduledHistory = MessagesGetScheduledHistory
    GetScheduledMessages = MessagesGetScheduledMessages
    GetSearchCounters = MessagesGetSearchCounters
    GetSearchResultsCalendar = MessagesGetSearchResultsCalendar
    GetSearchResultsPositions = MessagesGetSearchResultsPositions
    GetSplitRanges = MessagesGetSplitRanges
    GetSponsoredMessages = MessagesGetSponsoredMessages
    GetStickerSet = MessagesGetStickerSet
    GetStickers = MessagesGetStickers
    GetSuggestedDialogFilters = MessagesGetSuggestedDialogFilters
    GetTopReactions = MessagesGetTopReactions
    GetUnreadMentions = MessagesGetUnreadMentions
    GetUnreadPollVotes = MessagesGetUnreadPollVotes
    GetUnreadReactions = MessagesGetUnreadReactions
    GetWebPage = MessagesGetWebPage
    GetWebPagePreview = MessagesGetWebPagePreview
    HideAllChatJoinRequests = MessagesHideAllChatJoinRequests
    HideChatJoinRequest = MessagesHideChatJoinRequest
    HidePeerSettingsBar = MessagesHidePeerSettingsBar
    ImportChatInvite = MessagesImportChatInvite
    InitHistoryImport = MessagesInitHistoryImport
    InstallStickerSet = MessagesInstallStickerSet
    MarkDialogUnread = MessagesMarkDialogUnread
    MigrateChat = MessagesMigrateChat
    ProlongWebView = MessagesProlongWebView
    RateTranscribedAudio = MessagesRateTranscribedAudio
    ReadDiscussion = MessagesReadDiscussion
    ReadEncryptedHistory = MessagesReadEncryptedHistory
    ReadFeaturedStickers = MessagesReadFeaturedStickers
    ReadHistory = MessagesReadHistory
    ReadMentions = MessagesReadMentions
    ReadMessageContents = MessagesReadMessageContents
    ReadPollVotes = MessagesReadPollVotes
    ReadReactions = MessagesReadReactions
    ReadSavedHistory = MessagesReadSavedHistory
    ReceivedMessages = MessagesReceivedMessages
    ReceivedQueue = MessagesReceivedQueue
    ReorderPinnedDialogs = MessagesReorderPinnedDialogs
    ReorderPinnedForumTopics = MessagesReorderPinnedForumTopics
    ReorderPinnedSavedDialogs = MessagesReorderPinnedSavedDialogs
    ReorderQuickReplies = MessagesReorderQuickReplies
    ReorderStickerSets = MessagesReorderStickerSets
    Report = MessagesReport
    ReportEncryptedSpam = MessagesReportEncryptedSpam
    ReportMessagesDelivery = MessagesReportMessagesDelivery
    ReportMusicListen = MessagesReportMusicListen
    ReportReaction = MessagesReportReaction
    ReportReadMetrics = MessagesReportReadMetrics
    ReportSpam = MessagesReportSpam
    ReportSponsoredMessage = MessagesReportSponsoredMessage
    RequestAppWebView = MessagesRequestAppWebView
    RequestChatJoinWebView = MessagesRequestChatJoinWebView
    RequestEncryption = MessagesRequestEncryption
    RequestMainWebView = MessagesRequestMainWebView
    RequestSimpleWebView = MessagesRequestSimpleWebView
    RequestUrlAuth = MessagesRequestUrlAuth
    RequestWebView = MessagesRequestWebView
    SaveDefaultSendAs = MessagesSaveDefaultSendAs
    SaveDraft = MessagesSaveDraft
    SaveGif = MessagesSaveGif
    SavePreparedInlineMessage = MessagesSavePreparedInlineMessage
    SaveRecentSticker = MessagesSaveRecentSticker
    Search = MessagesSearch
    SearchCustomEmoji = MessagesSearchCustomEmoji
    SearchEmojiStickerSets = MessagesSearchEmojiStickerSets
    SearchGlobal = MessagesSearchGlobal
    SearchSentMedia = MessagesSearchSentMedia
    SearchStickerSets = MessagesSearchStickerSets
    SearchStickers = MessagesSearchStickers
    SendBotRequestedPeer = MessagesSendBotRequestedPeer
    SendEncrypted = MessagesSendEncrypted
    SendEncryptedFile = MessagesSendEncryptedFile
    SendEncryptedService = MessagesSendEncryptedService
    SendInlineBotResult = MessagesSendInlineBotResult
    SendMedia = MessagesSendMedia
    SendMessage = MessagesSendMessage
    SendMultiMedia = MessagesSendMultiMedia
    SendPaidReaction = MessagesSendPaidReaction
    SendQuickReplyMessages = MessagesSendQuickReplyMessages
    SendReaction = MessagesSendReaction
    SendScheduledMessages = MessagesSendScheduledMessages
    SendScreenshotNotification = MessagesSendScreenshotNotification
    SendVote = MessagesSendVote
    SendWebViewData = MessagesSendWebViewData
    SendWebViewResultMessage = MessagesSendWebViewResultMessage
    SetBotCallbackAnswer = MessagesSetBotCallbackAnswer
    SetBotGuestChatResult = MessagesSetBotGuestChatResult
    SetBotPrecheckoutResults = MessagesSetBotPrecheckoutResults
    SetBotShippingResults = MessagesSetBotShippingResults
    SetChatAvailableReactions = MessagesSetChatAvailableReactions
    SetChatTheme = MessagesSetChatTheme
    SetChatWallPaper = MessagesSetChatWallPaper
    SetDefaultHistoryTtl = MessagesSetDefaultHistoryTtl
    SetDefaultReaction = MessagesSetDefaultReaction
    SetEncryptedTyping = MessagesSetEncryptedTyping
    SetGameScore = MessagesSetGameScore
    SetHistoryTtl = MessagesSetHistoryTtl
    SetInlineBotResults = MessagesSetInlineBotResults
    SetInlineGameScore = MessagesSetInlineGameScore
    SetTyping = MessagesSetTyping
    StartBot = MessagesStartBot
    StartHistoryImport = MessagesStartHistoryImport
    SummarizeText = MessagesSummarizeText
    ToggleBotInAttachMenu = MessagesToggleBotInAttachMenu
    ToggleDialogFilterTags = MessagesToggleDialogFilterTags
    ToggleDialogPin = MessagesToggleDialogPin
    ToggleNoForwards = MessagesToggleNoForwards
    TogglePaidReactionPrivacy = MessagesTogglePaidReactionPrivacy
    TogglePeerTranslations = MessagesTogglePeerTranslations
    ToggleSavedDialogPin = MessagesToggleSavedDialogPin
    ToggleStickerSets = MessagesToggleStickerSets
    ToggleSuggestedPostApproval = MessagesToggleSuggestedPostApproval
    ToggleTodoCompleted = MessagesToggleTodoCompleted
    TranscribeAudio = MessagesTranscribeAudio
    TranslateRichMessage = MessagesTranslateRichMessage
    TranslateText = MessagesTranslateText
    UninstallStickerSet = MessagesUninstallStickerSet
    UnpinAllMessages = MessagesUnpinAllMessages
    UpdateDialogFilter = MessagesUpdateDialogFilter
    UpdateDialogFiltersOrder = MessagesUpdateDialogFiltersOrder
    UpdatePinnedForumTopic = MessagesUpdatePinnedForumTopic
    UpdatePinnedMessage = MessagesUpdatePinnedMessage
    UpdateSavedReactionTag = MessagesUpdateSavedReactionTag
    UploadEncryptedFile = MessagesUploadEncryptedFile
    UploadImportedMedia = MessagesUploadImportedMedia
    UploadMedia = MessagesUploadMedia
    ViewSponsoredMessage = MessagesViewSponsoredMessage

class payments:
    ApplyGiftCode = PaymentsApplyGiftCode
    AssignAppStoreTransaction = PaymentsAssignAppStoreTransaction
    AssignPlayMarketTransaction = PaymentsAssignPlayMarketTransaction
    BotCancelStarsSubscription = PaymentsBotCancelStarsSubscription
    CanPurchaseStore = PaymentsCanPurchaseStore
    ChangeStarsSubscription = PaymentsChangeStarsSubscription
    CheckCanSendGift = PaymentsCheckCanSendGift
    CheckGiftCode = PaymentsCheckGiftCode
    ClearSavedInfo = PaymentsClearSavedInfo
    ConnectStarRefBot = PaymentsConnectStarRefBot
    ConvertStarGift = PaymentsConvertStarGift
    CraftStarGift = PaymentsCraftStarGift
    CreateStarGiftCollection = PaymentsCreateStarGiftCollection
    DeleteStarGiftCollection = PaymentsDeleteStarGiftCollection
    EditConnectedStarRefBot = PaymentsEditConnectedStarRefBot
    ExportInvoice = PaymentsExportInvoice
    FulfillStarsSubscription = PaymentsFulfillStarsSubscription
    GetBankCardData = PaymentsGetBankCardData
    GetConnectedStarRefBot = PaymentsGetConnectedStarRefBot
    GetConnectedStarRefBots = PaymentsGetConnectedStarRefBots
    GetCraftStarGifts = PaymentsGetCraftStarGifts
    GetGiveawayInfo = PaymentsGetGiveawayInfo
    GetPaymentForm = PaymentsGetPaymentForm
    GetPaymentReceipt = PaymentsGetPaymentReceipt
    GetPremiumGiftCodeOptions = PaymentsGetPremiumGiftCodeOptions
    GetResaleStarGifts = PaymentsGetResaleStarGifts
    GetSavedInfo = PaymentsGetSavedInfo
    GetSavedStarGift = PaymentsGetSavedStarGift
    GetSavedStarGifts = PaymentsGetSavedStarGifts
    GetStarGiftActiveAuctions = PaymentsGetStarGiftActiveAuctions
    GetStarGiftAuctionAcquiredGifts = PaymentsGetStarGiftAuctionAcquiredGifts
    GetStarGiftAuctionState = PaymentsGetStarGiftAuctionState
    GetStarGiftCollections = PaymentsGetStarGiftCollections
    GetStarGiftUpgradeAttributes = PaymentsGetStarGiftUpgradeAttributes
    GetStarGiftUpgradePreview = PaymentsGetStarGiftUpgradePreview
    GetStarGiftWithdrawalUrl = PaymentsGetStarGiftWithdrawalUrl
    GetStarGifts = PaymentsGetStarGifts
    GetStarsGiftOptions = PaymentsGetStarsGiftOptions
    GetStarsGiveawayOptions = PaymentsGetStarsGiveawayOptions
    GetStarsRevenueAdsAccountUrl = PaymentsGetStarsRevenueAdsAccountUrl
    GetStarsRevenueStats = PaymentsGetStarsRevenueStats
    GetStarsRevenueWithdrawalUrl = PaymentsGetStarsRevenueWithdrawalUrl
    GetStarsStatus = PaymentsGetStarsStatus
    GetStarsSubscriptions = PaymentsGetStarsSubscriptions
    GetStarsTopupOptions = PaymentsGetStarsTopupOptions
    GetStarsTransactions = PaymentsGetStarsTransactions
    GetStarsTransactionsById = PaymentsGetStarsTransactionsById
    GetSuggestedStarRefBots = PaymentsGetSuggestedStarRefBots
    GetUniqueStarGift = PaymentsGetUniqueStarGift
    GetUniqueStarGiftValueInfo = PaymentsGetUniqueStarGiftValueInfo
    LaunchPrepaidGiveaway = PaymentsLaunchPrepaidGiveaway
    RefundStarsCharge = PaymentsRefundStarsCharge
    ReorderStarGiftCollections = PaymentsReorderStarGiftCollections
    ResolveStarGiftOffer = PaymentsResolveStarGiftOffer
    SaveStarGift = PaymentsSaveStarGift
    SendPaymentForm = PaymentsSendPaymentForm
    SendStarGiftOffer = PaymentsSendStarGiftOffer
    SendStarsForm = PaymentsSendStarsForm
    ToggleChatStarGiftNotifications = PaymentsToggleChatStarGiftNotifications
    ToggleStarGiftsPinnedToTop = PaymentsToggleStarGiftsPinnedToTop
    TransferStarGift = PaymentsTransferStarGift
    UpdateStarGiftCollection = PaymentsUpdateStarGiftCollection
    UpdateStarGiftPrice = PaymentsUpdateStarGiftPrice
    UpgradeStarGift = PaymentsUpgradeStarGift
    ValidateRequestedInfo = PaymentsValidateRequestedInfo

class phone:
    AcceptCall = PhoneAcceptCall
    CheckGroupCall = PhoneCheckGroupCall
    ConfirmCall = PhoneConfirmCall
    CreateConferenceCall = PhoneCreateConferenceCall
    CreateGroupCall = PhoneCreateGroupCall
    DeclineConferenceCallInvite = PhoneDeclineConferenceCallInvite
    DeleteConferenceCallParticipants = PhoneDeleteConferenceCallParticipants
    DeleteGroupCallMessages = PhoneDeleteGroupCallMessages
    DeleteGroupCallParticipantMessages = PhoneDeleteGroupCallParticipantMessages
    DiscardCall = PhoneDiscardCall
    DiscardGroupCall = PhoneDiscardGroupCall
    EditGroupCallParticipant = PhoneEditGroupCallParticipant
    EditGroupCallTitle = PhoneEditGroupCallTitle
    ExportGroupCallInvite = PhoneExportGroupCallInvite
    GetCallConfig = PhoneGetCallConfig
    GetGroupCall = PhoneGetGroupCall
    GetGroupCallChainBlocks = PhoneGetGroupCallChainBlocks
    GetGroupCallJoinAs = PhoneGetGroupCallJoinAs
    GetGroupCallStars = PhoneGetGroupCallStars
    GetGroupCallStreamChannels = PhoneGetGroupCallStreamChannels
    GetGroupCallStreamRtmpUrl = PhoneGetGroupCallStreamRtmpUrl
    GetGroupParticipants = PhoneGetGroupParticipants
    InviteConferenceCallParticipant = PhoneInviteConferenceCallParticipant
    InviteToGroupCall = PhoneInviteToGroupCall
    JoinGroupCall = PhoneJoinGroupCall
    JoinGroupCallPresentation = PhoneJoinGroupCallPresentation
    LeaveGroupCall = PhoneLeaveGroupCall
    LeaveGroupCallPresentation = PhoneLeaveGroupCallPresentation
    ReceivedCall = PhoneReceivedCall
    RequestCall = PhoneRequestCall
    SaveCallDebug = PhoneSaveCallDebug
    SaveCallLog = PhoneSaveCallLog
    SaveDefaultGroupCallJoinAs = PhoneSaveDefaultGroupCallJoinAs
    SaveDefaultSendAs = PhoneSaveDefaultSendAs
    SendConferenceCallBroadcast = PhoneSendConferenceCallBroadcast
    SendGroupCallEncryptedMessage = PhoneSendGroupCallEncryptedMessage
    SendGroupCallMessage = PhoneSendGroupCallMessage
    SendSignalingData = PhoneSendSignalingData
    SetCallRating = PhoneSetCallRating
    StartScheduledGroupCall = PhoneStartScheduledGroupCall
    ToggleGroupCallRecord = PhoneToggleGroupCallRecord
    ToggleGroupCallSettings = PhoneToggleGroupCallSettings
    ToggleGroupCallStartSubscription = PhoneToggleGroupCallStartSubscription

class photos:
    DeletePhotos = PhotosDeletePhotos
    GetUserPhotos = PhotosGetUserPhotos
    UpdateProfilePhoto = PhotosUpdateProfilePhoto
    UploadContactProfilePhoto = PhotosUploadContactProfilePhoto
    UploadProfilePhoto = PhotosUploadProfilePhoto

class premium:
    ApplyBoost = PremiumApplyBoost
    GetBoostsList = PremiumGetBoostsList
    GetBoostsStatus = PremiumGetBoostsStatus
    GetMyBoosts = PremiumGetMyBoosts
    GetUserBoosts = PremiumGetUserBoosts

class smsjobs:
    FinishJob = SmsjobsFinishJob
    GetSmsJob = SmsjobsGetSmsJob
    GetStatus = SmsjobsGetStatus
    IsEligibleToJoin = SmsjobsIsEligibleToJoin
    Join = SmsjobsJoin
    Leave = SmsjobsLeave
    UpdateSettings = SmsjobsUpdateSettings

class stats:
    GetBroadcastStats = StatsGetBroadcastStats
    GetMegagroupStats = StatsGetMegagroupStats
    GetMessagePublicForwards = StatsGetMessagePublicForwards
    GetMessageStats = StatsGetMessageStats
    GetPollStats = StatsGetPollStats
    GetStoryPublicForwards = StatsGetStoryPublicForwards
    GetStoryStats = StatsGetStoryStats
    LoadAsyncGraph = StatsLoadAsyncGraph

class stickers:
    AddStickerToSet = StickersAddStickerToSet
    ChangeSticker = StickersChangeSticker
    ChangeStickerPosition = StickersChangeStickerPosition
    CheckShortName = StickersCheckShortName
    CreateStickerSet = StickersCreateStickerSet
    DeleteStickerSet = StickersDeleteStickerSet
    RemoveStickerFromSet = StickersRemoveStickerFromSet
    RenameStickerSet = StickersRenameStickerSet
    ReplaceSticker = StickersReplaceSticker
    SetStickerSetThumb = StickersSetStickerSetThumb
    SuggestShortName = StickersSuggestShortName

class stories:
    ActivateStealthMode = StoriesActivateStealthMode
    CanSendStory = StoriesCanSendStory
    CreateAlbum = StoriesCreateAlbum
    DeleteAlbum = StoriesDeleteAlbum
    DeleteStories = StoriesDeleteStories
    EditStory = StoriesEditStory
    ExportStoryLink = StoriesExportStoryLink
    GetAlbumStories = StoriesGetAlbumStories
    GetAlbums = StoriesGetAlbums
    GetAllReadPeerStories = StoriesGetAllReadPeerStories
    GetAllStories = StoriesGetAllStories
    GetChatsToSend = StoriesGetChatsToSend
    GetPeerMaxIds = StoriesGetPeerMaxIds
    GetPeerStories = StoriesGetPeerStories
    GetPinnedStories = StoriesGetPinnedStories
    GetStoriesArchive = StoriesGetStoriesArchive
    GetStoriesById = StoriesGetStoriesById
    GetStoriesViews = StoriesGetStoriesViews
    GetStoryReactionsList = StoriesGetStoryReactionsList
    GetStoryViewsList = StoriesGetStoryViewsList
    IncrementStoryViews = StoriesIncrementStoryViews
    ReadStories = StoriesReadStories
    ReorderAlbums = StoriesReorderAlbums
    Report = StoriesReport
    SearchPosts = StoriesSearchPosts
    SendReaction = StoriesSendReaction
    SendStory = StoriesSendStory
    StartLive = StoriesStartLive
    ToggleAllStoriesHidden = StoriesToggleAllStoriesHidden
    TogglePeerStoriesHidden = StoriesTogglePeerStoriesHidden
    TogglePinned = StoriesTogglePinned
    TogglePinnedToTop = StoriesTogglePinnedToTop
    UpdateAlbum = StoriesUpdateAlbum

class updates:
    GetChannelDifference = UpdatesGetChannelDifference
    GetDifference = UpdatesGetDifference
    GetState = UpdatesGetState

class upload:
    GetCdnFile = UploadGetCdnFile
    GetCdnFileHashes = UploadGetCdnFileHashes
    GetFile = UploadGetFile
    GetFileHashes = UploadGetFileHashes
    GetWebFile = UploadGetWebFile
    ReuploadCdnFile = UploadReuploadCdnFile
    SaveBigFilePart = UploadSaveBigFilePart
    SaveFilePart = UploadSaveFilePart

class users:
    GetFullUser = UsersGetFullUser
    GetRequirementsToContact = UsersGetRequirementsToContact
    GetSavedMusic = UsersGetSavedMusic
    GetSavedMusicById = UsersGetSavedMusicById
    GetUsers = UsersGetUsers
    SetSecureValueErrors = UsersSetSecureValueErrors
    SuggestBirthday = UsersSuggestBirthday
