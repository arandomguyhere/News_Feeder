# Testing Guide

## Quick Test

Run the basic functionality test:

```bash
python test_aggregator.py
```

This tests:
- Story creation and data structures
- NLP processing (entity extraction, keywords)
- Similarity calculation
- Story correlation and clustering
- Verifies related stories cluster together

## Full Integration Test

To test the full aggregator with real data:

```bash
# Without API keys (uses GDELT and web scraping only)
python aggregator.py

# With NewsAPI key for better results
echo "NEWSAPI_KEY=your_key" > .env
python aggregator.py
```

Expected output:
- Logs in `logs/aggregator.log`
- JSON files in `data/output/`:
  - `stories_*.json` - All collected stories
  - `clusters_*.json` - Story clusters
  - `summary_*.json` - Summary statistics
  - `report_*.html` - Visual report

## Manual Testing Checklist

### 1. Data Collection
- [ ] NewsAPI collector works (if key provided)
- [ ] GDELT collector works
- [ ] Web scrapers work (Google News, Bing News)
- [ ] Stories are deduplicated correctly
- [ ] No duplicate URLs in output

### 2. NLP Processing
- [ ] Entities are extracted from stories
- [ ] Keywords are extracted
- [ ] Similarity calculations return reasonable values (0.0-1.0)
- [ ] Works with and without spaCy installed

### 3. Correlation Engine
- [ ] Related stories cluster together
- [ ] Unrelated stories stay separate
- [ ] Similarity threshold is respected
- [ ] Shared entities are identified

### 4. Output Generation
- [ ] JSON files are valid JSON
- [ ] HTML report renders correctly
- [ ] All stories are included in output
- [ ] No errors in logs

## Testing Different Scenarios

### Low Similarity Threshold (0.1-0.15)
```yaml
# config/config.yaml
processing:
  similarity_threshold: 0.1
```
**Expected:** More stories cluster together, some may be loosely related

### Medium Similarity Threshold (0.15-0.3)
```yaml
processing:
  similarity_threshold: 0.2
```
**Expected:** Balanced clustering, most clusters have truly related stories

### High Similarity Threshold (0.3-0.5)
```yaml
processing:
  similarity_threshold: 0.4
```
**Expected:** Only very similar stories cluster, most stories in single-story clusters

## Performance Testing

Test with different query volumes:

```yaml
# Small test - Fast
gdelt:
  queries:
    - "cyberattack"
  max_records: 50

# Medium test - Moderate
gdelt:
  queries:
    - "cyberattack"
    - "data breach"
  max_records: 100

# Large test - Slow but comprehensive
gdelt:
  queries:
    - "cyberattack"
    - "data breach"
    - "intelligence"
    - "surveillance"
  max_records: 250
```

## Troubleshooting Tests

### No stories collected
**Check:**
- Internet connection
- Collector enabled in config
- API keys (if using NewsAPI)
- Logs for error messages

### Stories not clustering
**Check:**
- Similarity threshold (try lowering to 0.1)
- Stories have enough text content
- NLP processor working correctly

### Import errors
**Fix:**
```bash
pip install -r requirements.txt
```

### spaCy warnings
**Optional fix:**
```bash
python -m spacy download en_core_web_sm
```
Note: Aggregator works without spaCy using fallback processing

## Automated Testing

### GitHub Actions
Tests run automatically on push:
- `test.yml` - Runs basic functionality tests
- `lint.yml` - Code quality checks
- `security.yml` - Security scans

View results at: `https://github.com/arandomguyhere/News_Feeder/actions`

### Local CI Simulation

Run the same checks locally:

```bash
# Install test tools
pip install flake8 black safety bandit

# Run all checks
python test_aggregator.py          # Functionality
flake8 src/ --count                # Linting
black --check src/                 # Formatting
safety check                       # Security (dependencies)
bandit -r src/                     # Security (code)
```

## Test Coverage

Current test coverage:
- ✅ Basic functionality (test_aggregator.py)
- ✅ Import verification
- ✅ GitHub Actions CI/CD
- ⚠️ Unit tests for individual components (future)
- ⚠️ Integration tests with mock data (future)
- ⚠️ Performance benchmarks (future)

## Future Testing Improvements

1. **Unit Tests**
   - Individual collector tests with mocked responses
   - NLP processor tests with sample texts
   - Correlation engine tests with known similar stories

2. **Integration Tests**
   - End-to-end tests with sample datasets
   - Test different configuration combinations
   - Verify output format compliance

3. **Performance Tests**
   - Benchmark processing speed
   - Memory usage profiling
   - Scalability tests with large datasets

4. **Regression Tests**
   - Keep known good outputs
   - Compare against previous runs
   - Detect unexpected changes
