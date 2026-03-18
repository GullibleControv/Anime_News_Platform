"""
Management command to run the APScheduler for automatic news fetching.

Usage:
    python manage.py runapscheduler

This will start a background scheduler that fetches news every 6 hours.
"""

import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import Article
from news.services.news_fetcher import AnimaNewsFetcher

logger = logging.getLogger(__name__)


def fetch_anime_news():
    """
    Scheduled job to fetch anime news from external sources.
    Runs every 6 hours by default.
    """
    logger.info("Starting scheduled news fetch...")

    try:
        fetcher = AnimaNewsFetcher()
        articles_data = fetcher.fetch_news(limit=15)

        created_count = 0
        for data in articles_data:
            # Check if article already exists
            if Article.objects.filter(title=data['title']).exists():
                continue

            try:
                Article.objects.create(
                    title=data['title'],
                    content=data['content'],
                    category=data['category'],
                    image_url=data.get('image_url'),
                    view_count=0,
                    is_featured=False,
                )
                created_count += 1
            except Exception as e:
                logger.warning(f"Failed to create article: {e}")

        # Update featured article to the most recent
        if created_count > 0:
            latest = Article.objects.order_by('-published_date').first()
            if latest:
                Article.objects.update(is_featured=False)
                latest.is_featured = True
                latest.save(update_fields=['is_featured'])

        logger.info(f"Scheduled news fetch complete. Created {created_count} new articles.")

    except Exception as e:
        logger.error(f"Scheduled news fetch failed: {e}")


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    Delete job execution entries older than `max_age` seconds (default: 7 days).
    This prevents the database from filling up with old execution records.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler for automatic news fetching."

    def add_arguments(self, parser):
        parser.add_argument(
            '--interval',
            type=int,
            default=6,
            help='News fetch interval in hours (default: 6)'
        )

    def handle(self, *args, **options):
        interval_hours = options['interval']

        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # Add job to fetch news periodically
        scheduler.add_job(
            fetch_anime_news,
            trigger=IntervalTrigger(hours=interval_hours),
            id="fetch_anime_news",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(f"Added job 'fetch_anime_news' to run every {interval_hours} hours.")

        # Add job to clean up old job executions
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="sun", hour="00", minute="00"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job to delete old job executions.")

        # Run fetch immediately on startup
        self.stdout.write("Running initial news fetch...")
        fetch_anime_news()

        try:
            self.stdout.write(self.style.SUCCESS(
                f"Scheduler started! News will update every {interval_hours} hours."
            ))
            self.stdout.write("Press Ctrl+C to stop.")
            scheduler.start()
        except KeyboardInterrupt:
            self.stdout.write("Stopping scheduler...")
            scheduler.shutdown()
            self.stdout.write(self.style.SUCCESS("Scheduler stopped."))
