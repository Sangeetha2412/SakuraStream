from django.contrib import admin
from django.utils.html import format_html
from .models import Anime, Genre, Studio, Collection, AnimeRelation


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'established_year', 'website']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


class AnimeRelationInline(admin.TabularInline):
    model = AnimeRelation
    fk_name = 'from_anime'
    extra = 1


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ['title', 'anime_type', 'status', 'score', 'popularity', 'season_year', 'is_featured', 'is_trending', 'poster_preview']
    list_filter = ['status', 'anime_type', 'season', 'season_year', 'is_featured', 'is_trending', 'is_editor_pick']
    search_fields = ['title', 'title_english', 'title_japanese']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['genres', 'studios']
    inlines = [AnimeRelationInline]
    readonly_fields = ['created_at', 'updated_at', 'poster_preview_large']
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'title_english', 'title_japanese', 'slug', 'synopsis', 'background')
        }),
        ('Media', {
            'fields': ('poster', 'poster_url', 'banner', 'banner_url', 'trailer_url', 'trailer_embed_id', 'poster_preview_large')
        }),
        ('Details', {
            'fields': ('anime_type', 'status', 'source', 'season', 'season_year', 'aired_from', 'aired_to', 'episodes', 'duration', 'rating')
        }),
        ('Stats', {
            'fields': ('score', 'scored_by', 'rank', 'popularity', 'members', 'favorites')
        }),
        ('Relations', {
            'fields': ('genres', 'studios')
        }),
        ('Featured', {
            'fields': ('is_featured', 'is_editor_pick', 'is_trending')
        }),
        ('External IDs', {
            'fields': ('mal_id', 'anilist_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def poster_preview(self, obj):
        url = obj.display_poster
        if url:
            return format_html('<img src="{}" width="40" height="60" style="object-fit:cover;border-radius:4px;" />', url)
        return '-'
    poster_preview.short_description = 'Poster'

    def poster_preview_large(self, obj):
        url = obj.display_poster
        if url:
            return format_html('<img src="{}" width="120" height="180" style="object-fit:cover;border-radius:8px;" />', url)
        return '-'
    poster_preview_large.short_description = 'Preview'


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_featured', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['anime']
    list_filter = ['is_featured']
