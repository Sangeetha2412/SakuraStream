from apps.anime.models import Anime
from django.db.models import Q


def get_similar_anime(anime, limit=12):
    genres = anime.genres.all()
    similar = Anime.objects.filter(genres__in=genres).exclude(pk=anime.pk).distinct().order_by('-score')[:limit]
    return similar


def get_personalized_recommendations(user, limit=12):
    completed = user.watchlist.filter(status='completed').values_list('anime_id', flat=True)
    if not completed:
        return Anime.objects.filter(score__gte=8).order_by('-score')[:limit]
    from apps.anime.models import Genre
    genre_ids = Anime.objects.filter(id__in=completed).values_list('genres__id', flat=True).distinct()
    return Anime.objects.filter(genres__id__in=genre_ids).exclude(id__in=completed).distinct().order_by('-score')[:limit]
