from django.contrib import admin
from .models import Review, Comment, Discussion

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'anime', 'score', 'is_recommended', 'created_at']
    list_filter = ['is_recommended', 'is_spoiler', 'score']
    search_fields = ['user__username', 'anime__title', 'content']

@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'views', 'is_pinned', 'created_at']
    list_filter = ['is_pinned']
