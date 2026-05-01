# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
import subprocess
import re

today = datetime.now().strftime('%a %d %b %Y')

# Install required packages
subprocess.run(['pip', 'install', 'feedparser', 'beautifulsoup4', '-q'], check=False)

import feedparser
from bs4 import BeautifulSoup

def clean_html(html_text):
    """Remove HTML tags and clean up text"""
    if not html_text:
        return ""
    soup = BeautifulSoup(html_text, 'html.parser')
    text = soup.get_text()
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Limit to 400 characters
    return text[:400]

def get_news_from_rss():
    """Fetch news from major news outlets RSS feeds"""
    world_feeds = {
        'BBC': 'http://feeds.bbc.co.uk/news/world/rss.xml',
        'Reuters': 'https://www.reutersagency.com/feed/?taxonomy=best-topics&output=rss',
        'AP': 'https://apnews.com/hub/world-news/feed',
    }
    
    tech_feeds = {
        'TechCrunch': 'http://feeds.feedburner.com/TechCrunch/',
        'TheVerge': 'https://www.theverge.com/rss/index.xml',
        'ArsTechnica': 'https://feeds.arstechnica.com/arstechnica/index',
    }
    
    world_articles = []
    tech_articles = []
    
    # Fetch world news
    for source, url in world_feeds.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:3]:
                summary = clean_html(entry.get('summary', 'No summary available'))
                world_articles.append({
                    'title': entry.get('title', 'No title'),
                    'summary': summary,
                    'link': entry.get('link', ''),
                    'source': source
                })
        except:
            pass
    
    # Fetch tech news
    for source, url in tech_feeds.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:3]:
                summary = clean_html(entry.get('summary', 'No summary available'))
                tech_articles.append({
                    'title': entry.get('title', 'No title'),
                    'summary': summary,
                    'link': entry.get('link', ''),
                    'source': source
                })
        except:
            pass
    
    return world_articles, tech_articles

# Fetch real news
world_articles, tech_articles = get_news_from_rss()

# Build email body
lines = ["每日簡報 — " + today, "", "=" * 50, ""]

if world_articles or tech_articles:
    if world_articles:
        lines.append("世界新聞\n")
        for i, article in enumerate(world_articles[:5], 1):
            lines.append(f"{i}. {article['title']}")
            lines.append(f"   來源: {article['source']}")
            lines.append(f"\n   {article['summary']}...")
            if article['link']:
                lines.append(f"\n   閱讀全文: {article['link']}")
            lines.append("\n" + "-" * 50 + "\n")
    
    if tech_articles:
        lines.append("\n科技新聞\n")
        for i, article in enumerate(tech_articles[:5], 1):
            lines.append(f"{i}. {article['title']}")
            lines.append(f"   來源: {article['source']}")
            lines.append(f"\n   {article['summary']}...")
            if article['link']:
                lines.append(f"\n   閱讀全文: {article['link']}")
            lines.append("\n" + "-" * 50 + "\n")
else:
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
