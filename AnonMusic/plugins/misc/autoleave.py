# Copyright (c) 2026 Vibe-Bots
# Open-sourced under MIT terms.
# Included within AnonMusic framework.


import asyncio
import logging
from datetime import datetime

from pyrogram.enums import ChatType
from pytgcalls.exceptions import NoActiveGroupCall

import config
from AnonMusic import app
from AnonMusic.core.call import Anony, autoend
from AnonMusic.misc import db
from AnonMusic.utils.database import (
    get_client,
    is_active_chat,
    is_autoend,
    is_autoleave,
    set_loop,
)


async def auto_leave():
    while not await asyncio.sleep(900):
        from AnonMusic.core.userbot import assistants

        ender = await is_autoleave()
        if not ender:
            continue
        for num in assistants:
            client = await get_client(num)
            left = 0
            try:
                async for i in client.get_dialogs():
                    if i.chat.type in [
                        ChatType.SUPERGROUP,
                        ChatType.GROUP,
                        ChatType.CHANNEL,
                    ] and (
                        i.chat.id != config.LOG_GROUP_ID
                        and i.chat.id != -1002500829755
                    ):
                        if left == 20:
                            continue
                        if not await is_active_chat(i.chat.id):
                            try:
                                await client.leave_chat(i.chat.id)
                                left += 1
                            except Exception as e:
                                logging.error(
                                    f"Error leaving chat {i.chat.id}: {e}"
                                )
                                continue
            except Exception as e:
                logging.error(f"Error processing dialogs: {e}")


asyncio.create_task(auto_leave())


async def auto_end():
    global autoend, counter
    while True:
        await asyncio.sleep(60)
        try:
            ender = await is_autoend()
            if not ender:
                continue

            chatss = autoend
            keys_to_remove = []

            for chat_id in chatss:
                nocall = False
                try:
                    assistant = await group_assistant(Anony, chat_id)
                    participants = await assistant.get_participants(chat_id)
                    users = len(participants)
                except NoActiveGroupCall:
                    users = 1
                    nocall = True
                except Exception:
                    users = 100

                timer = autoend.get(chat_id)
                if users == 1 and isinstance(timer, datetime):
                    if datetime.now() >= timer:
                        await set_loop(chat_id, 0)
                        keys_to_remove.append(chat_id)

                        try:
                            await db[chat_id][0]["mystic"].delete()
                        except Exception:
                            pass

                        try:
                            await Anony.stop_stream(chat_id)
                        except Exception:
                            pass

                        try:
                            if not nocall:
                                await app.send_message(
                                    chat_id,
                                    "» ʙᴏᴛ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ʟᴇғᴛ ᴠɪᴅᴇᴏᴄʜᴀᴛ "
                                    "ʙᴇᴄᴀᴜsᴇ ɴᴏ ᴏɴᴇ ᴡᴀs ʟɪsᴛᴇɴɪɴɢ ᴏɴ ᴠɪᴅᴇᴏᴄʜᴀᴛ.",
                                )
                        except Exception:
                            pass

            for chat_id in keys_to_remove:
                try:
                    del autoend[chat_id]
                except Exception:
                    pass

        except Exception as e:
            logging.info(e)


asyncio.create_task(auto_end())
