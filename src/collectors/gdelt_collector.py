"""GDELT collector - Global Database of Events, Language, and Tone."""

import requests
from typing import List, Dict, Any
from datetime import datetime
from .base_collector import BaseCollector, Story
import urllib.parse


class GDELTCollector(BaseCollector):
    """Collects stories from GDELT Project."""

    # GDELT 2.0 Doc API
    BASE_URL = "https://api.gdeltproject.org/api/v2/doc/doc"

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.queries = config.get('queries', [])
        self.max_records = config.get('max_records', 250)

    def collect(self) -> List[Story]:
        """Collect stories from GDELT."""
        if not self.is_enabled():
            self.logger.info("GDELT collector is disabled")
            return []

        all_stories = []

        for query in self.queries:
            try:
                stories = self._fetch_query(query)
                all_stories.extend(stories)
                self.logger.info(f"Collected {len(stories)} stories for query: '{query}'")
            except Exception as e:
                self.logger.error(f"Error fetching GDELT query '{query}': {e}")

        # Deduplicate by URL
        unique_stories = {story.url: story for story in all_stories}
        self.logger.info(f"GDELT total: {len(unique_stories)} unique stories")

        return list(unique_stories.values())

    def _fetch_query(self, query: str) -> List[Story]:
        """Fetch stories for a specific query."""
        params = {
            'query': query,
            'mode': 'artlist',
            'maxrecords': self.max_records,
            'format': 'json',
            'sort': 'datedesc'
        }

        response = requests.get(self.BASE_URL, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()
        articles = data.get('articles', [])

        stories = []
        for article in articles:
            try:
                story = self._parse_article(article, query)
                if story:
                    stories.append(story)
            except Exception as e:
                self.logger.warning(f"Error parsing GDELT article: {e}")

        return stories

    def _parse_article(self, article: Dict[str, Any], query: str) -> Story:
        """Parse GDELT article into Story object."""
        # Parse date - GDELT uses format: YYYYMMDDTHHmmssZ
        date_str = article.get('seendate', '')
        try:
            pub_date = datetime.strptime(date_str, '%Y%m%dT%H%M%SZ')
        except (ValueError, TypeError):
            pub_date = datetime.now()

        # Extract domain from URL for source name
        url = article.get('url', '')
        try:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
            source = domain.replace('www.', '')
        except:
            source = 'Unknown'

        return Story(
            title=article.get('title', 'No title'),
            url=url,
            source=source,
            published_date=pub_date,
            content='',  # GDELT doesn't provide full content
            description='',
            author='',
            collector='gdelt',
            metadata={
                'query': query,
                'domain': article.get('domain', ''),
                'language': article.get('language', ''),
                'seendate': date_str,
                'socialimage': article.get('socialimage', '')
            }
        )
