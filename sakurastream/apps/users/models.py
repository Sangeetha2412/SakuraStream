from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.urls import reverse
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    display_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    avatar_url = models.URLField(blank=True)
    banner = models.ImageField(upload_to='user_banners/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True)
    password_reset_token = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'username': self.username})

    @property
    def display_avatar(self):
        if self.avatar:
            return self.avatar.url
        return self.avatar_url or '/static/images/default-avatar.jpg'

    @property
    def level_title(self):
        titles = {
            1: 'Anime Newcomer', 2: 'Casual Watcher', 3: 'Anime Fan',
            4: 'Anime Enthusiast', 5: 'Otaku', 6: 'Anime Veteran',
            7: 'Anime Expert', 8: 'Anime Sage', 9: 'Sakura Master', 10: 'Otaku Legend'
        }
        lvl = min(self.level, 10)
        return titles.get(lvl, 'Otaku Legend')

    @property
    def xp_to_next_level(self):
        return self.level * 500

    @property
    def xp_progress_percent(self):
        next_level_xp = self.xp_to_next_level
        current_level_xp = (self.level - 1) * 500
        progress_xp = self.xp - current_level_xp
        return min(int((progress_xp / (next_level_xp - current_level_xp)) * 100), 100)

    def add_xp(self, amount):
        self.xp += amount
        while self.xp >= self.level * 500:
            self.xp -= self.level * 500
            self.level += 1
        self.save()


class Achievement(models.Model):
    RARITY_CHOICES = [
        ('common', 'Common'),
        ('uncommon', 'Uncommon'),
        ('rare', 'Rare'),
        ('epic', 'Epic'),
        ('legendary', 'Legendary'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)
    rarity = models.CharField(max_length=20, choices=RARITY_CHOICES, default='common')
    xp_reward = models.IntegerField(default=50)
    users = models.ManyToManyField(User, through='UserAchievement', related_name='achievements')

    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'achievement']


class UserFavorite(models.Model):
    from apps.anime.models import Anime
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    anime = models.ForeignKey('anime.Anime', on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'anime']
        ordering = ['-added_at']


class UserActivity(models.Model):
    ACTIVITY_TYPES = [
        ('watched', 'Watched Episode'),
        ('completed', 'Completed Anime'),
        ('started', 'Started Watching'),
        ('reviewed', 'Wrote Review'),
        ('favorited', 'Favorited Anime'),
        ('achievement', 'Earned Achievement'),
        ('leveled_up', 'Leveled Up'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    message = models.CharField(max_length=300)
    anime = models.ForeignKey('anime.Anime', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
