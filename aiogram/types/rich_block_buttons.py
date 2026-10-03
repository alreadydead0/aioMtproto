from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from ..enums import RichBlockType
from .rich_block import RichBlock

if TYPE_CHECKING:
    from .rich_message_button import RichMessageButton


class RichBlockButtons(RichBlock):
    """
    A block containing buttons.

    Source: https://core.telegram.org/bots/api#richblockbuttons
    """

    type: Literal[RichBlockType.BUTTONS] = RichBlockType.BUTTONS
    """Type of the block, always 'buttons'"""
    buttons: list[RichMessageButton]
    """Buttons in the block"""
    align: str | None = None
    """*Optional*. Alignment of the buttons; one of 'left', 'center', or 'right'"""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via `butcher`

        def __init__(
            __pydantic__self__,
            *,
            type: Literal[RichBlockType.BUTTONS] = RichBlockType.BUTTONS,
            buttons: list[RichMessageButton],
            align: str | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via `butcher`
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(type=type, buttons=buttons, align=align, **__pydantic_kwargs)
