from django.core.management.base import BaseCommand
from news.models import Article
import random


class Command(BaseCommand):
    help = 'Creates sample anime news articles for demonstration'

    def handle(self, *args, **options):
        sample_articles = [
            {
                'title': 'Demon Slayer Season 4 Announces Spring 2025 Premiere Date',
                'content': '''The highly anticipated fourth season of Demon Slayer: Kimetsu no Yaiba has officially announced its premiere date for Spring 2025. Ufotable will return to animate the Hashira Training Arc, promising stunning visuals that fans have come to expect from the series.

The new season will focus on the intense training regimen that Tanjiro and his friends undergo with the powerful Hashira. This arc is crucial for preparing them for the final battle against Muzan Kibutsuji.

Fans worldwide are excited to see the character development and breathtaking action sequences that have made Demon Slayer one of the most popular anime of the decade. Pre-orders for the soundtrack and merchandise have already begun.

Industry analysts predict this season will break previous streaming records, with millions of viewers expected to tune in for the premiere episode.''',
                'category': 'NEWS',
                'image_url': 'https://images.unsplash.com/photo-1578632767115-351597cf2477?w=800',
                'is_featured': True,
                'view_count': random.randint(5000, 15000),
            },
            {
                'title': 'One Piece Film: Red Breaks Box Office Records Worldwide',
                'content': '''One Piece Film: Red has surpassed expectations, breaking box office records in multiple countries and becoming the highest-grossing One Piece film to date.

The film features Uta, a new character voiced by Ado, whose songs have dominated music charts globally. The combination of epic storytelling and incredible musical performances has resonated with both longtime fans and newcomers.

Theaters have reported sold-out screenings weeks after release, with fans returning multiple times to experience the film's emotional story and stunning animation.''',
                'category': 'NEWS',
                'image_url': 'https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=800',
                'view_count': random.randint(3000, 8000),
            },
            {
                'title': 'Jujutsu Kaisen 0 Movie Review: A Prequel Worth Watching',
                'content': '''Jujutsu Kaisen 0 delivers an emotional and action-packed prequel story that stands strong on its own while enriching the main series.

The film follows Yuta Okkotsu, a high school student haunted by the spirit of his childhood friend Rika. His journey to Jujutsu High and his growth as a sorcerer is both heartwarming and thrilling.

MAPPA's animation quality is consistently excellent, with fight scenes that rival anything in the TV series. The character development, particularly the relationship between Yuta and Gojo, adds depth to the Jujutsu Kaisen universe.

Rating: 9/10 - A must-watch for fans and newcomers alike.''',
                'category': 'REVIEW',
                'image_url': 'https://images.unsplash.com/photo-1560707303-4e980ce876ad?w=800',
                'view_count': random.randint(2000, 6000),
            },
            {
                'title': 'My Hero Academia: Complete Figure Collection Announced',
                'content': '''Bandai Namco has announced an exclusive My Hero Academia figure collection featuring all Class 1-A students in their hero costumes.

Each figure stands at 1/8 scale with incredible attention to detail, from Deku's Full Cowling effects to Bakugo's explosive gauntlets. The collection will be released over 12 months, with pre-orders opening next week.

Collectors can also purchase a special display case designed to look like the UA High School building. Early bird orders receive an exclusive Toshinori Yagi (All Might weakened form) bonus figure.

Pricing starts at $89.99 per figure, with the complete set available at a discounted bundle price.''',
                'category': 'MERCH',
                'image_url': 'https://images.unsplash.com/photo-1608889825103-eb5ed706fc64?w=800',
                'view_count': random.randint(1500, 4000),
            },
            {
                'title': 'Anime NYC 2025 Guest Lineup Revealed',
                'content': '''Anime NYC has revealed its impressive guest lineup for the 2025 convention, featuring voice actors, directors, and artists from some of the biggest anime series.

Highlights include the English voice cast of Attack on Titan for a final reunion panel, the director of Chainsaw Man, and surprise appearances from Japanese voice actors of Spy x Family.

The convention will also feature exclusive merchandise, advance screenings of upcoming anime, and interactive exhibits celebrating 50 years of anime in America.

Tickets are expected to sell out quickly, with VIP packages offering meet-and-greet opportunities with featured guests.''',
                'category': 'EVENT',
                'image_url': 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800',
                'view_count': random.randint(1000, 3000),
            },
            {
                'title': 'Chainsaw Man Part 2 Manga Sales Surpass 20 Million Copies',
                'content': '''Tatsuki Fujimoto's Chainsaw Man continues to dominate sales charts, with Part 2 of the manga series surpassing 20 million copies in circulation worldwide.

The sequel, following new protagonist Asa Mitaka and the War Devil, has captivated readers with its unique storytelling and unpredictable plot twists. Weekly chapters consistently trend globally on social media.

Publishers report that demand continues to outpace supply, with multiple reprints scheduled to meet reader demand.''',
                'category': 'NEWS',
                'image_url': 'https://images.unsplash.com/photo-1618336753974-aae8e04506aa?w=800',
                'view_count': random.randint(4000, 10000),
            },
            {
                'title': 'Spy x Family Season 2 Review: Family Fun Continues',
                'content': '''Spy x Family returns with its second season, delivering more heartwarming moments and comedic brilliance that made the first season a hit.

The Forger family dynamics remain the heart of the show, with Anya's telepathic antics stealing every scene. New character introductions add fresh energy while maintaining the series' charm.

WIT Studio and CloverWorks maintain their high production standards, with fluid animation and expressive character designs that bring the manga to life.

Rating: 8.5/10 - A delightful continuation that keeps you coming back for more family shenanigans.''',
                'category': 'REVIEW',
                'image_url': 'https://images.unsplash.com/photo-1553095066-5014bc7b7f2d?w=800',
                'view_count': random.randint(2500, 7000),
            },
            {
                'title': 'Limited Edition Evangelion x Seiko Watch Collection',
                'content': '''Seiko has partnered with Evangelion to create a limited edition watch collection celebrating the franchise's legacy.

The collection features five watches, each inspired by an EVA unit. The Unit-01 model features a distinctive purple and green color scheme with luminous hands that glow like an EVA's eyes.

Only 3,000 pieces of each design will be produced, with prices ranging from $450 to $850. Each watch comes with a special display case and certificate of authenticity.

Pre-orders begin next month exclusively through authorized dealers.''',
                'category': 'MERCH',
                'image_url': 'https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=800',
                'view_count': random.randint(1200, 3500),
            },
            {
                'title': 'Studio Ghibli Fest 2025 Returns to Theaters',
                'content': '''Studio Ghibli Fest returns in 2025 with remastered screenings of beloved classics and the theatrical debut of newer films.

The lineup includes 4K restorations of Spirited Away, Princess Mononoke, and My Neighbor Totoro, along with special anniversary screenings of Howl's Moving Castle.

Select screenings will feature exclusive behind-the-scenes content and interviews with animation staff. Commemorative posters will be available while supplies last.

Tickets go on sale next month through participating theaters.''',
                'category': 'EVENT',
                'image_url': 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=800',
                'view_count': random.randint(2000, 5000),
            },
            {
                'title': 'Blue Lock Takes Sports Anime by Storm',
                'content': '''Blue Lock has emerged as the breakout sports anime of the season, combining intense competition with psychological drama that sets it apart from typical sports series.

The premise of selecting Japan's ultimate striker through an elimination-style program creates constant tension and unpredictable matchups. Character development is handled exceptionally well.

8bit studio delivers impressive animation during match sequences, with creative visual representations of each player's unique abilities and "ego."

This series is a must-watch for sports anime fans looking for something different.''',
                'category': 'REVIEW',
                'image_url': 'https://images.unsplash.com/photo-1431324155629-1a6deb1dec8d?w=800',
                'view_count': random.randint(3500, 9000),
            },
        ]

        created_count = 0
        for article_data in sample_articles:
            article, created = Article.objects.get_or_create(
                title=article_data['title'],
                defaults=article_data
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created: {article.title}")
            else:
                # Update existing article with new view counts
                article.view_count = article_data.get('view_count', 0)
                article.is_featured = article_data.get('is_featured', False)
                article.save()
                self.stdout.write(f"Updated: {article.title}")

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created/updated {len(sample_articles)} sample articles')
        )
