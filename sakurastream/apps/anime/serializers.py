from rest_framework import serializers, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Anime, Genre, Studio, Collection


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug', 'color']


class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = ['id', 'name', 'slug']


class AnimeListSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Anime
        fields = [
            'id', 'title', 'title_english', 'slug', 'poster_url',
            'anime_type', 'status', 'score', 'popularity', 'episodes',
            'season', 'season_year', 'genres', 'is_trending', 'is_featured'
        ]


class AnimeDetailSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    studios = StudioSerializer(many=True, read_only=True)

    class Meta:
        model = Anime
        fields = '__all__'


class AnimeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Anime.objects.all().prefetch_related('genres', 'studios')
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'anime_type', 'season', 'season_year', 'is_trending', 'is_featured']
    search_fields = ['title', 'title_english', 'synopsis']
    ordering_fields = ['score', 'popularity', 'members', 'aired_from']
    ordering = ['-score']

    def get_serializer_class(self):
        if self.action == 'list':
            return AnimeListSerializer
        return AnimeDetailSerializer


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
