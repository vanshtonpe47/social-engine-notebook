import hashlib
import re
from pathlib import Path

import pandas as pd


RSS_FILE = Path(
    "round3/data/google_news_reddit_raw.csv"
)

GNEWS_FILE = Path(
    "round3/data/gnews_new.csv"
)

OUTPUT_FILE = Path(
    "round3/data/self_collected_round3_raw.csv"
)


def clean_title(value):
    value = str(value).lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def load_file(file_path):
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return pd.DataFrame()

    print(f"Reading: {file_path}")
    return pd.read_csv(file_path)


def main():
    rss_data = load_file(RSS_FILE)
    gnews_data = load_file(GNEWS_FILE)

    all_data = pd.concat(
        [rss_data, gnews_data],
        ignore_index=True,
        sort=False,
    )

    if all_data.empty:
        print("No data was found.")
        return

    all_data["title_key"] = (
        all_data["title"]
        .fillna("")
        .map(clean_title)
    )

    all_data["url_key"] = (
        all_data["url"]
        .fillna("")
        .astype(str)
        .str.split("?")
        .str[0]
    )

    all_data["duplicate_key"] = (
        all_data["url_key"]
        .where(
            all_data["url_key"].str.len() > 0,
            all_data["title_key"],
        )
    )

    before_count = len(all_data)

    all_data = all_data.drop_duplicates(
        subset=["duplicate_key"]
    )

    after_count = len(all_data)

    all_data["record_id"] = all_data.apply(
        lambda row: hashlib.sha1(
            f"{row['source_type']}|"
            f"{row['url']}|"
            f"{row['title']}".encode()
        ).hexdigest()[:16],
        axis=1,
    )

    columns = [
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

    for column in columns:
        if column not in all_data.columns:
            all_data[column] = ""

    all_data[columns].to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8",
    )

    print("")
    print(f"Records before duplicate removal: {before_count}")
    print(f"Records after duplicate removal: {after_count}")
    print(f"Saved combined dataset: {OUTPUT_FILE}")
    print("")
    print("Source breakdown:")
    print(
        all_data["source_type"]
        .value_counts()
        .to_string()
    )


if __name__ == "__main__":
    main()
