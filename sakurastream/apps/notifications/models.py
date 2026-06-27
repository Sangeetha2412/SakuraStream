from django.db import models
from apps.users.models import User


class Notification(models.Model):
    TYPE_CHOICES = [
        ('new_anime', 'New Anime'),
        ('episode', 'New Episode'),
        ('watchlist', 'Watchlist Reminder'),
        ('recommendation', 'Recommendation'),
        ('achievement', 'Achievement Unlocked'),
        ('review_like', 'Review Liked'),
        ('comment', 'New Comment'),
        ('system', 'System Notification'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    url = models.URLField(blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username}: {self.title}'
