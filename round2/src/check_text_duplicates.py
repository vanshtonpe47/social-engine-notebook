from pathlib import Path

import pandas as pd


# ------------------------------------------------------------
# 1. Locate and load the dataset
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    PROJECT_ROOT
    / "round2"
    / "data"
    / "raw"
    / "Labeled_Social_NLP_Training_Data.csv"
)

data = pd.read_csv(
    DATA_FILE,
    encoding="utf-8-sig"
)


# ------------------------------------------------------------
# 2. Count repeated text values
# ------------------------------------------------------------

text_counts = (
    data["post_text"]
    .value_counts()
)

repeated_texts = text_counts[
    text_counts > 1
]

print("TEXT DUPLICATE ANALYSIS")
print("-----------------------")
print(f"Total records: {len(data)}")
print(f"Unique text values: {data['post_text'].nunique()}")
print(f"Repeated text values: {len(repeated_texts)}")
print(
    f"Records belonging to repeated text values: "
    f"{data['post_text'].isin(repeated_texts.index).sum()}"
)


# ------------------------------------------------------------
# 3. Check whether repeated text has conflicting sentiment
# ------------------------------------------------------------

sentiment_consistency = (
    data.groupby("post_text")["sentiment_label"]
    .nunique()
)

conflicting_sentiment = sentiment_consistency[
    sentiment_consistency > 1
]

print()
print("SENTIMENT CONSISTENCY")
print("---------------------")
print(
    f"Repeated texts with conflicting sentiment labels: "
    f"{len(conflicting_sentiment)}"
)


# ------------------------------------------------------------
# 4. Check whether repeated text has conflicting topics
# ------------------------------------------------------------

topic_consistency = (
    data.groupby("post_text")["topic_category"]
    .nunique()
)

conflicting_topics = topic_consistency[
    topic_consistency > 1
]

print()
print("TOPIC CONSISTENCY")
print("-----------------")
print(
    f"Repeated texts with conflicting topic labels: "
    f"{len(conflicting_topics)}"
)


# ------------------------------------------------------------
# 5. Show examples of repeated text
# ------------------------------------------------------------

if len(repeated_texts) > 0:

    repeated_data = (
        data[data["post_text"].isin(repeated_texts.index)]
        .sort_values("post_text")
        .loc[
            :,
            [
                "text_id",
                "post_text",
                "sentiment_label",
                "topic_category",
            ],
        ]
        .head(10)
    )

    print()
    print("EXAMPLES OF REPEATED TEXT")
    print("-------------------------")
    print(repeated_data.to_string(index=False))


print()
print("TEXT DUPLICATE ANALYSIS COMPLETED")
