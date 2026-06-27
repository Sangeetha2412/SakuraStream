from django.contrib.sitemaps import Sitemap
from .models import Anime


class AnimeSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Anime.objects.all()

    def lastmod(self, obj):
        return obj.updated_at
