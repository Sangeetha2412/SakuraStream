from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.community_home, name='home'),
    path('review/<slug:anime_slug>/', views.submit_review, name='submit_review'),
    path('review/<int:review_id>/like/', views.like_review, name='like_review'),
]
