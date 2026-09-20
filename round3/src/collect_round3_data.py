from __future__ import annotations

import csv
import hashlib
import html
import os
import re
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import quote_plus

import requests

GOOGLE_QUERIES = [
    '"Claude for Teachers"',
    "Anthropic Claude teachers education AI",
    "Claude for Teachers criticism privacy classroom",
]
REDDIT_FEEDS = [
    "https://www.reddit.com/r/edtech/search.rss?q=Claude+for+Teachers&restrict_sr=1&sort=new",
    "https://www.reddit.com/r/education/search.rss?q=Claude+for+Teachers&restrict_sr=1&sort=new",
    "https://www.reddit.com/r/ClaudeAI/search.rss?q=teachers&restrict_sr=1&sort=new",
]
NEWS_RSS = "https://news.google.com/rss/search?q={}&hl=en-US&gl=US&ceid=US:en"
GNEWS_API = "https://gnews.io/api/v4/search"
USER_AGENT = "Round3SocialEngineStudy/1.0"
FIELDS = [
    "record_id", "source_type", "source_name", "subreddit", "title", "text",
    "url", "published_at", "collected_at", "engagement_value", "engagement_type", "query",
]


def now():
    return datetime.now(timezone.utc).isoformat()


def clean(value):
    value = html.unescape(value or "")
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def parse_date(value):
    try:
        return parsedate_to_datetime(value).astimezone(timezone.utc).isoformat()
    except Exception:
        return value or ""


def rid(source, url, title):
    return hashlib.sha1(f"{source}|{url}|{title}".encode()).hexdigest()[:16]


def get(url, params=None):
    response = requests.get(url, params=params, headers={"User-Agent": USER_AGENT}, timeout=30)
    response.raise_for_status()
    return response


def add(rows, source, source_name, subreddit, title, text, url, published, query, kind):
    if not title or not url:
        return
    rows.append({
        "record_id": rid(source, url, title),
        "source_type": source,
        "source_name": source_name,
        "subreddit": subreddit,
        "title": title,
        "text": f"{title}. {text}".strip(),
        "url": url,
        "published_at": published,
        "collected_at": now(),
        "engagement_value": 1,
        "engagement_type": kind,
        "query": query,
    })


def collect_gnews(rows):
    key = os.getenv("GNEWS_API_KEY")
    if not key:
        print("GNEWS_API_KEY not set; skipping GNews API.")
        return
    for query in GOOGLE_QUERIES:
        response = get(GNEWS_API, {"q": query, "lang": "en", "max": 10, "sortby": "publishedAt", "apikey": key})
        for article in response.json().get("articles", []):
            source = article.get("source") or {}
            add(rows, "gnews_api", source.get("name", ""), "", article.get("title", ""), article.get("description", ""), article.get("url", ""), article.get("publishedAt", ""), query, "article_mention")
        time.sleep(3)


def collect_google(rows):
    for query in GOOGLE_QUERIES:
        root = ET.fromstring(get(NEWS_RSS.format(quote_plus(query))).content)
        for item in root.findall("./channel/item"):
            source = item.find("source")
            add(rows, "google_news_rss", source.text.strip() if source is not None and source.text else "Google News RSS", "", clean(item.findtext("title", "")), clean(item.findtext("description", "")), item.findtext("link", ""), parse_date(item.findtext("pubDate", "")), query, "article_mention")
        time.sleep(3)


def collect_reddit(rows):
    for feed in REDDIT_FEEDS:
        try:
            root = ET.fromstring(get(feed).content)
        except Exception as error:
            print(f"Reddit feed unavailable: {error}")
            continue
        subreddit_match = re.search(r"/r/([^/]+)", feed)
        subreddit = subreddit_match.group(1) if subreddit_match else ""
        ns = "{http://www.w3.org/2005/Atom}"
        for entry in root.findall(f"{ns}entry"):
            link = entry.find(f"{ns}link")
            add(rows, "reddit_rss", "Reddit", subreddit, clean(entry.findtext(f"{ns}title", "")), clean(entry.findtext(f"{ns}content", "")), link.attrib.get("href", "") if link is not None else "", entry.findtext(f"{ns}updated", ""), feed, "discussion_mention")
        time.sleep(5)


def main():
    output = Path(sys.argv[1] if len(sys.argv) > 1 else "round3/data/self_collected_round3_raw.csv")
    rows = []
    collect_gnews(rows)
    collect_google(rows)
    collect_reddit(rows)
    unique = {}
    for row in rows:
        key = row["url"].split("?")[0] or row["title"].lower()
        unique[key] = row
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(unique.values())
    print(f"Collected {len(unique)} unique records.")
    print(f"Saved: {output}")
    print("API keys are read from the environment and are not written to the dataset.")


if __name__ == "__main__":
    main()
