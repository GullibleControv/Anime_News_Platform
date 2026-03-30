"""
Simple REST API endpoints for Anime News Platform.

These endpoints provide JSON access to article data without requiring
Django REST Framework, keeping the project lightweight.
"""

import logging
from typing import Any

from django.http import HttpRequest, JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django_ratelimit.decorators import ratelimit

from .models import Article

logger = logging.getLogger(__name__)

ARTICLES_PER_PAGE = 20


def serialize_article(article: Article) -> dict[str, Any]:
    """Serialize an Article model to a dictionary."""
    return {
        'id': article.id,
        'title': article.title,
        'content': article.content,
        'category': article.category,
        'category_display': article.get_category_display(),
        'published_date': article.published_date.isoformat(),
        'image_url': article.image_url,
        'source_url': article.source_url,
        'view_count': article.view_count,
        'is_featured': article.is_featured,
        'reading_time': article.reading_time,
    }


@ratelimit(key='ip', rate='60/m', method='GET', block=True)
def api_articles_list(request: HttpRequest) -> JsonResponse:
    """
    List all articles with pagination.

    Query parameters:
    - page: Page number (default: 1)
    - category: Filter by category (NEWS, REVIEW, MERCH, EVENT)
    - featured: Filter by featured status (true/false)

    Returns JSON with articles array and pagination metadata.
    """
    page = request.GET.get('page', '1')
    category = request.GET.get('category')
    featured = request.GET.get('featured')

    try:
        page = int(page)
    except ValueError:
        page = 1

    # Build queryset
    articles = Article.objects.all()

    if category and category in ['NEWS', 'REVIEW', 'MERCH', 'EVENT']:
        articles = articles.filter(category=category)

    if featured:
        articles = articles.filter(is_featured=featured.lower() == 'true')

    # Paginate
    paginator = Paginator(articles, ARTICLES_PER_PAGE)
    page_obj = paginator.get_page(page)

    return JsonResponse({
        'success': True,
        'data': [serialize_article(article) for article in page_obj],
        'pagination': {
            'page': page_obj.number,
            'total_pages': paginator.num_pages,
            'total_count': paginator.count,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
        }
    })


@ratelimit(key='ip', rate='60/m', method='GET', block=True)
def api_article_detail(request: HttpRequest, article_id: int) -> JsonResponse:
    """
    Get a single article by ID.

    Returns JSON with article data or 404 error.
    """
    try:
        article = Article.objects.get(pk=article_id)
        return JsonResponse({
            'success': True,
            'data': serialize_article(article)
        })
    except Article.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Article not found'
        }, status=404)


@ratelimit(key='ip', rate='30/m', method='GET', block=True)
def api_search(request: HttpRequest) -> JsonResponse:
    """
    Search articles by title or content.

    Query parameters:
    - q: Search query (required, min 2 characters)
    - page: Page number (default: 1)
    - limit: Results per page (default: 20, max: 50)

    Returns JSON with matching articles.
    """
    query = request.GET.get('q', '').strip()
    page = request.GET.get('page', '1')
    limit = request.GET.get('limit', '20')

    try:
        page = int(page)
        limit = min(int(limit), 50)  # Cap at 50
    except ValueError:
        page = 1
        limit = 20

    # Validate query
    if len(query) < 2:
        return JsonResponse({
            'success': False,
            'error': 'Query must be at least 2 characters'
        }, status=400)

    # Truncate very long queries
    if len(query) > 100:
        query = query[:100]

    # Search
    articles = Article.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query)
    ).order_by('-published_date')

    # Paginate
    paginator = Paginator(articles, limit)
    page_obj = paginator.get_page(page)

    logger.info(f"API search for '{query}' returned {paginator.count} results")

    return JsonResponse({
        'success': True,
        'query': query,
        'data': [serialize_article(article) for article in page_obj],
        'pagination': {
            'page': page_obj.number,
            'total_pages': paginator.num_pages,
            'total_count': paginator.count,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
        }
    })


@ratelimit(key='ip', rate='60/m', method='GET', block=True)
def api_categories(request: HttpRequest) -> JsonResponse:
    """
    Get list of available categories.

    Returns JSON with category codes and display names.
    """
    return JsonResponse({
        'success': True,
        'data': [
            {'code': code, 'name': name}
            for code, name in Article.CATEGORY_CHOICES
        ]
    })


@ratelimit(key='ip', rate='30/m', method='GET', block=True)
def api_stats(request: HttpRequest) -> JsonResponse:
    """
    Get site statistics.

    Returns JSON with total articles, views, and category counts.
    """
    from django.db.models import Sum, Count

    stats = Article.objects.aggregate(
        total_articles=Count('id'),
        total_views=Sum('view_count')
    )

    category_counts = Article.objects.values('category').annotate(
        count=Count('category')
    )

    return JsonResponse({
        'success': True,
        'data': {
            'total_articles': stats['total_articles'] or 0,
            'total_views': stats['total_views'] or 0,
            'total_categories': len(Article.CATEGORY_CHOICES),
            'articles_by_category': {
                item['category']: item['count']
                for item in category_counts
            }
        }
    })
