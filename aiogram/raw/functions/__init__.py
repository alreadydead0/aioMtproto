"""
Official Telegram TL RPC Functions for MTProto.
"""

from __future__ import annotations

import struct
from typing import Any, BinaryIO, List, Optional

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
    Authorization,
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

        def __init__(self, phone_number: str, api_id: int, api_hash: str) -> None:
            self.phone_number = phone_number
            self.api_id = api_id
            self.api_hash = api_hash

        def write(self) -> bytes:
            # flags = 0
            # settings = CodeSettings (flags=0)
            code_settings = struct.pack("<II", 0xAD253618, 0)
            return (
                struct.pack("<I", self.ID)
                + write_string(self.phone_number)
                + write_int(self.api_id)
                + write_string(self.api_hash)
                + code_settings
            )

        def read_result(self, b: BinaryIO) -> SentCode:
            read_uint(b)
            return SentCode.read(b)

    class SignIn(TLRequest[Authorization]):
        ID = 0x8D52A951
        QUALNAME = "functions.auth.SignIn"

        def __init__(self, phone_number: str, phone_code_hash: str, phone_code: str) -> None:
            self.phone_number = phone_number
            self.phone_code_hash = phone_code_hash
            self.phone_code = phone_code

        def write(self) -> bytes:
            # flags (int) = 0
            return (
                struct.pack("<II", self.ID, 0)
                + write_string(self.phone_number)
                + write_string(self.phone_code_hash)
                + write_string(self.phone_code)
            )

        def read_result(self, b: BinaryIO) -> Authorization:
            read_uint(b)
            return Authorization.read(b)

    class ImportBotAuthorization(TLRequest[Authorization]):
        ID = 0x67A3FFCA
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

    class LogOut(TLRequest[bool]):
        ID = 0x3E72BA14
        QUALNAME = "functions.auth.LogOut"

        def write(self) -> bytes:
            return struct.pack("<I", self.ID)

        def read_result(self, b: BinaryIO) -> bool:
            return True


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
                # InputReplyToMessage constructor (0x0bad8270)
                res += struct.pack("<IIi", 0x0BAD8270, 0, self.reply_to_msg_id)
            res += write_string(self.message)
            res += write_long(self.random_id)
            return res

        def read_result(self, b: BinaryIO) -> Updates:
            from aiogram.raw.all import read_tl_object
            return read_tl_object(b)

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

        def read_result(self, b: BinaryIO) -> Updates:
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

        def __init__(self, file_id: int, file_part: int, file_total_parts: int, bytes: bytes) -> None:
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
        ID = 0xBE250526
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
