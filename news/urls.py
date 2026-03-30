from django.urls import path

from . import views
from . import api

urlpatterns = [
    # Page views
    path('', views.home, name='home'),
    path('article/<int:article_id>/', views.detail, name='detail'),
    path('article/<int:article_id>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('search/', views.search, name='search'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe'),
    path('profile/', views.profile, name='profile'),

    # REST API endpoints
    path('api/articles/', api.api_articles_list, name='api_articles_list'),
    path('api/articles/<int:article_id>/', api.api_article_detail, name='api_article_detail'),
    path('api/search/', api.api_search, name='api_search'),
    path('api/categories/', api.api_categories, name='api_categories'),
    path('api/stats/', api.api_stats, name='api_stats'),
]
