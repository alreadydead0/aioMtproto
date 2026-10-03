from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import TelegramObject


class EphemeralMessageParameters(TelegramObject):
    """
    Describes parameters of an ephemeral message.

    Source: https://core.telegram.org/bots/api#ephemeralmessageparameters
    """

    receiver_user_id: int | None = None
    """*Optional*. Unique identifier of the user who will receive the message; for group and supergroup chats only. It is not guaranteed that the user will receive the message, especially if they are offline"""
    callback_query_id: str | None = None
    """*Optional*. Identifier of the callback query which triggered the message if any"""
    replace_callback_query_message: bool | None = None
    """*Optional*. Pass :code:`True` to replace the message to which the callback query was attached with the ephemeral message"""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via `butcher`

        def __init__(
            __pydantic__self__,
            *,
            receiver_user_id: int | None = None,
            callback_query_id: str | None = None,
            replace_callback_query_message: bool | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via `butcher`
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(
                receiver_user_id=receiver_user_id,
                callback_query_id=callback_query_id,
                replace_callback_query_message=replace_callback_query_message,
                **__pydantic_kwargs,
            )
