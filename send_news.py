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
subprocess.run(['pip', 'install', 'feedparser', 'beautifulsoup4', 'google-trans-new', '-q'], check=False)

import feedparser
from bs4 import BeautifulSoup
from google_trans_new import google_translator

translator = google_translator()

def clean_html(html_text):
    """Remove HTML tags and clean up text"""
    if not html_text:
        return ""
    soup = BeautifulSoup(html_text, 'html.parser')
    text = soup.get_text()
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:400]

def translate_to_chinese(text):
    """Translate text to Traditional Chinese"""
    if not text:
        return ""
    try:
        result = translator.translate(text, lang_src='en', lang_tgt='zh-TW')
        return result
    except:
        return text

def get_news_from_rss():
    """Fetch news from major news outlets RSS feeds"""
    world_feeds = {
        'BBC World': 'http://feeds.bbc.co.uk/news/world/rss.xml',
        'CNN': 'http://rss.cnn.com/rss/cnn_world.rss',
        'Guardian': 'https://www.theguardian.com/world/rss',
        'Reuters': 'https://www.reuters.com/world',
    }
    
    tech_feeds = {
        'TechCrunch': 'http://feeds.feedburner.com/TechCrunch/',
        'TheVerge': 'https://www.theverge.com/rss/index.xml',
        'Wired': 'https://www.wired.com/feed/rss',
        'Ars Technica': 'https://feeds.arstechnica.com/arstechnica/index',
    }
    
    world_articles = []
    tech_articles = []
    
    # Fetch world news
    for source, url in world_feeds.items():
        try:
            feed = feedparser.parse(url)
            if feed.entries:
                for entry in feed.entries[:3]:
                    summary = clean_html(entry.get('summary', '') or entry.get('description', ''))
                    if summary:
                        world_articles.append({
                            'title': translate_to_chinese(entry.get('title', 'No title')),
                            'summary': translate_to_chinese(summary),
                            'link': entry.get('link', ''),
                            'source': source
                        })
        except Exception as e:
            pass
    
    # Fetch tech news
    for source, url in tech_feeds.items():
        try:
            feed = feedparser.parse(url)
            if feed.entries:
                for entry in feed.entries[:3]:
                    summary = clean_html(entry.get('summary', '') or entry.get('description', ''))
                    if summary:
                        tech_articles.append({
                            'title': translate_to_chinese(entry.get('title', 'No title')),
                            'summary': translate_to_chinese(summary),
                            'link': entry.get('link', ''),
                            'source': source
                        })
        except Exception as e:
            pass
    
    return world_articles, tech_articles

# Fetch real news
world_articles, tech_articles = get_news_from_rss()

# Build email body
lines = ["每日簡報 — " + today, "", "=" * 50, ""]

if world_articles or tech_articles:
    if world_articles:
        lines.append("\n世界新聞\n")
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
    print("Email sent with Traditional Chinese content")
except Exception as e:
    print("ERROR: " + str(e))
    exit(1)
