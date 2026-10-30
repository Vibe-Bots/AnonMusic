# Copyright (c) 2026 Vibe-Bots
# Open-sourced under MIT terms.
# Included within AnonMusic framework.


from pyrogram import filters
from pyrogram.types import Message

from AnonMusic import app
from AnonMusic.core.call import Anony
from AnonMusic.utils.database import is_music_playing, music_on
from AnonMusic.utils.decorators import AdminRightsCheck
from AnonMusic.utils.inline import close_markup
from config import BANNED_USERS


@app.on_message(filters.command(["resume", "cresume"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def resume_com(cli, message: Message, _, chat_id):
    if await is_music_playing(chat_id):
        return await message.reply_text(_["admin_3"])
    await music_on(chat_id)
    try:
        await Anony.resume_stream(chat_id)
    except Exception:
        pass
    await message.reply_text(
        _["admin_4"].format(message.from_user.mention), reply_markup=close_markup(_)
    )
