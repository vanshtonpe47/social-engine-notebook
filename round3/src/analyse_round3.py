from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


INPUT_FILE = Path(
    "round3/outputs/classified_public_reaction.csv"
)

OUTPUT_DIR = Path("round3/outputs")
FIGURES_DIR = Path("round3/figures")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


SENTIMENT_SCORE = {
    "Negative": -1,
    "Neutral": 0,
    "Positive": 1,
}


def save_plot(path):
    plt.tight_layout()
    plt.savefig(
        path,
        dpi=180,
        bbox_inches="tight",
    )
    plt.close()


def main():
    data = pd.read_csv(INPUT_FILE)

    data["published_at"] = pd.to_datetime(
        data["published_at"],
        errors="coerce",
        utc=True,
    )

    data = data.dropna(
        subset=["published_at"]
    ).copy()

    data["date"] = data[
        "published_at"
    ].dt.strftime("%Y-%m-%d")

    data["sentiment_score"] = data[
        "sentiment_prediction"
    ].map(SENTIMENT_SCORE)

    data["attention_proxy"] = 1

    daily = data.groupby(
        "date",
        as_index=False,
    ).agg(
        records=("record_id", "count"),
        attention_proxy=(
            "attention_proxy",
            "sum",
        ),
        mean_sentiment=(
            "sentiment_score",
            "mean",
        ),
        positive_share=(
            "sentiment_prediction",
            lambda x: (x == "Positive").mean(),
        ),
        negative_share=(
            "sentiment_prediction",
            lambda x: (x == "Negative").mean(),
        ),
        neutral_share=(
            "sentiment_prediction",
            lambda x: (x == "Neutral").mean(),
        ),
    )

    daily["date"] = pd.to_datetime(
        daily["date"]
    )

    daily = daily.sort_values(
        "date"
    )

    daily["sentiment_change"] = (
        daily["mean_sentiment"].diff()
    )

    spike_cutoff = daily[
        "attention_proxy"
    ].quantile(0.90)

    daily["attention_spike"] = (
        daily["attention_proxy"]
        >= spike_cutoff
    )

    daily.to_csv(
        OUTPUT_DIR / "daily_analysis.csv",
        index=False,
    )

    shifts = daily.dropna(
        subset=["sentiment_change"]
    ).copy()

    shifts["absolute_change"] = (
        shifts["sentiment_change"].abs()
    )

    shifts = shifts.sort_values(
        "absolute_change",
        ascending=False,
    ).head(10)

    shifts.to_csv(
        OUTPUT_DIR / "sentiment_shifts.csv",
        index=False,
    )

    spikes = daily.sort_values(
        [
            "attention_proxy",
            "records",
        ],
        ascending=False,
    ).head(10)

    spikes.to_csv(
        OUTPUT_DIR / "engagement_spikes.csv",
        index=False,
    )

    topics = data.groupby(
        "topic_prediction",
        as_index=False,
    ).agg(
        records=("record_id", "count"),
        mean_sentiment=(
            "sentiment_score",
            "mean",
        ),
    )

    topics["share"] = (
        topics["records"] / len(data)
    )

    topics = topics.sort_values(
        "records",
        ascending=False,
    )

    topics.to_csv(
        OUTPUT_DIR / "topic_summary.csv",
        index=False,
    )

    sources = data.groupby(
        "source_type",
        as_index=False,
    ).agg(
        records=("record_id", "count")
    )

    sources.to_csv(
        OUTPUT_DIR / "source_summary.csv",
        index=False,
    )

    plt.figure(figsize=(10, 5))

    plt.plot(
        daily["date"],
        daily["mean_sentiment"],
        marker="o",
        color="#345995",
    )

    plt.axhline(
        0,
        color="black",
        linewidth=0.8,
    )

    plt.title(
        "Daily predicted sentiment: Claude for Teachers"
    )

    plt.xlabel("Publication date")

    plt.ylabel(
        "Mean sentiment (-1 negative, 0 neutral, +1 positive)"
    )

    plt.xticks(rotation=35)

    save_plot(
        FIGURES_DIR / "sentiment_timeline.png"
    )

    plt.figure(figsize=(10, 5))

    plt.bar(
        daily["date"].dt.strftime(
            "%Y-%m-%d"
        ),
        daily["attention_proxy"],
        color="#e07a5f",
    )

    plt.title(
        "Daily attention proxy: collected public mentions"
    )

    plt.xlabel("Publication date")

    plt.ylabel(
        "Number of collected mentions"
    )

    plt.xticks(
        rotation=60,
        ha="right",
    )

    save_plot(
        FIGURES_DIR / "engagement_spike_timeline.png"
    )

    plt.figure(figsize=(8, 5))

    plt.bar(
        topics["topic_prediction"],
        topics["records"],
        color="#6a994e",
    )

    plt.title(
        "Round 2 topic predictions"
    )

    plt.xlabel("Predicted topic")

    plt.ylabel(
        "Number of records"
    )

    plt.xticks(
        rotation=25,
        ha="right",
    )

    save_plot(
        FIGURES_DIR / "topic_distribution.png"
    )

    print("Analysis completed.")
    print(f"Records analysed: {len(data)}")

    print(
        "Daily file:",
        OUTPUT_DIR / "daily_analysis.csv",
    )

    print(
        "Sentiment-shift file:",
        OUTPUT_DIR / "sentiment_shifts.csv",
    )

    print(
        "Attention-spike file:",
        OUTPUT_DIR / "engagement_spikes.csv",
    )

    print(
        "Topic file:",
        OUTPUT_DIR / "topic_summary.csv",
    )

    print("")
    print("Topic summary:")
    print(topics.to_string(index=False))

    print("")
    print("Largest sentiment changes:")
    print(
        shifts[
            [
                "date",
                "records",
                "mean_sentiment",
                "sentiment_change",
            ]
        ]
        .head(5)
        .to_string(index=False)
    )

    print("")
    print("Largest attention days:")
    print(
        spikes[
            [
                "date",
                "records",
                "attention_proxy",
            ]
        ]
        .head(5)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
