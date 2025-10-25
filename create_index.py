#!/usr/bin/env python3
"""Create index.html for GitHub Pages"""

import os
from pathlib import Path
from datetime import datetime

# Scan docs directory for report files
docs_dir = Path('docs')
docs_dir.mkdir(exist_ok=True)

html_files = sorted(docs_dir.glob('*.html'), key=os.path.getmtime, reverse=True)
json_files = sorted(docs_dir.glob('*.json'), key=os.path.getmtime, reverse=True)

# Filter out index.html
html_files = [f for f in html_files if f.name != 'index.html']

# Build file list HTML
files_html = ''
if html_files or json_files:
    for html_file in html_files:
        file_time = datetime.fromtimestamp(html_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        files_html += f'''
            <li>
                <a href="{html_file.name}">
                    <span class="icon">📊</span>
                    {html_file.name}
                    <span class="badge">HTML Report</span>
                    <span class="time">{file_time}</span>
                </a>
            </li>'''

    for json_file in json_files:
        file_time = datetime.fromtimestamp(json_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        files_html += f'''
            <li>
                <a href="{json_file.name}">
                    <span class="icon">📄</span>
                    {json_file.name}
                    <span class="badge">JSON Data</span>
                    <span class="time">{file_time}</span>
                </a>
            </li>'''
else:
    files_html = '<li><span class="icon">ℹ️</span> No reports available yet. Run the aggregator to generate reports.</li>'

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OSINT Story Aggregator - Reports</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        h1 {{
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}
        .subtitle {{
            color: #666;
            margin-bottom: 30px;
            font-size: 1.2em;
        }}
        .section {{
            margin: 30px 0;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        .section h2 {{
            color: #667eea;
            margin-bottom: 15px;
        }}
        .file-list {{
            list-style: none;
        }}
        .file-list li {{
            padding: 10px;
            margin: 5px 0;
            background: white;
            border-radius: 5px;
            transition: transform 0.2s;
        }}
        .file-list li:hover {{
            transform: translateX(5px);
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .file-list a {{
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
            display: flex;
            align-items: center;
            flex-wrap: wrap;
        }}
        .file-list a:hover {{
            color: #764ba2;
        }}
        .icon {{
            margin-right: 10px;
            font-size: 1.2em;
        }}
        .badge {{
            display: inline-block;
            padding: 5px 10px;
            background: #e7e7ff;
            color: #667eea;
            border-radius: 12px;
            font-size: 0.9em;
            margin-left: 10px;
        }}
        .time {{
            display: inline-block;
            margin-left: auto;
            font-size: 0.85em;
            color: #999;
        }}
        .info-box {{
            background: #e7f3ff;
            border: 1px solid #b3d9ff;
            border-radius: 5px;
            padding: 15px;
            margin: 20px 0;
        }}
        .info-box strong {{
            color: #0066cc;
        }}
        footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            text-align: center;
            color: #666;
        }}
        .github-link {{
            display: inline-block;
            margin-top: 10px;
            padding: 10px 20px;
            background: #333;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background 0.2s;
        }}
        .github-link:hover {{
            background: #000;
        }}
        code {{
            background: #f5f5f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: monospace;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 OSINT Story Aggregator</h1>
        <p class="subtitle">Mosaic Intelligence Reports</p>

        <div class="info-box">
            <strong>About:</strong> This page displays reports generated by the OSINT Story Aggregator,
            which collects and correlates stories from multiple sources to build comprehensive intelligence pictures.
        </div>

        <div class="section">
            <h2>📊 Latest Reports</h2>
            <ul class="file-list">
                {files_html}
            </ul>
        </div>

        <div class="section">
            <h2>📄 Features</h2>
            <ul class="file-list">
                <li><span class="icon">🔗</span> Multi-source data collection (NewsAPI, GDELT, Google News)</li>
                <li><span class="icon">🧠</span> NLP-powered entity extraction and keyword analysis</li>
                <li><span class="icon">🧩</span> Story correlation and clustering (Mosaic Intelligence)</li>
                <li><span class="icon">📈</span> Interactive HTML reports with visualizations</li>
                <li><span class="icon">🔍</span> JSON data exports for further analysis</li>
            </ul>
        </div>

        <div class="section">
            <h2>🚀 Quick Start</h2>
            <p>To generate your own reports, clone the repository and run:</p>
            <p style="margin-top: 10px;">
                <code>git clone https://github.com/arandomguyhere/News_Feeder.git</code><br>
                <code>cd News_Feeder</code><br>
                <code>pip install -r requirements.txt</code><br>
                <code>python aggregator.py</code>
            </p>
        </div>

        <footer>
            <p>Built with Python, scikit-learn, and open-source intelligence principles</p>
            <a href="https://github.com/arandomguyhere/News_Feeder" class="github-link" target="_blank">
                View on GitHub
            </a>
        </footer>
    </div>
</body>
</html>
'''

with open('docs/index.html', 'w') as f:
    f.write(html_content)

print('✅ Index page created successfully at docs/index.html')
if html_files or json_files:
    print(f'   Found {len(html_files)} HTML reports and {len(json_files)} JSON files')
else:
    print('   No reports found in docs/ directory yet')
