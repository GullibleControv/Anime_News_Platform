"""
Tests for REST API endpoints.

TDD Approach: Tests verify that the API returns correct JSON responses.
"""

import pytest
from django.urls import reverse

from news.models import Article


@pytest.mark.django_db
class TestAPIArticlesList:
    """Tests for the articles list API endpoint."""

    def test_api_articles_list_returns_json(self, client, sample_article):
        """Test that API returns JSON response."""
        response = client.get('/api/articles/')
        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'

    def test_api_articles_list_structure(self, client, sample_article):
        """Test that API response has correct structure."""
        response = client.get('/api/articles/')
        data = response.json()

        assert 'success' in data
        assert data['success'] is True
        assert 'data' in data
        assert 'pagination' in data

    def test_api_articles_list_article_fields(self, client, sample_article):
        """Test that articles have all expected fields."""
        response = client.get('/api/articles/')
        data = response.json()
        article = data['data'][0]

        expected_fields = [
            'id', 'title', 'content', 'category', 'category_display',
            'published_date', 'image_url', 'source_url', 'view_count',
            'is_featured', 'reading_time'
        ]
        for field in expected_fields:
            assert field in article, f"Missing field: {field}"

    def test_api_articles_pagination(self, client, multiple_articles):
        """Test that pagination info is correct."""
        response = client.get('/api/articles/')
        data = response.json()
        pagination = data['pagination']

        assert 'page' in pagination
        assert 'total_pages' in pagination
        assert 'total_count' in pagination
        assert 'has_next' in pagination
        assert 'has_previous' in pagination

    def test_api_articles_filter_by_category(self, client, multiple_articles):
        """Test filtering articles by category."""
        response = client.get('/api/articles/?category=NEWS')
        data = response.json()

        for article in data['data']:
            assert article['category'] == 'NEWS'

    def test_api_articles_filter_by_featured(self, client, featured_article):
        """Test filtering by featured status."""
        response = client.get('/api/articles/?featured=true')
        data = response.json()

        for article in data['data']:
            assert article['is_featured'] is True


@pytest.mark.django_db
class TestAPIArticleDetail:
    """Tests for the article detail API endpoint."""

    def test_api_article_detail_returns_json(self, client, sample_article):
        """Test that API returns JSON response."""
        response = client.get(f'/api/articles/{sample_article.id}/')
        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'

    def test_api_article_detail_data(self, client, sample_article):
        """Test that article detail contains correct data."""
        response = client.get(f'/api/articles/{sample_article.id}/')
        data = response.json()

        assert data['success'] is True
        assert data['data']['id'] == sample_article.id
        assert data['data']['title'] == sample_article.title

    def test_api_article_detail_404(self, client, db):
        """Test that non-existent article returns 404."""
        response = client.get('/api/articles/99999/')
        assert response.status_code == 404

        data = response.json()
        assert data['success'] is False
        assert 'error' in data


@pytest.mark.django_db
class TestAPISearch:
    """Tests for the search API endpoint."""

    def test_api_search_returns_json(self, client, sample_article):
        """Test that search API returns JSON response."""
        response = client.get('/api/search/?q=test')
        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'

    def test_api_search_results(self, client, sample_article):
        """Test that search returns matching results."""
        response = client.get('/api/search/?q=test')
        data = response.json()

        assert data['success'] is True
        assert 'data' in data
        assert 'query' in data
        assert len(data['data']) > 0

    def test_api_search_query_too_short(self, client, sample_article):
        """Test that short queries return error."""
        response = client.get('/api/search/?q=a')
        data = response.json()

        assert response.status_code == 400
        assert data['success'] is False
        assert 'error' in data

    def test_api_search_empty_query(self, client, sample_article):
        """Test that empty query returns error."""
        response = client.get('/api/search/?q=')
        data = response.json()

        assert response.status_code == 400
        assert data['success'] is False


@pytest.mark.django_db
class TestAPICategories:
    """Tests for the categories API endpoint."""

    def test_api_categories_returns_json(self, client):
        """Test that categories API returns JSON response."""
        response = client.get('/api/categories/')
        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'

    def test_api_categories_list(self, client):
        """Test that categories list is complete."""
        response = client.get('/api/categories/')
        data = response.json()

        assert data['success'] is True
        categories = data['data']

        # Should have all 4 categories
        codes = [c['code'] for c in categories]
        assert 'NEWS' in codes
        assert 'REVIEW' in codes
        assert 'MERCH' in codes
        assert 'EVENT' in codes


@pytest.mark.django_db
class TestAPIStats:
    """Tests for the stats API endpoint."""

    def test_api_stats_returns_json(self, client, sample_article):
        """Test that stats API returns JSON response."""
        response = client.get('/api/stats/')
        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'

    def test_api_stats_structure(self, client, sample_article):
        """Test that stats have correct structure."""
        response = client.get('/api/stats/')
        data = response.json()

        assert data['success'] is True
        stats = data['data']

        assert 'total_articles' in stats
        assert 'total_views' in stats
        assert 'total_categories' in stats
        assert 'articles_by_category' in stats

    def test_api_stats_values(self, client, multiple_articles):
        """Test that stats have correct values."""
        response = client.get('/api/stats/')
        data = response.json()
        stats = data['data']

        assert stats['total_articles'] == 15
        assert stats['total_categories'] == 4
