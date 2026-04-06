import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class NewsConfig(AppConfig):
    name = 'news'

    def ready(self):
        # Only start the scheduler in the main process, not in Django's
        # auto-reloader child processes, and not during management commands
        # that don't need it (e.g. migrate, collectstatic).
        import os
        import sys
        # Skip during management commands that don't need the scheduler
        skip_commands = {'migrate', 'makemigrations', 'collectstatic', 'test', 'shell'}
        if skip_commands.intersection(sys.argv):
            return
        # In dev (runserver), only start in the main process, not the reloader watcher
        if 'runserver' in sys.argv and os.environ.get('RUN_MAIN') != 'true':
            return

        try:
            from apscheduler.schedulers.background import BackgroundScheduler
            from apscheduler.triggers.cron import CronTrigger
            from apscheduler.triggers.interval import IntervalTrigger
            from django.conf import settings
            from django_apscheduler.jobstores import DjangoJobStore
            from news.management.commands.runapscheduler import (
                delete_old_job_executions,
                fetch_anime_news,
            )

            scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
            scheduler.add_jobstore(DjangoJobStore(), "default")

            scheduler.add_job(
                fetch_anime_news,
                trigger=IntervalTrigger(hours=6),
                id="fetch_anime_news",
                max_instances=1,
                replace_existing=True,
            )

            scheduler.add_job(
                delete_old_job_executions,
                trigger=CronTrigger(day_of_week="sun", hour="00", minute="00"),
                id="delete_old_job_executions",
                max_instances=1,
                replace_existing=True,
            )

            scheduler.start()
            logger.info("APScheduler started (BackgroundScheduler) from AppConfig.ready().")
        except Exception as exc:  # pragma: no cover
            logger.warning("APScheduler could not be started: %s", exc)
