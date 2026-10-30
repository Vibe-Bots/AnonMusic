# Copyright (c) 2026 Vibe-Bots
# Open-sourced under MIT terms.
# Included within AnonMusic framework.

import asyncio
import time

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.errors.exceptions.flood_420 import SlowmodeWait
from pyrogram.errors.exceptions.not_acceptable_406 import ChannelPrivate
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

import config
from AnonMusic import app
from AnonMusic.misc import _boot_
from AnonMusic.plugins.sudo.sudoers import sudoers_list
from AnonMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from AnonMusic.utils.decorators.language import LanguageStart
from AnonMusic.utils.formatters import get_readable_time
from AnonMusic.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS, LOGGER_ID, START_IMG_URL
from strings import get_string


@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    args = message.text.split()

    if len(args) > 1:
        name = args[1]

        if name.startswith("help"):
            keyboard = help_pannel(_)
            return await message.reply_photo(
                photo=START_IMG_URL,
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )

        if name.startswith("sud"):
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                await app.send_message(
                    LOGGER_ID,
                    f"{message.from_user.mention} checked sudolist.\n"
                    f"ID: `{message.from_user.id}`\nUsername: @{message.from_user.username}",
                )
            return

        if name.startswith("inf"):
            m = await message.reply_text("💻")
            video_id = name.replace("info_", "", 1)
            await show_track_info(message, video_id, _, m)
            return

    out = private_panel(_)
    await message.reply_photo(
        photo=START_IMG_URL,
        caption=_["start_2"].format(message.from_user.mention, app.mention),
        reply_markup=InlineKeyboardMarkup(out),
    )
    if await is_on_off(2):
        await app.send_message(
            LOGGER_ID,
            f"{message.from_user.mention} started the bot.\n"
            f"ID: `{message.from_user.id}`\nUsername: @{message.from_user.username}",
        )


async def show_track_info(message, video_id, _, loading_msg):
    from py_yt import VideosSearch

    query = f"https://www.youtube.com/watch?v={video_id}"
    results = VideosSearch(query, limit=1)

    for result in (await results.next())["result"]:
        title = result["title"]
        duration = result["duration"]
        views = result["viewCount"]["short"]
        thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        channel_link = result["channel"]["link"]
        channel = result["channel"]["name"]
        video_link = result["link"]
        published = result["publishedTime"]

    searched_text = _["start_6"].format(
        title, duration, views, published, channel_link, channel, app.mention
    )

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["S_B_8"], url=video_link),
                InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
            ]
        ]
    )

    await loading_msg.delete()
    await app.send_photo(
        chat_id=message.chat.id,
        photo=thumbnail,
        caption=searched_text,
        reply_markup=keyboard,
    )


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = get_readable_time(int(time.time() - _boot_))

    for attempt in range(2):
        try:
            await message.reply_photo(
                photo=START_IMG_URL,
                caption=_["start_1"].format(app.mention, uptime),
                reply_markup=InlineKeyboardMarkup(out),
            )
            await add_served_chat(message.chat.id)
            return
        except ChannelPrivate:
            return
        except SlowmodeWait as e:
            if attempt == 0:
                await asyncio.sleep(e.value)
                continue
            return
        except:
            return


@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        if await is_banned_user(member.id):
            try:
                await message.chat.ban_member(member.id)
            except:
                pass
            continue

        if member.id != app.id:
            continue

        language = await get_lang(message.chat.id)
        _ = get_string(language)

        if message.chat.type != ChatType.SUPERGROUP:
            await message.reply_text(_["start_4"])
            return await app.leave_chat(message.chat.id)

        if message.chat.id in await blacklisted_chats():
            await message.reply_text(
                _["start_5"].format(
                    app.mention,
                    f"https://t.me/{app.username}?start=sudolist",
                    config.SUPPORT_CHAT,
                ),
                disable_web_page_preview=True,
            )
            return await app.leave_chat(message.chat.id)

        out = start_panel(_)
        await message.reply_photo(
            photo=START_IMG_URL,
            caption=_["start_3"].format(
                message.from_user.first_name,
                app.mention,
                message.chat.title,
                app.mention,
            ),
            reply_markup=InlineKeyboardMarkup(out),
        )
        await add_served_chat(message.chat.id)
        await message.stop_propagation()
