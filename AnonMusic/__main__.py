# Copyright (c) 2026 Vibe-Bots
# Open-sourced under MIT terms.
# Included within AnonMusic framework.


import asyncio
import importlib
import sys

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from AnonMusic import LOGGER, app, userbot
from AnonMusic.core.call import Anony
from AnonMusic.misc import sudo
from AnonMusic.plugins import ALL_MODULES
from AnonMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        sys.exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("AnonMusic.plugins" + all_module)
    LOGGER("AnonMusic.plugins").info("Successfully Imported Modules...")
    await userbot.start()
    await Anony.start()
    try:
        await Anony.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("AnonMusic").error(
            "Please turn on the videochat of your log group\\channel.\n\nStopping Bot..."
        )
        sys.exit()
    except:
        pass
    await Anony.decorators()
    LOGGER("AnonMusic").info(
        "\x41\x6e\x6f\x6e\x20\x4d\x75\x73\x69\x63\x20\x53\x74\x61\x72\x74\x65\x64\x20\x53\x75\x63\x63\x65\x73\x73\x66\x75\x6c\x6c\x79\x2e"
    )
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("AnonMusic").info("Stopping Anony Music Bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
