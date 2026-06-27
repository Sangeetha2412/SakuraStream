from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Character, AnimeCharacter

def character_list(request):
    characters = Character.objects.all().order_by('-favorites')
    paginator = Paginator(characters, 24)
    page_obj = paginator.get_page(request.GET.get('page', 1))
    return render(request, 'characters/list.html', {'characters': page_obj})

def character_detail(request, slug):
    character = get_object_or_404(Character, slug=slug)
    appearances = AnimeCharacter.objects.filter(character=character).select_related('anime')
    return render(request, 'characters/detail.html', {
        'character': character,
        'appearances': appearances,
    })
