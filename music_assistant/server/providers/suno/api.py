# Supported search types are 'public_song', 'library_song', 'tag_song', 'playlist', 'following_clip_feed' or 'user'

from aiohttp import ClientSession

from music_assistant.common.models.enums import MediaType
from music_assistant.common.models.media_items import Artist, Playlist, Track

PUBLIC_SONG = "public_song"
LIBRARY_SONG = "library_song"
TAG_SONG = "tag_song"
PLAYLIST = "playlist"
FOLLOWING_CLIP_FEED = "following_clip_feed"
USER = "user"

SEARCH_TYPES = [
    PUBLIC_SONG,
    LIBRARY_SONG,
    TAG_SONG,
    PLAYLIST,
    FOLLOWING_CLIP_FEED,
    USER,
]

MEDIA_SEARCH_TYPE_MAP = {Track: PUBLIC_SONG, Playlist: PLAYLIST, Artist: USER}

SUNO_DOMAIN = "https://suno.com"
SUNO_SEARCH_URL = f"{SUNO_DOMAIN}/api/search"


async def search(
    query: str,
    mediaTypes: list[MediaType],
    http_session: ClientSession,
    offset: int = 0,
) -> dict:
    body = {
        "search_queries": [
            {
                "search_type": MEDIA_SEARCH_TYPE_MAP[mediaType],
                "term": query,
                "offset": offset,
                "name": MEDIA_SEARCH_TYPE_MAP[mediaType],
                "rank_by": "default",
            }
            for mediaType in mediaTypes
            if mediaType in MEDIA_SEARCH_TYPE_MAP
        ],
    }

    response = await http_session.post(SUNO_SEARCH_URL, json=body)
    response.raise_for_status()

    data = await response.json()
    return data["result"]
