from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('news.urls')),
]

# Custom error handlers
handler404 = 'news.views.handler404'
handler500 = 'news.views.handler500'
