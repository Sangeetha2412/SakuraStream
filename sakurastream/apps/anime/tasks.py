from celery import shared_task
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)
JIKAN_URL = settings.JIKAN_API_URL


def safe_get(url, params=None):
    try:
        import time
        time.sleep(0.5)  # Rate limiting
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logger.error(f'API request failed: {e}')
        return None


def save_anime_from_jikan(data):
    from .models import Anime, Genre, Studio
    from django.utils.text import slugify

    mal_id = data.get('mal_id')
    if not mal_id:
        return None

    anime, created = Anime.objects.get_or_create(mal_id=mal_id)

    anime.title = data.get('title', '')
    anime.title_english = data.get('title_english') or ''
    anime.title_japanese = data.get('title_japanese') or ''
    anime.synopsis = data.get('synopsis') or ''
    anime.episodes = data.get('episodes')
    anime.status = {
        'Finished Airing': 'finished',
        'Currently Airing': 'airing',
        'Not yet aired': 'upcoming',
    }.get(data.get('status', ''), 'finished')
    anime.score = data.get('score')
    anime.scored_by = data.get('scored_by') or 0
    anime.rank = data.get('rank')
    anime.popularity = data.get('popularity')
    anime.members = data.get('members') or 0
    anime.favorites = data.get('favorites') or 0
    anime.anime_type = data.get('type', 'tv').lower() if data.get('type') else 'tv'

    images = data.get('images', {})
    jpg = images.get('jpg', {})
    anime.poster_url = jpg.get('large_image_url') or jpg.get('image_url') or ''

    trailer = data.get('trailer', {})
    anime.trailer_url = trailer.get('url') or ''
    anime.trailer_embed_id = trailer.get('youtube_id') or ''

    aired = data.get('aired', {})
    from_date = aired.get('from')
    if from_date:
        try:
            from datetime import datetime
            anime.aired_from = datetime.fromisoformat(from_date[:10]).date()
        except Exception:
            pass

    season = data.get('season')
    if season:
        anime.season = season.lower()
    anime.season_year = data.get('year')

    if not anime.slug:
        base_slug = slugify(anime.title)
        slug = base_slug
        counter = 1
        while Anime.objects.filter(slug=slug).exclude(pk=anime.pk).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1
        anime.slug = slug

    anime.save()

    # Genres
    for g in data.get('genres', []) + data.get('explicit_genres', []):
        genre_obj, _ = Genre.objects.get_or_create(
            name=g['name'],
            defaults={'slug': slugify(g['name'])}
        )
        anime.genres.add(genre_obj)

    # Studios
    from django.db import IntegrityError

    for s in data.get("studios", []):
        try:
            studio_obj, created = Studio.objects.get_or_create(
                mal_id=s["mal_id"],
                defaults={
                    "name": s["name"],
                    "slug": slugify(s["name"]),
                },
            )

        except IntegrityError:
            studio_obj = Studio.objects.filter(name=s["name"]).first()

            if not studio_obj:
                studio_obj = Studio.objects.filter(
                    mal_id=s["mal_id"]
                ).first()

        if studio_obj:
            anime.studios.add(studio_obj)

    return anime   

@shared_task
def fetch_trending_anime():
    logger.info('Fetching trending anime...')
    data = safe_get(f'{JIKAN_URL}/top/anime', {'filter': 'bypopularity', 'limit': 25})
    if not data:
        return
    from .models import Anime
    Anime.objects.update(is_trending=False)
    for item in data.get('data', []):
        anime = save_anime_from_jikan(item)
        if anime:
            anime.is_trending = True
            anime.save()
    logger.info('Trending anime updated.')


@shared_task
def fetch_seasonal_anime():
    from datetime import date
    today = date.today()
    month_to_season = {3: 'spring', 4: 'spring', 5: 'spring', 6: 'summer',
                       7: 'summer', 8: 'summer', 9: 'fall', 10: 'fall', 11: 'fall',
                       12: 'winter', 1: 'winter', 2: 'winter'}
    season = month_to_season[today.month]
    year = today.year
    logger.info(f'Fetching {season} {year} anime...')
    data = safe_get(f'{JIKAN_URL}/seasons/{year}/{season}')
    if data:
        for item in data.get('data', []):
            save_anime_from_jikan(item)
    logger.info('Seasonal anime updated.')


@shared_task
def fetch_upcoming_anime():
    logger.info('Fetching upcoming anime...')
    data = safe_get(f'{JIKAN_URL}/seasons/upcoming')
    if data:
        for item in data.get('data', [])[:50]:
            anime = save_anime_from_jikan(item)
            if anime:
                anime.status = 'upcoming'
                anime.save()
    logger.info('Upcoming anime updated.')


@shared_task
def fetch_top_anime():
    logger.info('Fetching top anime...')
    for page in range(1, 201):
        data = safe_get(f'{JIKAN_URL}/top/anime', {'page': page, 'limit': 25})
        if not data:
            break
        for item in data.get('data', []):
            save_anime_from_jikan(item)
    logger.info('Top anime updated.')
