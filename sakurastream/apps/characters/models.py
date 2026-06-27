from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from apps.anime.models import Anime


class Character(models.Model):
    ROLE_CHOICES = [
        ('main', 'Main'),
        ('supporting', 'Supporting'),
        ('background', 'Background'),
    ]

    name = models.CharField(max_length=300)
    name_kanji = models.CharField(max_length=300, blank=True)
    slug = models.SlugField(unique=True, max_length=400)
    about = models.TextField(blank=True)
    image = models.ImageField(upload_to='characters/', blank=True, null=True)
    image_url = models.URLField(blank=True)
    favorites = models.IntegerField(default=0)
    mal_id = models.IntegerField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-favorites']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Character.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('characters:detail', kwargs={'slug': self.slug})

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        return self.image_url or '/static/images/no-character.jpg'


class AnimeCharacter(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='anime_characters')
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='character_anime')
    role = models.CharField(max_length=20, choices=Character.ROLE_CHOICES, default='supporting')
    order = models.IntegerField(default=0)

    class Meta:
        unique_together = ['anime', 'character']
        ordering = ['order']

    def __str__(self):
        return f'{self.character.name} in {self.anime.title}'


class VoiceActor(models.Model):
    LANGUAGE_CHOICES = [
        ('japanese', 'Japanese'),
        ('english', 'English'),
        ('korean', 'Korean'),
        ('spanish', 'Spanish'),
        ('french', 'French'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, max_length=400)
    image = models.ImageField(upload_to='voice_actors/', blank=True, null=True)
    image_url = models.URLField(blank=True)
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='japanese')
    favorites = models.IntegerField(default=0)
    mal_id = models.IntegerField(unique=True, null=True, blank=True)
    characters = models.ManyToManyField(Character, through='VoiceActorRole', related_name='voice_actors')

    def __str__(self):
        return f'{self.name} ({self.language})'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        return self.image_url or '/static/images/no-person.jpg'


class VoiceActorRole(models.Model):
    voice_actor = models.ForeignKey(VoiceActor, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['voice_actor', 'character', 'anime']
