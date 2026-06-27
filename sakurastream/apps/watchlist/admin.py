from django.contrib import admin
from .models import WatchlistEntry

@admin.register(WatchlistEntry)
class WatchlistEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'anime', 'status', 'episodes_watched', 'score']
    list_filter = ['status']
    search_fields = ['user__username', 'anime__title']
