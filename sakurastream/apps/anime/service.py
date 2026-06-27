import logging
from datetime import datetime

import requests
from django.utils.text import slugify

from .models import Anime, Genre, Studio

logger = logging.getLogger(__name__)

JIKAN_BASE_URL = "https://api.jikan.moe/v4"

STATUS_MAP = {
    "Currently Airing": "airing",
    "Finished Airing": "finished",
    "Not yet aired": "upcoming",
    "On Hiatus": "hiatus",
}

SOURCE_MAP = {
    "Manga": "manga",
    "Light Novel": "light_novel",
    "Novel": "novel",
    "Original": "original",
    "Game": "game",
    "Visual Novel": "visual_novel",
}


def parse_date(value):
    if not value:
        return None

    try:
        return datetime.fromisoformat(
            value.replace("Z", "+00:00")
        ).date()
    except Exception:
        return None


def get_or_create_genres(items):
    genres = []

    for item in items or []:

        name = item.get("name")

        if not name:
            continue

        genre, _ = Genre.objects.get_or_create(
            name=name,
            defaults={
                "slug": slugify(name)
            }
        )

        genres.append(genre)

    return genres


def get_or_create_studios(items):

    studios = []

    for item in items or []:

        name = item.get("name")

        if not name:
            continue

        studio, _ = Studio.objects.get_or_create(
            name=name,
            defaults={
                "slug": slugify(name),
                "mal_id": item.get("mal_id")
            }
        )

        studios.append(studio)

    return studios
def import_anime_from_jikan(mal_id):

    response = requests.get(
        f"{JIKAN_BASE_URL}/anime/{mal_id}/full",
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()["data"]

    image = data.get("images", {}).get("jpg", {})
    trailer = data.get("trailer", {})
    aired = data.get("aired", {})

    anime_type = (data.get("type") or "TV").lower()

    valid_types = [
        "tv",
        "movie",
        "ova",
        "ona",
        "special",
        "music",
    ]

    if anime_type not in valid_types:
        anime_type = "tv"

    season = (data.get("season") or "").lower()

    valid_seasons = [
        "spring",
        "summer",
        "fall",
        "winter",
    ]

    if season not in valid_seasons:
        season = ""

    anime, created = Anime.objects.update_or_create(

        mal_id=data["mal_id"],

        defaults={

            "title": data.get("title") or "",

            "title_english": data.get("title_english") or "",

            "title_japanese": data.get("title_japanese") or "",

            "synopsis": data.get("synopsis") or "",

            "background": data.get("background") or "",

            "poster_url": image.get("large_image_url")
            or image.get("image_url")
            or "",

            "banner_url": trailer.get("images", {}).get(
                "maximum_image_url", ""
            ),

            "trailer_url": trailer.get("url") or "",

            "trailer_embed_id": trailer.get("youtube_id") or "",

            "anime_type": anime_type,

            "status": STATUS_MAP.get(
                data.get("status"),
                "finished",
            ),

            "source": SOURCE_MAP.get(
                data.get("source"),
                "other",
            ),

            "season": season,

            "season_year": data.get("year"),

            "aired_from": parse_date(
                aired.get("from")
            ),

            "aired_to": parse_date(
                aired.get("to")
            ),

            "episodes": data.get("episodes"),

            "duration": data.get("duration") or "",

            "rating": data.get("rating") or "",

            "score": data.get("score"),

            "scored_by": data.get("scored_by") or 0,

            "rank": data.get("rank"),

            "popularity": data.get("popularity"),

            "members": data.get("members") or 0,

            "favorites": data.get("favorites") or 0,

        }

    )

    anime.genres.set(
        get_or_create_genres(
            data.get("genres", [])
        )
    )

    anime.studios.set(
        get_or_create_studios(
            data.get("studios", [])
        )
    )

    logger.info("Imported anime %s", anime.title)

    return anime, created
def search_jikan_anime(query, limit=10):

    response = requests.get(
        f"{JIKAN_BASE_URL}/anime",
        params={
            "q": query,
            "limit": limit,
            "sfw": "true",
        },
        timeout=30,
    )

    response.raise_for_status()

    return response.json().get("data", [])