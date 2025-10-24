# Usage Guide

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Collection & Analysis

```bash
python3 mosaic_intelligence.py
```

This will:
- Search 50+ Google News categories
- Collect stories (takes 5-10 minutes due to rate limiting)
- Analyze and correlate stories
- Generate reports in `data/output/`

### 3. View Results

Open the HTML report:
```bash
# Mac
open data/output/mosaic_intelligence_report.html

# Linux
xdg-open data/output/mosaic_intelligence_report.html

# Windows
start data/output/mosaic_intelligence_report.html
```

## Understanding the Output

### HTML Report Sections

**1. Summary Statistics**
- Total stories collected
- Number of story clusters identified
- Connection points found
- Key themes count

**2. Top Themes**
- Categories with most stories
- Trending topics

**3. Key Connection Points**
- Entities (countries, threat actors, etc.) mentioned across multiple stories
- Badge shows how many stories mention each entity

**4. Story Clusters**
- Groups of related stories
- Each cluster represents a distinct intelligence thread
- Larger clusters = bigger/more covered stories

**5. Timeline**
- Recent stories in chronological order
- Helps identify emerging threats

### JSON Data Structure

```json
{
  "timestamp": "2025-10-23T...",
  "summary": {
    "total_stories": 150,
    "story_clusters": 45,
    "top_themes": {...},
    "connection_points": 67
  },
  "clusters": [
    {
      "size": 5,
      "stories": [...]
    }
  ],
  "connections": {
    "countries": {...},
    "threat_actors": {...},
    ...
  },
  "timeline": [...],
  "graph": {
    "nodes": [...],
    "edges": [...]
  }
}
```

## Customization

### Adjust Similarity Threshold

Edit `mosaic_intelligence.py` line 73:

```python
intelligence_report = analyze_stories(stories, similarity_threshold=0.3)
```

- **Lower (0.1-0.2)**: More aggressive clustering, finds looser connections
- **Medium (0.3-0.4)**: Balanced (default)
- **Higher (0.5-0.7)**: Only very similar stories cluster together

### Add Custom Search Queries

Edit `src/collectors/google_news_scraper.py`:

```python
searches = [
    # Add your searches here
    ("your topic when:24h", "Your Category"),

    # Example: Track specific threat actor
    ("Lazarus Group when:24h", "Lazarus"),

    # Example: Monitor specific company
    ("site:company.com security when:24h", "Company Security"),

    # ... existing searches
]
```

### Change Time Window

Modify search queries to change time range:
- `when:24h` - Last 24 hours (default)
- `when:7d` - Last 7 days
- `when:1m` - Last month

Example:
```python
("China cyber when:7d", "China Cyber Weekly")
```

## Advanced Usage

### Run Only Collection

```python
from src.collectors.google_news_scraper import scrape_google_news_multi
stories = scrape_google_news_multi()
```

### Run Only Analysis

```python
from src.processors.story_correlator import analyze_stories
import json

# Load existing data
with open('data/raw/stories_20251023_120000.json') as f:
    stories = json.load(f)

# Analyze
report = analyze_stories(stories, similarity_threshold=0.3)
```

### Extract Specific Intelligence

```python
from src.processors.story_correlator import StoryCorrelator

correlator = StoryCorrelator()

# Find all stories mentioning China
china_stories = [s for s in stories if 'china' in s['Title'].lower()]

# Find connections
connections = correlator.identify_connections(china_stories)

# Get clusters
clusters = correlator.find_story_clusters(china_stories)
```

## Automation

### Schedule Regular Collection

**Linux/Mac (cron):**

```bash
# Edit crontab
crontab -e

# Add line to run every 6 hours
0 */6 * * * cd /path/to/News_Feeder && /usr/bin/python3 mosaic_intelligence.py >> logs/cron.log 2>&1
```

**Windows (Task Scheduler):**

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., every 6 hours)
4. Action: Start a program
   - Program: `python`
   - Arguments: `mosaic_intelligence.py`
   - Start in: `C:\path\to\News_Feeder`

## Troubleshooting

### No Stories Collected

**Issue:** Google News blocking requests

**Solutions:**
- Add longer delays between searches (edit `google_news_scraper.py`)
- Use VPN/proxy
- Reduce number of searches

### Low Similarity / Few Clusters

**Issue:** Stories not clustering

**Solutions:**
- Lower similarity threshold (try 0.2)
- Verify entities are being extracted (check raw JSON)
- Add more entity patterns in `story_correlator.py`

### Import Errors

**Issue:** Module not found

**Solutions:**
```bash
# Ensure you're in project directory
cd News_Feeder

# Run with Python path
PYTHONPATH=. python3 mosaic_intelligence.py

# Or install in development mode
pip install -e .
```

## Tips for Better Intelligence

1. **Run regularly** - Intelligence is more valuable when you can track changes over time

2. **Compare reports** - Keep historical reports to identify new campaigns or shifting focus

3. **Focus searches** - Add searches for specific threats relevant to your organization

4. **Adjust threshold** - Experiment with similarity threshold for your use case

5. **Manual review** - Always manually review clusters - automated correlation aids but doesn't replace human analysis

6. **Export data** - Use JSON exports for further analysis in other tools

7. **Track entities** - Pay attention to entities appearing across multiple unrelated stories - may indicate broader campaign

## Next Steps

See README.md for planned enhancements including:
- Better NLP with spaCy
- Interactive network graphs
- Additional data sources
- Real-time monitoring
- Threat scoring
- MITRE ATT&CK mapping
