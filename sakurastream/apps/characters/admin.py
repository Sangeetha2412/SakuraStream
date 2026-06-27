from django.contrib import admin
from .models import Character, AnimeCharacter, VoiceActor

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_kanji', 'favorites']
    search_fields = ['name', 'name_kanji']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(VoiceActor)
class VoiceActorAdmin(admin.ModelAdmin):
    list_display = ['name', 'language', 'favorites']
    search_fields = ['name']
    list_filter = ['language']
