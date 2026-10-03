from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import TelegramObject


class RichMessageButton(TelegramObject):
    """
    Describes a button in a rich formatted message.

    Source: https://core.telegram.org/bots/api#richmessagebutton
    """

    text: str
    """Label text on the button"""
    url: str | None = None
    """*Optional*. HTTP or tg:// URL to be opened when the button is pressed"""
    callback_data: str | None = None
    """*Optional*. Data to be sent in a callback query to the bot when the button is pressed, 1-64 bytes"""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via `butcher`

        def __init__(
            __pydantic__self__,
            *,
            text: str,
            url: str | None = None,
            callback_data: str | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via `butcher`
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(
                text=text,
                url=url,
                callback_data=callback_data,
                **__pydantic_kwargs,
            )
