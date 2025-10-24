#!/usr/bin/env python3
"""
OSINT Mosaic Intelligence Aggregator
Collects stories from multiple sources and identifies connections to build the big picture
"""

import os
import sys
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from collectors.google_news_scraper import scrape_google_news_multi
from processors.story_correlator import analyze_stories


def save_json_report(data: dict, filename: str):
    """Save data to JSON file"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved: {filename}")


def save_html_report(report: dict, filename: str):
    """Generate interactive HTML report with network visualization"""
    html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>OSINT Mosaic Intelligence Report</title>
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
        .header .subtitle {{
            opacity: 0.9;
            margin-top: 10px;
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
        .stat-card .number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-card .label {{
            color: #666;
            margin-top: 5px;
        }}
        .section {{
            background: white;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            margin-top: 0;
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        .cluster {{
            border-left: 4px solid #667eea;
            padding: 15px;
            margin: 15px 0;
            background: #f9f9f9;
        }}
        .cluster-header {{
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }}
        .story {{
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }}
        .story:last-child {{
            border-bottom: none;
        }}
        .story a {{
            color: #333;
            text-decoration: none;
        }}
        .story a:hover {{
            color: #667eea;
        }}
        .story .source {{
            color: #999;
            font-size: 0.9em;
            margin-left: 10px;
        }}
        .connection-group {{
            margin: 15px 0;
        }}
        .connection-group h3 {{
            color: #667eea;
            font-size: 1.1em;
            margin-bottom: 10px;
        }}
        .entity {{
            display: inline-block;
            background: #e7e7ff;
            padding: 5px 12px;
            margin: 5px;
            border-radius: 15px;
            font-size: 0.9em;
        }}
        .entity .count {{
            background: #667eea;
            color: white;
            padding: 2px 8px;
            border-radius: 10px;
            margin-left: 8px;
            font-weight: bold;
        }}
        .timeline-item {{
            padding: 10px;
            border-left: 3px solid #667eea;
            margin: 10px 0;
            padding-left: 20px;
        }}
        .timeline-item .time {{
            color: #999;
            font-size: 0.85em;
        }}
        .badge {{
            display: inline-block;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.85em;
            margin-right: 8px;
        }}
        .badge-category {{
            background: #e7e7ff;
            color: #667eea;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 OSINT Mosaic Intelligence Report</h1>
        <div class="subtitle">Generated: {timestamp}</div>
    </div>

    <div class="stats">
        <div class="stat-card">
            <div class="number">{total_stories}</div>
            <div class="label">Total Stories Collected</div>
        </div>
        <div class="stat-card">
            <div class="number">{story_clusters}</div>
            <div class="label">Story Clusters Identified</div>
        </div>
        <div class="stat-card">
            <div class="number">{connection_points}</div>
            <div class="label">Connection Points</div>
        </div>
        <div class="stat-card">
            <div class="number">{theme_count}</div>
            <div class="label">Key Themes</div>
        </div>
    </div>

    <div class="section">
        <h2>📊 Top Themes</h2>
        {themes_html}
    </div>

    <div class="section">
        <h2>🔗 Key Connection Points</h2>
        <p>These entities appear across multiple stories, connecting different threads of intelligence:</p>
        {connections_html}
    </div>

    <div class="section">
        <h2>🧩 Story Clusters (Mosaic Tiles)</h2>
        <p>Related stories grouped together. Each cluster represents a distinct intelligence thread:</p>
        {clusters_html}
    </div>

    <div class="section">
        <h2>⏱️ Recent Intelligence Timeline</h2>
        {timeline_html}
    </div>

    <div class="section">
        <h2>📄 Full Data Export</h2>
        <p>View complete JSON data: <a href="mosaic_intelligence_report.json" target="_blank">mosaic_intelligence_report.json</a></p>
    </div>
</body>
</html>"""

    # Build themes HTML
    themes_html = ""
    for theme, count in list(report['summary']['top_themes'].items())[:10]:
        themes_html += f'<div class="entity">{theme}<span class="count">{count}</span></div>'

    # Build connections HTML
    connections_html = ""
    for entity_type, entities in report['connections'].items():
        if entities:
            connections_html += f'<div class="connection-group"><h3>{entity_type.replace("_", " ").title()}</h3>'
            for name, data in list(entities.items())[:8]:
                connections_html += f'<div class="entity">{name}<span class="count">{data["mention_count"]}</span></div>'
            connections_html += '</div>'

    # Build clusters HTML
    clusters_html = ""
    for i, cluster in enumerate(report['clusters'][:15], 1):
        clusters_html += f'<div class="cluster">'
        clusters_html += f'<div class="cluster-header">Cluster {i} — {cluster["size"]} related stories</div>'
        for story in cluster['stories']:
            clusters_html += f'<div class="story">'
            clusters_html += f'<a href="{story["link"]}" target="_blank">{story["title"]}</a>'
            clusters_html += f'<span class="source">{story["source"]}</span>'
            clusters_html += f'<span class="badge badge-category">{story["category"]}</span>'
            clusters_html += f'</div>'
        clusters_html += '</div>'

    # Build timeline HTML
    timeline_html = ""
    for item in report['timeline'][:30]:
        timeline_html += f'<div class="timeline-item">'
        timeline_html += f'<div class="time">{item["time"]} — {item["source"]}</div>'
        timeline_html += f'<a href="{item["link"]}" target="_blank">{item["title"]}</a>'
        timeline_html += f'<span class="badge badge-category">{item["category"]}</span>'
        timeline_html += '</div>'

    # Format HTML
    html = html_template.format(
        timestamp=report['timestamp'],
        total_stories=report['summary']['total_stories'],
        story_clusters=report['summary']['story_clusters'],
        connection_points=report['summary']['connection_points'],
        theme_count=len(report['summary']['top_themes']),
        themes_html=themes_html,
        connections_html=connections_html,
        clusters_html=clusters_html,
        timeline_html=timeline_html
    )

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Saved: {filename}")


def main():
    """Main orchestration function"""
    print("="*70)
    print("🔍 OSINT MOSAIC INTELLIGENCE AGGREGATOR")
    print("="*70)
    print("Collecting intelligence from 50+ Google News searches...")
    print("Then analyzing connections to build the bigger picture\n")

    # Create output directories
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("data/output", exist_ok=True)

    # Step 1: Collect stories
    print("\n[STEP 1] Collecting stories from Google News...")
    stories = scrape_google_news_multi()

    if not stories:
        print("\n❌ No stories collected. Exiting.")
        return

    # Save raw data
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    raw_file = f"data/raw/stories_{timestamp}.json"
    save_json_report(stories, raw_file)

    # Step 2: Analyze and correlate
    print("\n[STEP 2] Analyzing stories and building mosaic intelligence...")
    intelligence_report = analyze_stories(stories, similarity_threshold=0.3)

    # Save processed intelligence report
    json_report = "data/output/mosaic_intelligence_report.json"
    save_json_report(intelligence_report, json_report)

    # Generate HTML visualization
    print("\n[STEP 3] Generating HTML report...")
    html_report = "data/output/mosaic_intelligence_report.html"
    save_html_report(intelligence_report, html_report)

    # Also save to docs for easy access
    os.makedirs("docs", exist_ok=True)
    save_json_report(intelligence_report, "docs/latest_intelligence.json")
    save_html_report(intelligence_report, "docs/index.html")

    print("\n" + "="*70)
    print("✅ MOSAIC INTELLIGENCE ANALYSIS COMPLETE")
    print("="*70)
    print(f"\nReports generated:")
    print(f"  📄 HTML Report: {html_report}")
    print(f"  📊 JSON Data: {json_report}")
    print(f"  🌐 Web View: docs/index.html")
    print(f"\nTo view the report, open: {html_report}")


if __name__ == "__main__":
    main()
