# GitHub Pages Setup Guide

## 🌐 View Your Reports Online

GitHub Pages allows you to view your OSINT reports in a web browser without downloading files.

---

## Quick Setup (One-Time)

### Step 1: Enable GitHub Pages

1. Go to your repository on GitHub:
   - https://github.com/arandomguyhere/News_Feeder

2. Click **Settings** (top right)

3. In the left sidebar, click **Pages**

4. Under "Build and deployment":
   - **Source**: Select **GitHub Actions**
   - (NOT "Deploy from a branch")

5. Click **Save**

### Step 2: Run the Workflow

**Option A: Automatic (Recommended)**
- Merge your branch to `main`
- The Pages workflow runs automatically after tests pass
- Your site will be live in 2-3 minutes

**Option B: Manual Trigger**
1. Go to **Actions** tab
2. Click **Deploy to GitHub Pages** workflow
3. Click **Run workflow** button
4. Select branch: `main` (or your branch)
5. Click **Run workflow**

### Step 3: View Your Site

After deployment completes (2-3 minutes):
- Your site will be at: **https://arandomguyhere.github.io/News_Feeder/**
- Click the link in the Actions workflow to open it

---

## What You'll See

Your GitHub Pages site will show:
- 📊 **Interactive HTML Reports** - Visual story clusters and analysis
- 📄 **JSON Data Exports** - Raw data for further processing
- 🔗 **Story Connections** - Entity relationships and correlations
- 📈 **Timeline Views** - When stories were published

---

## How It Works

1. **Workflow runs** when you:
   - Push to main branch (after tests pass)
   - Manually trigger via Actions tab
   - Merge a pull request

2. **Aggregator collects** stories from:
   - GDELT database
   - Google News
   - Bing News
   - NewsAPI (if key provided)

3. **Reports generated** automatically:
   - HTML visual reports
   - JSON data exports
   - Index page listing all reports

4. **Deployed to GitHub Pages**:
   - Available at your GitHub Pages URL
   - Updates on each run

---

## Updating Reports

### Automatic Updates
Reports update automatically when:
- You push to main branch
- Tests pass successfully
- Pages workflow runs

### Manual Updates
To update reports on-demand:
1. Go to **Actions** tab
2. Select **Deploy to GitHub Pages**
3. Click **Run workflow**
4. Wait 2-3 minutes
5. Refresh your Pages URL

---

## Customization

### Change Report Frequency

Edit `.github/workflows/pages.yml` to add scheduled runs:

```yaml
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
    # or
    - cron: '0 0 * * *'    # Daily at midnight
```

### Customize Collectors

Edit `config/config.yaml` to change:
- Search queries
- Data sources
- Similarity threshold
- Output format

---

## Troubleshooting

### "404 Page Not Found"
**Solution:**
- Wait 3-5 minutes after first deployment
- Check Actions tab for deployment status
- Ensure Pages source is set to "GitHub Actions"

### "Workflow failed"
**Solution:**
- Check Actions tab for error details
- Ensure all dependencies in requirements.txt
- Check aggregator.py runs locally first

### "No reports showing"
**Solution:**
- Reports take time to generate (5-10 minutes)
- Check if aggregator collected any stories
- View workflow logs in Actions tab

---

## Testing Locally

Before deploying, test the pages locally:

```bash
# Run aggregator
python aggregator.py

# Copy reports to docs
mkdir -p docs
cp data/output/*.html docs/
cp data/output/*.json docs/

# Serve locally (Python 3)
cd docs
python -m http.server 8000

# View at: http://localhost:8000
```

---

## Security Notes

- ✅ API keys are stored in GitHub Secrets (never in code)
- ✅ Generated reports are public (GitHub Pages is public)
- ✅ No sensitive data should be in reports
- ⚠️ Don't commit `.env` file with real API keys

---

## Example GitHub Pages Sites

Your site structure will look like:
```
https://arandomguyhere.github.io/News_Feeder/
├── index.html                    # Main landing page
├── report_20241024_120000.html   # Latest report
├── stories_20241024_120000.json  # Story data
└── clusters_20241024_120000.json # Cluster data
```

---

## Next Steps

After setup:
1. ✅ Enable GitHub Pages (Settings → Pages → GitHub Actions)
2. ✅ Run the workflow (Actions → Deploy to GitHub Pages)
3. ✅ Bookmark your Pages URL
4. ✅ Share reports with your team
5. ✅ Set up scheduled runs (optional)

**Your GitHub Pages URL:**
https://arandomguyhere.github.io/News_Feeder/

---

**Need Help?**
- Check workflow logs: Actions → Deploy to GitHub Pages
- Review aggregator logs: logs/aggregator.log
- Test locally first: python aggregator.py
