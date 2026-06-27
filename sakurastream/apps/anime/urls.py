from django.urls import path
from . import views

app_name = 'anime'

urlpatterns = [
    path('', views.home, name='home'),
    path('anime/', views.anime_list, name='list'),
    path('anime/<slug:slug>/', views.anime_detail, name='detail'),
    path('genre/<slug:slug>/', views.genre_detail, name='genre_detail'),
    path('collection/<slug:slug>/', views.collection_detail, name='collection_detail'),
    path('trending/', views.trending, name='trending'),
    path('seasonal/', views.seasonal, name='seasonal'),
    path('upcoming/', views.upcoming, name='upcoming'),
    path('search/suggestions/', views.search_suggestions, name='search_suggestions'),
]
