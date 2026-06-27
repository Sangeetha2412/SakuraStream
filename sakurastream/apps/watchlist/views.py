from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import WatchlistEntry
from apps.anime.models import Anime
import json


@login_required
def watchlist(request):
    status = request.GET.get('status', 'all')
    entries = request.user.watchlist.select_related('anime').order_by('-updated_at')
    if status != 'all':
        entries = entries.filter(status=status)
    counts = {
        'all': request.user.watchlist.count(),
        'watching': request.user.watchlist.filter(status='watching').count(),
        'completed': request.user.watchlist.filter(status='completed').count(),
        'plan_to_watch': request.user.watchlist.filter(status='plan_to_watch').count(),
        'on_hold': request.user.watchlist.filter(status='on_hold').count(),
        'dropped': request.user.watchlist.filter(status='dropped').count(),
    }
    return render(request, 'watchlist/list.html', {
        'entries': entries, 'status': status, 'counts': counts
    })


@login_required
@require_POST
def toggle_watchlist(request, anime_slug):
    anime = get_object_or_404(Anime, slug=anime_slug)
    data = json.loads(request.body)
    status = data.get('status', 'plan_to_watch')

    entry, created = WatchlistEntry.objects.get_or_create(
        user=request.user, anime=anime,
        defaults={'status': status}
    )
    if not created:
        if entry.status == status:
            entry.delete()
            return JsonResponse({'action': 'removed'})
        entry.status = status
        entry.save()
        return JsonResponse({'action': 'updated', 'status': status})
    return JsonResponse({'action': 'added', 'status': status})


@login_required
@require_POST
def update_progress(request, entry_id):
    entry = get_object_or_404(WatchlistEntry, id=entry_id, user=request.user)
    data = json.loads(request.body)
    entry.episodes_watched = data.get('episodes_watched', entry.episodes_watched)
    entry.score = data.get('score', entry.score)
    entry.status = data.get('status', entry.status)
    entry.save()
    return JsonResponse({'success': True, 'progress': entry.progress_percent})
