"""
Central TL constructor registry and polymorphic reader.
"""

from __future__ import annotations

import io
import struct
from typing import Any, BinaryIO, Dict, Type

from aiogram.raw.core.primitives import TLObject, read_uint
from aiogram.raw.core.tl_core_types import (
    BadMsgNotification,
    BadServerSalt,
    DhGenOk,
    GzipPacked,
    MsgsAck,
    ResPQ,
    RpcError,
    RpcResult,
    ServerDHParamsOk,
)
from aiogram.raw.types import (
    Authorization,
    InputFile,
    InputFileBig,
    InputPeerChannel,
    InputPeerChat,
    InputPeerEmpty,
    InputPeerSelf,
    InputPeerUser,
    Message,
    NearestDc,
    PeerChannel,
    PeerChat,
    PeerUser,
    SentCode,
    UpdateNewMessage,
    Updates,
    UpdatesCombined,
    UpdateShort,
    UpdateShortChatMessage,
    UpdateShortMessage,
    User,
)

TL_REGISTRY: dict[int, type[TLObject]] = {
    GzipPacked.ID: GzipPacked,
    RpcResult.ID: RpcResult,
    RpcError.ID: RpcError,
    MsgsAck.ID: MsgsAck,
    BadServerSalt.ID: BadServerSalt,
    BadMsgNotification.ID: BadMsgNotification,
    ResPQ.ID: ResPQ,
    ServerDHParamsOk.ID: ServerDHParamsOk,
    DhGenOk.ID: DhGenOk,
    PeerUser.ID: PeerUser,
    PeerChat.ID: PeerChat,
    PeerChannel.ID: PeerChannel,
    InputPeerEmpty.ID: InputPeerEmpty,
    InputPeerSelf.ID: InputPeerSelf,
    InputPeerUser.ID: InputPeerUser,
    InputPeerChat.ID: InputPeerChat,
    InputPeerChannel.ID: InputPeerChannel,
    InputFile.ID: InputFile,
    InputFileBig.ID: InputFileBig,
    User.ID: User,
    Message.ID: Message,
    UpdateShort.ID: UpdateShort,
    UpdateShortMessage.ID: UpdateShortMessage,
    UpdateShortChatMessage.ID: UpdateShortChatMessage,
    UpdateNewMessage.ID: UpdateNewMessage,
    Updates.ID: Updates,
    UpdatesCombined.ID: UpdatesCombined,
    NearestDc.ID: NearestDc,
    SentCode.ID: SentCode,
    Authorization.ID: Authorization,
}


def read_tl_object(b: BinaryIO) -> Any:
    """
    Read constructor ID and instantiate corresponding TL object.
    Handles GzipPacked automatically.
    """
    c_id_bytes = b.read(4)
    if not c_id_bytes or len(c_id_bytes) < 4:
        return None
    c_id = struct.unpack("<I", c_id_bytes)[0]

    if c_id == GzipPacked.ID:
        decompressed = GzipPacked.read(b)
        return read_tl_object(io.BytesIO(decompressed))

    cls = TL_REGISTRY.get(c_id)
    if cls is not None:
        return cls.read(b)

    msg = f"Unknown TL constructor ID: {c_id:#010x}"
    raise ValueError(msg)
