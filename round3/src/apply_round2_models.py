import html
import pickle
import re
from pathlib import Path

import pandas as pd


INPUT_FILE = Path(
    "round3/data/self_collected_round3_clean.csv"
)

OUTPUT_FILE = Path(
    "round3/outputs/classified_public_reaction.csv"
)

SENTIMENT_MODEL_FILE = Path(
    "round3/models/sentiment_model.pkl"
)

TOPIC_MODEL_FILE = Path(
    "round3/models/topic_model.pkl"
)


def clean_text(value):
    text = html.unescape(str(value))

    text = re.sub(
        r"https?://\S+|www\.\S+",
        " URLTOKEN ",
        text,
     )

    text = re.sub(
        r"@\w+",
        " USERTOKEN ",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip().lower()


def main():
    print("Reading cleaned dataset...")

    data = pd.read_csv(INPUT_FILE)

    data["text"] = data["text"].fillna("").astype(str)
    data["model_text"] = data["text"].map(clean_text)

    print(f"Records loaded: {len(data)}")

    print("Loading Round 2 sentiment model...")

    with SENTIMENT_MODEL_FILE.open("rb") as file:
        sentiment_model = pickle.load(file)

    print("Loading Round 2 topic model...")

    with TOPIC_MODEL_FILE.open("rb") as file:
        topic_model = pickle.load(file)

    print("Predicting sentiment...")

    data["sentiment_prediction"] = (
        sentiment_model.predict(data["model_text"])
    )

    print("Predicting topic...")

    data["topic_prediction"] = (
        topic_model.predict(data["model_text"])
    )

    data = data.drop(
        columns=["model_text"]
    )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    data.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8",
    )

    print("")
    print("Model application completed.")
    print(f"Saved file: {OUTPUT_FILE}")
    print("")
    print("Sentiment predictions:")
    print(
        data["sentiment_prediction"]
        .value_counts()
        .to_string()
    )
    print("")
    print("Topic predictions:")
    print(
        data["topic_prediction"]
        .value_counts()
        .to_string()
    )


if __name__ == "__main__":
    main()
