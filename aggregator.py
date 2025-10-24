#!/usr/bin/env python3
"""
OSINT Story Aggregator - Mosaic Intelligence System

Collects stories from multiple sources and identifies related content
to build a comprehensive intelligence picture.
"""

import sys
import os
import logging
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from collectors import NewsAPICollector, GDELTCollector, WebScraperCollector, Story
from processors import NLPProcessor
from correlators import StoryCorrelator
from dotenv import load_dotenv


class OsintAggregator:
    """Main OSINT story aggregator orchestrator."""

    def __init__(self, config_path: str = 'config/config.yaml'):
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.logger = logging.getLogger(__name__)

        # Initialize components
        self.collectors = self._initialize_collectors()
        self.nlp_processor = NLPProcessor(self.config.get('processing', {}))
        self.correlator = StoryCorrelator(
            self.config.get('processing', {}),
            self.nlp_processor
        )

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        # Load environment variables
        load_dotenv()

        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        # Substitute environment variables
        config_str = yaml.dump(config)
        for env_var in os.environ:
            config_str = config_str.replace(f'${{{env_var}}}', os.environ[env_var])

        return yaml.safe_load(config_str)

    def _setup_logging(self):
        """Setup logging configuration."""
        log_config = self.config.get('logging', {})
        log_level = getattr(logging, log_config.get('level', 'INFO'))
        log_file = log_config.get('file', 'logs/aggregator.log')

        # Create logs directory
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )

    def _initialize_collectors(self) -> List:
        """Initialize all data collectors."""
        collectors = []
        sources = self.config.get('sources', {})

        # NewsAPI
        if 'newsapi' in sources:
            collectors.append(NewsAPICollector(sources['newsapi']))

        # GDELT
        if 'gdelt' in sources:
            collectors.append(GDELTCollector(sources['gdelt']))

        # Web Scrapers
        if 'scrapers' in sources:
            collectors.append(WebScraperCollector(sources['scrapers']))

        return collectors

    def collect_stories(self) -> List[Story]:
        """Collect stories from all sources."""
        self.logger.info("=" * 60)
        self.logger.info("Starting story collection...")
        self.logger.info("=" * 60)

        all_stories = []

        for collector in self.collectors:
            try:
                stories = collector.collect()
                all_stories.extend(stories)
            except Exception as e:
                self.logger.error(f"Collector {collector.__class__.__name__} failed: {e}")

        # Deduplicate by URL
        unique_stories = {story.url: story for story in all_stories}
        stories = list(unique_stories.values())

        self.logger.info(f"\nCollected {len(stories)} unique stories from {len(self.collectors)} sources")

        return stories

    def correlate_stories(self, stories: List[Story]):
        """Find related stories and create clusters."""
        self.logger.info("\n" + "=" * 60)
        self.logger.info("Correlating stories...")
        self.logger.info("=" * 60)

        clusters = self.correlator.find_related_stories(stories)

        return clusters

    def generate_output(self, stories: List[Story], clusters: List):
        """Generate output reports."""
        self.logger.info("\n" + "=" * 60)
        self.logger.info("Generating output...")
        self.logger.info("=" * 60)

        output_config = self.config.get('output', {})
        output_dir = Path(output_config.get('directory', 'data/output'))
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Generate JSON output
        if output_config.get('format') in ['json', 'both']:
            self._generate_json_output(stories, clusters, output_dir, timestamp)

        # Generate HTML report
        if output_config.get('format') in ['html', 'both']:
            self._generate_html_output(stories, clusters, output_dir, timestamp)

        self.logger.info(f"\nOutput saved to: {output_dir}")

    def _generate_json_output(self, stories: List[Story], clusters: List, output_dir: Path, timestamp: str):
        """Generate JSON output files."""
        # All stories
        stories_file = output_dir / f'stories_{timestamp}.json'
        with open(stories_file, 'w') as f:
            json.dump(
                [story.to_dict() for story in stories],
                f,
                indent=2,
                default=str
            )
        self.logger.info(f"Saved stories to: {stories_file}")

        # Clusters
        clusters_file = output_dir / f'clusters_{timestamp}.json'
        cluster_summaries = [cluster.get_summary() for cluster in clusters]
        with open(clusters_file, 'w') as f:
            json.dump(cluster_summaries, f, indent=2, default=str)
        self.logger.info(f"Saved clusters to: {clusters_file}")

        # Summary
        summary_file = output_dir / f'summary_{timestamp}.json'
        with open(summary_file, 'w') as f:
            json.dump({
                'timestamp': timestamp,
                'total_stories': len(stories),
                'total_clusters': len(clusters),
                'largest_cluster_size': max([len(c.stories) for c in clusters]) if clusters else 0,
                'sources': list(set([s.source for s in stories])),
                'date_range': {
                    'start': min([s.published_date for s in stories]).isoformat() if stories else None,
                    'end': max([s.published_date for s in stories]).isoformat() if stories else None
                }
            }, f, indent=2, default=str)
        self.logger.info(f"Saved summary to: {summary_file}")

    def _generate_html_output(self, stories: List[Story], clusters: List, output_dir: Path, timestamp: str):
        """Generate HTML report."""
        html_file = output_dir / f'report_{timestamp}.html'

        # Create simple HTML report
        html = self._create_html_report(stories, clusters, timestamp)

        with open(html_file, 'w') as f:
            f.write(html)

        self.logger.info(f"Saved HTML report to: {html_file}")

    def _create_html_report(self, stories: List[Story], clusters: List, timestamp: str) -> str:
        """Create HTML report content."""
        # Get top 5 largest clusters
        top_clusters = sorted(clusters, key=lambda c: len(c.stories), reverse=True)[:5]

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>OSINT Story Aggregator Report - {timestamp}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        h1 {{ color: #333; }}
        .summary {{ background: white; padding: 20px; margin: 20px 0; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .cluster {{ background: white; padding: 20px; margin: 20px 0; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .story {{ margin: 10px 0; padding: 10px; background: #f9f9f9; border-left: 3px solid #007bff; }}
        .entities {{ margin: 10px 0; padding: 10px; background: #e7f3ff; border-radius: 3px; }}
        .entity-type {{ font-weight: bold; color: #0056b3; }}
        a {{ color: #007bff; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .meta {{ color: #666; font-size: 0.9em; }}
    </style>
</head>
<body>
    <h1>🔍 OSINT Story Aggregator Report</h1>
    <p class="meta">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

    <div class="summary">
        <h2>📊 Summary</h2>
        <p><strong>Total Stories:</strong> {len(stories)}</p>
        <p><strong>Story Clusters:</strong> {len(clusters)}</p>
        <p><strong>Sources:</strong> {', '.join(set([s.source for s in stories]))}</p>
    </div>

    <h2>🔗 Top Story Clusters</h2>
"""

        for cluster in top_clusters:
            summary = cluster.get_summary()
            html += f"""
    <div class="cluster">
        <h3>Cluster #{summary['cluster_id'] + 1} - {summary['story_count']} Related Stories</h3>

        <div class="entities">
"""
            # Show entities
            for entity_type, entities in summary.get('shared_entities', {}).items():
                if entities:
                    html += f'<p><span class="entity-type">{entity_type}:</span> {", ".join(entities[:5])}</p>'

            html += """
        </div>

        <h4>Stories:</h4>
"""
            # Show stories
            for story_info in summary['stories']:
                html += f"""
        <div class="story">
            <strong><a href="{story_info['url']}" target="_blank">{story_info['title']}</a></strong><br>
            <span class="meta">Source: {story_info['source']} | Published: {story_info['published_date'][:10]}</span>
        </div>
"""

            html += """
    </div>
"""

        html += """
</body>
</html>
"""
        return html

    def run(self):
        """Run the complete aggregation pipeline."""
        try:
            # Collect stories
            stories = self.collect_stories()

            if not stories:
                self.logger.warning("No stories collected. Exiting.")
                return

            # Correlate stories
            clusters = self.correlate_stories(stories)

            # Generate output
            self.generate_output(stories, clusters)

            self.logger.info("\n" + "=" * 60)
            self.logger.info("✅ OSINT aggregation complete!")
            self.logger.info("=" * 60)

        except Exception as e:
            self.logger.error(f"Fatal error: {e}", exc_info=True)
            sys.exit(1)


def main():
    """Main entry point."""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║       OSINT Story Aggregator - Mosaic Intelligence       ║
    ║                                                          ║
    ║   Collecting and correlating stories from the web to     ║
    ║   build comprehensive intelligence pictures              ║
    ╚══════════════════════════════════════════════════════════╝
    """)

    aggregator = OsintAggregator()
    aggregator.run()


if __name__ == '__main__':
    main()
