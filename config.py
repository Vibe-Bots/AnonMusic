import re
import sys
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()


def validate_env_var(var_name, required=True, cast_type=str, default=None):
    value = getenv(var_name, default)
    if required and (value is None or value == ""):
        sys.exit(f"[ERROR] - Required environment variable '{var_name}' is missing.")
    if cast_type:
        try:
            return cast_type(value)
        except ValueError:
            sys.exit(
                f"[ERROR] - Environment variable '{var_name}' must be of type {cast_type.__name__}"
            )
    return value


API_ID = validate_env_var("API_ID", cast_type=int)
API_HASH = validate_env_var("API_HASH")
BOT_TOKEN = validate_env_var("BOT_TOKEN")
LOGGER_ID = validate_env_var("LOGGER_ID", cast_type=int)
OWNER_ID = validate_env_var("OWNER_ID", cast_type=int)
MONGO_DB_URI = getenv("MONGO_DB_URI")

BASE_API_URL = getenv("BASE_API_URL", "https://api.vibebots.fun")
BASE_API_KEY = getenv("BASE_API_KEY", "VibeBots_RsszUDPo1HjFWIsPqih")

COOKIES_URL = getenv("COOKIES_URL")

DURATION_LIMIT_MIN = validate_env_var("DURATION_LIMIT", cast_type=int, default=300)

HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/Vibe-Bots/AnonMusic")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "Master")
GIT_TOKEN = getenv("GIT_TOKEN")


SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/VibeBots")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/VibeBotsSupport")

AUTO_END_VC_STREAM = getenv("AUTO_END_VC_STREAM", "false").lower() in ("true", "1")
AUTO_LEAVING_ASSISTANT = getenv("AUTO_LEAVING_ASSISTANT", "false").lower() in (
    "true",
    "1",
)
ASSISTANT_LEAVE_TIME = validate_env_var(
    "ASSISTANT_LEAVE_TIME", cast_type=int, default=6400
)

SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "22b6125bfe224587b722d6815002db2b")
SPOTIFY_CLIENT_SECRET = getenv(
    "SPOTIFY_CLIENT_SECRET", "c9c63c6fbf2f467c8bc68624851e9773"
)

PLAYLIST_FETCH_LIMIT = validate_env_var(
    "PLAYLIST_FETCH_LIMIT", cast_type=int, default=25
)

AUTH_LIMIT = validate_env_var("AUTH_LIMIT", cast_type=int, default=15)

TG_AUDIO_FILESIZE_LIMIT = validate_env_var(
    "TG_AUDIO_FILESIZE_LIMIT", cast_type=int, default=204857600
)
TG_VIDEO_FILESIZE_LIMIT = validate_env_var(
    "TG_VIDEO_FILESIZE_LIMIT", cast_type=int, default=2071824
)

PRIVATE_BOT_MODE_MEM = validate_env_var(
    "PRIVATE_BOT_MODE_MEM", cast_type=int, default=1
)

CACHE_DURATION = validate_env_var("CACHE_DURATION", cast_type=int, default=86400)
CACHE_SLEEP = validate_env_var("CACHE_SLEEP", cast_type=int, default=3600)


STRING1 = getenv("STRING_SESSION")
STRING2 = getenv("STRING_SESSION2")
STRING3 = getenv("STRING_SESSION3")
STRING4 = getenv("STRING_SESSION4")
STRING5 = getenv("STRING_SESSION5")


BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}
file_cache: dict[str, float] = {}


START_IMG_URL = getenv("START_IMG_URL", "https://files.catbox.moe/ihr1qu.jpg")
PING_IMG_URL = getenv("PING_IMG_URL", "https://files.catbox.moe/fhycjz.jpg")

PLAYLIST_IMG_URL = "https://files.catbox.moe/v7u8ji.jpg"
STATS_IMG_URL = "https://files.catbox.moe/fhycjz.jpg"
TELEGRAM_AUDIO_URL = "https://files.catbox.moe/fahcob.jpg"
TELEGRAM_VIDEO_URL = "https://files.catbox.moe/gy14qk.jpg"
STREAM_IMG_URL = "https://files.catbox.moe/h0m0wz.jpg"
SOUNCLOUD_IMG_URL = "https://files.catbox.moe/ieduw9.jpg"
YOUTUBE_IMG_URL = "https://files.catbox.moe/rnwmfw.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://files.catbox.moe/66ye0m.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://files.catbox.moe/66ye0m.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://files.catbox.moe/66ye0m.jpg"


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = time_to_seconds(f"{DURATION_LIMIT_MIN}:00")

for url_name, url in [
    ("SUPPORT_CHANNEL", SUPPORT_CHANNEL),
    ("SUPPORT_CHAT", SUPPORT_CHAT),
]:
    if not re.match(r"^(?:http|https)://", url):
        sys.exit(
            f"[ERROR] - {url_name} is invalid. It must start with http:// or https://"
        )
