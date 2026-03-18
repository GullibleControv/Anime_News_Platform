import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestHomeView:
    """Tests for the home view."""

    def test_home_page_loads(self, client):
        """Test that the home page loads successfully."""
        response = client.get(reverse('home'))
        assert response.status_code == 200

    def test_home_page_uses_correct_template(self, client):
        """Test that home page uses the correct template."""
        response = client.get(reverse('home'))
        assert 'news/home.html' in [t.name for t in response.templates]

    def test_home_page_shows_articles(self, client, sample_article):
        """Test that home page displays articles."""
        response = client.get(reverse('home'))
        assert sample_article.title in response.content.decode()

    def test_home_page_pagination(self, client, multiple_articles):
        """Test that home page is paginated."""
        response = client.get(reverse('home'))
        assert response.status_code == 200
        # Should have pagination context
        assert 'articles' in response.context

    def test_home_page_category_filter(self, client, multiple_articles):
        """Test category filtering on home page."""
        response = client.get(reverse('home') + '?category=NEWS')
        assert response.status_code == 200
        # All visible articles should be NEWS category
        for article in response.context['articles']:
            assert article.category == 'NEWS'

    def test_home_page_htmx_request(self, client, sample_article):
        """Test HTMX request returns partial template."""
        response = client.get(
            reverse('home'),
            HTTP_HX_REQUEST='true'
        )
        assert response.status_code == 200
        # Should return partial template (no full HTML structure)
        content = response.content.decode()
        assert '<!DOCTYPE html>' not in content

    def test_home_page_categories_in_context(self, client):
        """Test that categories are passed to template."""
        response = client.get(reverse('home'))
        assert 'categories' in response.context

    def test_home_page_empty_category_shows_all(self, client, multiple_articles):
        """Test that no category filter shows all articles."""
        response = client.get(reverse('home'))
        # Should have articles from multiple categories
        categories = set(a.category for a in response.context['articles'])
        assert len(categories) > 1


@pytest.mark.django_db
class TestDetailView:
    """Tests for the detail view."""

    def test_detail_page_loads(self, client, sample_article):
        """Test that detail page loads successfully."""
        response = client.get(reverse('detail', args=[sample_article.id]))
        assert response.status_code == 200

    def test_detail_page_uses_correct_template(self, client, sample_article):
        """Test that detail page uses the correct template."""
        response = client.get(reverse('detail', args=[sample_article.id]))
        assert 'news/detail.html' in [t.name for t in response.templates]

    def test_detail_page_shows_article_content(self, client, sample_article):
        """Test that detail page shows article content."""
        response = client.get(reverse('detail', args=[sample_article.id]))
        content = response.content.decode()
        assert sample_article.title in content
        assert sample_article.content in content

    def test_detail_page_404_for_nonexistent(self, client, db):
        """Test that detail page returns 404 for non-existent article."""
        response = client.get(reverse('detail', args=[99999]))
        assert response.status_code == 404

    def test_detail_page_shows_related_articles(self, client, news_articles):
        """Test that detail page shows related articles."""
        article = news_articles[0]
        response = client.get(reverse('detail', args=[article.id]))
        assert 'related_articles' in response.context
        # Related articles should be same category but not the current one
        for related in response.context['related_articles']:
            assert related.category == article.category
            assert related.id != article.id

    def test_detail_page_htmx_request(self, client, sample_article):
        """Test HTMX request on detail page."""
        response = client.get(
            reverse('detail', args=[sample_article.id]),
            HTTP_HX_REQUEST='true'
        )
        assert response.status_code == 200


@pytest.mark.django_db
class TestSearchView:
    """Tests for the search view."""

    def test_search_page_loads(self, client):
        """Test that search page loads successfully."""
        response = client.get(reverse('search'))
        assert response.status_code == 200

    def test_search_returns_results(self, client, sample_article):
        """Test that search returns matching results."""
        response = client.get(reverse('search') + '?q=Test')
        assert response.status_code == 200
        assert sample_article in response.context['articles']

    def test_search_no_results(self, client, sample_article):
        """Test search with no matching results."""
        response = client.get(reverse('search') + '?q=xyznonexistent')
        assert response.status_code == 200
        assert len(response.context['articles']) == 0

    def test_search_empty_query(self, client, sample_article):
        """Test search with empty query."""
        response = client.get(reverse('search') + '?q=')
        assert response.status_code == 200
        assert len(response.context['articles']) == 0

    def test_search_htmx_request(self, client, sample_article):
        """Test HTMX search request returns partial."""
        response = client.get(
            reverse('search') + '?q=Test',
            HTTP_HX_REQUEST='true'
        )
        assert response.status_code == 200
        content = response.content.decode()
        # Should return partial template
        assert '<!DOCTYPE html>' not in content

    def test_search_by_title(self, client, db):
        """Test searching by article title."""
        from news.models import Article
        Article.objects.create(
            title="Unique Title XYZ",
            content="Some content",
            category="NEWS"
        )
        response = client.get(reverse('search') + '?q=Unique Title XYZ')
        assert response.context['articles'].count() == 1

    def test_search_by_content(self, client, db):
        """Test searching by article content."""
        from news.models import Article
        Article.objects.create(
            title="Regular Title",
            content="Special unique content ABC123",
            category="NEWS"
        )
        response = client.get(reverse('search') + '?q=ABC123')
        assert response.context['articles'].count() == 1

    def test_search_case_insensitive(self, client, sample_article):
        """Test that search is case insensitive."""
        response_lower = client.get(reverse('search') + '?q=test')
        response_upper = client.get(reverse('search') + '?q=TEST')

        assert response_lower.context['articles'].count() == response_upper.context['articles'].count()


@pytest.mark.django_db
class TestURLRouting:
    """Tests for URL routing."""

    def test_home_url_resolves(self, client):
        """Test home URL resolves correctly."""
        response = client.get('/')
        assert response.status_code == 200

    def test_detail_url_resolves(self, client, sample_article):
        """Test detail URL resolves correctly."""
        response = client.get(f'/article/{sample_article.id}/')
        assert response.status_code == 200

    def test_search_url_resolves(self, client):
        """Test search URL resolves correctly."""
        response = client.get('/search/')
        assert response.status_code == 200

    def test_admin_url_resolves(self, client):
        """Test admin URL resolves correctly."""
        response = client.get('/admin/')
        # Should redirect to login (302) or show login page (200)
        assert response.status_code in [200, 302]


@pytest.mark.django_db
class TestNewsletterSubscription:
    """Tests for newsletter subscription functionality."""

    def test_subscribe_success(self, client):
        """Test successful newsletter subscription."""
        response = client.post(
            reverse('subscribe'),
            {'email': 'test@example.com'}
        )
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True

    def test_subscribe_duplicate_email(self, client):
        """Test subscribing with an already registered email."""
        from news.models import NewsletterSubscription
        NewsletterSubscription.objects.create(email='existing@example.com')

        response = client.post(
            reverse('subscribe'),
            {'email': 'existing@example.com'}
        )
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert 'already subscribed' in data['message'].lower()

    def test_subscribe_empty_email(self, client):
        """Test subscribing with empty email."""
        response = client.post(
            reverse('subscribe'),
            {'email': ''}
        )
        assert response.status_code == 400
        data = response.json()
        assert data['success'] is False

    def test_subscribe_get_not_allowed(self, client):
        """Test that GET requests are not allowed for subscribe."""
        response = client.get(reverse('subscribe'))
        assert response.status_code == 405


@pytest.mark.django_db
class TestViewCount:
    """Tests for view count functionality."""

    def test_view_count_increments(self, client, sample_article):
        """Test that view count increments when viewing article."""
        initial_count = sample_article.view_count
        client.get(reverse('detail', args=[sample_article.id]))

        sample_article.refresh_from_db()
        assert sample_article.view_count == initial_count + 1

    def test_multiple_views_increment(self, client, sample_article):
        """Test that multiple views increment count correctly."""
        initial_count = sample_article.view_count

        for _ in range(5):
            client.get(reverse('detail', args=[sample_article.id]))

        sample_article.refresh_from_db()
        assert sample_article.view_count == initial_count + 5


@pytest.mark.django_db
class TestHomePageEnhancements:
    """Tests for Phase 2 home page enhancements."""

    def test_home_page_has_featured_article(self, client, featured_article):
        """Test that home page shows featured article."""
        response = client.get(reverse('home'))
        assert 'featured_article' in response.context
        assert response.context['featured_article'] == featured_article

    def test_home_page_has_trending_articles(self, client, multiple_articles):
        """Test that home page has trending articles."""
        response = client.get(reverse('home'))
        assert 'trending_articles' in response.context

    def test_home_page_has_recent_articles(self, client, multiple_articles):
        """Test that home page has recent articles."""
        response = client.get(reverse('home'))
        assert 'recent_articles' in response.context

    def test_home_page_has_stats(self, client, multiple_articles):
        """Test that home page has stats data."""
        response = client.get(reverse('home'))
        assert 'total_articles' in response.context
        assert 'total_views' in response.context
        assert 'total_categories' in response.context
