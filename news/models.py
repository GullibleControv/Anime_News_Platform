from django.db import models
from django.db.models import F
from django.conf import settings
from django.utils import timezone


class Article(models.Model):
    CATEGORY_CHOICES = [
        ('NEWS', 'News'),
        ('REVIEW', 'Review'),
        ('MERCH', 'Merchandise'),
        ('EVENT', 'Event'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    # FIX: Add db_index for frequently filtered/sorted fields
    # Without index: full table scan O(n) for every category filter
    # With index: B-tree lookup O(log n) - much faster at scale
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='NEWS', db_index=True)
    published_date = models.DateTimeField(auto_now_add=True, db_index=True)  # Used in ORDER BY
    image_url = models.CharField(max_length=500, blank=True, null=True)
    source_url = models.URLField(max_length=500, blank=True, null=True, help_text="Original source URL")

    # Phase 2: Enhanced fields
    view_count = models.PositiveIntegerField(default=0, db_index=True)  # Used for trending sort
    is_featured = models.BooleanField(default=False, db_index=True)  # Queried on every home page load

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    @property
    def reading_time(self):
        """Estimate reading time based on word count (200 words per minute)."""
        word_count = len(self.content.split())
        minutes = max(1, round(word_count / 200))
        return minutes

    def increment_views(self):
        """Increment view count atomically.

        FIX: Uses F() expression to perform atomic database-level increment.
        Old code had race condition: read-modify-write pattern could lose updates.
        New code: UPDATE article SET view_count = view_count + 1 WHERE id = X
        This is atomic - database guarantees no lost updates under concurrency.
        """
        Article.objects.filter(pk=self.pk).update(view_count=F('view_count') + 1)
        self.refresh_from_db(fields=['view_count'])  # Sync local object with DB


class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email


class Bookmark(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'article']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.article.title}"