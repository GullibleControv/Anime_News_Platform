"""
Management command to fetch real anime news from external sources.

Usage:
    python manage.py fetch_news              # Fetch 20 articles
    python manage.py fetch_news --limit=50   # Fetch 50 articles
    python manage.py fetch_news --clear      # Clear old articles first
    python manage.py fetch_news --with-images  # Also fetch article images
"""

import logging
from django.core.management.base import BaseCommand
from django.utils import timezone

from news.models import Article
from news.services.news_fetcher import AnimaNewsFetcher

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Fetch real anime news from Anime News Network'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=20,
            help='Maximum number of articles to fetch (default: 20)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing articles before fetching'
        )
        parser.add_argument(
            '--with-images',
            action='store_true',
            help='Fetch article images from source pages (slower)'
        )

    def handle(self, *args, **options):
        limit = options['limit']
        clear = options['clear']
        with_images = options['with_images']

        # Clear existing articles if requested
        if clear:
            deleted_count = Article.objects.all().delete()[0]
            self.stdout.write(
                self.style.WARNING(f'Cleared {deleted_count} existing articles')
            )

        # Initialize fetcher
        fetcher = AnimaNewsFetcher()

        self.stdout.write(f'Fetching up to {limit} articles from Anime News Network...')

        # Fetch articles
        articles_data = fetcher.fetch_news(limit=limit)

        if not articles_data:
            self.stdout.write(
                self.style.ERROR('No articles fetched. Check your internet connection.')
            )
            return

        created_count = 0
        updated_count = 0
        skipped_count = 0

        for data in articles_data:
            # Check if article already exists (by title)
            existing = Article.objects.filter(title=data['title']).first()

            if existing:
                skipped_count += 1
                continue

            # Fetch image if requested and not available
            if with_images and not data.get('image_url') and data.get('source_url'):
                self.stdout.write(f"  Fetching image for: {data['title'][:50]}...")
                data['image_url'] = fetcher.fetch_article_image(data['source_url'])

            # Create article
            try:
                article = Article.objects.create(
                    title=data['title'],
                    content=data['content'],
                    category=data['category'],
                    image_url=data.get('image_url'),
                    view_count=0,
                    is_featured=False,
                )

                # Update published_date if provided
                if data.get('published_date'):
                    article.published_date = data['published_date']
                    article.save(update_fields=['published_date'])

                created_count += 1
                self.stdout.write(f"  + {data['title'][:60]}...")

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"  Failed to create: {data['title'][:40]}... - {e}")
                )

        # Set the most recent article as featured
        latest = Article.objects.order_by('-published_date').first()
        if latest:
            Article.objects.update(is_featured=False)
            latest.is_featured = True
            latest.save(update_fields=['is_featured'])

        # Summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'Done! Created: {created_count}, Skipped (duplicates): {skipped_count}'
        ))
        self.stdout.write(f'Total articles in database: {Article.objects.count()}')
