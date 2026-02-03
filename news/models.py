from django.db import models

class Article(models.Model):
    # These are the options we can choose from
    CATEGORY_CHOICES = [
        ('NEWS', 'News'),
        ('REVIEW', 'Review'),
        ('MERCH', 'Merchandise'),
        ('EVENT', 'Event'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    # NEW FIELD:
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='NEWS')
    
    published_date = models.DateTimeField(auto_now_add=True)
    image_url = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title