from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from ..enums import InputRichBlockType
from .input_rich_block import InputRichBlock

if TYPE_CHECKING:
    from .input_rich_block_union import InputRichBlockUnion
    from .rich_text_union import RichTextUnion


class InputRichBlockExpandableBlockQuotation(InputRichBlock):
    """
    An expandable block quotation to be sent.

    Source: https://core.telegram.org/bots/api#inputrichblockexpandableblockquotation
    """

    type: Literal[InputRichBlockType.EXPANDABLE_BLOCKQUOTE] = (
        InputRichBlockType.EXPANDABLE_BLOCKQUOTE
    )
    """Type of the block, always 'expandable_blockquote'"""
    blocks: list[InputRichBlockUnion]
    """Content of the block"""
    credit: RichTextUnion | None = None
    """*Optional*. Credit of the block"""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via `butcher`

        def __init__(
            __pydantic__self__,
            *,
            type: Literal[InputRichBlockType.EXPANDABLE_BLOCKQUOTE] = (
                InputRichBlockType.EXPANDABLE_BLOCKQUOTE
            ),
            blocks: list[InputRichBlockUnion],
            credit: RichTextUnion | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via `butcher`
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(type=type, blocks=blocks, credit=credit, **__pydantic_kwargs)
