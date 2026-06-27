from django.db import models
from apps.users.models import User
from apps.anime.models import Anime


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=200)
    content = models.TextField()
    score = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)])
    is_recommended = models.BooleanField(default=True)
    likes = models.ManyToManyField(User, related_name='liked_reviews', blank=True)
    is_spoiler = models.BooleanField(default=False)
    helpful_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'anime']
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} review of {self.anime.title}'

    @property
    def like_count(self):
        return self.likes.count()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=1000)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.user.username} comment on {self.review}'


class Discussion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discussions')
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='discussions', null=True, blank=True)
    title = models.CharField(max_length=300)
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='liked_discussions', blank=True)
    views = models.IntegerField(default=0)
    is_pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
