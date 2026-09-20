import json
from pathlib import Path


NOTEBOOK_FILE = Path(
    "round3/round3_analysis.ipynb"
)


def markdown(text):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": text.splitlines(
            keepends=True
        ),
    }


def code(text):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": text.splitlines(
            keepends=True
        ),
    }


cells = [
    markdown(
        "# Round 3 Analysis\n\n"
        "## Public Reaction to Claude for Teachers\n\n"
        "This notebook analyses public reaction to "
        "Claude for Teachers, selected as the case study "
        "for the assigned topic: Public Reaction to a "
        "New Educational Technology.\n\n"
        "The sentiment and topic predictions were created "
        "using the NLP models developed in Round 2."
    ),

    markdown(
        "## Data collection method\n\n"
        "The data was collected from Google News RSS, "
        "Reddit RSS, and the GNews API. The cleaned "
        "dataset contains records published from "
        "14 July 2026 onward."
    ),

    code(
        "import pandas as pd\n"
        "import matplotlib.pyplot as plt\n\n"
        "classified = pd.read_csv(\n"
        "    'outputs/classified_public_reaction.csv'\n"
        ")\n\n"
        "daily = pd.read_csv(\n"
        "    'outputs/daily_analysis.csv',\n"
        "    parse_dates=['date']\n"
        ")\n\n"
        "topics = pd.read_csv(\n"
        "    'outputs/topic_summary.csv'\n"
        ")\n\n"
        "print('Classified records:', len(classified))\n"
        "display(classified.head())"
    ),

    code(
        "print('Sentiment predictions:')\n"
        "display(\n"
        "    classified[\n"
        "        'sentiment_prediction'\n"
        "    ].value_counts().to_frame('records')\n"
        ")\n\n"
        "print('Topic predictions:')\n"
        "display(topics)"
    ),

    code(
        "plt.figure(figsize=(10, 5))\n"
        "plt.plot(\n"
        "    daily['date'],\n"
        "    daily['mean_sentiment'],\n"
        "    marker='o'\n"
        ")\n"
        "plt.axhline(0, color='black')\n"
        "plt.title('Daily predicted sentiment')\n"
        "plt.ylabel(\n"
        "    'Mean sentiment: -1 negative, '\n"
        "    '0 neutral, +1 positive'\n"
        ")\n"
        "plt.xticks(rotation=35)\n"
        "plt.tight_layout()\n"
        "plt.show()"
    ),

    code(
        "plt.figure(figsize=(10, 5))\n"
        "plt.bar(\n"
        "    daily['date'].dt.strftime('%Y-%m-%d'),\n"
        "    daily['attention_proxy']\n"
        ")\n"
        "plt.title('Daily attention proxy')\n"
        "plt.ylabel('Collected public mentions')\n"
        "plt.xticks(rotation=60, ha='right')\n"
        "plt.tight_layout()\n"
        "plt.show()"
    ),

    code(
        "print('Largest sentiment changes:')\n"
        "display(\n"
        "    pd.read_csv(\n"
        "        'outputs/sentiment_shifts.csv'\n"
        "    ).head(5)\n"
        ")\n\n"
        "print('Largest attention days:')\n"
        "display(\n"
        "    pd.read_csv(\n"
        "        'outputs/engagement_spikes.csv'\n"
        "    ).head(5)\n"
        ")"
    ),

    markdown(
        "## Interpretation note\n\n"
        "The largest attention spike occurred immediately "
        "after the 14 July 2026 launch. The highest daily "
        "count was recorded on 15 July. Sentiment changes "
        "on dates with only one record are interpreted "
        "carefully because one article can create a large "
        "apparent change."
    ),
]


notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python"
        },
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}


NOTEBOOK_FILE.parent.mkdir(
    parents=True,
    exist_ok=True,
)

NOTEBOOK_FILE.write_text(
    json.dumps(notebook, indent=2),
    encoding="utf-8",
)

print(
    f"Notebook created: {NOTEBOOK_FILE}"
)
