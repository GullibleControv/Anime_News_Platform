from django.contrib import admin  
from django.urls import path
from news.views import home, detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('article/<int:article_id>/', detail, name='detail'),
]