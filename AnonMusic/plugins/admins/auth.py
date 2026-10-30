# Copyright (c) 2026 Vibe-Bots
# Open-sourced under MIT terms.
# Included within AnonMusic framework.

from pyrogram import filters
from pyrogram.types import Message

from AnonMusic import app
from AnonMusic.utils import extract_user, int_to_alpha
from AnonMusic.utils.database import (
    delete_authuser,
    get_authuser,
    get_authuser_names,
    save_authuser,
)
from AnonMusic.utils.decorators import AdminActual, language
from AnonMusic.utils.inline import close_markup
from config import AUTH_LIMIT, BANNED_USERS, adminlist


@app.on_message(filters.command("auth") & filters.group & ~BANNED_USERS)
@AdminActual
async def auth(client, message: Message, _):
    user = await extract_user(message)
    if not user:
        return await message.reply_text(_["general_1"])

    token = await int_to_alpha(user.id)

    if len(await get_authuser_names(message.chat.id)) >= AUTH_LIMIT:
        return await message.reply_text(_["auth_1"])

    if token in await get_authuser_names(message.chat.id):
        return await message.reply_text(_["auth_3"].format(user.mention))

    await save_authuser(
        message.chat.id,
        token,
        {
            "auth_user_id": user.id,
            "auth_name": user.first_name,
            "admin_id": message.from_user.id,
            "admin_name": message.from_user.first_name,
        },
    )

    admin_cache = adminlist.get(message.chat.id)
    if admin_cache and user.id not in admin_cache:
        admin_cache.append(user.id)

    await message.reply_text(_["auth_2"].format(user.mention))


@app.on_message(filters.command("unauth") & filters.group & ~BANNED_USERS)
@AdminActual
async def unauthusers(client, message: Message, _):
    user = await extract_user(message)
    if not user:
        return await message.reply_text(_["general_1"])

    token = await int_to_alpha(user.id)

    deleted = await delete_authuser(message.chat.id, token)

    admin_cache = adminlist.get(message.chat.id)
    if admin_cache and user.id in admin_cache:
        admin_cache.remove(user.id)

    msg = _["auth_4"] if deleted else _["auth_5"]
    await message.reply_text(msg.format(user.mention))


@app.on_message(
    filters.command(["authlist", "authusers"]) & filters.group & ~BANNED_USERS
)
@language
async def authusers(client, message: Message, _):
    auth_list = await get_authuser_names(message.chat.id)

    if not auth_list:
        return await message.reply_text(_["setting_4"])

    mystic = await message.reply_text(_["auth_6"])
    text = _["auth_7"].format(message.chat.title)
    count = 0

    for token in auth_list:
        data = await get_authuser(message.chat.id, token)
        if not data:
            continue

        try:
            user = await app.get_users(data["auth_user_id"])
            count += 1
            text += (
                f"{count}➤ {user.first_name} [<code>{data['auth_user_id']}</code>]\n"
            )
            text += f"   {_['auth_8']} {data['admin_name']} [<code>{data['admin_id']}</code>]\n\n"
        except:
            continue

    await mystic.edit_text(text, reply_markup=close_markup(_))
