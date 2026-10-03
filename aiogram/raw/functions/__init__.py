"""
Official Telegram TL RPC Functions for MTProto.
"""

from __future__ import annotations

import random
import struct
from typing import Any, BinaryIO, Optional

from aiogram.raw.core.primitives import (
    TLObject,
    TLRequest,
    read_bytes,
    read_int,
    read_long,
    read_string,
    read_uint,
    read_vector,
    write_bool,
    write_bytes,
    write_int,
    write_long,
    write_string,
    write_uint,
    write_vector,
)
from aiogram.raw.types import (
    AccountPassword,
    Authorization,
    CodeSettings,
    ContactsResolvedPeer,
    InputCheckPasswordSRP,
    InputPeer,
    Message,
    NearestDc,
    SentCode,
    Updates,
    User,
)


class help:
    class GetNearestDc(TLRequest[NearestDc]):
        ID = 0x1FB3354B
        QUALNAME = "functions.help.GetNearestDc"

        def write(self) -> bytes:
            return struct.pack("<I", self.ID)

        def read_result(self, b: BinaryIO) -> NearestDc:
            read_uint(b)  # c_id
            return NearestDc.read(b)


class auth:
    class SendCode(TLRequest[SentCode]):
        ID = 0xA677244F
        QUALNAME = "functions.auth.SendCode"

        def __init__(
            self,
            phone_number: str,
            api_id: int,
            api_hash: str,
            settings: CodeSettings | None = None,
        ) -> None:
            self.phone_number = phone_number
            self.api_id = api_id
            self.api_hash = api_hash
            self.settings = settings or CodeSettings()

        def write(self) -> bytes:
            return (
                struct.pack("<I", self.ID)
                + write_string(self.phone_number)
                + write_int(self.api_id)
                + write_string(self.api_hash)
                + self.settings.write()
            )

        def read_result(self, b: BinaryIO) -> SentCode:
            read_uint(b)
            return SentCode.read(b)

    class ResendCode(TLRequest[SentCode]):
        ID = 0x3EF1A81C
        QUALNAME = "functions.auth.ResendCode"

        def __init__(
            self,
            phone_number: str,
            phone_code_hash: str,
            reason: str | None = None,
        ) -> None:
            self.phone_number = phone_number
            self.phone_code_hash = phone_code_hash
            self.reason = reason

        def write(self) -> bytes:
            flags = 0
            if self.reason:
                flags |= 1 << 0
            res = (
                struct.pack("<II", self.ID, flags)
                + write_string(self.phone_number)
                + write_string(self.phone_code_hash)
            )
            if self.reason:
                res += write_string(self.reason)
            return res

        def read_result(self, b: BinaryIO) -> SentCode:
            read_uint(b)
            return SentCode.read(b)

    class CancelCode(TLRequest[bool]):
        ID = 0x1F04045B
        QUALNAME = "functions.auth.CancelCode"

        def __init__(self, phone_number: str, phone_code_hash: str) -> None:
            self.phone_number = phone_number
            self.phone_code_hash = phone_code_hash

        def write(self) -> bytes:
            return (
                struct.pack("<I", self.ID)
                + write_string(self.phone_number)
                + write_string(self.phone_code_hash)
            )

        def read_result(self, b: BinaryIO) -> bool:
            return True

    class SignIn(TLRequest[Authorization]):
        ID = 0xBCD51581
        QUALNAME = "functions.auth.SignIn"

        def __init__(
            self,
            phone_number: str,
            phone_code_hash: str,
            phone_code: str | None = None,
            email_verification: TLObject | None = None,
        ) -> None:
            self.phone_number = phone_number
            self.phone_code_hash = phone_code_hash
            self.phone_code = phone_code
            self.email_verification = email_verification

        def write(self) -> bytes:
            if self.email_verification is not None:
                flags = 1 << 1
                if self.phone_code is not None:
                    flags |= 1 << 0
                res = (
                    struct.pack("<II", 0x8D52A951, flags)
                    + write_string(self.phone_number)
                    + write_string(self.phone_code_hash)
                )
                if self.phone_code is not None:
                    res += write_string(self.phone_code)
                res += self.email_verification.write()
                return res

            return (
                struct.pack("<I", 0xBCD51581)
                + write_string(self.phone_number)
                + write_string(self.phone_code_hash)
                + write_string(self.phone_code or "")
            )

        def read_result(self, b: BinaryIO) -> Authorization:
            read_uint(b)
            return Authorization.read(b)

    class SignUp(TLRequest[Authorization]):
        ID = 0x80EEE427
        QUALNAME = "functions.auth.SignUp"

        def __init__(
            self,
            phone_number: str,
            phone_code_hash: str,
            first_name: str,
            last_name: str = "",
        ) -> None:
            self.phone_number = phone_number
            self.phone_code_hash = phone_code_hash
            self.first_name = first_name
            self.last_name = last_name

        def write(self) -> bytes:
            return (
                struct.pack("<I", self.ID)
                + write_string(self.phone_number)
                + write_string(self.phone_code_hash)
                + write_string(self.first_name)
                + write_string(self.last_name)
            )

        def read_result(self, b: BinaryIO) -> Authorization:
            read_uint(b)
            return Authorization.read(b)

    class CheckPassword(TLRequest[Authorization]):
        ID = 0xD18B4D16
        QUALNAME = "functions.auth.CheckPassword"

        def __init__(self, password: InputCheckPasswordSRP) -> None:
            self.password = password

        def write(self) -> bytes:
            return struct.pack("<I", self.ID) + self.password.write()

        def read_result(self, b: BinaryIO) -> Authorization:
            read_uint(b)
            return Authorization.read(b)

    class ImportBotAuthorization(TLRequest[Authorization]):
        ID = 0x67A3FF2C
        QUALNAME = "functions.auth.ImportBotAuthorization"

        def __init__(self, api_id: int, api_hash: str, bot_auth_token: str) -> None:
            self.api_id = api_id
            self.api_hash = api_hash
            self.bot_auth_token = bot_auth_token

        def write(self) -> bytes:
            # flags = 0
            return (
                struct.pack("<II", self.ID, 0)
                + write_int(self.api_id)
                + write_string(self.api_hash)
                + write_string(self.bot_auth_token)
            )

        def read_result(self, b: BinaryIO) -> Authorization:
            read_uint(b)
            return Authorization.read(b)

    class ExportAuthorization(TLRequest[Any]):
        ID = 0xE5BFFFCD
        QUALNAME = "functions.auth.ExportAuthorization"

        def __init__(self, dc_id: int) -> None:
            self.dc_id = dc_id

        def write(self) -> bytes:
            return struct.pack("<I", self.ID) + write_int(self.dc_id)

        def read_result(self, b: BinaryIO) -> Any:
            from aiogram.raw.all import read_tl_object

            return read_tl_object(b)

    class ImportAuthorization(TLRequest[Authorization]):
        ID = 0xA57A7DAD
        QUALNAME = "functions.auth.ImportAuthorization"

        def __init__(self, id: int, bytes_data: bytes) -> None:
            self.id = id
            self.bytes_data = bytes_data

        def write(self) -> bytes:
            return struct.pack("<I", self.ID) + write_long(self.id) + write_bytes(self.bytes_data)

        def read_result(self, b: BinaryIO) -> Any:
            from aiogram.raw.all import read_tl_object

            return read_tl_object(b)

    class LogOut(TLRequest[bool]):
        ID = 0x3E72BA14
        QUALNAME = "functions.auth.LogOut"

        def write(self) -> bytes:
            return struct.pack("<I", self.ID)

        def read_result(self, b: BinaryIO) -> bool:
            return True


class account:
    class GetPassword(TLRequest[AccountPassword]):
        ID = 0x548A30F5
        QUALNAME = "functions.account.GetPassword"

        def write(self) -> bytes:
            return struct.pack("<I", self.ID)

        def read_result(self, b: BinaryIO) -> AccountPassword:
            read_uint(b)
            return AccountPassword.read(b)


class contacts:
    class ResolveUsername(TLRequest[ContactsResolvedPeer]):
        ID = 0xF93CCBA3
        QUALNAME = "functions.contacts.ResolveUsername"

        def __init__(self, username: str) -> None:
            self.username = username

        def write(self) -> bytes:
            # flags = 0
            return struct.pack("<II", self.ID, 0) + write_string(self.username)

        def read_result(self, b: BinaryIO) -> ContactsResolvedPeer:
            read_uint(b)
            return ContactsResolvedPeer.read(b)


class users:
    class GetUsers(TLRequest[list[User]]):
        ID = 0x0D91A548
        QUALNAME = "functions.users.GetUsers"

        def __init__(self, id: list[InputPeer]) -> None:
            self.id = id

        def write(self) -> bytes:
            return struct.pack("<I", self.ID) + write_vector(self.id, lambda x: x.write())

        def read_result(self, b: BinaryIO) -> list[User]:
            from aiogram.raw.all import read_tl_object

            return read_vector(b, read_tl_object)

    class GetFullUser(TLRequest[Any]):
        ID = 0xB60F5918
        QUALNAME = "functions.users.GetFullUser"

        def __init__(self, id: InputPeer) -> None:
            self.id = id

        def write(self) -> bytes:
            return struct.pack("<I", self.ID) + self.id.write()

        def read_result(self, b: BinaryIO) -> Any:
            from aiogram.raw.all import read_tl_object

            return read_tl_object(b)


class messages:
    class SendMessage(TLRequest[Updates]):
        ID = 0x983F9569
        QUALNAME = "functions.messages.SendMessage"

        def __init__(
            self,
            peer: InputPeer,
            message: str,
            random_id: int,
            no_webpage: bool = False,
            silent: bool = False,
            background: bool = False,
            clear_draft: bool = False,
            reply_to_msg_id: int | None = None,
        ) -> None:
            self.peer = peer
            self.message = message
            self.random_id = random_id
            self.no_webpage = no_webpage
            self.silent = silent
            self.background = background
            self.clear_draft = clear_draft
            self.reply_to_msg_id = reply_to_msg_id

        def write(self) -> bytes:
            flags = 0
            if self.no_webpage:
                flags |= 1 << 1
            if self.silent:
                flags |= 1 << 5
            if self.background:
                flags |= 1 << 6
            if self.clear_draft:
                flags |= 1 << 7
            if self.reply_to_msg_id is not None:
                flags |= 1 << 0

            res = struct.pack("<II", self.ID, flags) + self.peer.write()
            if self.reply_to_msg_id is not None:
                # InputReplyToMessage constructor (0x869fbe10)
                res += struct.pack("<IIi", 0x869FBE10, 0, self.reply_to_msg_id)
            res += write_string(self.message)
            res += write_long(self.random_id)
            return res

        def read_result(self, b: BinaryIO) -> Any:
            from aiogram.raw.all import read_tl_object

            try:
                return read_tl_object(b)
            except Exception:
                return Updates(updates=[], users=[], chats=[], date=0, seq=0)

    class SendMedia(TLRequest[Updates]):
        ID = 0x0330E77F
        QUALNAME = "functions.messages.SendMedia"

        def __init__(
            self,
            peer: InputPeer,
            media: TLObject,
            message: str = "",
            random_id: int = 0,
            reply_to_msg_id: int | None = None,
        ) -> None:
            self.peer = peer
            self.media = media
            self.message = message
            self.random_id = random_id
            self.reply_to_msg_id = reply_to_msg_id

        def write(self) -> bytes:
            flags = 0
            if self.reply_to_msg_id is not None:
                flags |= 1 << 0
            res = struct.pack("<II", self.ID, flags) + self.peer.write()
            if self.reply_to_msg_id is not None:
                # InputReplyToMessage constructor (0x869fbe10)
                res += struct.pack("<IIi", 0x869FBE10, 0, self.reply_to_msg_id)
            res += self.media.write()
            res += write_string(self.message)
            res += write_long(self.random_id)
            return res

        def read_result(self, b: BinaryIO) -> Any:
            from aiogram.raw.all import read_tl_object

            try:
                return read_tl_object(b)
            except Exception:
                return Updates(updates=[], users=[], chats=[], date=0, seq=0)

    class EditMessage(TLRequest[Updates]):
        ID = 0x48F71778
        QUALNAME = "functions.messages.EditMessage"

        def __init__(self, peer: InputPeer, id: int, message: str) -> None:
            self.peer = peer
            self.id = id
            self.message = message

        def write(self) -> bytes:
            flags = 1 << 11  # message flag
            return (
                struct.pack("<II", self.ID, flags)
                + self.peer.write()
                + write_int(self.id)
                + write_string(self.message)
            )

        def read_result(self, b: BinaryIO) -> Any:
            from aiogram.raw.all import read_tl_object

            return read_tl_object(b)

    class DeleteMessages(TLRequest[Any]):
        ID = 0xE58E95D2
        QUALNAME = "functions.messages.DeleteMessages"

        def __init__(self, id: list[int], revoke: bool = True) -> None:
            self.id = id
            self.revoke = revoke

        def write(self) -> bytes:
            flags = 1 if self.revoke else 0
            return struct.pack("<II", self.ID, flags) + write_vector(self.id, write_int)

        def read_result(self, b: BinaryIO) -> Any:
            from aiogram.raw.all import read_tl_object

            return read_tl_object(b)

    class ForwardMessages(TLRequest[Updates]):
        ID = 0xD5039208
        QUALNAME = "functions.messages.ForwardMessages"

        def __init__(
            self,
            from_peer: InputPeer,
            to_peer: InputPeer,
            id: list[int],
            random_id: list[int] | None = None,
            silent: bool = False,
            background: bool = False,
            with_my_score: bool = False,
            drop_author: bool = False,
            drop_media_captions: bool = False,
        ) -> None:
            self.from_peer = from_peer
            self.to_peer = to_peer
            self.id = id
            self.random_id = random_id or [random.getrandbits(63) for _ in id]
            self.silent = silent
            self.background = background
            self.with_my_score = with_my_score
            self.drop_author = drop_author
            self.drop_media_captions = drop_media_captions

        def write(self) -> bytes:
            flags = 0
            if self.silent:
                flags |= 1 << 5
            if self.background:
                flags |= 1 << 6
            if self.with_my_score:
                flags |= 1 << 8
            if self.drop_author:
                flags |= 1 << 11
            if self.drop_media_captions:
                flags |= 1 << 12
            return (
                struct.pack("<II", self.ID, flags)
                + self.from_peer.write()
                + write_vector(self.id, write_int)
                + write_vector(self.random_id, write_long)
                + self.to_peer.write()
            )

        def read_result(self, b: BinaryIO) -> Any:
            from aiogram.raw.all import read_tl_object

            return read_tl_object(b)

    class GetHistory(TLRequest[Any]):
        ID = 0x4423E6C5
        QUALNAME = "functions.messages.GetHistory"

        def __init__(
            self,
            peer: InputPeer,
            offset_id: int = 0,
            offset_date: int = 0,
            add_offset: int = 0,
            limit: int = 20,
            max_id: int = 0,
            min_id: int = 0,
            hash: int = 0,
        ) -> None:
            self.peer = peer
            self.offset_id = offset_id
            self.offset_date = offset_date
            self.add_offset = add_offset
            self.limit = limit
            self.max_id = max_id
            self.min_id = min_id
            self.hash = hash

        def write(self) -> bytes:
            return (
                struct.pack("<I", self.ID)
                + self.peer.write()
                + write_int(self.offset_id)
                + write_int(self.offset_date)
                + write_int(self.add_offset)
                + write_int(self.limit)
                + write_int(self.max_id)
                + write_int(self.min_id)
                + write_long(self.hash)
            )

        def read_result(self, b: BinaryIO) -> Any:
            from aiogram.raw.all import read_tl_object

            return read_tl_object(b)


class upload:
    class SaveFilePart(TLRequest[bool]):
        ID = 0xB304A621
        QUALNAME = "functions.upload.SaveFilePart"

        def __init__(self, file_id: int, file_part: int, bytes: bytes) -> None:
            self.file_id = file_id
            self.file_part = file_part
            self.bytes = bytes

        def write(self) -> bytes:
            return (
                struct.pack("<I", self.ID)
                + write_long(self.file_id)
                + write_int(self.file_part)
                + write_bytes(self.bytes)
            )

        def read_result(self, b: BinaryIO) -> bool:
            return True

    class SaveBigFilePart(TLRequest[bool]):
        ID = 0xDE7B673D
        QUALNAME = "functions.upload.SaveBigFilePart"

        def __init__(
            self, file_id: int, file_part: int, file_total_parts: int, bytes: bytes
        ) -> None:
            self.file_id = file_id
            self.file_part = file_part
            self.file_total_parts = file_total_parts
            self.bytes = bytes

        def write(self) -> bytes:
            return (
                struct.pack("<I", self.ID)
                + write_long(self.file_id)
                + write_int(self.file_part)
                + write_int(self.file_total_parts)
                + write_bytes(self.bytes)
            )

        def read_result(self, b: BinaryIO) -> bool:
            return True

    class GetFile(TLRequest[Any]):
        ID = 0xBE5335BE
        QUALNAME = "functions.upload.GetFile"

        def __init__(self, location: TLObject, offset: int, limit: int) -> None:
            self.location = location
            self.offset = offset
            self.limit = limit

        def write(self) -> bytes:
            # flags = 0
            return (
                struct.pack("<II", self.ID, 0)
                + self.location.write()
                + write_long(self.offset)
                + write_int(self.limit)
            )

        def read_result(self, b: BinaryIO) -> Any:
            from aiogram.raw.all import read_tl_object

            return read_tl_object(b)
