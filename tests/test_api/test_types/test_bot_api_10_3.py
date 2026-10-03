from aiogram.enums import (
    ButtonStyle,
    ContentType,
    InputRichBlockType,
    RichBlockType,
    RichTextType,
    UpdateType,
)
from aiogram.types import (
    CallbackQuery,
    Chat,
    ChatAdministratorRights,
    Community,
    CommunityChatJoined,
    DisabledButton,
    EphemeralMessageParameters,
    InlineKeyboardButton,
    InputMediaDocument,
    InputRichBlockButtons,
    InputRichBlockDocument,
    InputRichBlockExpandableBlockQuotation,
    InputRichBlockParagraph,
    InputRichBlockTable,
    Message,
    MessageGenerationStopped,
    RichBlockButtons,
    RichBlockDocument,
    RichBlockExpandableBlockQuotation,
    RichBlockParagraph,
    RichBlockTable,
    RichMessageButton,
    RichTextButton,
    UniqueGift,
    UniqueGiftInfo,
    Update,
    User,
)


def test_bot_api_10_3_enums():
    assert ButtonStyle.LINK == "link"
    assert RichBlockType.EXPANDABLE_BLOCKQUOTE == "expandable_blockquote"
    assert RichBlockType.DOCUMENT == "document"
    assert RichBlockType.BUTTONS == "buttons"
    assert InputRichBlockType.EXPANDABLE_BLOCKQUOTE == "expandable_blockquote"
    assert InputRichBlockType.DOCUMENT == "document"
    assert InputRichBlockType.BUTTONS == "buttons"
    assert RichTextType.BUTTON == "button"
    assert UpdateType.STOPPED_MESSAGE_GENERATION == "stopped_message_generation"
    assert ContentType.COMMUNITY_CHAT_JOINED == "community_chat_joined"


def test_disabled_button():
    btn = DisabledButton(is_disabled=True, reason="Cooldown active")
    assert btn.is_disabled is True
    assert btn.reason == "Cooldown active"
    dump = btn.model_dump(exclude_none=True)
    assert dump == {"is_disabled": True, "reason": "Cooldown active"}


def test_ephemeral_message_parameters():
    params = EphemeralMessageParameters(
        receiver_user_id=12345,
        callback_query_id="query_abc",
        replace_callback_query_message=True,
    )
    assert params.receiver_user_id == 12345
    assert params.callback_query_id == "query_abc"
    assert params.replace_callback_query_message is True


def test_message_and_callback_query_as_ephemeral_parameters():
    user = User(id=999, is_bot=False, first_name="Tester")
    chat = Chat(id=-100123, type="supergroup", title="Test Supergroup")
    msg = Message(message_id=1, date=1234567890, chat=chat, from_user=user)

    cb = CallbackQuery(id="cb_123", from_user=user, chat_instance="instance_1", message=msg)
    cb_params = cb.as_ephemeral_message_parameters(replace_callback_query_message=True)
    assert cb_params.receiver_user_id == 999
    assert cb_params.callback_query_id == "cb_123"
    assert cb_params.replace_callback_query_message is True

    msg_params = msg.as_ephemeral_message_parameters()
    assert msg_params.receiver_user_id == 999
    assert msg_params.callback_query_id is None


def test_update_stopped_message_generation():
    chat = Chat(id=123, type="private")
    stopped = MessageGenerationStopped(chat=chat, draft_id=42)
    update = Update(update_id=1, stopped_message_generation=stopped)
    assert update.event_type == "stopped_message_generation"
    assert update.event == stopped


def test_community_chat_joined():
    community = Community(id=1, name="My Community")
    event = CommunityChatJoined(community=community)
    assert event.community.id == 1
    assert event.community.name == "My Community"


def test_rich_block_buttons_and_document():
    rm_btn = RichMessageButton(text="Click me", url="https://example.com", style="link")
    block_btns = RichBlockButtons(buttons=[rm_btn])
    assert block_btns.type == "buttons"
    assert len(block_btns.buttons) == 1
    assert block_btns.buttons[0].text == "Click me"

    input_btns = InputRichBlockButtons(buttons=[rm_btn])
    assert input_btns.type == "buttons"

    doc_block = RichBlockDocument(document={"file_id": "doc123", "file_unique_id": "u123"})
    assert doc_block.type == "document"

    input_doc = InputRichBlockDocument(document=InputMediaDocument(media="doc123"))
    assert input_doc.type == "document"


def test_rich_block_expandable_blockquote():
    para = RichBlockParagraph(text="Quote text")
    expandable = RichBlockExpandableBlockQuotation(blocks=[para])
    assert expandable.type == "expandable_blockquote"

    input_para = InputRichBlockParagraph(text="Input quote")
    input_expandable = InputRichBlockExpandableBlockQuotation(blocks=[input_para])
    assert input_expandable.type == "expandable_blockquote"


def test_rich_text_button():
    rm_btn = RichMessageButton(text="Pay", action="payment_action")
    rt_btn = RichTextButton(button=rm_btn)
    assert rt_btn.type == "button"
    assert rt_btn.button.text == "Pay"
    assert rt_btn.button.action == "payment_action"


def test_table_is_compact():
    table = RichBlockTable(cells=[], is_compact=True)
    assert table.is_compact is True

    input_table = InputRichBlockTable(cells=[], is_compact=True)
    assert input_table.is_compact is True


def test_inline_keyboard_button_disabled():
    btn = InlineKeyboardButton(
        text="Disabled Btn",
        callback_data="cb",
        disabled=DisabledButton(is_disabled=True, reason="Under maintenance"),
    )
    assert btn.disabled is not None
    assert btn.disabled.is_disabled is True
    assert btn.disabled.reason == "Under maintenance"


def test_chat_administrator_rights_welcome_messages():
    rights = ChatAdministratorRights(
        is_anonymous=False,
        can_manage_chat=True,
        can_delete_messages=True,
        can_manage_video_chats=True,
        can_restrict_members=True,
        can_promote_members=False,
        can_change_info=True,
        can_invite_users=True,
        can_post_stories=False,
        can_edit_stories=False,
        can_delete_stories=False,
        can_send_welcome_messages=True,
    )
    assert rights.can_send_welcome_messages is True
    dump = rights.model_dump(exclude_none=True)
    assert dump["can_send_welcome_messages"] is True


def test_unique_gift_info():
    gift = UniqueGift.model_construct(
        gift_id="gift_123",
        base_name="Gift",
        name="Gift #1",
        number=1,
    )
    info = UniqueGiftInfo(
        gift=gift,
        origin="transfer",
        text="Special Gift for you",
        is_private=True,
    )
    assert info.text == "Special Gift for you"
    assert info.is_private is True
