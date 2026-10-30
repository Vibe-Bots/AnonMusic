# Copyright (c) 2026 Vibe-Bots
# Open-sourced under MIT terms.
# Included within AnonMusic framework.

from py_yt import VideosSearch
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultPhoto,
)

from AnonMusic import app
from AnonMusic.utils.inlinequery import answer
from config import BANNED_USERS


@app.on_inline_query(~BANNED_USERS)
async def inline_query_handler(client, query):
    text = query.query.strip()

    if not text:
        try:
            await client.answer_inline_query(query.id, results=answer, cache_time=10)
        except:
            pass
        return

    search = VideosSearch(text, limit=15)
    results = (await search.next()).get("result", [])

    if not results:
        return

    answers = []
    for result in results[:15]:
        title = result["title"].title()
        duration = result["duration"]
        views = result["viewCount"]["short"]
        thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        channel_link = result["channel"]["link"]
        channel = result["channel"]["name"]
        video_link = result["link"]
        published = result["publishedTime"]

        description = f"{views} | {duration} mins | {channel} | {published}"

        buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton("📺 YouTube", url=video_link)]]
        )

        caption = f"""
❄ <b>Title:</b> <a href={video_link}>{title}</a>

⏳ <b>Duration:</b> {duration} mins
👀 <b>Views:</b> <code>{views}</code>
🎥 <b>Channel:</b> <a href={channel_link}>{channel}</a>
⏰ <b>Published:</b> {published}

<u><b>➻ Inline search by {app.name}</b></u>"""

        answers.append(
            InlineQueryResultPhoto(
                photo_url=thumbnail,
                title=title,
                thumb_url=thumbnail,
                description=description,
                caption=caption,
                reply_markup=buttons,
            )
        )

    try:
        await client.answer_inline_query(query.id, results=answers, cache_time=10)
    except:
        pass
