from django.db import models
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
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='NEWS')
    published_date = models.DateTimeField(auto_now_add=True)
    image_url = models.CharField(max_length=500, blank=True, null=True)

    # Phase 2: Enhanced fields
    view_count = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)

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
        """Increment view count."""
        self.view_count += 1
        self.save(update_fields=['view_count'])


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