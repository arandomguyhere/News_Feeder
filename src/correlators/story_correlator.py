"""Story correlation engine to find related stories."""

import logging
from typing import List, Dict, Any, Set, Tuple
from collections import defaultdict
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class StoryCluster:
    """Represents a cluster of related stories."""

    def __init__(self, cluster_id: int):
        self.id = cluster_id
        self.stories = []
        self.shared_entities = defaultdict(set)
        self.shared_keywords = set()
        self.topics = []

    def add_story(self, story, story_data: Dict[str, Any]):
        """Add a story to this cluster."""
        self.stories.append({
            'story': story,
            'data': story_data
        })

        # Update shared entities
        for entity_type, entities in story_data.get('entities', {}).items():
            for entity in entities:
                self.shared_entities[entity_type].add(entity)

        # Update shared keywords
        keywords = story_data.get('keywords', [])
        self.shared_keywords.update(keywords)

    def get_summary(self) -> Dict[str, Any]:
        """Get cluster summary."""
        if not self.stories:
            return {}

        # Find most common entities
        top_entities = {}
        for entity_type, entities in self.shared_entities.items():
            top_entities[entity_type] = list(entities)[:5]

        # Get date range
        dates = [s['story'].published_date for s in self.stories]
        min_date = min(dates)
        max_date = max(dates)

        # Get sources
        sources = list(set([s['story'].source for s in self.stories]))

        return {
            'cluster_id': self.id,
            'story_count': len(self.stories),
            'stories': [
                {
                    'id': s['story'].id,
                    'title': s['story'].title,
                    'url': s['story'].url,
                    'source': s['story'].source,
                    'published_date': s['story'].published_date.isoformat()
                }
                for s in self.stories
            ],
            'shared_entities': top_entities,
            'shared_keywords': list(self.shared_keywords)[:10],
            'date_range': {
                'start': min_date.isoformat(),
                'end': max_date.isoformat()
            },
            'sources': sources
        }


class StoryCorrelator:
    """Correlates stories to find related content."""

    def __init__(self, config: Dict[str, Any], nlp_processor):
        self.config = config
        self.nlp_processor = nlp_processor
        self.similarity_threshold = config.get('similarity_threshold', 0.3)

    def find_related_stories(self, stories: List) -> List[StoryCluster]:
        """Find clusters of related stories."""
        if not stories:
            return []

        logger.info(f"Correlating {len(stories)} stories...")

        # Process all stories with NLP
        processed_stories = []
        for story in stories:
            try:
                story_data = self.nlp_processor.process_story(story)
                processed_stories.append({
                    'story': story,
                    'data': story_data
                })
            except Exception as e:
                logger.warning(f"Error processing story '{story.title[:50]}': {e}")

        # Find relationships
        relationships = self._find_relationships(processed_stories)

        # Create clusters
        clusters = self._create_clusters(processed_stories, relationships)

        logger.info(f"Found {len(clusters)} story clusters")

        return clusters

    def _find_relationships(self, processed_stories: List[Dict]) -> List[Tuple[int, int, float]]:
        """Find relationships between stories based on similarity."""
        relationships = []
        total_comparisons = len(processed_stories) * (len(processed_stories) - 1) // 2
        comparisons_done = 0
        last_log_percent = 0

        # Compare each story with every other story
        for i, story1 in enumerate(processed_stories):
            for j, story2 in enumerate(processed_stories[i + 1:], start=i + 1):
                similarity = self._calculate_story_similarity(story1, story2)

                if similarity >= self.similarity_threshold:
                    relationships.append((i, j, similarity))

                # Progress logging every 10%
                comparisons_done += 1
                percent_done = int((comparisons_done / total_comparisons) * 100)
                if percent_done >= last_log_percent + 10:
                    logger.info(f"Correlation progress: {percent_done}% ({comparisons_done}/{total_comparisons} comparisons)")
                    last_log_percent = percent_done

        logger.info(f"Found {len(relationships)} story relationships")
        return relationships

    def _calculate_story_similarity(self, story1: Dict, story2: Dict) -> float:
        """Calculate overall similarity between two stories."""
        data1 = story1['data']
        data2 = story2['data']

        # Text similarity (highest weight)
        text_sim = self.nlp_processor.calculate_similarity(
            data1.get('text_for_similarity', ''),
            data2.get('text_for_similarity', '')
        )

        # Entity overlap
        entity_sim = self._entity_similarity(
            data1.get('entities', {}),
            data2.get('entities', {})
        )

        # Keyword overlap
        keyword_sim = self._keyword_similarity(
            set(data1.get('keywords', [])),
            set(data2.get('keywords', []))
        )

        # Temporal proximity (stories published around the same time are more likely related)
        temporal_sim = self._temporal_similarity(
            story1['story'].published_date,
            story2['story'].published_date
        )

        # Weighted combination
        total_similarity = (
            text_sim * 0.4 +
            entity_sim * 0.3 +
            keyword_sim * 0.2 +
            temporal_sim * 0.1
        )

        return total_similarity

    def _entity_similarity(self, entities1: Dict, entities2: Dict) -> float:
        """Calculate similarity based on shared entities."""
        if not entities1 or not entities2:
            return 0.0

        # Flatten all entities
        all_entities1 = set()
        all_entities2 = set()

        for entity_list in entities1.values():
            all_entities1.update([e.lower() for e in entity_list])

        for entity_list in entities2.values():
            all_entities2.update([e.lower() for e in entity_list])

        if not all_entities1 or not all_entities2:
            return 0.0

        # Jaccard similarity
        intersection = len(all_entities1 & all_entities2)
        union = len(all_entities1 | all_entities2)

        return intersection / union if union > 0 else 0.0

    def _keyword_similarity(self, keywords1: Set, keywords2: Set) -> float:
        """Calculate similarity based on shared keywords."""
        if not keywords1 or not keywords2:
            return 0.0

        intersection = len(keywords1 & keywords2)
        union = len(keywords1 | keywords2)

        return intersection / union if union > 0 else 0.0

    def _temporal_similarity(self, date1: datetime, date2: datetime) -> float:
        """Calculate similarity based on temporal proximity."""
        time_diff = abs((date1 - date2).total_seconds())

        # Within 1 hour: very similar (1.0)
        # Within 24 hours: somewhat similar (0.5)
        # Within 7 days: low similarity (0.2)
        # Beyond 7 days: no similarity (0.0)

        if time_diff < 3600:  # 1 hour
            return 1.0
        elif time_diff < 86400:  # 24 hours
            return 0.5
        elif time_diff < 604800:  # 7 days
            return 0.2
        else:
            return 0.0

    def _create_clusters(self, processed_stories: List[Dict], relationships: List[Tuple]) -> List[StoryCluster]:
        """Create clusters from relationships using connected components."""
        if not relationships:
            # Each story is its own cluster
            clusters = []
            for i, ps in enumerate(processed_stories):
                cluster = StoryCluster(i)
                cluster.add_story(ps['story'], ps['data'])
                clusters.append(cluster)
            return clusters

        # Build adjacency list
        graph = defaultdict(set)
        for i, j, _ in relationships:
            graph[i].add(j)
            graph[j].add(i)

        # Find connected components (clusters)
        visited = set()
        clusters = []

        def dfs(node, current_cluster_nodes):
            visited.add(node)
            current_cluster_nodes.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    dfs(neighbor, current_cluster_nodes)

        cluster_id = 0
        for i in range(len(processed_stories)):
            if i not in visited:
                current_cluster_nodes = set()
                dfs(i, current_cluster_nodes)

                # Create cluster
                cluster = StoryCluster(cluster_id)
                for node in current_cluster_nodes:
                    ps = processed_stories[node]
                    cluster.add_story(ps['story'], ps['data'])

                clusters.append(cluster)
                cluster_id += 1

        # Sort clusters by size (largest first)
        clusters.sort(key=lambda c: len(c.stories), reverse=True)

        return clusters
