# 🔍 OSINT Story Aggregator - Mosaic Intelligence

A Python-based OSINT (Open Source Intelligence) tool that collects stories from multiple sources and identifies related content to build comprehensive intelligence pictures. Think of it as **mosaic intelligence** - individual stories are tiles that contribute to a bigger picture.

## 🎯 Features

- **Multi-Source Collection**: Gathers stories from:
  - NewsAPI (80k+ news sources)
  - GDELT (Global news events database)
  - Google News scraping
  - Bing News scraping

- **NLP Processing**:
  - Named Entity Recognition (people, organizations, locations, events)
  - Keyword extraction
  - Text similarity analysis

- **Story Correlation**:
  - Finds related stories across sources
  - Clusters stories by similarity
  - Identifies shared entities and topics
  - Temporal and semantic relationship detection

- **Output Formats**:
  - JSON (stories, clusters, summaries)
  - HTML reports with visualizations
  - Entity graphs and timelines

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip
- Internet connection

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/arandomguyhere/News_Feeder.git
cd News_Feeder
```

2. **Run the setup script**:
```bash
./setup.sh
```

This will:
- Create a virtual environment
- Install all dependencies
- Download spaCy language model
- Create necessary directories
- Set up configuration files

3. **Configure API keys (optional)**:
```bash
cp .env.example .env
# Edit .env and add your NewsAPI key (optional)
```

### Usage

**Activate the virtual environment**:
```bash
source venv/bin/activate
```

**Run the aggregator**:
```bash
python aggregator.py
```

The aggregator will:
1. Collect stories from all configured sources
2. Process them with NLP to extract entities and keywords
3. Find related stories and create clusters
4. Generate output reports in `data/output/`

## 📋 Configuration

Edit `config/config.yaml` to customize:

- **Data sources**: Enable/disable collectors, add queries
- **Processing settings**: Similarity thresholds, entity types
- **Output options**: Formats, report types

Example configuration:

```yaml
sources:
  newsapi:
    enabled: true
    queries:
      - "cybersecurity attack"
      - "data breach"

  gdelt:
    enabled: true
    queries:
      - "cyberattack"
      - "intelligence"

processing:
  similarity_threshold: 0.3  # 0.0-1.0
  max_story_age_hours: 48

output:
  format: "both"  # json, html, or both
```

## 📊 Understanding Output

### JSON Files

- **`stories_*.json`**: All collected stories with metadata
- **`clusters_*.json`**: Related story clusters with shared entities
- **`summary_*.json`**: High-level statistics and overview

### HTML Reports

Interactive reports showing:
- Story clusters by topic
- Shared entities across stories
- Timeline of events
- Source distribution

## 🔑 API Keys

### NewsAPI (Optional)

Get a free API key at [newsapi.org](https://newsapi.org/):
- Free tier: 100 requests/day
- Access to 80,000+ news sources

Add to `.env`:
```
NEWSAPI_KEY=your_key_here
```

**Note**: The aggregator works without NewsAPI using GDELT and web scraping, but NewsAPI provides richer content.

## 🏗️ Architecture

```
News_Feeder/
├── aggregator.py          # Main orchestration script
├── config/
│   └── config.yaml        # Configuration file
├── src/
│   ├── collectors/        # Data collection modules
│   │   ├── newsapi_collector.py
│   │   ├── gdelt_collector.py
│   │   └── web_scraper_collector.py
│   ├── processors/        # NLP processing
│   │   └── nlp_processor.py
│   └── correlators/       # Story correlation
│       └── story_correlator.py
├── data/
│   └── output/           # Generated reports
└── logs/                 # Log files
```

## 🔧 Advanced Usage

### Custom Queries

Edit `config/config.yaml` to add your own search queries:

```yaml
sources:
  gdelt:
    queries:
      - "your topic here"
      - "another topic"
```

### Adjusting Similarity Threshold

Higher threshold = stricter matching (fewer, more related clusters):

```yaml
processing:
  similarity_threshold: 0.5  # Range: 0.0-1.0
```

### Adding New Collectors

Extend `BaseCollector` class in `src/collectors/`:

```python
class MyCollector(BaseCollector):
    def collect(self) -> List[Story]:
        # Your collection logic
        pass
```

## 📈 Use Cases

- **Threat Intelligence**: Track cybersecurity incidents across sources
- **Geopolitical Analysis**: Monitor evolving situations globally
- **Brand Monitoring**: Find all mentions of topics/entities
- **Research**: Aggregate information on specific subjects
- **News Analysis**: Understand story coverage patterns

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- Additional data sources (Twitter, Reddit, etc.)
- Advanced NLP (semantic embeddings, topic modeling)
- Graph database integration (Neo4j)
- Real-time monitoring
- Web dashboard
- Advanced visualizations

## 📝 License

MIT License - see LICENSE file

## ⚠️ Ethical Use

This tool is for **defensive security and research purposes only**:
- ✅ Threat intelligence gathering
- ✅ Security research
- ✅ News analysis
- ✅ Academic research
- ❌ Malicious reconnaissance
- ❌ Privacy invasion
- ❌ Unauthorized data harvesting

Always respect:
- Website terms of service
- Rate limiting
- robots.txt files
- Privacy laws and regulations

## 🐛 Troubleshooting

**"spaCy model not found"**:
```bash
python -m spacy download en_core_web_sm
```

**"No stories collected"**:
- Check your internet connection
- Verify API keys (if using NewsAPI)
- Check logs in `logs/aggregator.log`

**"Import errors"**:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## 📚 Resources

- [OSINT Framework](https://osintframework.com/)
- [Bellingcat](https://www.bellingcat.com/)
- [GDELT Project](https://www.gdeltproject.org/)
- [spaCy Documentation](https://spacy.io/)

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review logs in `logs/`

---

**Built with Python, spaCy, and open-source intelligence principles**
