#!/usr/bin/env python3
"""
Combined OSINT Intelligence Aggregator
Comprehensive intelligence collection across 4 critical domains:
- Cyber Threat Intelligence (84 searches)
- Military Drone Intelligence (53 searches)
Total: 137 targeted OSINT searches for Daily Drop newsletter feed.

Coverage:
- Nation-state cyber threats (China, Russia, Iran, DPRK)
- APT groups (Salt Typhoon, Volt Typhoon, etc.)
- Military UAV operations & autonomous systems
- Semiconductor supply chain & critical minerals
- Economic warfare & export controls
- Space/satellite intelligence & warfare
"""

import os
import sys
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from collectors.google_news_scraper import scrape_google_news_multi
from collectors.drone_news_scraper import scrape_drone_news_multi
from processors.story_correlator import analyze_stories


def merge_intelligence_sources(cyber_stories, drone_stories):
    """Merge cyber and drone intelligence into unified dataset"""
    all_stories = []

    # Add cyber stories with category tag
    for story in cyber_stories:
        story['intelligence_type'] = 'CYBER_THREAT'
        all_stories.append(story)

    # Add drone stories with category tag
    for story in drone_stories:
        story['intelligence_type'] = 'MILITARY_DRONE'
        all_stories.append(story)

    print(f"\n{'='*60}")
    print(f"MERGED INTELLIGENCE SOURCES")
    print(f"{'='*60}")
    print(f"Cyber Threat Intelligence: {len(cyber_stories)} stories")
    print(f"Military Drone Intelligence: {len(drone_stories)} stories")
    print(f"Total Combined: {len(all_stories)} stories")
    print(f"{'='*60}\n")

    return all_stories


def save_json_report(data: dict, filename: str):
    """Save data to JSON file"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved: {filename}")


def save_html_report(report: dict, filename: str):
    """Generate comprehensive HTML report with both intelligence types"""

    # Separate cyber and drone stories
    cyber_stories = [s for s in report.get('all_stories', []) if s.get('intelligence_type') == 'CYBER_THREAT']
    drone_stories = [s for s in report.get('all_stories', []) if s.get('intelligence_type') == 'MILITARY_DRONE']

    html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Combined OSINT Intelligence Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}
        .section {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            margin-top: 0;
            color: #333;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        .intelligence-type {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: bold;
            margin-left: 10px;
        }}
        .cyber-badge {{
            background: #e7f3ff;
            color: #0066cc;
        }}
        .drone-badge {{
            background: #fff3e7;
            color: #cc6600;
        }}
        .story {{
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #667eea;
            background: #f9f9f9;
            border-radius: 4px;
        }}
        .story h3 {{
            margin: 0 0 10px 0;
            color: #333;
        }}
        .story-meta {{
            font-size: 0.9em;
            color: #666;
            margin: 5px 0;
        }}
        .cluster {{
            margin-bottom: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border: 1px solid #dee2e6;
        }}
        .cluster-header {{
            font-weight: bold;
            color: #495057;
            margin-bottom: 15px;
            font-size: 1.1em;
        }}
        a {{
            color: #667eea;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 Combined OSINT Intelligence Report</h1>
        <p>Generated: {timestamp}</p>
    </div>

    <div class="stats">
        <div class="stat-card">
            <div class="stat-number">{total_stories}</div>
            <div class="stat-label">Total Intelligence Reports</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{cyber_count}</div>
            <div class="stat-label">Cyber Threat Intel</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{drone_count}</div>
            <div class="stat-label">Military Drone Intel</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{cluster_count}</div>
            <div class="stat-label">Story Clusters</div>
        </div>
    </div>

    <div class="section">
        <h2>🎯 Top Intelligence Clusters</h2>
        {clusters_html}
    </div>

    <div class="section">
        <h2>💻 Cyber Threat Intelligence ({cyber_count} stories)</h2>
        {cyber_stories_html}
    </div>

    <div class="section">
        <h2>🚁 Military Drone Intelligence ({drone_count} stories)</h2>
        {drone_stories_html}
    </div>

    <div class="section">
        <h2>📊 Intelligence Sources</h2>
        <p><strong>Cyber Coverage:</strong> 51 searches covering nation-state actors (China, Russia, Iran, DPRK),
        APT groups (Salt Typhoon, Volt Typhoon), critical infrastructure, zero-days, ransomware,
        premium sources (FT, Krebs, Dark Reading, WSJ, Bloomberg)</p>

        <p><strong>Drone Coverage:</strong> 53 searches covering military drones, autonomous systems,
        geopolitical programs, counter-drone tech, defense publications (Defense News, Jane's, Military.com)</p>
    </div>
</body>
</html>"""

    # Generate clusters HTML
    clusters_html = ""
    for i, cluster in enumerate(report.get('top_clusters', [])[:10], 1):
        entities_str = ", ".join([f"{k}: {', '.join(v[:3])}" for k, v in cluster.get('shared_entities', {}).items() if v])
        clusters_html += f"""
        <div class="cluster">
            <div class="cluster-header">Cluster #{cluster.get('cluster_id', i)} - {cluster.get('story_count', 0)} Related Stories</div>
            <div><strong>Key Entities:</strong> {entities_str or 'Various'}</div>
            <div style="margin-top: 10px;">
                <strong>Stories:</strong>
                <ul>
        """
        for story in cluster.get('stories', [])[:5]:
            intel_type = story.get('intelligence_type', 'UNKNOWN')
            badge_class = 'cyber-badge' if intel_type == 'CYBER_THREAT' else 'drone-badge'
            badge_text = '💻 CYBER' if intel_type == 'CYBER_THREAT' else '🚁 DRONE'
            clusters_html += f"""
                    <li>
                        <a href="{story.get('Link', '#')}" target="_blank">{story.get('Title', 'Untitled')}</a>
                        <span class="intelligence-type {badge_class}">{badge_text}</span>
                        <div class="story-meta">Source: {story.get('Source', 'Unknown')} | {story.get('Published', 'Unknown')}</div>
                    </li>
            """
        clusters_html += """
                </ul>
            </div>
        </div>
        """

    # Generate cyber stories HTML
    cyber_stories_html = ""
    for story in cyber_stories[:20]:
        cyber_stories_html += f"""
        <div class="story">
            <h3><a href="{story.get('Link', '#')}" target="_blank">{story.get('Title', 'Untitled')}</a></h3>
            <div class="story-meta">Source: {story.get('Source', 'Unknown')} | Published: {story.get('Published', 'Unknown')}</div>
            <div class="story-meta">Category: {story.get('Category', 'Uncategorized')}</div>
        </div>
        """

    # Generate drone stories HTML
    drone_stories_html = ""
    for story in drone_stories[:20]:
        drone_stories_html += f"""
        <div class="story">
            <h3><a href="{story.get('Link', '#')}" target="_blank">{story.get('Title', 'Untitled')}</a></h3>
            <div class="story-meta">Source: {story.get('Source', 'Unknown')} | Published: {story.get('Published', 'Unknown')}</div>
            <div class="story-meta">Category: {story.get('Category', 'Uncategorized')}</div>
        </div>
        """

    html = html_template.format(
        timestamp=report.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        total_stories=report.get('total_stories', 0),
        cyber_count=len(cyber_stories),
        drone_count=len(drone_stories),
        cluster_count=report.get('cluster_count', 0),
        clusters_html=clusters_html,
        cyber_stories_html=cyber_stories_html or "<p>No cyber stories collected</p>",
        drone_stories_html=drone_stories_html or "<p>No drone stories collected</p>"
    )

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ Saved: {filename}")


def main():
    print("\n" + "="*60)
    print("COMBINED OSINT INTELLIGENCE AGGREGATOR")
    print("="*60)
    print("Cyber Threat Intelligence: 84 searches")
    print("  - APTs, nation-states, vulnerabilities")
    print("  - Semiconductor supply chain")
    print("  - Economic warfare & sanctions")
    print("  - Space/satellite intelligence")
    print("Military Drone Intelligence: 53 searches")
    print("  - Combat UAVs, autonomous systems")
    print("  - Geopolitical programs, counter-drone")
    print("Total: 137 targeted OSINT searches")
    print("="*60 + "\n")

    # Collect cyber threat intelligence
    print("📡 PHASE 1: Collecting Cyber Threat Intelligence...")
    print("="*60)
    cyber_stories = scrape_google_news_multi()

    # Collect military drone intelligence
    print("\n📡 PHASE 2: Collecting Military Drone Intelligence...")
    print("="*60)
    drone_stories = scrape_drone_news_multi()

    # Merge all intelligence
    all_stories = merge_intelligence_sources(cyber_stories, drone_stories)

    # Correlate and analyze
    print("🔗 PHASE 3: Correlating Intelligence...")
    print("="*60)
    intelligence_report = analyze_stories(all_stories, similarity_threshold=0.3)

    # Add intelligence breakdown
    intelligence_report['cyber_count'] = len(cyber_stories)
    intelligence_report['drone_count'] = len(drone_stories)

    # Save outputs
    print("\n💾 PHASE 4: Saving Reports...")
    print("="*60)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    os.makedirs('data/output', exist_ok=True)

    # Save JSON report
    save_json_report(
        intelligence_report,
        f'data/output/combined_intelligence_{timestamp}.json'
    )

    # Save HTML report
    save_html_report(
        intelligence_report,
        f'data/output/combined_intelligence_{timestamp}.html'
    )

    print("\n" + "="*60)
    print("✅ COMBINED INTELLIGENCE COLLECTION COMPLETE")
    print("="*60)
    print(f"Cyber Intelligence: {len(cyber_stories)} stories")
    print(f"Drone Intelligence: {len(drone_stories)} stories")
    print(f"Total Stories: {intelligence_report['total_stories']}")
    print(f"Story Clusters: {intelligence_report['cluster_count']}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
