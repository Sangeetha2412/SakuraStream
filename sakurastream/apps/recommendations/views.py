from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .engine import get_personalized_recommendations
from apps.anime.models import Anime

@login_required
def recommendations(request):
    anime = get_personalized_recommendations(request.user)
    data = [{'title': a.title, 'slug': a.slug, 'poster_url': a.poster_url, 'score': str(a.score or '')} for a in anime]
    return JsonResponse({'recommendations': data})
