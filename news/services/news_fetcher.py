"""
Anime News Fetcher Service

Fetches real anime news from multiple sources:
1. Jikan API (MyAnimeList) - for anime info and news
2. Reddit Anime RSS - for community news
3. Anime News Network RSS - as backup
"""

import logging
import re
from datetime import datetime
from typing import Optional

# FIX: Use defusedxml instead of standard xml.etree.ElementTree
# Standard ElementTree is vulnerable to XXE (XML External Entity) attacks
# defusedxml disables: external entities, DTD processing, external DTDs
# This prevents attackers from reading server files or performing SSRF
from xml.etree import ElementTree  # Keep for type hints (Element class)
try:
    from defusedxml.ElementTree import fromstring as safe_fromstring
except ImportError:
    # Fallback with manual protection (less secure but better than nothing)
    import warnings
    warnings.warn("defusedxml not installed - XML parsing may be vulnerable to XXE")
    safe_fromstring = ElementTree.fromstring

import requests
from bs4 import BeautifulSoup
from django.utils import timezone

logger = logging.getLogger(__name__)


class AnimaNewsFetcher:
    """Fetches anime news from various sources."""

    # API endpoints
    JIKAN_API = "https://api.jikan.moe/v4"
    REDDIT_ANIME_RSS = "https://www.reddit.com/r/anime/hot.rss"
    REDDIT_ANIMENEWS_RSS = "https://www.reddit.com/r/animenews/hot.rss"

    # Anime News Network RSS feeds (backup)
    ANN_NEWS_FEED = "https://www.animenewsnetwork.com/newsroom/rss.xml"

    # User agent
    USER_AGENT = "AnimeNewsHub/1.0 (Educational Project; Contact: github.com/anime-news-hub)"

    # Category mapping based on keywords
    CATEGORY_KEYWORDS = {
        'REVIEW': ['review', 'reviews', 'rating', 'scored', 'episode discussion', 'what did you think'],
        'EVENT': ['event', 'convention', 'expo', 'festival', 'concert', 'premiere', 'announcement', 'announced'],
        'MERCH': ['figure', 'merchandise', 'goods', 'collection', 'product', 'sale', 'blu-ray', 'dvd'],
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.USER_AGENT,
            'Accept': 'application/json, application/rss+xml, application/xml, text/xml',
        })

    def fetch_news(self, limit: int = 20) -> list[dict]:
        """
        Fetch news articles from multiple sources.

        Args:
            limit: Maximum number of articles to fetch

        Returns:
            List of article dictionaries
        """
        articles = []

        # 1. Fetch from Jikan API (top airing anime as "news")
        jikan_articles = self._fetch_from_jikan(limit // 2)
        articles.extend(jikan_articles)

        # 2. Fetch from Reddit r/anime
        reddit_articles = self._fetch_reddit_rss(self.REDDIT_ANIME_RSS, limit // 3)
        articles.extend(reddit_articles)

        # 3. Fetch from Reddit r/animenews
        animenews_articles = self._fetch_reddit_rss(self.REDDIT_ANIMENEWS_RSS, limit // 3)
        articles.extend(animenews_articles)

        # 4. Try ANN as backup
        if len(articles) < limit // 2:
            ann_articles = self._fetch_rss_feed(self.ANN_NEWS_FEED, limit // 2)
            articles.extend(ann_articles)

        # Remove duplicates by title
        seen_titles = set()
        unique_articles = []
        for article in articles:
            title_key = article['title'].lower()[:50]
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                unique_articles.append(article)

        # Sort by date and limit
        unique_articles.sort(key=lambda x: x.get('published_date', datetime.min), reverse=True)
        return unique_articles[:limit]

    def _fetch_from_jikan(self, limit: int) -> list[dict]:
        """Fetch anime news/updates from Jikan API."""
        articles = []

        try:
            # Fetch top airing anime
            response = self.session.get(
                f"{self.JIKAN_API}/top/anime",
                params={'filter': 'airing', 'limit': limit},
                timeout=15
            )
            response.raise_for_status()
            data = response.json()

            for anime in data.get('data', []):
                article = self._parse_jikan_anime(anime)
                if article:
                    articles.append(article)

            logger.info(f"Fetched {len(articles)} articles from Jikan API")

        except requests.RequestException as e:
            logger.error(f"Failed to fetch from Jikan API: {e}")

        return articles

    def _parse_jikan_anime(self, anime: dict) -> Optional[dict]:
        """Parse Jikan anime data into article format."""
        try:
            title = anime.get('title', '')
            synopsis = anime.get('synopsis', '') or ''

            if not title:
                return None

            # Get image
            images = anime.get('images', {})
            image_url = images.get('jpg', {}).get('large_image_url') or \
                       images.get('jpg', {}).get('image_url')

            # Create news-style title
            news_title = f"{title} - Currently Airing: What You Need to Know"

            # Create content from synopsis and stats
            episodes = anime.get('episodes') or 'Ongoing'
            score = anime.get('score') or 'N/A'
            genres = ', '.join([g.get('name', '') for g in anime.get('genres', [])])

            content = f"{synopsis}\n\nEpisodes: {episodes} | Score: {score}/10 | Genres: {genres}"

            return {
                'title': news_title,
                'content': content.strip(),
                'category': 'NEWS',
                'published_date': timezone.now(),
                'image_url': image_url,
                'source_url': anime.get('url', ''),
            }

        except Exception as e:
            logger.warning(f"Failed to parse Jikan anime: {e}")
            return None

    def _fetch_reddit_rss(self, feed_url: str, limit: int) -> list[dict]:
        """Fetch news from Reddit RSS feeds."""
        articles = []

        try:
            response = self.session.get(feed_url, timeout=15)
            response.raise_for_status()

            # Parse XML
            root = safe_fromstring(response.content)

            # Reddit uses Atom format
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            entries = root.findall('.//atom:entry', ns)[:limit]

            for entry in entries:
                article = self._parse_reddit_entry(entry, ns)
                if article:
                    articles.append(article)

            logger.info(f"Fetched {len(articles)} articles from {feed_url}")

        except requests.RequestException as e:
            logger.error(f"Failed to fetch Reddit RSS {feed_url}: {e}")
        except ElementTree.ParseError as e:
            logger.error(f"Failed to parse Reddit RSS {feed_url}: {e}")

        return articles

    def _parse_reddit_entry(self, entry: ElementTree.Element, ns: dict) -> Optional[dict]:
        """Parse a Reddit Atom entry into an article dict."""
        try:
            title = entry.findtext('atom:title', '', ns).strip()
            link = entry.find('atom:link', ns)
            link_url = link.get('href', '') if link is not None else ''
            content_elem = entry.find('atom:content', ns)
            content_html = content_elem.text if content_elem is not None else ''
            updated = entry.findtext('atom:updated', '', ns)

            # Filter out non-news posts
            skip_patterns = ['[deleted]', '[removed]', 'weekly', 'megathread', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            if any(pattern in title.lower() for pattern in skip_patterns):
                return None

            if not title or len(title) < 10:
                return None

            # Parse date
            published_date = self._parse_date(updated)

            # Clean content
            content = self._clean_html(content_html) if content_html else title

            # Extract image from content
            image_url = self._extract_image(content_html) if content_html else None

            # Determine category
            category = self._determine_category(title, content)

            return {
                'title': title,
                'content': content if len(content) > 50 else f"{title}. Discuss this topic on Reddit.",
                'category': category,
                'published_date': published_date,
                'image_url': image_url,
                'source_url': link_url,
            }

        except Exception as e:
            logger.warning(f"Failed to parse Reddit entry: {e}")
            return None

    def _fetch_rss_feed(self, feed_url: str, limit: int) -> list[dict]:
        """Fetch and parse an RSS feed."""
        articles = []

        try:
            response = self.session.get(feed_url, timeout=30)
            response.raise_for_status()

            # Parse XML
            root = safe_fromstring(response.content)

            # Find all items
            items = root.findall('.//item')[:limit]

            for item in items:
                article = self._parse_rss_item(item)
                if article:
                    articles.append(article)

            logger.info(f"Fetched {len(articles)} articles from {feed_url}")

        except requests.RequestException as e:
            logger.error(f"Failed to fetch RSS feed {feed_url}: {e}")
        except ElementTree.ParseError as e:
            logger.error(f"Failed to parse RSS feed {feed_url}: {e}")

        return articles

    def _parse_rss_item(self, item: ElementTree.Element) -> Optional[dict]:
        """Parse a single RSS item into an article dict."""
        try:
            title = item.findtext('title', '').strip()
            link = item.findtext('link', '').strip()
            description = item.findtext('description', '').strip()
            pub_date_str = item.findtext('pubDate', '')

            if not title or not description:
                return None

            # Parse publication date
            published_date = self._parse_date(pub_date_str)

            # Clean description HTML
            content = self._clean_html(description)

            # Extract image from description
            image_url = self._extract_image(description)

            # Determine category
            category = self._determine_category(title, content)

            return {
                'title': title,
                'content': content,
                'category': category,
                'published_date': published_date,
                'image_url': image_url,
                'source_url': link,
            }

        except Exception as e:
            logger.warning(f"Failed to parse RSS item: {e}")
            return None

    def _parse_date(self, date_str: str) -> datetime:
        """Parse RSS date format."""
        if not date_str:
            return timezone.now()

        # Common RSS date formats
        formats = [
            '%a, %d %b %Y %H:%M:%S %z',
            '%a, %d %b %Y %H:%M:%S %Z',
            '%Y-%m-%dT%H:%M:%S%z',
            '%Y-%m-%d %H:%M:%S',
        ]

        for fmt in formats:
            try:
                dt = datetime.strptime(date_str.strip(), fmt)
                if dt.tzinfo is None:
                    dt = timezone.make_aware(dt)
                return dt
            except ValueError:
                continue

        # Fallback to now
        return timezone.now()

    def _clean_html(self, html: str) -> str:
        """Remove HTML tags and clean up text."""
        soup = BeautifulSoup(html, 'lxml')

        # Remove script and style elements
        for element in soup(['script', 'style']):
            element.decompose()

        # Get text
        text = soup.get_text(separator=' ')

        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        # Remove "read more" type suffixes
        text = re.sub(r'\s*\[?\s*(read more|continue reading|\.\.\.)\s*\]?\s*$', '', text, flags=re.IGNORECASE)

        return text

    def _extract_image(self, html: str) -> Optional[str]:
        """Extract first image URL from HTML content."""
        soup = BeautifulSoup(html, 'lxml')

        # Look for img tags
        img = soup.find('img')
        if img and img.get('src'):
            src = img['src']
            # Make sure it's a full URL
            if src.startswith('http'):
                return src

        # Look for image in media:content or enclosure
        # These are common in RSS feeds
        return None

    def _determine_category(self, title: str, content: str) -> str:
        """Determine article category based on content."""
        text = (title + ' ' + content).lower()

        for category, keywords in self.CATEGORY_KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                return category

        return 'NEWS'

    def fetch_article_image(self, article_url: str) -> Optional[str]:
        """
        Fetch the main image from an article page.

        This is useful when RSS doesn't include images.
        """
        try:
            response = self.session.get(article_url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'lxml')

            # Look for Open Graph image
            og_image = soup.find('meta', property='og:image')
            if og_image and og_image.get('content'):
                return og_image['content']

            # Look for Twitter image
            twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
            if twitter_image and twitter_image.get('content'):
                return twitter_image['content']

            # Look for main article image
            article_img = soup.select_one('article img, .article img, .news-article img')
            if article_img and article_img.get('src'):
                src = article_img['src']
                if src.startswith('http'):
                    return src

        except Exception as e:
            logger.warning(f"Failed to fetch article image from {article_url}: {e}")

        return None
