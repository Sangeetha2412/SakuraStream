from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from taggit.managers import TaggableManager


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, default='#FF77C8')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('anime:genre_detail', kwargs={'slug': self.slug})


class Studio(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='studios/', blank=True, null=True)
    website = models.URLField(blank=True)
    established_year = models.IntegerField(null=True, blank=True)
    mal_id = models.IntegerField(unique=True, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Anime(models.Model):
    STATUS_CHOICES = [
        ('airing', 'Currently Airing'),
        ('finished', 'Finished Airing'),
        ('upcoming', 'Not Yet Aired'),
        ('hiatus', 'On Hiatus'),
        ('discontinued', 'Discontinued'),
    ]
    SEASON_CHOICES = [
        ('spring', 'Spring'),
        ('summer', 'Summer'),
        ('fall', 'Fall'),
        ('winter', 'Winter'),
    ]
    TYPE_CHOICES = [
        ('tv', 'TV Series'),
        ('movie', 'Movie'),
        ('ova', 'OVA'),
        ('ona', 'ONA'),
        ('special', 'Special'),
        ('music', 'Music'),
    ]
    SOURCE_CHOICES = [
        ('manga', 'Manga'),
        ('light_novel', 'Light Novel'),
        ('novel', 'Novel'),
        ('original', 'Original'),
        ('game', 'Game'),
        ('visual_novel', 'Visual Novel'),
        ('other', 'Other'),
    ]

    # Core
    title = models.CharField(max_length=500)
    title_english = models.CharField(max_length=500, blank=True)
    title_japanese = models.CharField(max_length=500, blank=True)
    slug = models.SlugField(unique=True, max_length=600)
    synopsis = models.TextField(blank=True)
    background = models.TextField(blank=True)

    # Media
    poster = models.ImageField(
        upload_to='anime/posters/',
        blank=True,
        null=True
    )

    banner = models.ImageField(
        upload_to='anime/banners/',
        blank=True,
        null=True
    )

    poster_url = models.URLField(
        blank=True,
        null=True
    )

    banner_url = models.URLField(
        blank=True,
        null=True
    )

    trailer_url = models.URLField(
        blank=True,
        null=True
    )

    trailer_embed_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    # Info
    anime_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='tv')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='finished')
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='manga')
    season = models.CharField(max_length=10, choices=SEASON_CHOICES, blank=True)
    season_year = models.IntegerField(null=True, blank=True)
    aired_from = models.DateField(null=True, blank=True)
    aired_to = models.DateField(null=True, blank=True)
    episodes = models.IntegerField(null=True, blank=True)
    duration = models.CharField(max_length=50, blank=True)
    rating = models.CharField(max_length=50, blank=True)  # G, PG, PG-13, R, etc.

    # Scores
    score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    scored_by = models.IntegerField(default=0)
    rank = models.IntegerField(null=True, blank=True)
    popularity = models.IntegerField(null=True, blank=True)
    members = models.IntegerField(default=0)
    favorites = models.IntegerField(default=0)

    # Relations
    genres = models.ManyToManyField(Genre, blank=True, related_name='anime')
    studios = models.ManyToManyField(Studio, blank=True, related_name='anime')
    tags = TaggableManager(blank=True)

    # External IDs
    mal_id = models.IntegerField(unique=True, null=True, blank=True)
    anilist_id = models.IntegerField(unique=True, null=True, blank=True)

    # Meta
    is_featured = models.BooleanField(default=False)
    is_editor_pick = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-score', '-popularity']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['season', 'season_year']),
            models.Index(fields=['is_trending']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['score']),
            models.Index(fields=['popularity']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Anime.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('anime:detail', kwargs={'slug': self.slug})

    @property
    def display_poster(self):
        # Local uploaded poster
        if self.poster:
            return self.poster.url

        # External URL (Cloudinary/Jikan)
        if self.poster_url:
            return self.poster_url

        # Default image
        return "/static/images/no-poster.jpg"

    @property
    def display_banner(self):
        # Local uploaded banner
        if self.banner:
            return self.banner.url

        # External URL
        if self.banner_url:
            return self.banner_url

        # Fallback to poster
        return self.display_poster

class AnimeRelation(models.Model):
    RELATION_TYPES = [
        ('sequel', 'Sequel'),
        ('prequel', 'Prequel'),
        ('alternative_version', 'Alternative Version'),
        ('side_story', 'Side Story'),
        ('parent_story', 'Parent Story'),
        ('spin_off', 'Spin-off'),
        ('adaptation', 'Adaptation'),
        ('other', 'Other'),
    ]
    from_anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='relations_from')
    to_anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='relations_to')
    relation_type = models.CharField(max_length=30, choices=RELATION_TYPES)

    class Meta:
        unique_together = ['from_anime', 'to_anime']

    def __str__(self):
        return f'{self.from_anime} → {self.relation_type} → {self.to_anime}'


class Collection(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to='collections/', blank=True, null=True)
    anime = models.ManyToManyField(Anime, related_name='collections')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('anime:collection_detail', kwargs={'slug': self.slug})
