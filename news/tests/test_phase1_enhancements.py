"""
Tests for Phase 1 Enhancements: Type hints, Admin, Caching

TDD Approach: Write tests FIRST (RED), then implement (GREEN), then refactor.
"""

import pytest
from django.urls import reverse
from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory
from typing import get_type_hints

from news.models import Article, NewsletterSubscription, Bookmark
from news import views
from news.admin import ArticleAdmin, NewsletterSubscriptionAdmin, BookmarkAdmin


class TestTypeHints:
    """Test that all view functions have proper type hints."""

    def test_home_view_has_type_hints(self):
        """Test home view has type annotations."""
        hints = get_type_hints(views.home)
        assert 'request' in hints, "home() should have type hint for 'request' parameter"
        assert 'return' in hints, "home() should have return type hint"

    def test_detail_view_has_type_hints(self):
        """Test detail view has type annotations."""
        hints = get_type_hints(views.detail)
        assert 'request' in hints, "detail() should have type hint for 'request' parameter"
        assert 'article_id' in hints, "detail() should have type hint for 'article_id' parameter"
        assert 'return' in hints, "detail() should have return type hint"

    def test_search_view_has_type_hints(self):
        """Test search view has type annotations."""
        hints = get_type_hints(views.search)
        assert 'request' in hints, "search() should have type hint for 'request' parameter"
        assert 'return' in hints, "search() should have return type hint"

    def test_subscribe_newsletter_has_type_hints(self):
        """Test subscribe_newsletter view has type annotations."""
        hints = get_type_hints(views.subscribe_newsletter)
        assert 'request' in hints, "subscribe_newsletter() should have type hint for 'request' parameter"
        assert 'return' in hints, "subscribe_newsletter() should have return type hint"

    def test_toggle_bookmark_has_type_hints(self):
        """Test toggle_bookmark view has type annotations."""
        hints = get_type_hints(views.toggle_bookmark)
        assert 'request' in hints, "toggle_bookmark() should have type hint for 'request' parameter"
        assert 'article_id' in hints, "toggle_bookmark() should have type hint for 'article_id' parameter"
        assert 'return' in hints, "toggle_bookmark() should have return type hint"

    def test_profile_view_has_type_hints(self):
        """Test profile view has type annotations."""
        hints = get_type_hints(views.profile)
        assert 'request' in hints, "profile() should have type hint for 'request' parameter"
        assert 'return' in hints, "profile() should have return type hint"

    def test_handler404_has_type_hints(self):
        """Test handler404 has type annotations."""
        hints = get_type_hints(views.handler404)
        assert 'request' in hints, "handler404() should have type hint for 'request' parameter"
        assert 'return' in hints, "handler404() should have return type hint"

    def test_handler500_has_type_hints(self):
        """Test handler500 has type annotations."""
        hints = get_type_hints(views.handler500)
        assert 'request' in hints, "handler500() should have type hint for 'request' parameter"
        assert 'return' in hints, "handler500() should have return type hint"


@pytest.mark.django_db
class TestAdminEnhancements:
    """Test enhanced admin panel configuration."""

    def test_article_admin_list_display(self):
        """Test ArticleAdmin has enhanced list_display."""
        admin = ArticleAdmin(Article, AdminSite())
        expected_fields = ['title', 'category', 'published_date', 'view_count', 'is_featured']
        for field in expected_fields:
            assert field in admin.list_display, f"{field} should be in ArticleAdmin.list_display"

    def test_article_admin_list_filter(self):
        """Test ArticleAdmin has proper filters."""
        admin = ArticleAdmin(Article, AdminSite())
        expected_filters = ['category', 'is_featured', 'published_date']
        for field in expected_filters:
            assert field in admin.list_filter, f"{field} should be in ArticleAdmin.list_filter"

    def test_article_admin_list_editable(self):
        """Test ArticleAdmin has editable fields."""
        admin = ArticleAdmin(Article, AdminSite())
        assert hasattr(admin, 'list_editable'), "ArticleAdmin should have list_editable"
        assert 'is_featured' in admin.list_editable, "is_featured should be editable in list view"

    def test_article_admin_search_fields(self):
        """Test ArticleAdmin has proper search fields."""
        admin = ArticleAdmin(Article, AdminSite())
        expected_search = ['title', 'content']
        for field in expected_search:
            assert field in admin.search_fields, f"{field} should be in ArticleAdmin.search_fields"

    def test_article_admin_ordering(self):
        """Test ArticleAdmin has ordering defined."""
        admin = ArticleAdmin(Article, AdminSite())
        assert hasattr(admin, 'ordering'), "ArticleAdmin should have ordering"
        assert admin.ordering == ['-published_date'], "Articles should be ordered by newest first"

    def test_article_admin_date_hierarchy(self):
        """Test ArticleAdmin has date_hierarchy for quick navigation."""
        admin = ArticleAdmin(Article, AdminSite())
        assert hasattr(admin, 'date_hierarchy'), "ArticleAdmin should have date_hierarchy"
        assert admin.date_hierarchy == 'published_date', "date_hierarchy should be published_date"

    def test_newsletter_subscription_admin_exists(self):
        """Test NewsletterSubscriptionAdmin is registered."""
        admin = NewsletterSubscriptionAdmin(NewsletterSubscription, AdminSite())
        assert admin is not None

    def test_newsletter_subscription_admin_list_display(self):
        """Test NewsletterSubscriptionAdmin has proper list_display."""
        admin = NewsletterSubscriptionAdmin(NewsletterSubscription, AdminSite())
        expected_fields = ['email', 'subscribed_at', 'is_active']
        for field in expected_fields:
            assert field in admin.list_display, f"{field} should be in NewsletterSubscriptionAdmin.list_display"

    def test_newsletter_subscription_admin_list_filter(self):
        """Test NewsletterSubscriptionAdmin has proper filters."""
        admin = NewsletterSubscriptionAdmin(NewsletterSubscription, AdminSite())
        assert 'is_active' in admin.list_filter, "is_active should be a filter"
        assert 'subscribed_at' in admin.list_filter, "subscribed_at should be a filter"

    def test_bookmark_admin_exists(self):
        """Test BookmarkAdmin is registered."""
        admin = BookmarkAdmin(Bookmark, AdminSite())
        assert admin is not None

    def test_bookmark_admin_list_display(self):
        """Test BookmarkAdmin has proper list_display."""
        admin = BookmarkAdmin(Bookmark, AdminSite())
        expected_fields = ['user', 'article', 'created_at']
        for field in expected_fields:
            assert field in admin.list_display, f"{field} should be in BookmarkAdmin.list_display"

    def test_bookmark_admin_list_filter(self):
        """Test BookmarkAdmin has proper filters."""
        admin = BookmarkAdmin(Bookmark, AdminSite())
        assert 'created_at' in admin.list_filter, "created_at should be a filter"


@pytest.mark.django_db
class TestCaching:
    """Test caching functionality for homepage stats."""

    def test_home_page_stats_are_cached(self, client, multiple_articles):
        """Test that homepage stats use caching."""
        from django.core.cache import cache

        # Clear cache first
        cache.clear()

        # First request - should set cache
        response1 = client.get(reverse('home'))
        assert response1.status_code == 200

        # Check that cache was set
        cached_stats = cache.get('homepage_stats')
        # Note: This test will fail initially (RED) until we implement caching
        assert cached_stats is not None, "Homepage stats should be cached"

    def test_cache_contains_expected_keys(self, client, multiple_articles):
        """Test that cached stats contain expected data."""
        from django.core.cache import cache

        cache.clear()
        client.get(reverse('home'))

        cached_stats = cache.get('homepage_stats')
        assert cached_stats is not None
        assert 'total_articles' in cached_stats
        assert 'total_views' in cached_stats

    def test_cache_invalidation_on_new_article(self, client, db):
        """Test that cache is invalidated when a new article is created."""
        from django.core.cache import cache

        cache.clear()

        # Create initial article and visit home to set cache
        Article.objects.create(title="Initial", content="Content", category="NEWS")
        client.get(reverse('home'))

        initial_stats = cache.get('homepage_stats')
        initial_count = initial_stats['total_articles'] if initial_stats else 0

        # Create another article (should invalidate cache via signal)
        Article.objects.create(title="New Article", content="New Content", category="NEWS")

        # Visit home again
        client.get(reverse('home'))

        new_stats = cache.get('homepage_stats')
        # After invalidation, the new count should be updated
        assert new_stats['total_articles'] == initial_count + 1


@pytest.mark.django_db
class TestErrorHandling:
    """Test enhanced error handling with logging."""

    def test_subscribe_logs_error_on_exception(self, client, mocker):
        """Test that subscribe_newsletter logs errors properly."""
        # Mock the model to raise an exception
        mocker.patch(
            'news.views.NewsletterSubscription.objects.get_or_create',
            side_effect=Exception("Database error")
        )

        mock_logger = mocker.patch('news.views.logger')

        response = client.post(
            reverse('subscribe'),
            {'email': 'test@example.com'}
        )

        assert response.status_code == 500
        # Should log the error with exc_info for stack trace
        mock_logger.error.assert_called()


@pytest.mark.django_db
class TestSourceUrlField:
    """Test source_url field on Article model (Phase 2 prep)."""

    def test_article_has_source_url_field(self):
        """Test that Article model has source_url field."""
        assert hasattr(Article, 'source_url'), "Article should have source_url field"

    def test_article_source_url_is_optional(self, db):
        """Test that source_url can be blank."""
        article = Article.objects.create(
            title="Test Article",
            content="Test content",
            category="NEWS"
        )
        assert article.source_url is None or article.source_url == ""

    def test_article_source_url_stores_value(self, db):
        """Test that source_url properly stores URLs."""
        article = Article.objects.create(
            title="Test Article",
            content="Test content",
            category="NEWS",
            source_url="https://example.com/article"
        )
        assert article.source_url == "https://example.com/article"

    def test_detail_page_shows_source_url(self, client, db):
        """Test that detail page displays source URL when available."""
        article = Article.objects.create(
            title="Test Article",
            content="Test content",
            category="NEWS",
            source_url="https://example.com/source"
        )

        response = client.get(reverse('detail', args=[article.id]))
        content = response.content.decode()

        # Source URL should be displayed somewhere on the page
        assert 'example.com' in content or 'Source' in content
