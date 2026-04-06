"""
Management command: send_newsletter

Sends a digest of recent anime news to all active newsletter subscribers.
Run manually or schedule via cron / APScheduler.

Usage:
    python manage.py send_newsletter
    python manage.py send_newsletter --hours 48
"""
import logging
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Send a newsletter digest of recent anime news to all active subscribers.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--hours',
            type=int,
            default=24,
            help='Include articles published in the last N hours (default: 24)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Print what would be sent without actually sending emails.',
        )

    def handle(self, *args, **options):
        from news.models import Article, NewsletterSubscription

        hours = options['hours']
        dry_run = options['dry_run']
        since = timezone.now() - timedelta(hours=hours)

        # Get recent articles
        articles = Article.objects.filter(
            published_date__gte=since
        ).order_by('-published_date')[:10]

        if not articles.exists():
            self.stdout.write(self.style.WARNING(f'No articles published in the last {hours} hours. Skipping.'))
            return

        # Get active subscribers
        subscribers = NewsletterSubscription.objects.filter(is_active=True).values_list('email', flat=True)
        subscriber_list = list(subscribers)

        if not subscriber_list:
            self.stdout.write(self.style.WARNING('No active subscribers. Skipping.'))
            return

        # Build email content
        subject = f'🎌 Anime News Digest — {timezone.now().strftime("%B %d, %Y")}'
        body = self._build_email_body(articles, hours)

        if dry_run:
            self.stdout.write(self.style.SUCCESS(f'[DRY RUN] Would send to {len(subscriber_list)} subscribers'))
            self.stdout.write(f'Subject: {subject}')
            self.stdout.write(body)
            return

        sent = 0
        failed = 0
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@animenews.com')

        for email in subscriber_list:
            try:
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=from_email,
                    recipient_list=[email],
                    fail_silently=False,
                )
                sent += 1
            except Exception as exc:
                logger.error('Failed to send newsletter to %s: %s', email, exc)
                failed += 1

        self.stdout.write(
            self.style.SUCCESS(f'Newsletter sent: {sent} delivered, {failed} failed.')
        )
        logger.info('Newsletter sent: %d delivered, %d failed', sent, failed)

    def _build_email_body(self, articles, hours: int) -> str:
        lines = [
            f'Here are the latest anime news from the past {hours} hours:\n',
        ]
        for article in articles:
            lines.append(f'• {article.title}')
            if article.source_url:
                lines.append(f'  Read more: {article.source_url}')
            lines.append('')

        lines += [
            '---',
            'You are receiving this because you subscribed to the Anime News newsletter.',
            'To unsubscribe, visit our website and manage your preferences.',
        ]
        return '\n'.join(lines)
