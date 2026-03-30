"""
Enhanced Django Admin configuration for Anime News Platform.

Provides comprehensive admin interfaces for managing:
- Articles (with filtering, search, and inline editing)
- Newsletter subscriptions (with activity tracking)
- User bookmarks (with relationship display)
"""

from django.contrib import admin
from .models import Article, NewsletterSubscription, Bookmark


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Enhanced admin for Article model with comprehensive filtering and display."""

    list_display = ('title', 'category', 'published_date', 'view_count', 'is_featured')
    list_filter = ('category', 'is_featured', 'published_date')
    list_editable = ('is_featured',)
    search_fields = ('title', 'content')
    ordering = ['-published_date']
    date_hierarchy = 'published_date'
    readonly_fields = ('view_count', 'published_date')
    list_per_page = 25

    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'category')
        }),
        ('Media', {
            'fields': ('image_url', 'source_url'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_featured', 'view_count', 'published_date'),
        }),
    )


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    """Admin for managing newsletter subscriptions."""

    list_display = ('email', 'subscribed_at', 'is_active')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
    ordering = ['-subscribed_at']
    list_editable = ('is_active',)
    date_hierarchy = 'subscribed_at'
    list_per_page = 50

    actions = ['activate_subscriptions', 'deactivate_subscriptions']

    @admin.action(description='Activate selected subscriptions')
    def activate_subscriptions(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} subscription(s) activated.')

    @admin.action(description='Deactivate selected subscriptions')
    def deactivate_subscriptions(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} subscription(s) deactivated.')


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    """Admin for viewing user bookmarks."""

    list_display = ('user', 'article', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'article__title')
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    list_per_page = 50
    raw_id_fields = ('user', 'article')
