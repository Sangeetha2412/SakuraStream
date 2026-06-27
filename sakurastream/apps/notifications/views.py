from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification

@login_required
def mark_read(request, pk):
    Notification.objects.filter(pk=pk, user=request.user).update(is_read=True)
    return JsonResponse({'ok': True})

@login_required
def list_notifications(request):
    notifs = request.user.notifications.filter(is_read=False)[:10]
    data = [{'id': n.id, 'title': n.title, 'message': n.message, 'url': n.url} for n in notifs]
    return JsonResponse({'notifications': data, 'count': notifs.count()})
