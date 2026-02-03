import requests
from django.core.management.base import BaseCommand
from news.models import Article

class Command(BaseCommand):
    help = 'Fetches news from Jikan API and saves to database'

    def handle(self, *args, **kwargs):
        # 1. EXTRACT (Get data from the internet)
        url = "https://api.jikan.moe/v4/anime/1/news"
        self.stdout.write(f"Connecting to {url}...")
        response = requests.get(url)

        if response.status_code != 200:
            self.stdout.write(self.style.ERROR('Failed to connect to API'))
            return

        data = response.json()
        news_list = data['data']

        # 2. TRANSFORM & LOAD (Loop and Save)
        for item in news_list[:5]: # Let's take the top 5
            
            # Check if this article already exists to avoid duplicates
            if not Article.objects.filter(title=item['title']).exists():
                
                Article.objects.create(
                    title=item['title'],
                    # Jikan gives a short intro, we use that as content
                    content=item.get('excerpt', 'Click link to read more...'),
                    category='NEWS',
                    image_url=item['images']['jpg']['image_url'], 
                    # Note: We are grabbing the image directly from the API!
                )
                self.stdout.write(self.style.SUCCESS(f"Saved: {item['title']}"))
            
            else:
                self.stdout.write(f"Skipped (Already exists): {item['title']}")

        self.stdout.write(self.style.SUCCESS('Successfully loaded news!'))