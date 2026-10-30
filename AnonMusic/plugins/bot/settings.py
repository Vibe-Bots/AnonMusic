# Copyright (c) 2026 Vibe-Bots
# Open-sourced under MIT terms.
# Included within AnonMusic framework.

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.errors import MessageNotModified
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from AnonMusic import app
from AnonMusic.utils import bot_sys_stats
from AnonMusic.utils.database import (
    add_nonadmin_chat,
    get_authuser,
    get_authuser_names,
    get_playmode,
    get_playtype,
    get_upvote_count,
    is_nonadmin_chat,
    is_skipmode,
    remove_nonadmin_chat,
    set_playmode,
    set_playtype,
    set_upvotes,
    skip_off,
    skip_on,
)
from AnonMusic.utils.decorators.admins import ActualAdminCB
from AnonMusic.utils.decorators.language import language, languageCB
from AnonMusic.utils.inline.settings import (
    auth_users_markup,
    playmode_users_markup,
    setting_markup,
    vote_mode_markup,
)
from AnonMusic.utils.inline.start import private_panel
from config import BANNED_USERS


async def quick_answer(query: CallbackQuery, text: str, alert: bool = False):
    try:
        await query.answer(text, show_alert=alert)
    except:
        pass


@app.on_message(
    filters.command(["settings", "setting"]) & filters.group & ~BANNED_USERS
)
@language
async def settings_mar(client, message: Message, _):
    await message.reply_text(
        _["setting_1"].format(app.mention, message.chat.id, message.chat.title),
        reply_markup=InlineKeyboardMarkup(setting_markup(_)),
    )


@app.on_callback_query(filters.regex("settings_helper") & ~BANNED_USERS)
@languageCB
async def settings_cb(client, query: CallbackQuery, _):
    await quick_answer(query, _["set_cb_5"])
    try:
        await query.edit_message_text(
            _["setting_1"].format(
                app.mention, query.message.chat.id, query.message.chat.title
            ),
            reply_markup=InlineKeyboardMarkup(setting_markup(_)),
        )
    except MessageNotModified:
        pass


@app.on_callback_query(filters.regex("settingsback_helper") & ~BANNED_USERS)
@languageCB
async def settings_back_markup(client, query: CallbackQuery, _):
    await quick_answer(query, "")

    if query.message.chat.type == ChatType.PRIVATE:
        buttons = private_panel(_)
        UP, CPU, RAM, DISK = await bot_sys_stats()
        await query.edit_message_text(
            _["start_2"].format(
                query.from_user.mention, app.mention, UP, DISK, CPU, RAM
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(setting_markup(_))
        )


INFO_HANDLERS = {
    "SEARCHANSWER": lambda _: _["setting_2"],
    "PLAYMODEANSWER": lambda _: _["setting_5"],
    "PLAYTYPEANSWER": lambda _: _["setting_6"],
    "AUTHANSWER": lambda _: _["setting_3"],
    "VOTEANSWER": lambda _: _["setting_8"],
}


@app.on_callback_query(
    filters.regex(
        r"^(SEARCHANSWER|PLAYMODEANSWER|PLAYTYPEANSWER|AUTHANSWER|VOTEANSWER)$"
    )
    & ~BANNED_USERS
)
@languageCB
async def handle_info_buttons(client, query: CallbackQuery, _):
    command = query.matches[0].group(1)
    text = INFO_HANDLERS[command](_)
    await quick_answer(query, text, alert=True)


@app.on_callback_query(filters.regex("ANSWERVOMODE") & ~BANNED_USERS)
@languageCB
async def handle_vote_info(client, query: CallbackQuery, _):
    current = await get_upvote_count(query.message.chat.id)
    await quick_answer(query, _["setting_9"].format(current), alert=True)


MODE_HANDLERS = {
    "PM": lambda chat_id, _: get_playmode_buttons(chat_id, _),
    "AU": lambda chat_id, _: get_auth_buttons(chat_id, _),
    "VM": lambda chat_id, _: get_vote_buttons(chat_id, _),
}


async def get_playmode_buttons(chat_id, _):
    playmode = await get_playmode(chat_id)
    playtype = await get_playtype(chat_id)
    is_non_admin = await is_nonadmin_chat(chat_id)
    return playmode_users_markup(
        _,
        True if playmode == "Direct" else None,
        True if not is_non_admin else None,
        None if playtype == "Everyone" else True,
    )


async def get_auth_buttons(chat_id, _):
    is_non_admin = await is_nonadmin_chat(chat_id)
    return auth_users_markup(_, True if not is_non_admin else None)


async def get_vote_buttons(chat_id, _):
    mode = await is_skipmode(chat_id)
    current = await get_upvote_count(chat_id)
    return vote_mode_markup(_, current, mode)


@app.on_callback_query(filters.regex(r"^(PM|AU|VM)$") & ~BANNED_USERS)
@languageCB
async def handle_mode_buttons(client, query: CallbackQuery, _):
    await quick_answer(
        query,
        _["set_cb_2"] if query.matches[0].group(1) == "PM" else _["set_cb_1"],
        alert=True,
    )
    command = query.matches[0].group(1)
    buttons = await MODE_HANDLERS[command](query.message.chat.id, _)
    try:
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        pass


@app.on_callback_query(filters.regex("FERRARIUDTI") & ~BANNED_USERS)
@ActualAdminCB
async def handle_vote_count_change(client, query: CallbackQuery, _):
    chat_id = query.message.chat.id

    if not await is_skipmode(chat_id):
        return await quick_answer(query, _["setting_10"], alert=True)

    mode = query.data.strip().split(None, 1)[1]
    current = await get_upvote_count(chat_id)

    if mode == "M":
        final = max(2, current - 2)
        if current == 2:
            return await quick_answer(query, _["setting_11"], alert=True)
    else:
        final = min(15, current + 2)
        if current == 15:
            return await quick_answer(query, _["setting_12"], alert=True)

    await set_upvotes(chat_id, final)
    buttons = vote_mode_markup(_, final, True)
    try:
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        pass


@app.on_callback_query(
    filters.regex(r"^(MODECHANGE|CHANNELMODECHANGE|PLAYTYPECHANGE)$") & ~BANNED_USERS
)
@ActualAdminCB
async def handle_playmode_change(client, query: CallbackQuery, _):
    chat_id = query.message.chat.id
    cmd = query.matches[0].group(1)

    if cmd == "CHANNELMODECHANGE":
        if await is_nonadmin_chat(chat_id):
            await remove_nonadmin_chat(chat_id)
        else:
            await add_nonadmin_chat(chat_id)
    elif cmd == "MODECHANGE":
        await quick_answer(query, _["set_cb_3"], alert=True)
        playmode = await get_playmode(chat_id)
        await set_playmode(chat_id, "Inline" if playmode == "Direct" else "Direct")
    elif cmd == "PLAYTYPECHANGE":
        await quick_answer(query, _["set_cb_3"], alert=True)
        playtype = await get_playtype(chat_id)
        await set_playtype(chat_id, "Admin" if playtype == "Everyone" else "Everyone")

    buttons = await get_playmode_buttons(chat_id, _)
    try:
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        pass


@app.on_callback_query(filters.regex(r"^(AUTH|AUTHLIST)$") & ~BANNED_USERS)
@ActualAdminCB
async def handle_auth_list(client, query: CallbackQuery, _):
    chat_id = query.message.chat.id
    cmd = query.matches[0].group(1)

    if cmd == "AUTHLIST":
        auth_users = await get_authuser_names(chat_id)
        if not auth_users:
            return await quick_answer(query, _["setting_4"], alert=True)

        await quick_answer(query, _["set_cb_4"], alert=True)
        await query.edit_message_text(_["auth_6"])

        msg = _["auth_7"].format(query.message.chat.title)
        count = 0

        for token in auth_users:
            data = await get_authuser(chat_id, token)
            try:
                user = await app.get_users(data["auth_user_id"])
                count += 1
                msg += (
                    f"{count}➤ {user.first_name}[<code>{data['auth_user_id']}</code>]\n"
                )
                msg += f"   {_['auth_8']} {data['admin_name']}[<code>{data['admin_id']}</code>]\n\n"
            except:
                continue

        buttons = [
            [
                InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="AU"),
                InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
            ]
        ]
        await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        is_non_admin = await is_nonadmin_chat(chat_id)
        if not is_non_admin:
            await add_nonadmin_chat(chat_id)
            auth_state = None
        else:
            await remove_nonadmin_chat(chat_id)
            auth_state = True

        await quick_answer(query, _["set_cb_3"], alert=True)
        buttons = auth_users_markup(_, auth_state)
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )


@app.on_callback_query(filters.regex("VOMODECHANGE") & ~BANNED_USERS)
@ActualAdminCB
async def handle_vote_toggle(client, query: CallbackQuery, _):
    await quick_answer(query, _["set_cb_3"], alert=True)
    chat_id = query.message.chat.id

    if await is_skipmode(chat_id):
        await skip_off(chat_id)
        is_enabled = None
    else:
        await skip_on(chat_id)
        is_enabled = True

    current = await get_upvote_count(chat_id)
    buttons = vote_mode_markup(_, current, is_enabled)
    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
