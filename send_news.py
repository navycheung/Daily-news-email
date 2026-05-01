# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
import subprocess
import json

today = datetime.now().strftime('%a %d %b %Y')

# Install required package
subprocess.run(['pip', 'install', 'feedparser', '-q'], check=False)
import feedparser

def get_news_from_rss():
    """Fetch news from major news outlets RSS feeds"""
    feeds = {
        'BBC': 'http://feeds.bbc.co.uk/news/world/rss.xml',
        'Reuters': 'https://www.reutersagency.com/feed/?taxonomy=best-topics&output=rss',
        'TechCrunch': 'http://feeds.feedburner.com/TechCrunch/',
    }
    
    articles = []
    for source, url in feeds.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:2]:  # Get top 2 from each source
                articles.append({
                    'title': entry.get('title', 'No title'),
                    'summary': entry.get('summary', 'No summary available')[:500],  # First 500 chars
                    'link': entry.get('link', ''),
                    'source': source
                })
        except:
            pass
    
    return articles

# Fetch real news
all_articles = get_news_from_rss()

# Build email body
lines = ["每日簡報 — " + today, ""]

if all_articles:
    lines.append("世界新聞")
    for i, article in enumerate(all_articles[:5], 1):
        lines.append(f"\n{i}. {article['title']}")
        lines.append(f"來源: {article['source']}")
        lines.append(f"\n{article['summary']}...")
        if article['link']:
            lines.append(f"\n閱讀全文: {article['link']}")
        lines.append("")
    
    lines.append("\n科技新聞")
    for i, article in enumerate(all_articles[5:10], 1):
        lines.append(f"\n{i}. {article['title']}")
        lines.append(f"來源: {article['source']}")
        lines.append(f"\n{article['summary']}...")
        if article['link']:
            lines.append(f"\n閱讀全文: {article['link']}")
        lines.append("")
else:
    # Fallback to summary if RSS fails
    lines.append("Unable to fetch live news. Please check news sites directly.")

body = "\n".join(lines)

sender = "navycheung@gmail.com"
recipient = "navycheung@msn.com"
password = os.environ.get('GMAIL_PASSWORD')

if not password:
    print("ERROR: GMAIL_PASSWORD not set")
    exit(1)

message = MIMEMultipart('alternative')
message['From'] = sender
message['To'] = recipient
message['Subject'] = "每日簡報 — " + today
message.attach(MIMEText(body, 'plain', 'utf-8'))

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    server.send_message(message)
    server.quit()
    print("Email sent with full article content")
except Exception as e:
    print("ERROR: " + str(e))
    exit(1)
