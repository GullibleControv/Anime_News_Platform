import pytest
from django.test import Client

from news.models import Article, NewsletterSubscription


@pytest.fixture
def client():
    """Django test client."""
    return Client()


@pytest.fixture
def sample_article(db):
    """Create a single sample article."""
    return Article.objects.create(
        title="Test Anime News Article",
        content="This is test content for the article. It contains information about anime.",
        category="NEWS",
        image_url="https://example.com/image.jpg",
        view_count=100,
    )


@pytest.fixture
def featured_article(db):
    """Create a featured article for hero section."""
    return Article.objects.create(
        title="Featured Anime News Article",
        content="This is a featured article with lots of content. " * 50,
        category="NEWS",
        image_url="https://example.com/featured.jpg",
        is_featured=True,
        view_count=5000,
    )


@pytest.fixture
def multiple_articles(db):
    """Create multiple articles with different categories."""
    articles = []
    categories = ["NEWS", "REVIEW", "MERCH", "EVENT"]

    for i in range(15):
        article = Article.objects.create(
            title=f"Test Article {i + 1}",
            content=f"Content for test article number {i + 1}. This article is about anime.",
            category=categories[i % 4],
            image_url=f"https://example.com/image{i}.jpg" if i % 2 == 0 else None
        )
        articles.append(article)

    return articles


@pytest.fixture
def news_articles(db):
    """Create multiple NEWS category articles."""
    articles = []
    for i in range(5):
        article = Article.objects.create(
            title=f"News Article {i + 1}",
            content=f"News content {i + 1}",
            category="NEWS",
        )
        articles.append(article)
    return articles


@pytest.fixture
def review_articles(db):
    """Create multiple REVIEW category articles."""
    articles = []
    for i in range(3):
        article = Article.objects.create(
            title=f"Review Article {i + 1}",
            content=f"Review content {i + 1}",
            category="REVIEW",
        )
        articles.append(article)
    return articles
