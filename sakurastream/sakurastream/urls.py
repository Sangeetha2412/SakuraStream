from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from apps.anime.sitemaps import AnimeSitemap

sitemaps = {'anime': AnimeSitemap}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.anime.urls')),
    path('characters/', include('apps.characters.urls')),
    path('users/', include('apps.users.urls')),
    path('watchlist/', include('apps.watchlist.urls')),
    path('community/', include('apps.community.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('recommendations/', include('apps.recommendations.urls')),
    path('api/', include('apps.anime.api_urls')),
    path('api/characters/', include('apps.characters.api_urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = '🌸 SakuraStream Admin'
admin.site.site_title = 'SakuraStream'
admin.site.index_title = 'Control Panel'
