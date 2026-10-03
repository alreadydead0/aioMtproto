from aiogram.dispatcher.flags import FlagGenerator

from . import enums, errors, methods, mtproto, raw, types
from .__meta__ import __api_version__, __version__
from .client import session
from .client.bot import Bot
from .client.mtproto import MTProtoClient
from .client.user import UserClient
from .dispatcher.dispatcher import Dispatcher
from .dispatcher.middlewares.base import BaseMiddleware
from .dispatcher.router import Router
from .dispatcher.userbot.filters import Filter, filters
from .session.string import StringSession
from .utils.magic_filter import MagicFilter
from .utils.text_decorations import html_decoration as html
from .utils.text_decorations import markdown_decoration as md

F = MagicFilter()
flags = FlagGenerator()

__all__ = (
    "BaseMiddleware",
    "Bot",
    "Dispatcher",
    "F",
    "Filter",
    "MTProtoClient",
    "Router",
    "StringSession",
    "UserClient",
    "__api_version__",
    "__version__",
    "enums",
    "errors",
    "filters",
    "flags",
    "html",
    "md",
    "methods",
    "mtproto",
    "raw",
    "session",
    "types",
)
