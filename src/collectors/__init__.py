"""Data collectors for various OSINT sources."""

from .base_collector import BaseCollector, Story
from .newsapi_collector import NewsAPICollector
from .gdelt_collector import GDELTCollector
from .web_scraper_collector import WebScraperCollector

__all__ = [
    'BaseCollector',
    'Story',
    'NewsAPICollector',
    'GDELTCollector',
    'WebScraperCollector'
]
