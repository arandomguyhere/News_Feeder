# GitHub Pages Quick Start - Step by Step

## 🎯 Goal
Get your OSINT reports viewable online at: **https://arandomguyhere.github.io/News_Feeder/**

---

## ✅ Step 1: Enable GitHub Pages (One-Time Setup)

### 1.1 Go to Repository Settings
1. Open your browser
2. Go to: **https://github.com/arandomguyhere/News_Feeder**
3. Look at the top of the page
4. Click the **⚙️ Settings** tab (far right, after "Insights")

### 1.2 Navigate to Pages Settings
1. In the left sidebar, scroll down
2. Look for the "Code and automation" section
3. Click **Pages** (it has a 🌐 icon)

### 1.3 Configure Build Source
You'll see a page titled "GitHub Pages"

**Under "Build and deployment" section:**

1. Find the **Source** dropdown (currently says "Deploy from a branch")
2. Click the **Source** dropdown
3. Select **GitHub Actions** ← THIS IS CRITICAL!
   - ❌ DO NOT select "Deploy from a branch"
   - ✅ SELECT "GitHub Actions"

4. The page will refresh automatically
5. You'll see "GitHub Actions" is now selected

**That's it for Settings!** ✅

---

## ✅ Step 2: Run the Deployment Workflow

### 2.1 Go to Actions Tab
1. At the top of your repository page
2. Click the **Actions** tab (between "Pull requests" and "Projects")

### 2.2 Find the Pages Workflow
You'll see a list of workflows on the left:
- Tests
- Lint
- Security Scan
- Demo Run (Manual)
- **Deploy to GitHub Pages** ← Click this one!

### 2.3 Run the Workflow
1. Click **Deploy to GitHub Pages** in the left sidebar
2. On the right side, you'll see a blue button: **Run workflow** ▼
3. Click the **Run workflow** button
4. A dropdown appears:
   ```
   Run workflow
   ┌─────────────────────────────────────┐
   │ Use workflow from                   │
   │ Branch: main                        │  ← Leave as "main" or select your branch
   │                                     │
   │        [Run workflow]               │  ← Click this green button
   └─────────────────────────────────────┘
   ```
5. Click the green **Run workflow** button inside the dropdown

### 2.4 Watch the Workflow
1. The page will refresh
2. You'll see a new yellow dot 🟡 appear (or orange spinner)
3. Click on the workflow run (the row with "Deploy to GitHub Pages")
4. You'll see two jobs:
   - **build** - Collecting stories and creating reports
   - **deploy** - Deploying to GitHub Pages

### 2.5 Wait for Completion
- The workflow takes about **5-8 minutes**
- Yellow 🟡 = Running
- Green ✅ = Success
- Red ❌ = Failed (check logs)

---

## ✅ Step 3: View Your Site!

### 3.1 Get Your URL
Once the workflow shows ✅ (green checkmark):

**Your site is live at:**
```
https://arandomguyhere.github.io/News_Feeder/
```

### 3.2 What You'll See
Your GitHub Pages site includes:

1. **Landing Page** - Beautiful index with:
   - List of all generated reports
   - Feature highlights
   - Quick start guide
   - Link back to GitHub repo

2. **HTML Reports** - Interactive reports showing:
   - Story clusters
   - Shared entities
   - Timeline of events
   - Source distribution

3. **JSON Data** - Raw data exports for analysis

---

## 📋 Summary Checklist

Use this checklist to verify everything is set up:

- [ ] **Settings → Pages**
  - [ ] Source is set to "GitHub Actions" (NOT "Deploy from a branch")

- [ ] **Actions Tab**
  - [ ] Clicked "Deploy to GitHub Pages" workflow
  - [ ] Clicked "Run workflow" button
  - [ ] Selected branch and ran workflow

- [ ] **Wait for Completion**
  - [ ] Build job completed ✅
  - [ ] Deploy job completed ✅

- [ ] **Test Your Site**
  - [ ] Visit: https://arandomguyhere.github.io/News_Feeder/
  - [ ] See landing page with reports
  - [ ] Click on a report to view it

---

## 🔄 How to Update Reports

### Automatic Updates
Reports update automatically when you:
- Push to main branch (after tests pass)
- Merge a pull request to main

### Manual Updates
To generate fresh reports anytime:
1. Go to **Actions** tab
2. Click **Deploy to GitHub Pages**
3. Click **Run workflow**
4. Click green **Run workflow** button
5. Wait 5-8 minutes
6. Refresh your GitHub Pages URL

---

## ❓ Troubleshooting

### "404 - Page Not Found"

**Check 1:** Is Pages enabled?
- Go to Settings → Pages
- Verify Source is "GitHub Actions"

**Check 2:** Did workflow complete?
- Go to Actions tab
- Check if "Deploy to GitHub Pages" shows ✅
- If ❌ red, click it to see error logs

**Check 3:** Wait a few minutes
- First deployment can take 3-5 minutes
- Try a hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)

### Workflow Failed ❌

**Common fixes:**

1. **Check the logs:**
   - Click the failed workflow
   - Click the failed job
   - Read the error message

2. **Missing dependencies:**
   - Workflow installs from requirements.txt
   - Check if requirements.txt is correct

3. **Aggregator timeout:**
   - Normal! Workflow has 5-minute timeout
   - Reports should still be generated from cached data

### No Reports Showing

**Possible reasons:**

1. **First run:**
   - Takes 5-8 minutes to collect stories
   - Be patient!

2. **No stories collected:**
   - Check workflow logs for errors
   - GDELT and web scrapers should work without API keys

3. **Reports not copied:**
   - Check "Generate reports" step in workflow logs
   - Should see "cp data/output/*.html docs/"

---

## 🎨 Customization

### Change Collection Frequency

Edit `.github/workflows/pages.yml` to add scheduled runs:

```yaml
on:
  workflow_dispatch:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_run:
    workflows: ["Tests"]
    types: [completed]
    branches: [main, master]
```

### Customize Queries

Edit `config/config.yaml` to change what stories are collected:

```yaml
sources:
  gdelt:
    queries:
      - "your topic here"
      - "another topic"
```

---

## 📞 Need Help?

1. **Check workflow logs:** Actions → Deploy to GitHub Pages → Click failed run
2. **Test locally first:** Run `python aggregator.py` on your machine
3. **Review docs:** See GITHUB_PAGES_SETUP.md for detailed troubleshooting
4. **Check GitHub status:** https://www.githubstatus.com/

---

## ✅ Success Indicators

You know it's working when:

- ✅ Settings → Pages shows "Your site is live at https://arandomguyhere.github.io/News_Feeder/"
- ✅ Actions → Deploy to GitHub Pages shows green ✅
- ✅ Visiting the URL shows your landing page
- ✅ Reports are listed and clickable
- ✅ JSON and HTML files are accessible

---

**🎉 Congratulations! Your OSINT reports are now online!**

Share your GitHub Pages URL with your team:
**https://arandomguyhere.github.io/News_Feeder/**
