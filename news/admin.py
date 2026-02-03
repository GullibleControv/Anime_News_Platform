from django.contrib import admin
from .models import Article

# CORRECTED LINE: It uses admin.ModelAdmin (no .site in the middle)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date')
    search_fields = ('title', 'content')
    list_filter = ('published_date',)

admin.site.register(Article, ArticleAdmin)