from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from ..enums import RichTextType
from .rich_text import RichText

if TYPE_CHECKING:
    from .rich_message_button import RichMessageButton
    from .rich_text_union import RichTextUnion


class RichTextButton(RichText):
    """
    A rich text button.

    Source: https://core.telegram.org/bots/api#richtextbutton
    """

    type: Literal[RichTextType.BUTTON] = RichTextType.BUTTON
    """Type of the rich text, always 'button'"""
    button: RichMessageButton
    """The button"""
    text: RichTextUnion | None = None
    """*Optional*. Text of the button"""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via `butcher`

        def __init__(
            __pydantic__self__,
            *,
            type: Literal[RichTextType.BUTTON] = RichTextType.BUTTON,
            button: RichMessageButton,
            text: RichTextUnion | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via `butcher`
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(type=type, button=button, text=text, **__pydantic_kwargs)
