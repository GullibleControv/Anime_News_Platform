import pytest
from django.utils import timezone

from news.models import Article


@pytest.mark.django_db
class TestArticleModel:
    """Tests for the Article model."""

    def test_article_creation(self):
        """Test that an article can be created."""
        article = Article.objects.create(
            title="Test Title",
            content="Test Content",
            category="NEWS"
        )
        assert article.pk is not None
        assert article.title == "Test Title"
        assert article.content == "Test Content"
        assert article.category == "NEWS"

    def test_article_str_representation(self):
        """Test the string representation of an article."""
        article = Article.objects.create(
            title="My Article Title",
            content="Content",
            category="NEWS"
        )
        assert str(article) == "My Article Title"

    def test_article_category_choices(self):
        """Test that category choices are valid."""
        valid_categories = ["NEWS", "REVIEW", "MERCH", "EVENT"]

        for category in valid_categories:
            article = Article.objects.create(
                title=f"Test {category}",
                content="Content",
                category=category
            )
            assert article.category == category

    def test_article_category_display(self):
        """Test get_category_display method."""
        article = Article.objects.create(
            title="Test",
            content="Content",
            category="REVIEW"
        )
        assert article.get_category_display() == "Review"

    def test_article_published_date_auto_now(self):
        """Test that published_date is automatically set."""
        article = Article.objects.create(
            title="Test",
            content="Content",
            category="NEWS"
        )
        assert article.published_date is not None
        assert article.published_date <= timezone.now()

    def test_article_image_url_optional(self):
        """Test that image_url is optional."""
        article = Article.objects.create(
            title="Test",
            content="Content",
            category="NEWS"
        )
        assert article.image_url is None or article.image_url == ""

    def test_article_with_image_url(self):
        """Test article with image URL."""
        url = "https://example.com/image.jpg"
        article = Article.objects.create(
            title="Test",
            content="Content",
            category="NEWS",
            image_url=url
        )
        assert article.image_url == url

    def test_article_ordering(self, multiple_articles):
        """Test that articles are ordered by published_date descending."""
        articles = Article.objects.all().order_by('-published_date')
        for i in range(len(articles) - 1):
            assert articles[i].published_date >= articles[i + 1].published_date

    def test_article_filter_by_category(self, multiple_articles):
        """Test filtering articles by category."""
        news_articles = Article.objects.filter(category="NEWS")
        review_articles = Article.objects.filter(category="REVIEW")

        assert news_articles.count() > 0
        assert review_articles.count() > 0

        for article in news_articles:
            assert article.category == "NEWS"

    def test_article_title_max_length(self):
        """Test article title max length constraint."""
        long_title = "A" * 200  # Max length is 200
        article = Article.objects.create(
            title=long_title,
            content="Content",
            category="NEWS"
        )
        assert len(article.title) == 200
