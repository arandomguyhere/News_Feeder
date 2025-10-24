"""Web scraper collector for Google News and Bing News."""

import requests
from typing import List, Dict, Any
from datetime import datetime
from bs4 import BeautifulSoup
from .base_collector import BaseCollector, Story
import urllib.parse
import time


class WebScraperCollector(BaseCollector):
    """Scrapes Google News and Bing News."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.targets = config.get('targets', [])
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def collect(self) -> List[Story]:
        """Collect stories from web scrapers."""
        if not self.is_enabled():
            self.logger.info("Web scraper collector is disabled")
            return []

        all_stories = []

        for target in self.targets:
            target_type = target.get('type', '')
            queries = target.get('queries', [])
            max_results = target.get('max_results', 50)

            for query in queries:
                try:
                    if target_type == 'google_news':
                        stories = self._scrape_google_news(query, max_results)
                    elif target_type == 'bing_news':
                        stories = self._scrape_bing_news(query, max_results)
                    else:
                        self.logger.warning(f"Unknown scraper type: {target_type}")
                        continue

                    all_stories.extend(stories)
                    self.logger.info(f"Collected {len(stories)} stories from {target_type} for '{query}'")
                    time.sleep(1)  # Be respectful, add delay between requests
                except Exception as e:
                    self.logger.error(f"Error scraping {target_type} for '{query}': {e}")

        # Deduplicate by URL
        unique_stories = {story.url: story for story in all_stories}
        self.logger.info(f"Web scraper total: {len(unique_stories)} unique stories")

        return list(unique_stories.values())

    def _scrape_google_news(self, query: str, max_results: int) -> List[Story]:
        """Scrape Google News search results."""
        encoded_query = urllib.parse.quote(query)
        url = f"https://news.google.com/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"

        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
        except Exception as e:
            self.logger.error(f"Failed to fetch Google News: {e}")
            return []

        soup = BeautifulSoup(response.text, 'lxml')
        stories = []

        # Google News uses article tags
        articles = soup.find_all('article')[:max_results]

        for article in articles:
            try:
                # Find title link
                title_elem = article.find('a', class_='gPFEn')
                if not title_elem:
                    continue

                title = title_elem.text.strip()
                # Google News URLs are relative, need to construct full URL
                relative_url = title_elem.get('href', '')
                if relative_url.startswith('./'):
                    relative_url = relative_url[2:]
                article_url = f"https://news.google.com/{relative_url}"

                # Find source
                source_elem = article.find('a', class_='wEwyrc')
                source = source_elem.text.strip() if source_elem else 'Google News'

                # Find time (usually relative like "3 hours ago")
                time_elem = article.find('time')
                pub_date = datetime.now()  # Default to now
                if time_elem and time_elem.get('datetime'):
                    try:
                        pub_date = datetime.fromisoformat(time_elem['datetime'].replace('Z', '+00:00'))
                    except:
                        pass

                story = Story(
                    title=title,
                    url=article_url,
                    source=source,
                    published_date=pub_date,
                    content='',
                    description='',
                    author='',
                    collector='google_news',
                    metadata={'query': query}
                )
                stories.append(story)

            except Exception as e:
                self.logger.debug(f"Error parsing Google News article: {e}")
                continue

        return stories

    def _scrape_bing_news(self, query: str, max_results: int) -> List[Story]:
        """Scrape Bing News search results."""
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.bing.com/news/search?q={encoded_query}&FORM=HDRSC6"

        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
        except Exception as e:
            self.logger.error(f"Failed to fetch Bing News: {e}")
            return []

        soup = BeautifulSoup(response.text, 'lxml')
        stories = []

        # Bing uses news card divs
        news_cards = soup.find_all('div', class_='news-card')[:max_results]

        for card in news_cards:
            try:
                # Find title and URL
                title_elem = card.find('a', class_='title')
                if not title_elem:
                    continue

                title = title_elem.text.strip()
                article_url = title_elem.get('href', '')

                # Find source
                source_elem = card.find('span', class_='source')
                source = source_elem.text.strip() if source_elem else 'Bing News'

                # Find snippet/description
                snippet_elem = card.find('div', class_='snippet')
                description = snippet_elem.text.strip() if snippet_elem else ''

                # Time - usually relative
                pub_date = datetime.now()

                story = Story(
                    title=title,
                    url=article_url,
                    source=source,
                    published_date=pub_date,
                    content='',
                    description=description,
                    author='',
                    collector='bing_news',
                    metadata={'query': query}
                )
                stories.append(story)

            except Exception as e:
                self.logger.debug(f"Error parsing Bing News article: {e}")
                continue

        return stories
