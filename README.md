# 🔍 OSINT Mosaic Intelligence Aggregator

An intelligent OSINT (Open Source Intelligence) system that collects cybersecurity stories from 50+ Google News searches and uses **mosaic intelligence** techniques to identify connections between seemingly separate events, building the bigger picture.

## 🎯 Concept: Mosaic Intelligence

Think of each news story as a tile in a mosaic. Individual tiles may not reveal much, but when you arrange them together and identify connections, a larger picture emerges. This tool:

- **Collects** stories from multiple sources (nation-state actors, APTs, vulnerabilities, critical infrastructure)
- **Extracts** entities (countries, threat actors, malware, companies, sectors)
- **Correlates** stories based on shared entities, topics, and timing
- **Clusters** related stories into intelligence threads
- **Visualizes** connections to reveal patterns and campaigns

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│         Google News Multi-Search Collector          │
│  50+ searches: Nation-states, APTs, CVEs, Sectors   │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│           Story Correlation Engine                   │
│  • Entity Extraction (regex-based NLP)              │
│  • Similarity Calculation (entity + word overlap)   │
│  • Clustering (group related stories)               │
│  • Connection Identification (shared entities)      │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│         Intelligence Report Generator                │
│  • JSON: Full data export                           │
│  • HTML: Interactive visual report                  │
│  • Clusters: Related story groups                   │
│  • Timeline: Temporal view                          │
│  • Graph: Network visualization (future)            │
└─────────────────────────────────────────────────────┘
```

## 📊 Data Sources

The collector searches Google News for:

**Nation-State Cyber Operations:**
- China, Russia, Iran, North Korea, DPRK cyber activities
- State-sponsored hacking campaigns

**Threat Actors & APTs:**
- Advanced Persistent Threats (APT groups)
- Ransomware operations
- Named threat actors (Salt Typhoon, Volt Typhoon, etc.)

**Critical Infrastructure:**
- Energy sector, power grid attacks
- Healthcare, financial sector targeting
- Supply chain compromises

**Vulnerabilities:**
- Zero-day exploits
- CVE disclosures
- VPN/network security (Ivanti, etc.)

**Emerging Tech:**
- AI security, quantum threats
- 5G, IoT security
- Blockchain vulnerabilities

**Premium Sources:**
- Financial Times, Wall Street Journal, Reuters, Bloomberg
- Security-focused: The Register, Dark Reading, Krebs, SecurityWeek
- Tech: TechCrunch, Wired, Forbes

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/arandomguyhere/News_Feeder.git
cd News_Feeder

# Install dependencies
pip install -r requirements.txt
```

### Run Intelligence Collection

```bash
# Run the mosaic intelligence aggregator
python3 mosaic_intelligence.py
```

This will:
1. Search 50+ Google News queries (takes 5-10 minutes)
2. Collect and deduplicate stories
3. Analyze connections and build clusters
4. Generate HTML and JSON reports

### View Results

```bash
# Open the interactive HTML report
open data/output/mosaic_intelligence_report.html

# Or view in browser
firefox docs/index.html
```

## 📁 Project Structure

```
News_Feeder/
├── mosaic_intelligence.py       # Main orchestration script
├── requirements.txt             # Python dependencies
├── config/
│   └── config.yaml             # Configuration settings
├── src/
│   ├── collectors/
│   │   └── google_news_scraper.py    # Multi-search Google News collector
│   ├── processors/
│   │   └── story_correlator.py       # Mosaic intelligence engine
│   └── correlators/                  # (Future: advanced correlation)
├── data/
│   ├── raw/                    # Raw collected stories (JSON)
│   ├── processed/              # (Future: NLP-processed data)
│   └── output/                 # Intelligence reports
└── docs/
    ├── index.html              # Latest HTML report (web view)
    └── latest_intelligence.json # Latest JSON data
```

## 🔬 How It Works

### 1. Collection Phase
The Google News scraper runs 50+ searches covering:
- Cyber operations by nation-state
- APT group activities
- Vulnerability disclosures
- Sector-specific attacks
- Premium news sources

Each search collects up to 10 articles, with deduplication applied.

### 2. Correlation Phase
The story correlator:
- **Extracts entities** using regex patterns for:
  - Countries (China, Russia, Iran, etc.)
  - Threat actors (APT groups)
  - Malware families
  - Vulnerabilities (CVEs)
  - Attack techniques
  - Targeted sectors

- **Calculates similarity** between stories:
  - Shared entities (70% weight)
  - Word overlap (30% weight)

- **Forms clusters** of related stories (similarity threshold: 0.3)

### 3. Intelligence Building
The system identifies:
- **Story clusters**: Groups of related stories (e.g., all stories about a specific campaign)
- **Connection points**: Entities appearing in multiple stories
- **Temporal patterns**: Stories emerging at the same time
- **Cross-domain links**: Stories connecting different sectors or actors

### 4. Report Generation
Outputs include:
- **HTML Report**: Interactive visual report with:
  - Summary statistics
  - Top themes
  - Key connection points
  - Story clusters
  - Timeline view

- **JSON Export**: Complete structured data for further analysis

## 📈 Example Use Cases

1. **Campaign Tracking**: Identify stories about the same APT campaign across different sources
2. **Attribution**: Find connections between different attacks by the same actor
3. **Threat Landscape**: See emerging threats and trending attack methods
4. **Sector Analysis**: Track threats to specific industries (healthcare, finance, etc.)
5. **Geopolitical Cyber**: Monitor nation-state cyber activities
6. **Supply Chain**: Connect stories about interconnected supply chain compromises

## ⚙️ Configuration

Edit `config/config.yaml` to customize:

```yaml
# Correlation sensitivity
processing:
  similarity_threshold: 0.3  # Lower = more connections (0.0-1.0)

# Output formats
output:
  format: "json"  # json, html, or both
  reports:
    timeline: true
    clusters: true
    entity_graph: true
```

## 🔮 Future Enhancements

**Phase 2 - Advanced NLP:**
- [ ] spaCy NER for better entity extraction
- [ ] Sentence-BERT embeddings for semantic similarity
- [ ] Topic modeling (LDA)
- [ ] Sentiment analysis

**Phase 3 - Visualization:**
- [ ] Interactive network graph (D3.js/Vis.js)
- [ ] Timeline visualization
- [ ] Geographic mapping
- [ ] Real-time dashboard

**Phase 4 - Additional Sources:**
- [ ] Twitter/X monitoring
- [ ] Reddit OSINT forums
- [ ] GDELT database integration
- [ ] Telegram channels
- [ ] Dark web monitoring

**Phase 5 - Intelligence Features:**
- [ ] Threat scoring
- [ ] Automated alerts
- [ ] IOC extraction
- [ ] MITRE ATT&CK mapping
- [ ] Campaign attribution

## 🛠️ Development

### Running Individual Components

```bash
# Test Google News scraper
python3 -c "from src.collectors.google_news_scraper import scrape_google_news_multi; scrape_google_news_multi()"

# Test correlation engine
python3 src/processors/story_correlator.py
```

### Adding New Search Queries

Edit `src/collectors/google_news_scraper.py` and add to the `searches` list:

```python
searches = [
    # Your new search
    ("your query when:24h", "Your Category Name"),
    # ... existing searches
]
```

## 📝 License

See LICENSE file for details.

## 🤝 Contributing

Contributions welcome! Areas of interest:
- Additional data sources
- Better NLP/entity extraction
- Visualization improvements
- New correlation algorithms
- IOC extraction
- MITRE ATT&CK mapping

## 🙏 Acknowledgments

Built for OSINT analysts, threat researchers, and security professionals who need to connect the dots across multiple information sources to build comprehensive threat intelligence.