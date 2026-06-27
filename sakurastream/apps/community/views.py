from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Review, Comment, Discussion
from apps.anime.models import Anime
import json


def community_home(request):
    reviews = Review.objects.select_related('user', 'anime').order_by('-created_at')[:20]
    discussions = Discussion.objects.select_related('user', 'anime').order_by('-created_at')[:10]
    return render(request, 'community/home.html', {
        'reviews': reviews, 'discussions': discussions
    })


@login_required
@require_POST
def submit_review(request, anime_slug):
    anime = get_object_or_404(Anime, slug=anime_slug)
    data = json.loads(request.body)
    review, created = Review.objects.update_or_create(
        user=request.user, anime=anime,
        defaults={
            'title': data.get('title', ''),
            'content': data.get('content', ''),
            'score': data.get('score', 7),
            'is_recommended': data.get('is_recommended', True),
            'is_spoiler': data.get('is_spoiler', False),
        }
    )
    return JsonResponse({
        'success': True,
        'review_id': review.id,
        'action': 'created' if created else 'updated'
    })


@login_required
@require_POST
def like_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user in review.likes.all():
        review.likes.remove(request.user)
        liked = False
    else:
        review.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'count': review.like_count})
