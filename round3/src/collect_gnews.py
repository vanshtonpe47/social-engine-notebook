from __future__ import annotations

import csv
import hashlib
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests


QUERIES = [
    "Claude for Teachers",
    "Anthropic Claude teachers education AI",
    "Claude for Teachers criticism privacy classroom",
]

API_URL = "https://gnews.io/api/v4/search"
USER_AGENT = "Round3SocialEngineStudy/1.0"


def now_iso( ):
    return datetime.now(timezone.utc).isoformat()


def make_record_id(url, title):
    text = f"{url}|{title}"
    return hashlib.sha1(text.encode()).hexdigest()[:16]


def main():
    api_key = os.getenv("GNEWS_API_KEY")

    if not api_key:
        print("ERROR: GNEWS_API_KEY is not set.")
        print("Set your key in PowerShell before running this program.")
        sys.exit(1)

    if len(sys.argv) > 1:
        output_file = Path(sys.argv[1])
    else:
        output_file = Path(
            "round3/data/gnews_claude_for_teachers.csv"
        )

    output_file.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    seen_urls = set()

    for query in QUERIES:
        print(f"Collecting articles for: {query}")

        response = requests.get(
            API_URL,
            params={
                "q": query,
                "lang": "en",
                "max": 10,
                "sortby": "publishedAt",
                "apikey": api_key,
            },
            headers={
                "User-Agent": USER_AGENT
            },
            timeout=30,
        )

        response.raise_for_status()
        time.sleep(3)
        result = response.json()

        for article in result.get("articles", []):
            title = (article.get("title") or "").strip()
            description = (article.get("description") or "").strip()
            url = (article.get("url") or "").strip()

            if not title or not url:
                continue

            if url in seen_urls:
                continue

            seen_urls.add(url)

            source = article.get("source") or {}

            rows.append(
                {
                    "record_id": make_record_id(url, title),
                    "source_type": "gnews_api",
                    "source_name": source.get("name", ""),
                    "title": title,
                    "text": f"{title}. {description}".strip(),
                    "url": url,
                    "published_at": article.get(
                        "publishedAt", ""
                    ),
                    "collected_at": now_iso(),
                    "engagement_value": 1,
                    "engagement_type": "article_mention",
                    "query": query,
                }
            )

    fields = [
        "record_id",
        "source_type",
        "source_name",
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
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print("")
    print(f"Collected {len(rows)} unique GNews records.")
    print(f"Saved file: {output_file}")
    print("Your API key was not saved in the CSV file.")


if __name__ == "__main__":
    main()
