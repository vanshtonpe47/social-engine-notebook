from pathlib import Path
import re

import pandas as pd


INPUT_FILE = Path(
    "round3/data/self_collected_round3_raw.csv"
)

CLEAN_FILE = Path(
    "round3/data/self_collected_round3_clean.csv"
)

LOG_FILE = Path(
    "round3/data/cleaning_log.csv"
)

EVENT_START_DATE = pd.Timestamp(
    "2026-07-14",
    tz="UTC",
)


def normalize_title(value):
    value = str(value).lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def is_relevant(text):
    text = str(text).lower()

    has_event_word = (
        "claude for teachers" in text
        or "anthropic" in text
    )

    education_words = [
        "teacher",
        "teachers",
        "classroom",
        "school",
        "education",
        "educator",
        "student",
        "k-12",
    ]

    has_education_word = any(
        word in text
        for word in education_words
    )

    return has_event_word and has_education_word


def main():
    if not INPUT_FILE.exists():
        print(f"Input file not found: {INPUT_FILE}")
        return

    data = pd.read_csv(INPUT_FILE)

    data["published_at_parsed"] = pd.to_datetime(
        data["published_at"],
        errors="coerce",
        utc=True,
    )

    data["title"] = data["title"].fillna("").astype(str)
    data["text"] = data["text"].fillna("").astype(str)
    data["url"] = data["url"].fillna("").astype(str)

    data["title_key"] = data["title"].map(
        normalize_title
    )

    data["url_key"] = (
        data["url"]
        .str.split("?")
        .str[0]
    )

    kept_rows = []
    removed_rows = []
    seen_keys = set()

    for index, row in data.iterrows():
        reason = ""

        if not row["title"].strip():
            reason = "empty title"

        elif not row["text"].strip():
            reason = "empty text"

        elif pd.isna(row["published_at_parsed"]):
            reason = "invalid publication date"

        elif row["published_at_parsed"] < EVENT_START_DATE:
            reason = "published before Claude for Teachers launch"

        elif not is_relevant(
            row["title"] + " " + row["text"]
        ):
            reason = "not clearly related to Claude for Teachers and education"

        else:
            duplicate_key = (
                row["url_key"]
                if row["url_key"].strip()
                else row["title_key"]
            )

            if duplicate_key in seen_keys:
                reason = "duplicate URL or normalized title"
            else:
                seen_keys.add(duplicate_key)

        if reason:
            removed_row = row.to_dict()
            removed_row["removal_reason"] = reason
            removed_rows.append(removed_row)
        else:
            kept_rows.append(row.to_dict())

    kept_data = pd.DataFrame(kept_rows)
    removed_data = pd.DataFrame(removed_rows)

    columns_to_remove = [
        "published_at_parsed",
        "title_key",
        "url_key",
    ]

    for column in columns_to_remove:
        if column in kept_data.columns:
            kept_data = kept_data.drop(
                columns=[column]
            )

        if column in removed_data.columns:
            removed_data = removed_data.drop(
                columns=[column]
            )

    CLEAN_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    kept_data.to_csv(
        CLEAN_FILE,
        index=False,
        encoding="utf-8",
    )

    removed_data.to_csv(
        LOG_FILE,
        index=False,
        encoding="utf-8",
    )

    print("")
    print(f"Original records: {len(data)}")
    print(f"Clean records: {len(kept_data)}")
    print(f"Removed records: {len(removed_data)}")
    print("")
    print(f"Clean dataset saved to: {CLEAN_FILE}")
    print(f"Cleaning log saved to: {LOG_FILE}")
    print("")
    print("Removal reasons:")

    if len(removed_data) > 0:
        print(
            removed_data["removal_reason"]
            .value_counts()
            .to_string()
        )
    else:
        print("No records were removed.")


if __name__ == "__main__":
    main()
