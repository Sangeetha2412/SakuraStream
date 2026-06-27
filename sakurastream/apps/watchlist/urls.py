from django.urls import path
from . import views

app_name = 'watchlist'

urlpatterns = [
    path('', views.watchlist, name='list'),
    path('toggle/<slug:anime_slug>/', views.toggle_watchlist, name='toggle'),
    path('update/<int:entry_id>/', views.update_progress, name='update_progress'),
]
