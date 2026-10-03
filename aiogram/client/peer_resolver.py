"""
Telegram MTProto Peer Resolver with caching and username RPC resolution.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from aiogram.raw import functions as raw_funcs
from aiogram.raw import types as raw_types

if TYPE_CHECKING:
    from aiogram.client.mtproto import MTProtoClient

logger = logging.getLogger("aiogram.client.peer_resolver")


class PeerResolver:
    """
    Resolves usernames, user/chat/channel IDs, and peer aliases into Telegram InputPeer objects.
    Maintains an in-memory cache of (peer_id, access_hash, peer_type) mappings.
    """

    def __init__(self, client: MTProtoClient) -> None:
        self.client = client
        # username (lowercase, no @) -> (peer_id, access_hash, peer_type)
        self._username_cache: dict[str, tuple[int, int, str]] = {}
        # peer_id -> (access_hash, peer_type)
        self._id_cache: dict[int, tuple[int, str]] = {}

    def cache_user(self, user: raw_types.User) -> None:
        """Cache user ID, access_hash, and username."""
        if not user or getattr(user, "id", None) is None:
            return
        access_hash = getattr(user, "access_hash", 0) or 0
        self._id_cache[user.id] = (access_hash, "user")
        uname = getattr(user, "username", None)
        if uname:
            self._username_cache[uname.lower()] = (user.id, access_hash, "user")

    def cache_peer(
        self, peer_id: int, access_hash: int, peer_type: str, username: str | None = None
    ) -> None:
        """Cache generic peer metadata."""
        self._id_cache[peer_id] = (access_hash, peer_type)
        if username:
            self._username_cache[username.lower()] = (peer_id, access_hash, peer_type)

    async def resolve_peer(self, peer: Any) -> raw_types.InputPeer:
        """
        Resolve peer identifier into raw InputPeer.
        Supports "me", "self", "@username", "username", integer IDs, InputPeer, and Peer instances.
        """
        if isinstance(peer, raw_types.InputPeer):
            return peer

        if isinstance(peer, raw_types.PeerUser):
            return await self.resolve_peer(peer.user_id)
        if isinstance(peer, raw_types.PeerChat):
            return raw_types.InputPeerChat(chat_id=peer.chat_id)
        if isinstance(peer, raw_types.PeerChannel):
            return await self.resolve_peer(int(f"-100{peer.channel_id}"))

        if isinstance(peer, str):
            s = peer.strip()
            if s.lower() in ("me", "self"):
                return raw_types.InputPeerSelf()

            # Numeric string
            if s.lstrip("-").isdigit():
                return await self.resolve_peer(int(s))

            username = s.lstrip("@").lower()
            if username in self._username_cache:
                peer_id, access_hash, peer_type = self._username_cache[username]
                if peer_type == "user":
                    return raw_types.InputPeerUser(user_id=peer_id, access_hash=access_hash)
                if peer_type == "channel":
                    return raw_types.InputPeerChannel(channel_id=peer_id, access_hash=access_hash)
                if peer_type == "chat":
                    return raw_types.InputPeerChat(chat_id=peer_id)

            # Resolve via RPC
            try:
                res = await self.client.invoke(
                    raw_funcs.contacts.ResolveUsername(username=username)
                )
                if getattr(res, "users", None):
                    for u in res.users:
                        self.cache_user(u)
                if getattr(res, "chats", None):
                    for c in res.chats:
                        c_id = getattr(c, "id", None)
                        c_access_hash = getattr(c, "access_hash", 0) or 0
                        if c_id:
                            self.cache_peer(
                                c_id, c_access_hash, "channel", getattr(c, "username", None)
                            )

                resolved = res.peer
                if isinstance(resolved, raw_types.PeerUser):
                    cached = self._id_cache.get(resolved.user_id, (0, "user"))
                    return raw_types.InputPeerUser(user_id=resolved.user_id, access_hash=cached[0])
                if isinstance(resolved, raw_types.PeerChannel):
                    cached = self._id_cache.get(resolved.channel_id, (0, "channel"))
                    return raw_types.InputPeerChannel(
                        channel_id=resolved.channel_id, access_hash=cached[0]
                    )
                if isinstance(resolved, raw_types.PeerChat):
                    return raw_types.InputPeerChat(chat_id=resolved.chat_id)
            except Exception as e:
                logger.debug("Failed to resolve username '%s' via MTProto RPC: %s", username, e)
                raise ValueError(f"Could not resolve username '@{username}': {e}") from e

        if isinstance(peer, int):
            # Check if self
            me_id = getattr(self.client.me, "id", None)
            session_uid = getattr(self.client.session_data, "user_id", None)
            if peer in (me_id, session_uid):
                return raw_types.InputPeerSelf()

            if peer > 0:
                access_hash, _ = self._id_cache.get(peer, (0, "user"))
                return raw_types.InputPeerUser(user_id=peer, access_hash=access_hash)

            peer_str = str(peer)
            if peer_str.startswith("-100"):
                channel_id = int(peer_str[4:])
                access_hash, _ = self._id_cache.get(channel_id, (0, "channel"))
                return raw_types.InputPeerChannel(channel_id=channel_id, access_hash=access_hash)

            return raw_types.InputPeerChat(chat_id=-peer)

        return raw_types.InputPeerSelf()
