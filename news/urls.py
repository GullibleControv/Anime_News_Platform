from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('article/<int:article_id>/', views.detail, name='detail'),
    path('article/<int:article_id>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('search/', views.search, name='search'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe'),
    path('profile/', views.profile, name='profile'),
]
