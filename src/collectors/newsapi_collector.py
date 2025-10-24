"""NewsAPI collector - aggregates from 80k+ news sources."""

import requests
from typing import List, Dict, Any
from datetime import datetime, timedelta
from .base_collector import BaseCollector, Story
import os


class NewsAPICollector(BaseCollector):
    """Collects stories from NewsAPI.org."""

    BASE_URL = "https://newsapi.org/v2/everything"

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = os.getenv('NEWSAPI_KEY', config.get('api_key', ''))
        self.queries = config.get('queries', [])
        self.language = config.get('language', 'en')
        self.page_size = min(config.get('page_size', 100), 100)  # Max 100 per request

    def collect(self) -> List[Story]:
        """Collect stories from NewsAPI."""
        if not self.is_enabled():
            self.logger.info("NewsAPI collector is disabled")
            return []

        if not self.api_key or self.api_key == "${NEWSAPI_KEY}":
            self.logger.warning("NewsAPI key not set, skipping NewsAPI collector")
            return []

        all_stories = []

        for query in self.queries:
            try:
                stories = self._fetch_query(query)
                all_stories.extend(stories)
                self.logger.info(f"Collected {len(stories)} stories for query: '{query}'")
            except Exception as e:
                self.logger.error(f"Error fetching NewsAPI query '{query}': {e}")

        # Deduplicate by URL
        unique_stories = {story.url: story for story in all_stories}
        self.logger.info(f"NewsAPI total: {len(unique_stories)} unique stories")

        return list(unique_stories.values())

    def _fetch_query(self, query: str) -> List[Story]:
        """Fetch stories for a specific query."""
        # Get stories from last 24 hours
        from_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

        params = {
            'q': query,
            'apiKey': self.api_key,
            'language': self.language,
            'pageSize': self.page_size,
            'from': from_date,
            'sortBy': 'publishedAt'
        }

        response = requests.get(self.BASE_URL, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()

        if data['status'] != 'ok':
            raise Exception(f"NewsAPI error: {data.get('message', 'Unknown error')}")

        stories = []
        for article in data.get('articles', []):
            try:
                story = self._parse_article(article, query)
                if story:
                    stories.append(story)
            except Exception as e:
                self.logger.warning(f"Error parsing article: {e}")

        return stories

    def _parse_article(self, article: Dict[str, Any], query: str) -> Story:
        """Parse NewsAPI article into Story object."""
        # Parse published date
        pub_date_str = article.get('publishedAt')
        if pub_date_str:
            pub_date = datetime.fromisoformat(pub_date_str.replace('Z', '+00:00'))
        else:
            pub_date = datetime.now()

        return Story(
            title=article.get('title', 'No title'),
            url=article.get('url', ''),
            source=article.get('source', {}).get('name', 'Unknown'),
            published_date=pub_date,
            content=article.get('content', ''),
            description=article.get('description', ''),
            author=article.get('author', ''),
            collector='newsapi',
            metadata={
                'query': query,
                'image_url': article.get('urlToImage', '')
            }
        )
