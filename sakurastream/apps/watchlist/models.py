from django.db import models
from apps.users.models import User
from apps.anime.models import Anime


class WatchlistEntry(models.Model):
    STATUS_CHOICES = [
        ('watching', 'Currently Watching'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('dropped', 'Dropped'),
        ('plan_to_watch', 'Plan to Watch'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='watchlisted_by')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='plan_to_watch')
    episodes_watched = models.IntegerField(default=0)
    score = models.IntegerField(null=True, blank=True, choices=[(i, str(i)) for i in range(1, 11)])
    notes = models.TextField(blank=True)
    is_favorite = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'anime']
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.user.username} - {self.anime.title} ({self.status})'

    @property
    def progress_percent(self):
        if self.anime.episodes and self.anime.episodes > 0:
            return min(int((self.episodes_watched / self.anime.episodes) * 100), 100)
        return 0
