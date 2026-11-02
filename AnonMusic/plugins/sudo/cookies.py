# Copyright (c) 2026 Vibe-Bots
# Open-sourced under MIT terms.
# Included within AnonMusic framework.


import os

import requests
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton as Button
from pyrogram.types import InlineKeyboardMarkup, Message

from AnonMusic import app
from config import COOKIES_URL, OWNER_ID


async def set_cookies(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        cookies_dir = os.path.join(os.getcwd(), "cookies")
        os.makedirs(cookies_dir, exist_ok=True)

        cookies_path = os.path.join(cookies_dir, "cookies.txt")
        with open(cookies_path, "wb") as file:
            file.write(response.content)

        return f"✅ Bot cookies updated and saved to : {cookies_path}"

    except requests.exceptions.RequestException as e:
        return f"🚫 Error downloading cookies : {e!s}"
    except Exception as e:
        return f"🚫 Unknown error : {e!s}"


@app.on_message(
    filters.command(["updatecookies", "updatecookie", "getc"]) & filters.user(OWNER_ID)
)
async def update_cookies(client, message: Message):
    if len(message.command) > 1:
        url = message.command[1]
        if not (
            url.startswith(
                (
                    "https://gist.github.com/",
                    "https://batbin.me/",
                    "https://pastebin.com/",
                )
            )
        ):
            return await message.reply_text(
                "🚫 ɪɴᴠᴀʟɪᴅ ᴄᴏᴏᴋɪᴇs ᴜʀʟ.\n ᴏɴʟʏ ɢɪsᴛ, ᴘᴀsᴛᴇʙɪɴ, ᴀɴᴅ ʙᴀᴛʙɪɴ ʟɪɴᴋs ᴀʀᴇ sᴜᴘᴘᴏʀᴛᴇᴅ.",
                reply_markup=InlineKeyboardMarkup(
                    [[Button("ᴄʟᴏsᴇ", callback_data="close")]]
                ),
            )
    else:
        url = COOKIES_URL

    res = await set_cookies(url)
    await message.reply_text(
        res,
        reply_markup=InlineKeyboardMarkup([[Button("ᴄʟᴏsᴇ", callback_data="close")]]),
    )
