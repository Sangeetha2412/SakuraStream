from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views import View
from .models import Anime, Genre, Studio, Collection
from apps.community.models import Review
from apps.characters.models import AnimeCharacter
import json


def home(request):
    trending = Anime.objects.filter(
    score__isnull=False
).order_by("-members")[:12]
    top_rated = Anime.objects.filter(score__isnull=False).order_by('-score')[:12]
    popular = Anime.objects.order_by("-members")[:12]
    latest = Anime.objects.order_by('-updated_at')[:12]
    upcoming = Anime.objects.filter(status="upcoming").order_by("aired_from")[:8]
    featured = Anime.objects.order_by("-score").first()
    editor_picks = Anime.objects.order_by('-favorites')[:6]
    collections = Collection.objects.all()[:4]
    top_genres = Genre.objects.all()[:10]
    recent_reviews = Review.objects.select_related('user', 'anime').order_by('-created_at')[:6]

    # Seasonal
    from datetime import date
    today = date.today()
    month = today.month
    if month in [3, 4, 5]:
        current_season = 'spring'
    elif month in [6, 7, 8]:
        current_season = 'summer'
    elif month in [9, 10, 11]:
        current_season = 'fall'
    else:
        current_season = 'winter'

    seasonal = Anime.objects.filter(season=current_season, season_year=today.year).order_by('-score')[:12]

    context = {
        'trending': trending,
        'top_rated': top_rated,
        'popular': popular,
        'latest': latest,
        'upcoming': upcoming,
        'featured': featured,
        'editor_picks': editor_picks,
        'collections': collections,
        'top_genres': top_genres,
        'recent_reviews': recent_reviews,
        'seasonal': seasonal,
        'current_season': current_season,
        'current_year': today.year,
        'total_anime': Anime.objects.count(),
    }
    return render(request, 'anime/home.html', context)


def anime_list(request):
    queryset = Anime.objects.all()

    # Filters
    genre = request.GET.get('genre')
    status = request.GET.get('status')
    anime_type = request.GET.get('type')
    season = request.GET.get('season')
    year = request.GET.get('year')
    order_by = request.GET.get('order_by', '-score')
    search = request.GET.get('q')
    min_score = request.GET.get('min_score')

    if search:
        queryset = queryset.filter(
            Q(title__icontains=search) |
            Q(title_english__icontains=search) |
            Q(title_japanese__icontains=search) |
            Q(synopsis__icontains=search)
        )
    if genre:
        queryset = queryset.filter(genres__slug=genre)
    if status:
        queryset = queryset.filter(status=status)
    if anime_type:
        queryset = queryset.filter(anime_type=anime_type)
    if season:
        queryset = queryset.filter(season=season)
    if year:
        queryset = queryset.filter(season_year=year)
    if min_score:
        queryset = queryset.filter(score__gte=min_score)

    valid_orders = ['-score', '-popularity', '-members', '-favorites', 'title', '-aired_from']
    if order_by in valid_orders:
        queryset = queryset.order_by(order_by)

    paginator = Paginator(queryset, 24)
    page = request.GET.get('page', 1)
    anime = paginator.get_page(page)

    genres = Genre.objects.all()
    years = Anime.objects.filter(season_year__isnull=False).values_list('season_year', flat=True).distinct().order_by('-season_year')

    context = {
        'anime': anime,
        'genres': genres,
        'years': years,
        'current_filters': {
            'genre': genre, 'status': status, 'type': anime_type,
            'season': season, 'year': year, 'order_by': order_by,
            'q': search, 'min_score': min_score,
        },
    }
    return render(request, 'anime/list.html', context)


def anime_detail(request, slug):
    anime = get_object_or_404(Anime, slug=slug)
    characters = AnimeCharacter.objects.filter(anime=anime).select_related('character').order_by('order')[:12]
    reviews = Review.objects.filter(anime=anime).select_related('user').order_by('-created_at')[:10]
    similar = Anime.objects.filter(genres__in=anime.genres.all()).exclude(pk=anime.pk).distinct().order_by('-score')[:12]
    relations = anime.relations_from.select_related('to_anime').all()

    user_watchlist_entry = None
    user_review = None
    if request.user.is_authenticated:
        from apps.watchlist.models import WatchlistEntry
        try:
            user_watchlist_entry = request.user.watchlist.get(anime=anime)
        except Exception:
            pass
        try:
            user_review = reviews.get(user=request.user)
        except Exception:
            pass

    context = {
        'anime': anime,
        'characters': characters,
        'reviews': reviews,
        'similar': similar,
        'relations': relations,
        'user_watchlist_entry': user_watchlist_entry,
        'user_review': user_review,
        'review_count': reviews.count(),
        'avg_score': reviews.aggregate(Avg('score'))['score__avg'],
    }
    return render(request, 'anime/detail.html', context)


def genre_detail(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    anime_list = Anime.objects.filter(genres=genre).order_by('-score')
    paginator = Paginator(anime_list, 24)
    anime = paginator.get_page(request.GET.get('page', 1))
    return render(request, 'anime/genre.html', {'genre': genre, 'anime': anime})


def collection_detail(request, slug):
    collection = get_object_or_404(Collection, slug=slug)
    return render(request, 'anime/collection.html', {'collection': collection})


def trending(request):
    anime = Anime.objects.filter(is_trending=True).order_by('-popularity')
    paginator = Paginator(anime, 24)
    page_obj = paginator.get_page(request.GET.get('page', 1))
    return render(request, 'anime/trending.html', {'anime': page_obj})


def seasonal(request):
    from datetime import date
    today = date.today()
    year = int(request.GET.get('year', today.year))
    season_map = {3: 'spring', 4: 'spring', 5: 'spring', 6: 'summer',
                  7: 'summer', 8: 'summer', 9: 'fall', 10: 'fall', 11: 'fall',
                  12: 'winter', 1: 'winter', 2: 'winter'}
    season = request.GET.get('season', season_map[today.month])
    anime = Anime.objects.filter(season=season, season_year=year).order_by('-score')
    return render(request, 'anime/seasonal.html', {'anime': anime, 'season': season, 'year': year})


def upcoming(request):
    upcoming = Anime.objects.none()
    paginator = Paginator(anime, 24)
    page_obj = paginator.get_page(request.GET.get('page', 1))
    return render(request, 'anime/upcoming.html', {'anime': page_obj})


def search_suggestions(request):
    q = request.GET.get('q', '')
    results = []
    if len(q) >= 2:
        anime = Anime.objects.filter(
            Q(title__icontains=q) | Q(title_english__icontains=q)
        ).values('title', 'title_english', 'slug', 'poster_url', 'score')[:8]
        results = list(anime)
    return JsonResponse({'results': results})
