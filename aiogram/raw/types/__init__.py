"""
Official Telegram TL Types for MTProto.
"""

from __future__ import annotations

import io
import struct
from typing import Any, BinaryIO

from aiogram.raw.core.primitives import (
    TLObject,
    read_bool,
    read_bytes,
    read_double,
    read_int,
    read_long,
    read_string,
    read_uint,
    read_vector,
    write_bool,
    write_bytes,
    write_double,
    write_int,
    write_long,
    write_string,
    write_uint,
    write_vector,
)


class Peer(TLObject):
    pass


class PeerUser(Peer):
    ID = 0x59511722
    QUALNAME = "types.PeerUser"

    def __init__(self, user_id: int) -> None:
        self.user_id = user_id

    def write(self) -> bytes:
        return struct.pack("<I", self.ID) + write_long(self.user_id)

    @classmethod
    def read(cls, b: BinaryIO) -> PeerUser:
        return PeerUser(user_id=read_long(b))


class PeerChat(Peer):
    ID = 0x36C6088A
    QUALNAME = "types.PeerChat"

    def __init__(self, chat_id: int) -> None:
        self.chat_id = chat_id

    def write(self) -> bytes:
        return struct.pack("<I", self.ID) + write_long(self.chat_id)

    @classmethod
    def read(cls, b: BinaryIO) -> PeerChat:
        return PeerChat(chat_id=read_long(b))


class PeerChannel(Peer):
    ID = 0xA2A5D432
    QUALNAME = "types.PeerChannel"

    def __init__(self, channel_id: int) -> None:
        self.channel_id = channel_id

    def write(self) -> bytes:
        return struct.pack("<I", self.ID) + write_long(self.channel_id)

    @classmethod
    def read(cls, b: BinaryIO) -> PeerChannel:
        return PeerChannel(channel_id=read_long(b))


class InputPeer(TLObject):
    pass


class InputPeerEmpty(InputPeer):
    ID = 0x7F3B18EA
    QUALNAME = "types.InputPeerEmpty"

    def write(self) -> bytes:
        return struct.pack("<I", self.ID)

    @classmethod
    def read(cls, b: BinaryIO) -> InputPeerEmpty:
        return InputPeerEmpty()


class InputPeerSelf(InputPeer):
    ID = 0x7DA07EC9
    QUALNAME = "types.InputPeerSelf"

    def write(self) -> bytes:
        return struct.pack("<I", self.ID)

    @classmethod
    def read(cls, b: BinaryIO) -> InputPeerSelf:
        return InputPeerSelf()


class InputPeerUser(InputPeer):
    ID = 0xDDE8A54C
    QUALNAME = "types.InputPeerUser"

    def __init__(self, user_id: int, access_hash: int) -> None:
        self.user_id = user_id
        self.access_hash = access_hash

    def write(self) -> bytes:
        return struct.pack("<I", self.ID) + write_long(self.user_id) + write_long(self.access_hash)

    @classmethod
    def read(cls, b: BinaryIO) -> InputPeerUser:
        return InputPeerUser(user_id=read_long(b), access_hash=read_long(b))


class InputPeerChat(InputPeer):
    ID = 0x3563E46C
    QUALNAME = "types.InputPeerChat"

    def __init__(self, chat_id: int) -> None:
        self.chat_id = chat_id

    def write(self) -> bytes:
        return struct.pack("<I", self.ID) + write_long(self.chat_id)

    @classmethod
    def read(cls, b: BinaryIO) -> InputPeerChat:
        return InputPeerChat(chat_id=read_long(b))


class InputPeerChannel(InputPeer):
    ID = 0x27BCBBFC
    QUALNAME = "types.InputPeerChannel"

    def __init__(self, channel_id: int, access_hash: int) -> None:
        self.channel_id = channel_id
        self.access_hash = access_hash

    def write(self) -> bytes:
        return (
            struct.pack("<I", self.ID) + write_long(self.channel_id) + write_long(self.access_hash)
        )

    @classmethod
    def read(cls, b: BinaryIO) -> InputPeerChannel:
        return InputPeerChannel(channel_id=read_long(b), access_hash=read_long(b))


class User(TLObject):
    ID = 0x215C4438
    QUALNAME = "types.User"

    def __init__(
        self,
        id: int,
        is_self: bool = False,
        contact: bool = False,
        mutual_contact: bool = False,
        deleted: bool = False,
        bot: bool = False,
        bot_chat_history: bool = False,
        bot_nochats: bool = False,
        verified: bool = False,
        restricted: bool = False,
        min: bool = False,
        bot_inline_geo: bool = False,
        support: bool = False,
        scam: bool = False,
        apply_min_photo: bool = False,
        fake: bool = False,
        bot_attach_menu: bool = False,
        premium: bool = False,
        attach_menu_enabled: bool = False,
        bot_can_edit: bool = False,
        close_friend: bool = False,
        stories_hidden: bool = False,
        stories_unavailable: bool = False,
        contact_require_premium: bool = False,
        bot_business: bool = False,
        bot_has_main_app: bool = False,
        access_hash: int | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        username: str | None = None,
        phone: str | None = None,
        lang_code: str | None = None,
    ) -> None:
        self.id = id
        self.is_self = is_self
        self.contact = contact
        self.mutual_contact = mutual_contact
        self.deleted = deleted
        self.bot = bot
        self.bot_chat_history = bot_chat_history
        self.bot_nochats = bot_nochats
        self.verified = verified
        self.restricted = restricted
        self.min = min
        self.bot_inline_geo = bot_inline_geo
        self.support = support
        self.scam = scam
        self.apply_min_photo = apply_min_photo
        self.fake = fake
        self.bot_attach_menu = bot_attach_menu
        self.premium = premium
        self.attach_menu_enabled = attach_menu_enabled
        self.bot_can_edit = bot_can_edit
        self.close_friend = close_friend
        self.stories_hidden = stories_hidden
        self.stories_unavailable = stories_unavailable
        self.contact_require_premium = contact_require_premium
        self.bot_business = bot_business
        self.bot_has_main_app = bot_has_main_app
        self.access_hash = access_hash
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.phone = phone
        self.lang_code = lang_code

    def write(self) -> bytes:
        flags = 0
        flags2 = 0
        if self.is_self:
            flags |= 1 << 10
        if self.contact:
            flags |= 1 << 11
        if self.mutual_contact:
            flags |= 1 << 12
        if self.deleted:
            flags |= 1 << 13
        if self.bot:
            flags |= 1 << 14
        if self.bot_chat_history:
            flags |= 1 << 15
        if self.bot_nochats:
            flags |= 1 << 16
        if self.verified:
            flags |= 1 << 17
        if self.restricted:
            flags |= 1 << 18
        if self.min:
            flags |= 1 << 20
        if self.bot_inline_geo:
            flags |= 1 << 21
        if self.support:
            flags |= 1 << 23
        if self.scam:
            flags |= 1 << 24
        if self.apply_min_photo:
            flags |= 1 << 25
        if self.fake:
            flags |= 1 << 26
        if self.bot_attach_menu:
            flags |= 1 << 27
        if self.premium:
            flags |= 1 << 28
        if self.attach_menu_enabled:
            flags |= 1 << 29
        if self.access_hash is not None:
            flags |= 1 << 0
        if self.first_name is not None:
            flags |= 1 << 1
        if self.last_name is not None:
            flags |= 1 << 2
        if self.username is not None:
            flags |= 1 << 3
        if self.phone is not None:
            flags |= 1 << 4
        if self.bot_can_edit:
            flags2 |= 1 << 1
        if self.close_friend:
            flags2 |= 1 << 2
        if self.stories_hidden:
            flags2 |= 1 << 3
        if self.stories_unavailable:
            flags2 |= 1 << 4
        if self.contact_require_premium:
            flags2 |= 1 << 10
        if self.bot_business:
            flags2 |= 1 << 11
        if self.bot_has_main_app:
            flags2 |= 1 << 13

        res = struct.pack("<IIIq", self.ID, flags, flags2, self.id)
        if self.access_hash is not None:
            res += write_long(self.access_hash)
        if self.first_name is not None:
            res += write_string(self.first_name)
        if self.last_name is not None:
            res += write_string(self.last_name)
        if self.username is not None:
            res += write_string(self.username)
        if self.phone is not None:
            res += write_string(self.phone)
        return res

    @classmethod
    def read(cls, b: BinaryIO) -> User:
        flags = read_uint(b)
        flags2 = read_uint(b)
        user_id = read_long(b)
        access_hash = read_long(b) if (flags & (1 << 0)) else None
        first_name = read_string(b) if (flags & (1 << 1)) else None
        last_name = read_string(b) if (flags & (1 << 2)) else None
        username = read_string(b) if (flags & (1 << 3)) else None
        phone = read_string(b) if (flags & (1 << 4)) else None

        return User(
            id=user_id,
            is_self=bool(flags & (1 << 10)),
            contact=bool(flags & (1 << 11)),
            mutual_contact=bool(flags & (1 << 12)),
            deleted=bool(flags & (1 << 13)),
            bot=bool(flags & (1 << 14)),
            bot_chat_history=bool(flags & (1 << 15)),
            bot_nochats=bool(flags & (1 << 16)),
            verified=bool(flags & (1 << 17)),
            restricted=bool(flags & (1 << 18)),
            min=bool(flags & (1 << 20)),
            bot_inline_geo=bool(flags & (1 << 21)),
            support=bool(flags & (1 << 23)),
            scam=bool(flags & (1 << 24)),
            apply_min_photo=bool(flags & (1 << 25)),
            fake=bool(flags & (1 << 26)),
            bot_attach_menu=bool(flags & (1 << 27)),
            premium=bool(flags & (1 << 28)),
            attach_menu_enabled=bool(flags & (1 << 29)),
            bot_can_edit=bool(flags2 & (1 << 1)),
            close_friend=bool(flags2 & (1 << 2)),
            stories_hidden=bool(flags2 & (1 << 3)),
            stories_unavailable=bool(flags2 & (1 << 4)),
            contact_require_premium=bool(flags2 & (1 << 10)),
            bot_business=bool(flags2 & (1 << 11)),
            bot_has_main_app=bool(flags2 & (1 << 13)),
            access_hash=access_hash,
            first_name=first_name,
            last_name=last_name,
            username=username,
            phone=phone,
        )


class Message(TLObject):
    ID = 0xB92F76CF
    QUALNAME = "types.Message"

    def __init__(
        self,
        id: int,
        peer_id: Peer,
        date: int,
        message: str,
        out: bool = False,
        mentioned: bool = False,
        media_unread: bool = False,
        silent: bool = False,
        post: bool = False,
        from_id: Peer | None = None,
        reply_to_msg_id: int | None = None,
        entities: list[Any] | None = None,
        media: Any = None,
    ) -> None:
        self.id = id
        self.peer_id = peer_id
        self.date = date
        self.message = message
        self.out = out
        self.mentioned = mentioned
        self.media_unread = media_unread
        self.silent = silent
        self.post = post
        self.from_id = from_id
        self.reply_to_msg_id = reply_to_msg_id
        self.entities = entities or []
        self.media = media

    def write(self) -> bytes:
        flags = 0
        if self.out:
            flags |= 1 << 1
        if self.mentioned:
            flags |= 1 << 4
        if self.media_unread:
            flags |= 1 << 5
        if self.silent:
            flags |= 1 << 13
        if self.post:
            flags |= 1 << 14
        if self.from_id is not None:
            flags |= 1 << 8
        if self.reply_to_msg_id is not None:
            flags |= 1 << 3
        if self.entities:
            flags |= 1 << 7

        res = struct.pack("<IIi", self.ID, flags, self.id)
        if self.from_id is not None:
            res += self.from_id.write()
        res += self.peer_id.write()
        res += write_int(self.date)
        res += write_string(self.message)
        return res

    @classmethod
    def read(cls, b: BinaryIO) -> Message:
        flags = read_uint(b)
        msg_id = read_int(b)
        from_id: Peer | None = None
        if flags & (1 << 8):
            peer_c_id = read_uint(b)
            if peer_c_id == PeerUser.ID:
                from_id = PeerUser.read(b)
            elif peer_c_id == PeerChat.ID:
                from_id = PeerChat.read(b)
            elif peer_c_id == PeerChannel.ID:
                from_id = PeerChannel.read(b)

        # peer_id
        peer_c_id = read_uint(b)
        peer_id: Peer
        if peer_c_id == PeerUser.ID:
            peer_id = PeerUser.read(b)
        elif peer_c_id == PeerChat.ID:
            peer_id = PeerChat.read(b)
        elif peer_c_id == PeerChannel.ID:
            peer_id = PeerChannel.read(b)
        else:
            peer_id = PeerUser(user_id=0)

        date = read_int(b)
        text = read_string(b)

        return Message(
            id=msg_id,
            peer_id=peer_id,
            date=date,
            message=text,
            out=bool(flags & (1 << 1)),
            mentioned=bool(flags & (1 << 4)),
            media_unread=bool(flags & (1 << 5)),
            silent=bool(flags & (1 << 13)),
            post=bool(flags & (1 << 14)),
            from_id=from_id,
        )


class UpdateShort(TLObject):
    ID = 0x78D4DEC1
    QUALNAME = "types.UpdateShort"

    def __init__(self, update: TLObject, date: int) -> None:
        self.update = update
        self.date = date

    @classmethod
    def read(cls, b: BinaryIO) -> UpdateShort:
        from aiogram.raw.all import read_tl_object

        update = read_tl_object(b)
        date = read_int(b)
        return UpdateShort(update=update, date=date)


class UpdateShortMessage(TLObject):
    ID = 0x313BC7F8
    QUALNAME = "types.UpdateShortMessage"

    def __init__(
        self,
        id: int,
        user_id: int,
        message: str,
        pts: int,
        pts_count: int,
        date: int,
        out: bool = False,
        mentioned: bool = False,
        media_unread: bool = False,
        silent: bool = False,
    ) -> None:
        self.id = id
        self.user_id = user_id
        self.message = message
        self.pts = pts
        self.pts_count = pts_count
        self.date = date
        self.out = out
        self.mentioned = mentioned
        self.media_unread = media_unread
        self.silent = silent

    @classmethod
    def read(cls, b: BinaryIO) -> UpdateShortMessage:
        flags = read_uint(b)
        msg_id = read_int(b)
        user_id = read_long(b)
        message = read_string(b)
        pts = read_int(b)
        pts_count = read_int(b)
        date = read_int(b)
        return UpdateShortMessage(
            id=msg_id,
            user_id=user_id,
            message=message,
            pts=pts,
            pts_count=pts_count,
            date=date,
            out=bool(flags & (1 << 1)),
            mentioned=bool(flags & (1 << 4)),
            media_unread=bool(flags & (1 << 5)),
            silent=bool(flags & (1 << 13)),
        )


class UpdateShortChatMessage(TLObject):
    ID = 0x4D6DEEA2
    QUALNAME = "types.UpdateShortChatMessage"

    def __init__(
        self,
        id: int,
        from_id: int,
        chat_id: int,
        message: str,
        pts: int,
        pts_count: int,
        date: int,
        out: bool = False,
        mentioned: bool = False,
        media_unread: bool = False,
        silent: bool = False,
    ) -> None:
        self.id = id
        self.from_id = from_id
        self.chat_id = chat_id
        self.message = message
        self.pts = pts
        self.pts_count = pts_count
        self.date = date
        self.out = out
        self.mentioned = mentioned
        self.media_unread = media_unread
        self.silent = silent

    @classmethod
    def read(cls, b: BinaryIO) -> UpdateShortChatMessage:
        flags = read_uint(b)
        msg_id = read_int(b)
        from_id = read_long(b)
        chat_id = read_long(b)
        message = read_string(b)
        pts = read_int(b)
        pts_count = read_int(b)
        date = read_int(b)
        return UpdateShortChatMessage(
            id=msg_id,
            from_id=from_id,
            chat_id=chat_id,
            message=message,
            pts=pts,
            pts_count=pts_count,
            date=date,
            out=bool(flags & (1 << 1)),
            mentioned=bool(flags & (1 << 4)),
            media_unread=bool(flags & (1 << 5)),
            silent=bool(flags & (1 << 13)),
        )


class UpdateNewMessage(TLObject):
    ID = 0x1F2B0AFD
    QUALNAME = "types.UpdateNewMessage"

    def __init__(self, message: TLObject, pts: int, pts_count: int) -> None:
        self.message = message
        self.pts = pts
        self.pts_count = pts_count

    @classmethod
    def read(cls, b: BinaryIO) -> UpdateNewMessage:
        from aiogram.raw.all import read_tl_object

        try:
            msg = read_tl_object(b)
        except Exception:
            msg = None
        pts = read_int(b) if b.readable() else 0
        pts_count = read_int(b) if b.readable() else 0
        return UpdateNewMessage(message=msg, pts=pts, pts_count=pts_count)


class UpdateMessageID(TLObject):
    ID = 0x4E90BFD6
    QUALNAME = "types.UpdateMessageID"

    def __init__(self, id: int, random_id: int) -> None:
        self.id = id
        self.random_id = random_id

    def write(self) -> bytes:
        return struct.pack("<I", self.ID) + write_int(self.id) + write_long(self.random_id)

    @classmethod
    def read(cls, b: BinaryIO) -> UpdateMessageID:
        return UpdateMessageID(id=read_int(b), random_id=read_long(b))


class UpdateEditMessage(TLObject):
    ID = 0xE40370A3
    QUALNAME = "types.UpdateEditMessage"

    def __init__(self, message: TLObject, pts: int, pts_count: int) -> None:
        self.message = message
        self.pts = pts
        self.pts_count = pts_count

    @classmethod
    def read(cls, b: BinaryIO) -> UpdateEditMessage:
        from aiogram.raw.all import read_tl_object

        try:
            msg = read_tl_object(b)
        except Exception:
            msg = None
        pts = read_int(b) if b.readable() else 0
        pts_count = read_int(b) if b.readable() else 0
        return UpdateEditMessage(message=msg, pts=pts, pts_count=pts_count)


class UpdateDeleteMessages(TLObject):
    ID = 0xA20DB0E5
    QUALNAME = "types.UpdateDeleteMessages"

    def __init__(self, messages: list[int], pts: int, pts_count: int) -> None:
        self.messages = messages
        self.pts = pts
        self.pts_count = pts_count

    @classmethod
    def read(cls, b: BinaryIO) -> UpdateDeleteMessages:
        try:
            messages = read_vector(b, read_int)
        except Exception:
            messages = []
        pts = read_int(b) if b.readable() else 0
        pts_count = read_int(b) if b.readable() else 0
        return UpdateDeleteMessages(messages=messages, pts=pts, pts_count=pts_count)


class UpdateNewChannelMessage(TLObject):
    ID = 0x62D45069
    QUALNAME = "types.UpdateNewChannelMessage"

    def __init__(self, message: TLObject, pts: int, pts_count: int) -> None:
        self.message = message
        self.pts = pts
        self.pts_count = pts_count

    @classmethod
    def read(cls, b: BinaryIO) -> UpdateNewChannelMessage:
        from aiogram.raw.all import read_tl_object

        try:
            msg = read_tl_object(b)
        except Exception:
            msg = None
        pts = read_int(b) if b.readable() else 0
        pts_count = read_int(b) if b.readable() else 0
        return UpdateNewChannelMessage(message=msg, pts=pts, pts_count=pts_count)


class UpdateEditChannelMessage(TLObject):
    ID = 0x1B3F4DF7
    QUALNAME = "types.UpdateEditChannelMessage"

    def __init__(self, message: TLObject, pts: int, pts_count: int) -> None:
        self.message = message
        self.pts = pts
        self.pts_count = pts_count

    @classmethod
    def read(cls, b: BinaryIO) -> UpdateEditChannelMessage:
        from aiogram.raw.all import read_tl_object

        try:
            msg = read_tl_object(b)
        except Exception:
            msg = None
        pts = read_int(b) if b.readable() else 0
        pts_count = read_int(b) if b.readable() else 0
        return UpdateEditChannelMessage(message=msg, pts=pts, pts_count=pts_count)


class Updates(TLObject):
    ID = 0x74AE4240
    QUALNAME = "types.Updates"

    def __init__(
        self,
        updates: list[TLObject],
        users: list[User],
        chats: list[Any],
        date: int,
        seq: int,
    ) -> None:
        self.updates = updates
        self.users = users
        self.chats = chats
        self.date = date
        self.seq = seq

    @classmethod
    def read(cls, b: BinaryIO) -> Updates:
        from aiogram.raw.all import read_tl_object

        try:
            updates = read_vector(b, read_tl_object)
        except Exception:
            updates = []
        try:
            users = read_vector(b, read_tl_object)
        except Exception:
            users = []
        try:
            chats = read_vector(b, read_tl_object)
        except Exception:
            chats = []
        date = read_int(b) if b.readable() else 0
        seq = read_int(b) if b.readable() else 0
        return Updates(updates=updates, users=users, chats=chats, date=date, seq=seq)


class UpdatesTooLong(TLObject):
    ID = 0xE317ED8B
    QUALNAME = "types.UpdatesTooLong"

    @classmethod
    def read(cls, b: BinaryIO) -> UpdatesTooLong:
        return UpdatesTooLong()


class UpdatesCombined(TLObject):
    ID = 0x725B04C2
    QUALNAME = "types.UpdatesCombined"

    def __init__(
        self,
        updates: list[TLObject],
        users: list[User],
        chats: list[Any],
        date: int,
        seq_start: int,
        seq: int,
    ) -> None:
        self.updates = updates
        self.users = users
        self.chats = chats
        self.date = date
        self.seq_start = seq_start
        self.seq = seq

    @classmethod
    def read(cls, b: BinaryIO) -> UpdatesCombined:
        from aiogram.raw.all import read_tl_object

        updates = read_vector(b, read_tl_object)
        users = read_vector(b, read_tl_object)
        chats = read_vector(b, read_tl_object)
        date = read_int(b)
        seq_start = read_int(b)
        seq = read_int(b)
        return UpdatesCombined(updates, users, chats, date, seq_start, seq)


class NearestDc(TLObject):
    ID = 0x8E1A1775
    QUALNAME = "types.NearestDc"

    def __init__(self, country: str, this_dc: int, nearest_dc: int) -> None:
        self.country = country
        self.this_dc = this_dc
        self.nearest_dc = nearest_dc

    @classmethod
    def read(cls, b: BinaryIO) -> NearestDc:
        return NearestDc(
            country=read_string(b),
            this_dc=read_int(b),
            nearest_dc=read_int(b),
        )


class SentCode(TLObject):
    ID = 0x5E002502
    QUALNAME = "auth.SentCode"

    def __init__(
        self,
        phone_code_hash: str,
        timeout: int | None = None,
        phone_registered: bool = False,
        code_type: str | None = None,
    ) -> None:
        self.phone_code_hash = phone_code_hash
        self.timeout = timeout
        self.phone_registered = phone_registered
        self.code_type = code_type

    @classmethod
    def read(cls, b: BinaryIO) -> SentCode:
        flags = read_uint(b)
        phone_registered = bool(flags & (1 << 0))
        type_c_id = read_uint(b)
        code_type = "app"

        if type_c_id in (0x3DBB5986, 0xC0000810, 0x5353C57F):  # app, sms, call
            read_int(b)  # length: int
            code_type = (
                "app"
                if type_c_id == 0x3DBB5986
                else ("sms" if type_c_id == 0xC0000810 else "call")
            )
        elif type_c_id == 0xAB03C6D9:  # flashCall
            read_string(b)  # pattern
            code_type = "flash_call"
        elif type_c_id == 0x820064E3:  # missedCall
            read_string(b)  # prefix
            read_int(b)  # length
            code_type = "missed_call"
        elif type_c_id == 0xD9565C39:  # fragmentSms
            read_string(b)  # url
            read_int(b)  # length
            code_type = "fragment_sms"
        elif type_c_id == 0xF450F59B:  # emailCode
            e_flags = read_uint(b)
            read_string(b)  # email_pattern
            read_int(b)  # length
            if e_flags & (1 << 3):
                read_int(b)
            if e_flags & (1 << 4):
                read_int(b)
            code_type = "email"
        elif type_c_id == 0xA5491EDE:  # setUpEmailRequired
            read_uint(b)  # flags
            code_type = "setup_email"
        elif type_c_id in (0xA41E4C71, 0xB30C163B):  # smsWord, smsPhrase
            s_flags = read_uint(b)
            if type_c_id == 0xA41E4C71:
                read_int(b)  # length
            if s_flags & (1 << 0):
                read_string(b)
            code_type = "sms"
        elif type_c_id == 0xE57B1432:  # firebaseSms
            f_flags = read_uint(b)
            if f_flags & (1 << 0):
                read_bytes(b)  # nonce
            if f_flags & (1 << 2):
                read_bytes(b)  # play_integrity_nonce
            if f_flags & (1 << 1):
                read_int(b)  # push_timeout
            read_int(b)  # length
            code_type = "firebase"

        phone_code_hash = read_string(b)

        if flags & (1 << 1):
            read_uint(b)  # next_type: CodeType
        timeout = read_int(b) if (flags & (1 << 2)) else None
        if flags & (1 << 3):
            # termsOfService
            read_uint(b)
            read_string(b)
        if flags & (1 << 4):
            # url
            read_string(b)

        return SentCode(
            phone_code_hash=phone_code_hash,
            timeout=timeout,
            phone_registered=phone_registered,
            code_type=code_type,
        )


class Authorization(TLObject):
    ID = 0xAD01D61D
    QUALNAME = "auth.Authorization"

    def __init__(self, user: User, setup_password_required: bool = False) -> None:
        self.user = user
        self.setup_password_required = setup_password_required

    @classmethod
    def read(cls, b: BinaryIO) -> Authorization:
        flags = read_uint(b)
        setup_pwd = bool(flags & (1 << 1))
        if flags & (1 << 1):
            read_int(b)  # otherwise_relogin_days
        if flags & (1 << 0):
            read_int(b)  # tmp_sessions
        if flags & (1 << 2):
            read_bytes(b)  # future_auth_token

        # user may be boxed User, userEmpty, or bare User
        c_id = read_uint(b)
        if c_id == 0xD3BC4B7A:  # userEmpty
            user = User(id=read_long(b))
        elif c_id in (0x215C4438, 0x83314F16):  # User
            user = User.read(b)
        else:
            b.seek(b.tell() - 4)
            user = User.read(b)
        return Authorization(user=user, setup_password_required=setup_pwd)


class ExportedAuthorization(TLObject):
    ID = 0xB434E2B8
    QUALNAME = "auth.ExportedAuthorization"

    def __init__(self, id: int, bytes_data: bytes) -> None:
        self.id = id
        self.bytes_data = bytes_data
        self.bytes = bytes_data

    @classmethod
    def read(cls, b: BinaryIO) -> ExportedAuthorization:
        return ExportedAuthorization(
            id=read_long(b),
            bytes_data=read_bytes(b),
        )


class ExportedAuthorizationLegacy(TLObject):
    ID = 0xDF969C2D
    QUALNAME = "auth.ExportedAuthorizationLegacy"

    @classmethod
    def read(cls, b: BinaryIO) -> ExportedAuthorization:
        return ExportedAuthorization(
            id=read_int(b),
            bytes_data=read_bytes(b),
        )


class InputFile(TLObject):
    ID = 0xF52FF12B
    QUALNAME = "types.InputFile"

    def __init__(self, id: int, parts: int, name: str, md5_checksum: str = "") -> None:
        self.id = id
        self.parts = parts
        self.name = name
        self.md5_checksum = md5_checksum

    def write(self) -> bytes:
        return (
            struct.pack("<I", self.ID)
            + write_long(self.id)
            + write_int(self.parts)
            + write_string(self.name)
            + write_string(self.md5_checksum)
        )

    @classmethod
    def read(cls, b: BinaryIO) -> InputFile:
        return InputFile(
            id=read_long(b),
            parts=read_int(b),
            name=read_string(b),
            md5_checksum=read_string(b),
        )


class InputFileBig(TLObject):
    ID = 0xFA4F0BB5
    QUALNAME = "types.InputFileBig"

    def __init__(self, id: int, parts: int, name: str) -> None:
        self.id = id
        self.parts = parts
        self.name = name

    def write(self) -> bytes:
        return (
            struct.pack("<I", self.ID)
            + write_long(self.id)
            + write_int(self.parts)
            + write_string(self.name)
        )

    @classmethod
    def read(cls, b: BinaryIO) -> InputFileBig:
        return InputFileBig(
            id=read_long(b),
            parts=read_int(b),
            name=read_string(b),
        )


class InputFileLocation(TLObject):
    pass


class InputDocumentFileLocation(InputFileLocation):
    ID = 0xBAD07584
    QUALNAME = "types.InputDocumentFileLocation"

    def __init__(
        self, id: int, access_hash: int, file_reference: bytes, thumb_size: str = ""
    ) -> None:
        self.id = id
        self.access_hash = access_hash
        self.file_reference = file_reference
        self.thumb_size = thumb_size

    def write(self) -> bytes:
        return (
            struct.pack("<I", self.ID)
            + write_long(self.id)
            + write_long(self.access_hash)
            + write_bytes(self.file_reference)
            + write_string(self.thumb_size)
        )

    @classmethod
    def read(cls, b: BinaryIO) -> InputDocumentFileLocation:
        return InputDocumentFileLocation(
            id=read_long(b),
            access_hash=read_long(b),
            file_reference=read_bytes(b),
            thumb_size=read_string(b),
        )


class InputPhotoFileLocation(InputFileLocation):
    ID = 0x40181FFE
    QUALNAME = "types.InputPhotoFileLocation"

    def __init__(
        self, id: int, access_hash: int, file_reference: bytes, thumb_size: str = ""
    ) -> None:
        self.id = id
        self.access_hash = access_hash
        self.file_reference = file_reference
        self.thumb_size = thumb_size

    def write(self) -> bytes:
        return (
            struct.pack("<I", self.ID)
            + write_long(self.id)
            + write_long(self.access_hash)
            + write_bytes(self.file_reference)
            + write_string(self.thumb_size)
        )

    @classmethod
    def read(cls, b: BinaryIO) -> InputPhotoFileLocation:
        return InputPhotoFileLocation(
            id=read_long(b),
            access_hash=read_long(b),
            file_reference=read_bytes(b),
            thumb_size=read_string(b),
        )


class InputPeerPhotoFileLocation(InputFileLocation):
    ID = 0x37257E96
    QUALNAME = "types.InputPeerPhotoFileLocation"

    def __init__(self, peer: TLObject, photo_id: int, big: bool = False) -> None:
        self.peer = peer
        self.photo_id = photo_id
        self.big = big

    def write(self) -> bytes:
        flags = 1 if self.big else 0
        return struct.pack("<II", self.ID, flags) + self.peer.write() + write_long(self.photo_id)

    @classmethod
    def read(cls, b: BinaryIO) -> InputPeerPhotoFileLocation:
        flags = read_uint(b)
        from aiogram.raw.all import read_tl_object

        peer = read_tl_object(b)
        photo_id = read_long(b)
        return InputPeerPhotoFileLocation(peer=peer, photo_id=photo_id, big=bool(flags & 1))


class UploadFile(TLObject):
    ID = 0x096A18D5
    QUALNAME = "types.upload.File"

    def __init__(self, type: Any = None, mtime: int = 0, bytes: bytes = b"") -> None:
        self.type = type
        self.mtime = mtime
        self.bytes = bytes

    def write(self) -> bytes:
        type_bytes = (
            self.type.write() if hasattr(self.type, "write") else struct.pack("<I", 0x40BC6F52)
        )
        return (
            struct.pack("<I", self.ID)
            + type_bytes
            + write_int(self.mtime)
            + write_bytes(self.bytes)
        )

    @classmethod
    def read(cls, b: BinaryIO) -> UploadFile:
        from aiogram.raw.all import read_tl_object

        file_type = read_tl_object(b)
        mtime = read_int(b)
        content = read_bytes(b)
        return UploadFile(type=file_type, mtime=mtime, bytes=content)


class UploadFileCdnRedirect(TLObject):
    ID = 0xF18CDA44
    QUALNAME = "types.upload.FileCdnRedirect"

    def __init__(
        self,
        dc_id: int,
        file_token: bytes,
        encryption_key: bytes,
        encryption_iv: bytes,
        file_hashes: list[Any] | None = None,
    ) -> None:
        self.dc_id = dc_id
        self.file_token = file_token
        self.encryption_key = encryption_key
        self.encryption_iv = encryption_iv
        self.file_hashes = file_hashes or []

    @classmethod
    def read(cls, b: BinaryIO) -> UploadFileCdnRedirect:
        from aiogram.raw.all import read_tl_object

        dc_id = read_int(b)
        file_token = read_bytes(b)
        encryption_key = read_bytes(b)
        encryption_iv = read_bytes(b)
        file_hashes = read_vector(b, read_tl_object)
        return UploadFileCdnRedirect(
            dc_id=dc_id,
            file_token=file_token,
            encryption_key=encryption_key,
            encryption_iv=encryption_iv,
            file_hashes=file_hashes,
        )


class StorageFileUnknown(TLObject):
    ID = 0x40BC6F52
    QUALNAME = "types.storage.FileUnknown"

    @classmethod
    def read(cls, b: BinaryIO) -> StorageFileUnknown:
        return StorageFileUnknown()

    def write(self) -> bytes:
        return struct.pack("<I", self.ID)


class StorageFilePartial(StorageFileUnknown):
    ID = 0x40BC6F52
    QUALNAME = "types.storage.FilePartial"


class StorageFileJpeg(TLObject):
    ID = 0x007EFE0E
    QUALNAME = "types.storage.FileJpeg"

    @classmethod
    def read(cls, b: BinaryIO) -> StorageFileJpeg:
        return StorageFileJpeg()

    def write(self) -> bytes:
        return struct.pack("<I", self.ID)


class StorageFileGif(TLObject):
    ID = 0xCAE81513
    QUALNAME = "types.storage.FileGif"

    @classmethod
    def read(cls, b: BinaryIO) -> StorageFileGif:
        return StorageFileGif()

    def write(self) -> bytes:
        return struct.pack("<I", self.ID)


class StorageFilePng(TLObject):
    ID = 0x0A4F63C0
    QUALNAME = "types.storage.FilePng"

    @classmethod
    def read(cls, b: BinaryIO) -> StorageFilePng:
        return StorageFilePng()

    def write(self) -> bytes:
        return struct.pack("<I", self.ID)


class StorageFilePdf(TLObject):
    ID = 0xAE1E508D
    QUALNAME = "types.storage.FilePdf"

    @classmethod
    def read(cls, b: BinaryIO) -> StorageFilePdf:
        return StorageFilePdf()

    def write(self) -> bytes:
        return struct.pack("<I", self.ID)


class StorageFileMp3(TLObject):
    ID = 0x528A0699
    QUALNAME = "types.storage.FileMp3"

    @classmethod
    def read(cls, b: BinaryIO) -> StorageFileMp3:
        return StorageFileMp3()

    def write(self) -> bytes:
        return struct.pack("<I", self.ID)


class StorageFileMov(TLObject):
    ID = 0x4B09EBBC
    QUALNAME = "types.storage.FileMov"

    @classmethod
    def read(cls, b: BinaryIO) -> StorageFileMov:
        return StorageFileMov()

    def write(self) -> bytes:
        return struct.pack("<I", self.ID)


class StorageFileMp4(TLObject):
    ID = 0xB3CEA0E4
    QUALNAME = "types.storage.FileMp4"

    @classmethod
    def read(cls, b: BinaryIO) -> StorageFileMp4:
        return StorageFileMp4()

    def write(self) -> bytes:
        return struct.pack("<I", self.ID)


class StorageFileWebp(TLObject):
    ID = 0x1081464C
    QUALNAME = "types.storage.FileWebp"

    @classmethod
    def read(cls, b: BinaryIO) -> StorageFileWebp:
        return StorageFileWebp()

    def write(self) -> bytes:
        return struct.pack("<I", self.ID)


class DocumentAttribute(TLObject):
    ID = 0
    QUALNAME = "types.DocumentAttribute"


class DocumentAttributeFilename(DocumentAttribute):
    ID = 0x15590068
    QUALNAME = "types.DocumentAttributeFilename"

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

    def write(self) -> bytes:
        return struct.pack("<I", self.ID) + write_string(self.file_name)

    @classmethod
    def read(cls, b: BinaryIO) -> DocumentAttributeFilename:
        return DocumentAttributeFilename(file_name=read_string(b))


class DocumentAttributeVideo(DocumentAttribute):
    ID = 0x0EF02CED
    QUALNAME = "types.DocumentAttributeVideo"

    def __init__(
        self,
        duration: float = 0.0,
        w: int = 0,
        h: int = 0,
        supports_streaming: bool = True,
        round_message: bool = False,
    ) -> None:
        self.duration = duration
        self.w = w
        self.h = h
        self.supports_streaming = supports_streaming
        self.round_message = round_message

    def write(self) -> bytes:
        flags = 0
        if self.round_message:
            flags |= 1 << 0
        if self.supports_streaming:
            flags |= 1 << 1
        return (
            struct.pack("<II", self.ID, flags)
            + write_double(self.duration)
            + write_int(self.w)
            + write_int(self.h)
        )

    @classmethod
    def read(cls, b: BinaryIO) -> DocumentAttributeVideo:
        flags = read_uint(b)
        duration = read_double(b)
        w = read_int(b)
        h = read_int(b)
        return DocumentAttributeVideo(
            duration=duration,
            w=w,
            h=h,
            supports_streaming=bool(flags & (1 << 1)),
            round_message=bool(flags & (1 << 0)),
        )


class DocumentAttributeAudio(DocumentAttribute):
    ID = 0x9852F9C6
    QUALNAME = "types.DocumentAttributeAudio"

    def __init__(
        self,
        duration: int = 0,
        title: str | None = None,
        performer: str | None = None,
        voice: bool = False,
    ) -> None:
        self.duration = duration
        self.title = title
        self.performer = performer
        self.voice = voice

    def write(self) -> bytes:
        flags = 0
        if self.title is not None:
            flags |= 1 << 0
        if self.performer is not None:
            flags |= 1 << 1
        if self.voice:
            flags |= 1 << 10
        res = struct.pack("<II", self.ID, flags) + write_int(self.duration)
        if self.title is not None:
            res += write_string(self.title)
        if self.performer is not None:
            res += write_string(self.performer)
        return res

    @classmethod
    def read(cls, b: BinaryIO) -> DocumentAttributeAudio:
        flags = read_uint(b)
        duration = read_int(b)
        title = read_string(b) if bool(flags & 1) else None
        performer = read_string(b) if bool(flags & (1 << 1)) else None
        return DocumentAttributeAudio(
            duration=duration,
            title=title,
            performer=performer,
            voice=bool(flags & (1 << 10)),
        )


class InputMedia(TLObject):
    ID = 0
    QUALNAME = "types.InputMedia"


class InputMediaUploadedDocument(InputMedia):
    ID = 0x5B38C6C1
    QUALNAME = "types.InputMediaUploadedDocument"

    def __init__(
        self,
        file: TLObject,
        mime_type: str = "application/octet-stream",
        attributes: list[TLObject] | None = None,
        thumb: TLObject | None = None,
        stickers: list[TLObject] | None = None,
        ttl_seconds: int | None = None,
        nosound_video: bool = False,
        force_file: bool = False,
        spoiler: bool = False,
    ) -> None:
        self.file = file
        self.mime_type = mime_type
        self.attributes = attributes or []
        self.thumb = thumb
        self.stickers = stickers
        self.ttl_seconds = ttl_seconds
        self.nosound_video = nosound_video
        self.force_file = force_file
        self.spoiler = spoiler

    def write(self) -> bytes:
        flags = 0
        if self.stickers is not None:
            flags |= 1 << 0
        if self.ttl_seconds is not None:
            flags |= 1 << 1
        if self.thumb is not None:
            flags |= 1 << 2
        if self.nosound_video:
            flags |= 1 << 3
        if self.force_file:
            flags |= 1 << 4
        if self.spoiler:
            flags |= 1 << 5

        res = struct.pack("<II", self.ID, flags) + self.file.write()
        if self.thumb is not None:
            res += self.thumb.write()
        res += write_string(self.mime_type)
        res += write_vector(self.attributes, lambda a: a.write())
        if self.stickers is not None:
            res += write_vector(self.stickers, lambda s: s.write())
        if self.ttl_seconds is not None:
            res += write_int(self.ttl_seconds)
        return res

    @classmethod
    def read(cls, b: BinaryIO) -> InputMediaUploadedDocument:
        from aiogram.raw.all import read_tl_object

        flags = read_uint(b)
        file = read_tl_object(b)
        thumb = read_tl_object(b) if bool(flags & (1 << 2)) else None
        mime_type = read_string(b)
        attributes = read_vector(b, read_tl_object)
        stickers = read_vector(b, read_tl_object) if bool(flags & 1) else None
        ttl_seconds = read_int(b) if bool(flags & (1 << 1)) else None
        return InputMediaUploadedDocument(
            file=file,
            mime_type=mime_type,
            attributes=attributes,
            thumb=thumb,
            stickers=stickers,
            ttl_seconds=ttl_seconds,
            nosound_video=bool(flags & (1 << 3)),
            force_file=bool(flags & (1 << 4)),
            spoiler=bool(flags & (1 << 5)),
        )


class CodeSettings(TLObject):
    ID = 0xAD253D78
    QUALNAME = "types.CodeSettings"

    def __init__(
        self,
        allow_flashcall: bool = False,
        current_number: bool = False,
        allow_app_hash: bool = False,
        allow_missed_call: bool = False,
        allow_firebase: bool = False,
        unknown_number: bool = False,
        logout_tokens: list[bytes] | None = None,
        token: str | None = None,
        app_sandbox: bool | None = None,
    ) -> None:
        self.allow_flashcall = allow_flashcall
        self.current_number = current_number
        self.allow_app_hash = allow_app_hash
        self.allow_missed_call = allow_missed_call
        self.allow_firebase = allow_firebase
        self.unknown_number = unknown_number
        self.logout_tokens = logout_tokens
        self.token = token
        self.app_sandbox = app_sandbox

    def write(self) -> bytes:
        flags = 0
        if self.allow_flashcall:
            flags |= 1 << 0
        if self.current_number:
            flags |= 1 << 1
        if self.allow_app_hash:
            flags |= 1 << 4
        if self.allow_missed_call:
            flags |= 1 << 5
        if self.allow_firebase:
            flags |= 1 << 7
        if self.unknown_number:
            flags |= 1 << 9
        if self.logout_tokens is not None:
            flags |= 1 << 6
        if self.token is not None:
            flags |= 1 << 8
        if self.app_sandbox is not None:
            flags |= 1 << 8

        res = struct.pack("<II", self.ID, flags)
        if self.logout_tokens is not None:
            res += write_vector(self.logout_tokens, write_bytes)
        if self.token is not None:
            res += write_string(self.token)
        if self.app_sandbox is not None:
            res += write_bool(self.app_sandbox)
        return res

    @classmethod
    def read(cls, b: BinaryIO) -> CodeSettings:
        flags = read_uint(b)
        allow_flashcall = bool(flags & (1 << 0))
        current_number = bool(flags & (1 << 1))
        allow_app_hash = bool(flags & (1 << 4))
        allow_missed_call = bool(flags & (1 << 5))
        allow_firebase = bool(flags & (1 << 7))
        unknown_number = bool(flags & (1 << 9))
        logout_tokens = read_vector(b, read_bytes) if (flags & (1 << 6)) else None
        token = read_string(b) if (flags & (1 << 8)) else None
        app_sandbox = read_bool(b) if (flags & (1 << 8)) else None
        return CodeSettings(
            allow_flashcall=allow_flashcall,
            current_number=current_number,
            allow_app_hash=allow_app_hash,
            allow_missed_call=allow_missed_call,
            allow_firebase=allow_firebase,
            unknown_number=unknown_number,
            logout_tokens=logout_tokens,
            token=token,
            app_sandbox=app_sandbox,
        )


class PasswordKdfAlgo(TLObject):
    ID = 0
    QUALNAME = "types.PasswordKdfAlgo"


class PasswordKdfAlgoUnknown(PasswordKdfAlgo):
    ID = 0xD45AB096
    QUALNAME = "types.PasswordKdfAlgoUnknown"

    @classmethod
    def read(cls, b: BinaryIO) -> PasswordKdfAlgoUnknown:
        return PasswordKdfAlgoUnknown()


class PasswordKdfAlgoSHA256SHA256PBKDF2HMACSHA512(PasswordKdfAlgo):
    ID = 0x3A912D4A
    QUALNAME = "types.PasswordKdfAlgoSHA256SHA256PBKDF2HMACSHA512"

    def __init__(self, salt1: bytes, salt2: bytes, g: int, p: bytes) -> None:
        self.salt1 = salt1
        self.salt2 = salt2
        self.g = g
        self.p = p

    def write(self) -> bytes:
        return (
            struct.pack("<I", self.ID)
            + write_bytes(self.salt1)
            + write_bytes(self.salt2)
            + write_int(self.g)
            + write_bytes(self.p)
        )

    @classmethod
    def read(cls, b: BinaryIO) -> PasswordKdfAlgoSHA256SHA256PBKDF2HMACSHA512:
        return PasswordKdfAlgoSHA256SHA256PBKDF2HMACSHA512(
            salt1=read_bytes(b),
            salt2=read_bytes(b),
            g=read_int(b),
            p=read_bytes(b),
        )


class SecurePasswordKdfAlgo(TLObject):
    ID = 0
    QUALNAME = "types.SecurePasswordKdfAlgo"


class SecurePasswordKdfAlgoUnknown(SecurePasswordKdfAlgo):
    ID = 0x004A8537
    QUALNAME = "types.SecurePasswordKdfAlgoUnknown"

    @classmethod
    def read(cls, b: BinaryIO) -> SecurePasswordKdfAlgoUnknown:
        return SecurePasswordKdfAlgoUnknown()


class SecurePasswordKdfAlgoPBKDF2HMACSHA512(SecurePasswordKdfAlgo):
    ID = 0xBBF2DDA0
    QUALNAME = "types.SecurePasswordKdfAlgoPBKDF2HMACSHA512"

    def __init__(self, salt: bytes) -> None:
        self.salt = salt

    def write(self) -> bytes:
        return struct.pack("<I", self.ID) + write_bytes(self.salt)

    @classmethod
    def read(cls, b: BinaryIO) -> SecurePasswordKdfAlgoPBKDF2HMACSHA512:
        return SecurePasswordKdfAlgoPBKDF2HMACSHA512(salt=read_bytes(b))


class SecurePasswordKdfAlgoSHA512(SecurePasswordKdfAlgo):
    ID = 0x86471D92
    QUALNAME = "types.SecurePasswordKdfAlgoSHA512"

    def __init__(self, salt: bytes) -> None:
        self.salt = salt

    def write(self) -> bytes:
        return struct.pack("<I", self.ID) + write_bytes(self.salt)

    @classmethod
    def read(cls, b: BinaryIO) -> SecurePasswordKdfAlgoSHA512:
        return SecurePasswordKdfAlgoSHA512(salt=read_bytes(b))


class AccountPassword(TLObject):
    ID = 0x95D4E410
    QUALNAME = "account.Password"

    def __init__(
        self,
        has_recovery: bool = False,
        has_secure_values: bool = False,
        has_password: bool = False,
        current_algo: PasswordKdfAlgo | None = None,
        srp_B: bytes | None = None,
        srp_id: int | None = None,
        hint: str | None = None,
        email_unconfirmed_pattern: str | None = None,
        new_algo: PasswordKdfAlgo | None = None,
        new_secure_algo: TLObject | None = None,
        secure_random: bytes | None = None,
        pending_reset_date: int | None = None,
        login_email_pattern: str | None = None,
    ) -> None:
        self.has_recovery = has_recovery
        self.has_secure_values = has_secure_values
        self.has_password = has_password
        self.current_algo = current_algo
        self.srp_B = srp_B
        self.srp_id = srp_id
        self.hint = hint
        self.email_unconfirmed_pattern = email_unconfirmed_pattern
        self.new_algo = new_algo
        self.new_secure_algo = new_secure_algo
        self.secure_random = secure_random
        self.pending_reset_date = pending_reset_date
        self.login_email_pattern = login_email_pattern

    @classmethod
    def read(cls, b: BinaryIO) -> AccountPassword:
        from aiogram.raw.all import read_tl_object

        flags = read_uint(b)
        has_recovery = bool(flags & (1 << 0))
        has_secure_values = bool(flags & (1 << 1))
        has_password = bool(flags & (1 << 2))
        current_algo = read_tl_object(b) if has_password else None
        srp_B = read_bytes(b) if has_password else None
        srp_id = read_long(b) if has_password else None
        hint = read_string(b) if (flags & (1 << 3)) else None
        email_unconfirmed_pattern = read_string(b) if (flags & (1 << 4)) else None
        new_algo = read_tl_object(b)
        new_secure_algo = read_tl_object(b)
        secure_random = read_bytes(b)
        pending_reset_date = read_int(b) if (flags & (1 << 5)) else None
        login_email_pattern = read_string(b) if (flags & (1 << 6)) else None
        return AccountPassword(
            has_recovery=has_recovery,
            has_secure_values=has_secure_values,
            has_password=has_password,
            current_algo=current_algo,
            srp_B=srp_B,
            srp_id=srp_id,
            hint=hint,
            email_unconfirmed_pattern=email_unconfirmed_pattern,
            new_algo=new_algo,
            new_secure_algo=new_secure_algo,
            secure_random=secure_random,
            pending_reset_date=pending_reset_date,
            login_email_pattern=login_email_pattern,
        )


class InputCheckPasswordSRP(TLObject):
    ID = 0xD27FF082
    QUALNAME = "types.InputCheckPasswordSRP"

    def __init__(self, srp_id: int, A: bytes, M1: bytes) -> None:
        self.srp_id = srp_id
        self.A = A
        self.M1 = M1

    def write(self) -> bytes:
        return (
            struct.pack("<I", self.ID)
            + write_long(self.srp_id)
            + write_bytes(self.A)
            + write_bytes(self.M1)
        )

    @classmethod
    def read(cls, b: BinaryIO) -> InputCheckPasswordSRP:
        return InputCheckPasswordSRP(srp_id=read_long(b), A=read_bytes(b), M1=read_bytes(b))


class InputCheckPasswordEmpty(TLObject):
    ID = 0x9880F658
    QUALNAME = "types.InputCheckPasswordEmpty"

    def write(self) -> bytes:
        return struct.pack("<I", self.ID)

    @classmethod
    def read(cls, b: BinaryIO) -> InputCheckPasswordEmpty:
        return InputCheckPasswordEmpty()


class ContactsResolvedPeer(TLObject):
    ID = 0x7F077AD9
    QUALNAME = "contacts.ResolvedPeer"

    def __init__(self, peer: Peer, chats: list[TLObject], users: list[User]) -> None:
        self.peer = peer
        self.chats = chats
        self.users = users

    def write(self) -> bytes:
        return (
            struct.pack("<I", self.ID)
            + self.peer.write()
            + write_vector(self.chats, lambda c: c.write())
            + write_vector(self.users, lambda u: u.write())
        )

    @classmethod
    def read(cls, b: BinaryIO) -> ContactsResolvedPeer:
        from aiogram.raw.all import read_tl_object

        peer = read_tl_object(b)
        chats = read_vector(b, read_tl_object)
        users = read_vector(b, read_tl_object)
        return ContactsResolvedPeer(peer=peer, chats=chats, users=users)
