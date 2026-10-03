from aiogram.methods import (
    EditEphemeralMessageCaption,
    EditEphemeralMessageText,
    PromoteChatMember,
    SendMessage,
    SendMessageDraft,
    SendRichMessageDraft,
)
from aiogram.types import (
    EphemeralMessageParameters,
    InputRichBlockParagraph,
    InputRichMessage,
)


def test_send_message_draft_can_stop():
    draft = SendMessageDraft(
        chat_id=123,
        draft_id=456,
        text="Generating...",
        can_stop=True,
        keep_on_stop=False,
    )
    dump = draft.model_dump(exclude_none=True)
    assert dump["can_stop"] is True
    assert dump["keep_on_stop"] is False


def test_send_rich_message_draft_can_stop():
    rich_msg = InputRichMessage(blocks=[InputRichBlockParagraph(text="Draft content")])
    draft = SendRichMessageDraft(
        chat_id=123,
        draft_id=456,
        rich_message=rich_msg,
        can_stop=True,
        keep_on_stop=True,
    )
    dump = draft.model_dump(exclude_none=True)
    assert dump["can_stop"] is True
    assert dump["keep_on_stop"] is True


def test_edit_ephemeral_message_text_rich():
    rich_msg = InputRichMessage(blocks=[InputRichBlockParagraph(text="Edited rich content")])
    edit = EditEphemeralMessageText(
        chat_id=123,
        receiver_user_id=456,
        ephemeral_message_id=789,
        rich_message=rich_msg,
    )
    dump = edit.model_dump(exclude_none=True)
    assert "rich_message" in dump
    assert dump["ephemeral_message_id"] == 789


def test_edit_ephemeral_message_caption_show_above():
    edit = EditEphemeralMessageCaption(
        chat_id=123,
        receiver_user_id=456,
        ephemeral_message_id=789,
        caption="New caption",
        show_caption_above_media=True,
    )
    dump = edit.model_dump(exclude_none=True)
    assert dump["show_caption_above_media"] is True


def test_promote_chat_member_welcome_messages():
    promote = PromoteChatMember(
        chat_id=123,
        user_id=456,
        can_send_welcome_messages=True,
    )
    dump = promote.model_dump(exclude_none=True)
    assert dump["can_send_welcome_messages"] is True


def test_send_message_ephemeral_parameters():
    params = EphemeralMessageParameters(
        receiver_user_id=456,
        callback_query_id="query_123",
        replace_callback_query_message=True,
    )
    send = SendMessage(
        chat_id=123,
        text="Ephemeral response",
        ephemeral_message_parameters=params,
    )
    dump = send.model_dump(exclude_none=True)
    assert dump["ephemeral_message_parameters"] == {
        "receiver_user_id": 456,
        "callback_query_id": "query_123",
        "replace_callback_query_message": True,
    }
