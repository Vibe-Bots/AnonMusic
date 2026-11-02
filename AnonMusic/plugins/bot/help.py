# Copyright (c) 2026 Vibe-Bots
# Open-sourced under MIT terms.
# Included within AnonMusic framework.


from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, Message

from AnonMusic import app
from AnonMusic.misc import SUDOERS
from AnonMusic.utils import help_pannel
from AnonMusic.utils.database import get_lang
from AnonMusic.utils.decorators.language import LanguageStart, languageCB
from AnonMusic.utils.inline.help import help_back_markup, private_help_panel
from config import BANNED_USERS, START_IMG_URL, SUPPORT_CHAT
from strings import get_string, helpers

HELP_MAP = {
    "hb1": helpers.HELP_1,
    "hb2": helpers.HELP_2,
    "hb3": helpers.HELP_3,
    "hb4": helpers.HELP_4,
    "hb5": helpers.HELP_5,
    "hb6": helpers.HELP_6,
    "hb7": helpers.HELP_7,
    "hb8": helpers.HELP_8,
    "hb9": helpers.HELP_9,
}


@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
async def helper_private(client: app, update: types.Message | types.CallbackQuery):
    is_callback = isinstance(update, types.CallbackQuery)
    if is_callback:
        await update.answer()
        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        keyboard = help_pannel(_, True)
        await update.edit_message_text(
            _["help_1"].format(SUPPORT_CHAT), reply_markup=keyboard
        )
    else:
        await update.delete()
        language = await get_lang(update.chat.id)
        _ = get_string(language)
        keyboard = help_pannel(_)
        await update.reply_photo(
            photo=START_IMG_URL,
            caption=_["help_1"].format(SUPPORT_CHAT),
            reply_markup=keyboard,
        )


@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(_["help_2"], reply_markup=InlineKeyboardMarkup(keyboard))


@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):
    cb = CallbackQuery.data.strip().split(None, 1)[1]
    keyboard = help_back_markup(_)

    if cb == "hb7" and CallbackQuery.from_user.id not in SUDOERS:
        await CallbackQuery.answer(
            "This button is only for 'sudo' users.", show_alert=True
        )
        return

    help_text = HELP_MAP.get(cb)
    if help_text:
        await CallbackQuery.edit_message_text(help_text, reply_markup=keyboard)
