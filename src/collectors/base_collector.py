"""Base collector class for all data sources."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class Story:
    """Represents a single news story/article."""

    def __init__(
        self,
        title: str,
        url: str,
        source: str,
        published_date: datetime,
        content: str = "",
        description: str = "",
        author: str = "",
        collector: str = "",
        metadata: Dict[str, Any] = None
    ):
        self.title = title
        self.url = url
        self.source = source
        self.published_date = published_date
        self.content = content
        self.description = description
        self.author = author
        self.collector = collector
        self.metadata = metadata or {}
        self.id = self._generate_id()

    def _generate_id(self) -> str:
        """Generate unique ID based on URL."""
        import hashlib
        return hashlib.md5(self.url.encode()).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        """Convert story to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'source': self.source,
            'published_date': self.published_date.isoformat(),
            'content': self.content,
            'description': self.description,
            'author': self.author,
            'collector': self.collector,
            'metadata': self.metadata
        }

    def __repr__(self):
        return f"Story(title='{self.title[:50]}...', source='{self.source}')"


class BaseCollector(ABC):
    """Abstract base class for all collectors."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def collect(self) -> List[Story]:
        """Collect stories from the source."""
        pass

    def is_enabled(self) -> bool:
        """Check if this collector is enabled."""
        return self.config.get('enabled', False)
