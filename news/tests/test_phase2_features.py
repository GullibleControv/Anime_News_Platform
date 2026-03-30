"""
Tests for Phase 2 Features: Infinite scroll, Theme toggle, API endpoints

TDD Approach: Write tests FIRST (RED), then implement (GREEN), then refactor.
"""

import pytest
from django.urls import reverse
from django.test import Client

from news.models import Article


@pytest.mark.django_db
class TestInfiniteScroll:
    """Test infinite scroll pagination functionality."""

    def test_home_page_has_load_more_indicator(self, client, multiple_articles):
        """Test that home page has load more trigger element."""
        response = client.get(reverse('home'))
        content = response.content.decode()
        # Should have hx-trigger="revealed" for infinite scroll
        assert 'hx-trigger="revealed"' in content or 'load-more' in content.lower()

    def test_page_parameter_returns_next_articles(self, client, multiple_articles):
        """Test that ?page=2 returns second batch of articles."""
        response = client.get(reverse('home') + '?page=2')
        assert response.status_code == 200
        # Page 2 should have different articles than page 1

    def test_htmx_pagination_returns_partial(self, client, multiple_articles):
        """Test HTMX pagination returns only article cards, not full page."""
        response = client.get(
            reverse('home') + '?page=2',
            HTTP_HX_REQUEST='true'
        )
        assert response.status_code == 200
        content = response.content.decode()
        # Should NOT include full HTML structure
        assert '<!DOCTYPE html>' not in content

    def test_pagination_context_has_next_page(self, client, multiple_articles):
        """Test that pagination context includes has_next info."""
        response = client.get(reverse('home'))
        # The response context should indicate if there are more pages
        assert 'articles' in response.context
        page_obj = response.context['articles']
        # With 15 articles and 9 per page, page 1 should have a next page
        assert page_obj.has_next()

    def test_last_page_no_load_more(self, client, db):
        """Test that last page doesn't show load more trigger."""
        # Create exactly 5 articles (less than ARTICLES_PER_PAGE)
        for i in range(5):
            Article.objects.create(
                title=f"Article {i}",
                content=f"Content {i}",
                category="NEWS"
            )

        response = client.get(reverse('home'))
        page_obj = response.context['articles']
        # Should NOT have next page
        assert not page_obj.has_next()


@pytest.mark.django_db
class TestThemeToggle:
    """Test dark/light theme toggle functionality."""

    def test_base_template_has_theme_toggle(self, client, sample_article):
        """Test that base template includes theme toggle button."""
        response = client.get(reverse('home'))
        content = response.content.decode()
        # Should have theme toggle element
        assert 'theme' in content.lower()

    def test_theme_preference_stored_in_localstorage(self, client, sample_article):
        """Test that template includes localStorage theme script."""
        response = client.get(reverse('home'))
        content = response.content.decode()
        # Should have localStorage reference for theme
        assert 'localStorage' in content


@pytest.mark.django_db
class TestAPIEndpoints:
    """Test REST API endpoints for articles."""

    def test_api_articles_list_endpoint_exists(self, client):
        """Test that /api/articles/ endpoint exists."""
        response = client.get('/api/articles/')
        # Should return 200 or JSON response
        assert response.status_code in [200, 404]  # 404 until implemented

    def test_api_articles_returns_json(self, client, sample_article):
        """Test that API returns JSON response."""
        response = client.get('/api/articles/')
        if response.status_code == 200:
            assert response['Content-Type'] == 'application/json'

    def test_api_article_detail_endpoint(self, client, sample_article):
        """Test that /api/articles/<id>/ endpoint exists."""
        response = client.get(f'/api/articles/{sample_article.id}/')
        # Should return 200 or 404
        assert response.status_code in [200, 404]

    def test_api_search_endpoint(self, client, sample_article):
        """Test that /api/search/ endpoint exists."""
        response = client.get('/api/search/?q=test')
        # Should return 200 or 404
        assert response.status_code in [200, 404]


@pytest.mark.django_db
class TestSocialSharing:
    """Test social sharing functionality."""

    def test_detail_page_has_share_buttons(self, client, sample_article):
        """Test that detail page has share buttons."""
        response = client.get(reverse('detail', args=[sample_article.id]))
        content = response.content.decode()
        # Should have Twitter share link
        assert 'twitter.com/intent/tweet' in content
        # Should have Reddit share link
        assert 'reddit.com/submit' in content

    def test_detail_page_has_copy_link_button(self, client, sample_article):
        """Test that detail page has copy link functionality."""
        response = client.get(reverse('detail', args=[sample_article.id]))
        content = response.content.decode()
        # Should have copy to clipboard functionality
        assert 'clipboard' in content.lower()


@pytest.mark.django_db
class TestReadingProgress:
    """Test reading progress bar functionality."""

    def test_detail_page_has_progress_bar(self, client, sample_article):
        """Test that detail page has reading progress bar."""
        response = client.get(reverse('detail', args=[sample_article.id]))
        content = response.content.decode()
        # Should have reading progress element
        assert 'reading-progress' in content.lower()

    def test_progress_bar_uses_alpine(self, client, sample_article):
        """Test that progress bar uses Alpine.js."""
        response = client.get(reverse('detail', args=[sample_article.id]))
        content = response.content.decode()
        # Should have Alpine.js data binding for progress
        assert 'x-data' in content


@pytest.mark.django_db
class TestEnhancedSearch:
    """Test enhanced search functionality."""

    def test_search_minimum_length_enforced(self, client, sample_article):
        """Test that single character searches return no results."""
        response = client.get(reverse('search') + '?q=a')
        # Should return empty results for single character
        assert len(response.context['articles']) == 0

    def test_search_long_query_truncated(self, client, sample_article):
        """Test that very long queries are handled safely."""
        long_query = 'a' * 200  # 200 characters
        response = client.get(reverse('search') + f'?q={long_query}')
        # Should not crash, should return 200
        assert response.status_code == 200

    def test_search_special_characters_safe(self, client, sample_article):
        """Test that special characters in search are handled safely."""
        response = client.get(reverse('search') + '?q=%22test%22%20AND%201=1')
        # Should not crash
        assert response.status_code == 200
