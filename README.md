# Social Engine Competition Project

This repository contains the work completed for the **Data Vortex A’26 Social Engine competition**. The project restores the Social Engine in three stages:

1. **Round 1 — Data Recovery, Cleaning, Validation, and Exploratory Analysis**
2. **Round 2 — Natural Language Processing and Model Training**
3. **Round 3 — Live Public-Web Data Collection and Time-Based Analysis**

The repository is designed to preserve the data, source code, trained models, visualisations, reports, and reproducible outputs for each round.

> **Important:** API credentials are not stored in this repository. The GNews API key is read from the `GNEWS_API_KEY` environment variable when collection is run.

---

## Repository structure

```text
social-engine/
│
├── README.md
│
├── phase1/
│   ├── raw/
│   ├── cleaned/
│   ├── figures/
│   ├── reports/
│   └── Python analysis scripts
│
├── phase2/
│   ├── sql/
│   ├── screenshots/
│   ├── results/
│   └── reports/
│
├── round2/
│   ├── data/
│   ├── figures/
│   ├── models/
│   │   ├── sentiment_model.pkl
│   │   └── topic_model.pkl
│   ├── reports/
│   └── src/
│
└── round3/
    ├── data/
    ├── figures/
    ├── models/
    ├── outputs/
    ├── reports/
    └── src/
```

---

# Round 1 — Data Recovery, Cleaning, and Exploratory Analysis

## Objective

Round 1 focused on recovering the supplied Social Engine datasets, cleaning and validating the records, and performing exploratory data analysis.

## Workflow

```text
Raw datasets
    ↓
Data inspection
    ↓
Cleaning and transformation
    ↓
Validation
    ↓
Exploratory analysis
    ↓
Cleaned datasets, figures, and report
```

## Main cleaning actions

The Round 1 workflow removed exact duplicate post rows, standardised mixed timestamp formats, decoded HTML entities, converted engagement columns to numeric values, identified invalid negative engagement values, preserved missing values rather than fabricating replacements, retained original timestamps for traceability, and checked that posts referred to valid users.

The cleaned datasets and Round 1 report are stored under `phase1/`.

---

# Phase 2 — Selected SQL Challenges

The SQL phase selected one question from each difficulty level.

| Difficulty | Selected question |
|---|---|
| Easy | E3 — Average Engagement by Platform |
| Medium | M2 — Do High Follower Users Get More Engagement? |
| Hard | H3 — Platform Performance Compared With Its Own Average |

The SQL files, screenshots, result files, logic explanation, and insight report are stored under `phase2/`.

The generated SQLite database is intentionally not committed because it can be recreated from the cleaned source files.

---

# Round 2 — NLP Semantic Understanding

## Objective

Round 2 rebuilt the Social Engine’s semantic understanding layer using supervised Natural Language Processing. Two classification tasks were developed:

- **Sentiment classification:** Negative, Neutral, and Positive.
- **Topic classification:** Community_Discussion, Feature_Feedback, Technical_Issues, and Account_Security.

## Method

The Round 2 pipeline used text preprocessing, TF-IDF feature extraction, and Logistic Regression classification. The data was split for training and evaluation, and performance was assessed using accuracy, precision, recall, macro F1-score, weighted F1-score, classification reports, and confusion matrices.

The trained models are stored in:

```text
round2/models/sentiment_model.pkl
round2/models/topic_model.pkl
```

These exact models were reused in Round 3. They were not retrained on the Round 3 public-web data.

## Round 2 reports

```text
round2/reports/evaluation_metrics.pdf
round2/reports/round2_technical_report.pdf
```

---

# Round 3 — Public Reaction to Claude for Teachers

## Research theme

The assigned theme was:

> **Public Reaction to a New Educational Technology**

The selected case study was **Claude for Teachers**, Anthropic’s education-focused Claude launch. The analysis examined how public attention, predicted sentiment, and predicted discussion topics changed after the 14 July 2026 launch.

## Data collection sources

The raw collection used three public-web collection channels:

1. **Google News RSS**, searched using Claude for Teachers and related education-AI queries.
2. **Reddit RSS**, searched in `r/edtech`, `r/education`, and `r/ClaudeAI`.
3. **GNews API**, accessed through the `GNEWS_API_KEY` environment variable.

The raw collection contained **146 records**:

| Raw source type | Records |
|---|---:|
| Google News RSS | 142 |
| Reddit RSS | 3 |
| GNews API | 1 |
| **Total** | **146** |

After relevance and time-window filtering, the final analysis dataset contained **50 records**:

| Final source type | Records |
|---|---:|
| Google News RSS | 49 |
| Reddit RSS | 1 |
| **Total** | **50** |

Google News RSS is an aggregator. The underlying publisher or outlet for each record is preserved in the dataset’s `source_name` column. The final source distribution therefore represents two collection channels and multiple publisher outlets.

The GNews API record was retained in the raw archive but did not remain in the final cleaned dataset after filtering. This is expected because the final dataset contains only records that passed the relevance and time-window rules.

## Cleaning and filtering

The cleaning process removed duplicate records, records published before the Claude for Teachers launch, and records that were not clearly related to Claude for Teachers and education. Critical or negative coverage was not removed because of its sentiment.

The final dataset is:

```text
round3/data/self_collected_round3_clean.csv
```

Supporting files are:

```text
round3/data/self_collected_round3_raw.csv
round3/data/cleaning_log.csv
```

## Reuse of Round 2 models

The Round 2 models were applied to every record in the final 50-record dataset:

```text
round2/models/sentiment_model.pkl
round2/models/topic_model.pkl
```

The Round 3 analysis produced the following predictions:

### Sentiment predictions

| Sentiment | Records |
|---|---:|
| Neutral | 39 |
| Negative | 9 |
| Positive | 2 |
| **Total** | **50** |

### Topic predictions

| Topic | Records |
|---|---:|
| Community_Discussion | 45 |
| Feature_Feedback | 4 |
| Technical_Issues | 1 |
| **Total** | **50** |

## Time-based findings

The analysis identified two sentiment transitions:

- Coverage moved from a mostly neutral launch period toward a more negative model prediction around 21 July 2026.
- An isolated positive-to-negative change occurred around 11–12 September 2026. Because only one record appeared on each of those dates, this is treated as a signal for follow-up rather than proof of a population-wide shift.

The largest attention spike occurred immediately after launch:

- 14 collected mentions on 14 July 2026.
- 19 collected mentions on 15 July 2026.

Because public RSS feeds do not consistently provide likes, comments, or shares, the analysis reports this as a **mention-volume attention proxy**, not as a direct measure of social-media engagement.

## Round 3 files

### Data

```text
round3/data/self_collected_round3_clean.csv
round3/data/self_collected_round3_raw.csv
round3/data/cleaning_log.csv
```

### Collection and analysis code

```text
round3/src/collect_round3_data.py
round3/src/collect_public_data.py
round3/src/merge_sources.py
round3/src/clean_dataset.py
round3/src/apply_round2_models.py
round3/src/analyse_round3.py
```

### Models

```text
round3/models/sentiment_model.pkl
round3/models/topic_model.pkl
```

### Outputs

```text
round3/outputs/classified_public_reaction.csv
round3/outputs/daily_analysis.csv
round3/outputs/sentiment_shifts.csv
round3/outputs/engagement_spikes.csv
round3/outputs/topic_summary.csv
round3/outputs/source_summary.csv
```

### Figures

```text
round3/figures/sentiment_timeline.png
round3/figures/engagement_spike_timeline.png
round3/figures/topic_distribution.png
```

### Reports

```text
round3/reports/round3_analysis_notebook.pdf
round3/reports/round3_analytical_report.pdf
```

The analytical report covers the required sections: data collection method, time window, sentiment analysis, activity analysis, topic and entity analysis, trigger explanations, limitations, and conclusion.

---

## Reproducibility

Run commands from the repository root. Round 2 model training can be reproduced using the scripts in `round2/src/`. Round 3 collection can be run with:

```powershell
python "round3\src\collect_round3_data.py"
```

To enable the optional GNews API collector, set the API key as an environment variable. Do not place the key directly in a Python file or commit it to GitHub:

```powershell
$env:GNEWS_API_KEY = "YOUR_KEY_HERE"
python "round3\src\collect_round3_data.py"
```

The key is used only during collection and is not written to the dataset.

---

## Limitations

The Round 3 dataset is a public-web sample rather than a census of public opinion. Google News RSS can return syndicated or broad-query results, so relevance filtering was necessary. Reddit RSS was rate-limited for two feeds, leaving one Reddit record in the final cleaned dataset. The attention metric is a collected-mention proxy because likes, comments, and shares were not consistently available. Finally, the Round 2 classifiers were trained on a different labelled dataset, so their Round 3 predictions should be interpreted as model-based analytical labels rather than verified ground truth.

---

## Technologies

| Purpose | Technology |
|---|---|
| Programming language | Python |
| Data processing | pandas |
| Machine learning | scikit-learn |
| Text features | TF-IDF |
| Classifier | Logistic Regression |
| Visualisation | Matplotlib |
| Database analysis | SQLite and SQL |
| Documentation | Markdown and PDF |
| Version control | Git and GitHub |

---

## Repository

GitHub repository:

```text
https://github.com/vanshtonpe47/social-engine-notebook
```

---

## Security

Never commit API keys, passwords, tokens, `.env` files, or private credentials. The Round 3 collection script reads the GNews credential from `GNEWS_API_KEY` and does not contain the actual key.
