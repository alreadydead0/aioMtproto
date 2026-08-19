"""
Central TL constructor registry and polymorphic reader.
"""

from __future__ import annotations

import io
import struct
from typing import Any, BinaryIO

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
    ExportedAuthorization,
    ExportedAuthorizationLegacy,
    DocumentAttributeAudio,
    DocumentAttributeFilename,
    DocumentAttributeVideo,
    InputDocumentFileLocation,
    InputFile,
    InputFileBig,
    InputMediaUploadedDocument,
    InputPeerChannel,
    InputPeerChat,
    InputPeerEmpty,
    InputPeerPhotoFileLocation,
    InputPeerSelf,
    InputPeerUser,
    InputPhotoFileLocation,
    Message,
    NearestDc,
    PeerChannel,
    PeerChat,
    PeerUser,
    SentCode,
    StorageFileGif,
    StorageFileJpeg,
    StorageFileMov,
    StorageFileMp3,
    StorageFileMp4,
    StorageFilePdf,
    StorageFilePng,
    StorageFileUnknown,
    StorageFileWebp,
    UpdateNewMessage,
    Updates,
    UpdatesCombined,
    UpdatesTooLong,
    UpdateShort,
    UpdateShortChatMessage,
    UpdateShortMessage,
    UploadFile,
    UploadFileCdnRedirect,
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
    InputDocumentFileLocation.ID: InputDocumentFileLocation,
    InputPhotoFileLocation.ID: InputPhotoFileLocation,
    InputPeerPhotoFileLocation.ID: InputPeerPhotoFileLocation,
    InputMediaUploadedDocument.ID: InputMediaUploadedDocument,
    DocumentAttributeFilename.ID: DocumentAttributeFilename,
    DocumentAttributeVideo.ID: DocumentAttributeVideo,
    DocumentAttributeAudio.ID: DocumentAttributeAudio,
    UploadFile.ID: UploadFile,
    UploadFileCdnRedirect.ID: UploadFileCdnRedirect,
    StorageFileUnknown.ID: StorageFileUnknown,
    StorageFileJpeg.ID: StorageFileJpeg,
    StorageFileGif.ID: StorageFileGif,
    StorageFilePng.ID: StorageFilePng,
    StorageFilePdf.ID: StorageFilePdf,
    StorageFileMp3.ID: StorageFileMp3,
    StorageFileMov.ID: StorageFileMov,
    StorageFileMp4.ID: StorageFileMp4,
    StorageFileWebp.ID: StorageFileWebp,
    User.ID: User,
    Message.ID: Message,
    UpdateShort.ID: UpdateShort,
    UpdateShortMessage.ID: UpdateShortMessage,
    UpdateShortChatMessage.ID: UpdateShortChatMessage,
    UpdateNewMessage.ID: UpdateNewMessage,
    Updates.ID: Updates,
    UpdatesCombined.ID: UpdatesCombined,
    UpdatesTooLong.ID: UpdatesTooLong,
    NearestDc.ID: NearestDc,
    SentCode.ID: SentCode,
    Authorization.ID: Authorization,
    ExportedAuthorization.ID: ExportedAuthorization,
    ExportedAuthorizationLegacy.ID: ExportedAuthorizationLegacy,
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
