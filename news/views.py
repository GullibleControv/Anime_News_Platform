import logging

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Article, NewsletterSubscription, Bookmark

logger = logging.getLogger(__name__)

ARTICLES_PER_PAGE = 9


def home(request):
    """Homepage with featured hero, stats, and sidebar."""
    category = request.GET.get('category')
    page = request.GET.get('page', 1)

    # Featured article for hero section
    featured_article = Article.objects.filter(is_featured=True).first()
    if not featured_article:
        featured_article = Article.objects.first()

    # Base queryset excluding featured
    articles = Article.objects.all()
    if featured_article:
        articles = articles.exclude(pk=featured_article.pk)

    # Filter by category if provided
    if category and category != 'all':
        articles = articles.filter(category=category)
        logger.debug(f"Filtering articles by category: {category}")

    # Paginate results
    paginator = Paginator(articles, ARTICLES_PER_PAGE)
    page_obj = paginator.get_page(page)

    # Stats data
    total_articles = Article.objects.count()
    total_views = sum(a.view_count for a in Article.objects.all())
    category_counts = Article.objects.values('category').annotate(count=Count('category'))

    # Trending articles (by view count)
    trending_articles = Article.objects.order_by('-view_count')[:5]

    # Recent articles for sidebar
    recent_articles = Article.objects.order_by('-published_date')[:5]

    context = {
        'featured_article': featured_article,
        'articles': page_obj,
        'categories': Article.CATEGORY_CHOICES,
        'current_category': category or 'all',
        # Stats
        'total_articles': total_articles,
        'total_views': total_views,
        'total_categories': len(Article.CATEGORY_CHOICES),
        # Sidebar
        'trending_articles': trending_articles,
        'recent_articles': recent_articles,
    }

    # Return partial template for HTMX requests
    if request.headers.get('HX-Request'):
        return render(request, 'news/partials/_article_list.html', context)

    return render(request, 'news/home.html', context)


def detail(request, article_id):
    """Article detail page with related articles and reading experience."""
    article = get_object_or_404(Article, pk=article_id)

    # Increment view count
    article.increment_views()

    # Get related articles (same category, excluding current)
    related_articles = Article.objects.filter(
        category=article.category
    ).exclude(pk=article_id).order_by('-published_date')[:4]

    # Trending articles for sidebar
    trending_articles = Article.objects.order_by('-view_count').exclude(pk=article_id)[:5]

    # Check if article is bookmarked by current user
    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(
            user=request.user,
            article=article
        ).exists()

    context = {
        'article': article,
        'related_articles': related_articles,
        'trending_articles': trending_articles,
        'is_bookmarked': is_bookmarked,
    }

    # Return just the content for HTMX requests
    if request.headers.get('HX-Request'):
        return render(request, 'news/detail.html', context)

    return render(request, 'news/detail.html', context)


def search(request):
    """Search articles by title or content."""
    query = request.GET.get('q', '').strip()
    articles = Article.objects.none()

    if query:
        articles = Article.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by('-published_date')[:20]
        logger.debug(f"Search for '{query}' returned {articles.count()} results")

    context = {
        'articles': articles,
        'query': query,
    }

    # Return partial template for HTMX requests (navbar dropdown)
    if request.headers.get('HX-Request'):
        return render(request, 'news/partials/_search_results.html', context)

    return render(request, 'news/search.html', context)


@require_POST
def subscribe_newsletter(request):
    """Handle newsletter subscription."""
    email = request.POST.get('email', '').strip()

    if not email:
        return JsonResponse({'success': False, 'error': 'Email is required'}, status=400)

    try:
        subscription, created = NewsletterSubscription.objects.get_or_create(email=email)
        if created:
            logger.info(f"New newsletter subscription: {email}")
            return JsonResponse({'success': True, 'message': 'Successfully subscribed!'})
        else:
            return JsonResponse({'success': True, 'message': 'You are already subscribed!'})
    except Exception as e:
        logger.error(f"Newsletter subscription error: {e}")
        return JsonResponse({'success': False, 'error': 'Something went wrong'}, status=500)


@login_required
@require_POST
def toggle_bookmark(request, article_id):
    """Toggle bookmark status for an article."""
    article = get_object_or_404(Article, pk=article_id)

    bookmark, created = Bookmark.objects.get_or_create(
        user=request.user,
        article=article
    )

    if not created:
        # Bookmark exists, remove it
        bookmark.delete()
        is_bookmarked = False
        message = 'Bookmark removed'
    else:
        is_bookmarked = True
        message = 'Article bookmarked'

    # For HTMX requests, return just the button
    if request.headers.get('HX-Request'):
        return render(request, 'news/partials/_bookmark_button.html', {
            'article': article,
            'is_bookmarked': is_bookmarked,
        })

    return JsonResponse({
        'success': True,
        'is_bookmarked': is_bookmarked,
        'message': message,
    })


@login_required
def profile(request):
    """User profile page with bookmarked articles."""
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('article')

    context = {
        'bookmarks': bookmarks,
        'bookmark_count': bookmarks.count(),
    }

    return render(request, 'news/profile.html', context)


def handler404(request, exception):
    """Custom 404 error handler."""
    return render(request, '404.html', status=404)


def handler500(request):
    """Custom 500 error handler."""
    return render(request, '500.html', status=500)
