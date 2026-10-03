from unittest.mock import AsyncMock, MagicMock

import pytest

from aiogram.client.mtproto import MTProtoClient
from aiogram.client.peer_resolver import PeerResolver
from aiogram.raw import types as raw_types


@pytest.mark.asyncio
async def test_peer_resolver_me_and_numeric():
    mock_client = MagicMock(spec=MTProtoClient)
    mock_client.me = MagicMock(id=123456)
    mock_client.session_data = MagicMock(user_id=123456)

    resolver = PeerResolver(mock_client)

    # "me" / "self"
    me_peer = await resolver.resolve_peer("me")
    assert isinstance(me_peer, raw_types.InputPeerSelf)

    self_peer = await resolver.resolve_peer("self")
    assert isinstance(self_peer, raw_types.InputPeerSelf)

    # numeric user id
    mock_client.me.id = 999999
    mock_client.session_data.user_id = 999999
    user_peer = await resolver.resolve_peer(123456)
    assert isinstance(user_peer, raw_types.InputPeerUser)
    assert user_peer.user_id == 123456

    # channel id (-100...)
    channel_peer = await resolver.resolve_peer(-1001234567890)
    assert isinstance(channel_peer, raw_types.InputPeerChannel)
    assert channel_peer.channel_id == 1234567890

    # chat id (negative)
    chat_peer = await resolver.resolve_peer(-98765)
    assert isinstance(chat_peer, raw_types.InputPeerChat)
    assert chat_peer.chat_id == 98765


@pytest.mark.asyncio
async def test_peer_resolver_cache():
    mock_client = MagicMock(spec=MTProtoClient)
    resolver = PeerResolver(mock_client)

    user = raw_types.User(id=777, access_hash=888, username="testuser")
    resolver.cache_user(user)

    resolved = await resolver.resolve_peer("@testuser")
    assert isinstance(resolved, raw_types.InputPeerUser)
    assert resolved.user_id == 777
    assert resolved.access_hash == 888
