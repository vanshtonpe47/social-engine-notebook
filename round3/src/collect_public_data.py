from __future__ import annotations

import csv
import hashlib
import html
import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import quote_plus
import time
import xml.etree.ElementTree as ET

import requests


GOOGLE_NEWS_QUERIES = [
    '"Claude for Teachers"',
    "Anthropic Claude teachers education AI",
    "Claude for Teachers criticism privacy classroom",
]

REDDIT_FEEDS = [
    "https://www.reddit.com/r/edtech/search.rss?q=Claude+for+Teachers&restrict_sr=1&sort=new",
    "https://www.reddit.com/r/education/search.rss?q=Claude+for+Teachers&restrict_sr=1&sort=new",
    "https://www.reddit.com/r/ClaudeAI/search.rss?q=teachers&restrict_sr=1&sort=new",
]

GOOGLE_NEWS_URL = (
    "https://news.google.com/rss/search"
    "?q={query}&hl=en-US&gl=US&ceid=US:en"
 )

USER_AGENT = "Round3SocialEngineStudy/1.0"


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def clean_text(value):
    value = html.unescape(value or "")
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def parse_date(value):
    if not value:
        return ""

    try:
        return parsedate_to_datetime(value).astimezone(
            timezone.utc
        ).isoformat()
    except Exception:
        return value


def make_record_id(source_type, url, title):
    value = f"{source_type}|{url}|{title}"
    return hashlib.sha1(value.encode()).hexdigest()[:16]


def download_xml(url):
    response = requests.get(
        url,
        headers={"User-Agent": USER_AGENT},
        timeout=30,
    )
    response.raise_for_status()
    return response.content


def get_xml_text(element, tag):
    child = element.find(tag)

    if child is None or child.text is None:
        return ""

    return child.text.strip()


def collect_google_news(rows):
    print("Collecting Google News RSS data...")

    for query in GOOGLE_NEWS_QUERIES:
        print(f"Google News search: {query}")

        url = GOOGLE_NEWS_URL.format(
            query=quote_plus(query)
        )

        try:
            xml_data = download_xml(url)
            root = ET.fromstring(xml_data)
        except Exception as error:
            print(f"Google News error: {error}")
            continue

        for item in root.findall("./channel/item"):
            title = clean_text(
                get_xml_text(item, "title")
            )

            description = clean_text(
                get_xml_text(item, "description")
            )

            article_url = get_xml_text(item, "link")
            source_name = get_xml_text(item, "source")
            published_at = parse_date(
                get_xml_text(item, "pubDate")
            )

            if not title or not article_url:
                continue

            rows.append(
                {
                    "record_id": make_record_id(
                        "google_news_rss",
                        article_url,
                        title,
                    ),
                    "source_type": "google_news_rss",
                    "source_name": source_name
                    or "Google News RSS",
                    "subreddit": "",
                    "title": title,
                    "text": f"{title}. {description}".strip(),
                    "url": article_url,
                    "published_at": published_at,
                    "collected_at": now_iso(),
                    "engagement_value": 1,
                    "engagement_type": "article_mention",
                    "query": query,
                }
            )

        time.sleep(3)


def collect_reddit(rows):
    print("Collecting Reddit RSS data...")

    for feed_url in REDDIT_FEEDS:
        print(f"Reddit feed: {feed_url}")

        try:
            xml_data = download_xml(feed_url)
            root = ET.fromstring(xml_data)
        except Exception as error:
            print(f"Reddit feed unavailable: {error}")
            continue

        atom_namespace = {
            "atom": "http://www.w3.org/2005/Atom"
        }

        entries = root.findall(
            "atom:entry",
            atom_namespace,
         )

        for entry in entries:
            title_element = entry.find(
                "atom:title",
                atom_namespace,
            )

            content_element = entry.find(
                "atom:content",
                atom_namespace,
            )

            updated_element = entry.find(
                "atom:updated",
                atom_namespace,
            )

            link_element = entry.find(
                "atom:link",
                atom_namespace,
            )

            title = clean_text(
                title_element.text
                if title_element is not None
                else ""
            )

            content = clean_text(
                content_element.text
                if content_element is not None
                else ""
            )

            published_at = (
                updated_element.text.strip()
                if updated_element is not None
                and updated_element.text
                else ""
            )

            article_url = (
                link_element.attrib.get("href", "")
                if link_element is not None
                else ""
            )

            subreddit_match = re.search(
                r"/r/([^/]+)",
                feed_url,
            )

            subreddit = (
                subreddit_match.group(1)
                if subreddit_match
                else ""
            )

            if not title or not article_url:
                continue

            rows.append(
                {
                    "record_id": make_record_id(
                        "reddit_rss",
                        article_url,
                        title,
                    ),
                    "source_type": "reddit_rss",
                    "source_name": "Reddit",
                    "subreddit": subreddit,
                    "title": title,
                    "text": f"{title}. {content}".strip(),
                    "url": article_url,
                    "published_at": published_at,
                    "collected_at": now_iso(),
                    "engagement_value": 1,
                    "engagement_type": "discussion_mention",
                    "query": feed_url,
                }
            )

        time.sleep(5)


def remove_duplicates(rows):
    unique_rows = []
    seen_urls = set()

    for row in rows:
        article_url = row["url"]

        if article_url in seen_urls:
            continue

        seen_urls.add(article_url)
        unique_rows.append(row)

    return unique_rows


def main():
    output_file = Path(
        "round3/data/"
        "google_news_reddit_raw.csv"
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    rows = []

    collect_google_news(rows)
    collect_reddit(rows)

    rows = remove_duplicates(rows)

    fields = [
        "record_id",
        "source_type",
        "source_name",
        "subreddit",
        "title",
        "text",
        "url",
        "published_at",
        "collected_at",
        "engagement_value",
        "engagement_type",
        "query",
    ]

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fields,
        )

        writer.writeheader()
        writer.writerows(rows)

    print("")
    print(f"Collected {len(rows)} unique RSS records.")
    print(f"Saved file: {output_file}")


if __name__ == "__main__":
    main()
