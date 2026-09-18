from pathlib import Path
import json

import pandas as pd


# ============================================================
# 1. Paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ROUND2_DIR = PROJECT_ROOT / "round2"
REPORT_DIR = ROUND2_DIR / "reports"
FIGURE_DIR = ROUND2_DIR / "figures"

METRICS_FILE = REPORT_DIR / "metrics.json"
SENTIMENT_ERRORS_FILE = REPORT_DIR / "sentiment_errors.csv"
TOPIC_ERRORS_FILE = REPORT_DIR / "topic_errors.csv"

EVALUATION_FILE = REPORT_DIR / "evaluation_metrics.md"
TECHNICAL_FILE = REPORT_DIR / "round2_technical_report.md"


# ============================================================
# 2. Check required files
# ============================================================

required_files = [
    METRICS_FILE,
    SENTIMENT_ERRORS_FILE,
    TOPIC_ERRORS_FILE,
    FIGURE_DIR / "sentiment_confusion_matrix.png",
    FIGURE_DIR / "topic_confusion_matrix.png",
]

for file_path in required_files:
    if not file_path.exists():
        raise FileNotFoundError(
            f"Required file not found: {file_path}"
        )


# ============================================================
# 3. Load generated results
# ============================================================

with open(METRICS_FILE, "r", encoding="utf-8") as file:
    metrics = json.load(file)

sentiment_errors = pd.read_csv(SENTIMENT_ERRORS_FILE)
topic_errors = pd.read_csv(TOPIC_ERRORS_FILE)

sentiment = metrics["sentiment"]
topic = metrics["topic"]


# ============================================================
# 4. Helper functions
# ============================================================

def score(value):
    return f"{float(value):.4f}"


def metric_lines(scores):
    return [
        "| Metric | Score |",
        "|---|---:|",
        f"| Accuracy | {score(scores['accuracy'])} |",
        f"| Macro precision | {score(scores['macro_precision'])} |",
        f"| Macro recall | {score(scores['macro_recall'])} |",
        f"| Macro F1-score | {score(scores['macro_f1'])} |",
        f"| Weighted F1-score | {score(scores['weighted_f1'])} |",
    ]


def validation_lines(comparison):
    lines = [
        "| Candidate model | Accuracy | Macro F1 | Weighted F1 |",
        "|---|---:|---:|---:|",
    ]

    for model_name, values in comparison.items():
        lines.append(
            f"| {model_name} | "
            f"{score(values['accuracy'])} | "
            f"{score(values['macro_f1'])} | "
            f"{score(values['weighted_f1'])} |"
        )

    return lines


def classification_lines(report, labels):
    lines = [
        "| Class | Precision | Recall | F1-score | Support |",
        "|---|---:|---:|---:|---:|",
    ]

    for label in labels:
        values = report.get(label)

        if values is not None:
            lines.append(
                f"| {label} | "
                f"{score(values['precision'])} | "
                f"{score(values['recall'])} | "
                f"{score(values['f1-score'])} | "
                f"{int(values['support'])} |"
            )

    return lines


def error_lines(error_data, target_column, count=5):
    lines = [
        "| Text ID | Actual label | Predicted label | Text |",
        "|---|---|---|---|",
    ]

    for _, row in error_data.head(count).iterrows():
        text = str(row["post_text"])
        text = text.replace("|", "\\|")
        text = text.replace("\n", " ")

        lines.append(
            f"| {row['text_id']} | "
            f"{row[target_column]} | "
            f"{row['predicted_label']} | "
            f"{text} |"
        )

    if len(lines) == 2:
        lines.append("| No errors recorded | - | - | - |")

    return lines


def add(lines, *new_lines):
    lines.extend(new_lines)


# ============================================================
# 5. Build Evaluation Metrics Report
# ============================================================

evaluation = []

add(
    evaluation,
    "# Round 2 Evaluation Metrics Report",
    "",
    "## Dataset and evaluation design",
    "",
    "The dataset contains 9,000 labelled text records. "
    "Two supervised NLP tasks were evaluated:",
    "",
    "1. Sentiment classification.",
    "2. Topic-category classification.",
    "",
    "A group-aware split prevented identical text values from "
    "appearing in more than one data split.",
    "",
    "| Split | Records |",
    "|---|---:|",
    f"| Training | {sentiment['training_records']} |",
    f"| Validation | {sentiment['validation_records']} |",
    f"| Testing | {sentiment['testing_records']} |",
    "",
    "Final metrics were calculated only on the untouched test set.",
    "",
    "---",
    "",
    "# 1. Sentiment classification",
    "",
    "## Target",
    "",
    "```text",
    "post_text -> sentiment_label",
    "```",
    "",
    "The classes are Negative, Neutral, and Positive.",
    "",
    "## Model selection",
    "",
)

evaluation.extend(
    validation_lines(
        sentiment["validation_model_comparison"]
    )
)

add(
    evaluation,
    "",
    f"Selected model: **{sentiment['selected_model']}**",
    "",
    "## Final test metrics",
    "",
)

evaluation.extend(metric_lines(sentiment["final_test_scores"]))

add(
    evaluation,
    "",
    "## Per-class metrics",
    "",
)

evaluation.extend(
    classification_lines(
        sentiment["classification_report"],
        ["Negative", "Neutral", "Positive"],
    )
)

add(
    evaluation,
    "",
    "## Confusion matrix",
    "",
    "![Sentiment confusion matrix]"
    "(../figures/sentiment_confusion_matrix.png)",
    "",
    "---",
    "",
    "# 2. Topic classification",
    "",
    "## Target",
    "",
    "```text",
    "post_text -> topic_category",
    "```",
    "",
    "The topic classes are Account Security, Community Discussion, "
    "Feature Feedback, and Technical Issues.",
    "",
    "## Model selection",
    "",
)

evaluation.extend(
    validation_lines(
        topic["validation_model_comparison"]
    )
)

add(
    evaluation,
    "",
    f"Selected model: **{topic['selected_model']}**",
    "",
    "## Final test metrics",
    "",
)

evaluation.extend(metric_lines(topic["final_test_scores"]))

add(
    evaluation,
    "",
    "## Per-class metrics",
    "",
)

evaluation.extend(
    classification_lines(
        topic["classification_report"],
        [
            "Account_Security",
            "Community_Discussion",
            "Feature_Feedback",
            "Technical_Issues",
        ],
    )
)

add(
    evaluation,
    "",
    "## Confusion matrix",
    "",
    "![Topic confusion matrix]"
    "(../figures/topic_confusion_matrix.png)",
    "",
    "---",
    "",
    "# 3. Interpretation",
    "",
    f"The sentiment classifier achieved a macro F1-score of "
    f"**{score(sentiment['final_test_scores']['macro_f1'])}**.",
    "",
    f"The topic classifier achieved accuracy of "
    f"**{score(topic['final_test_scores']['accuracy'])}** "
    f"and macro F1-score of "
    f"**{score(topic['final_test_scores']['macro_f1'])}**.",
    "",
    "The topic accuracy is high partly because "
    "`Community_Discussion` is the dominant class. "
    "Macro F1 is therefore also reported.",
)

EVALUATION_FILE.write_text(
    "\n".join(evaluation),
    encoding="utf-8",
)


# ============================================================
# 6. Build Technical Report
# ============================================================

technical = []

add(
    technical,
    "# Data Vortex 2026 - Round 2 Technical Report",
    "",
    "## 1. Problem Definition",
    "",
    "The Social Engine requires a semantic layer capable of "
    "interpreting short human-language posts.",
    "",
    "This project builds two classifiers:",
    "",
    "```text",
    "post_text -> sentiment_label",
    "post_text -> topic_category",
    "```",
    "",
    "The sentiment model predicts Positive, Negative, or Neutral. "
    "The topic model predicts the category of the post.",
    "",
    "## 2. Dataset Overview",
    "",
    "The dataset contains 9,000 records and four source columns:",
    "",
    "```text",
    "text_id",
    "post_text",
    "sentiment_label",
    "topic_category",
    "```",
    "",
    "The inspection found no missing values, blank text values, "
    "duplicate complete rows, or duplicate text IDs.",
    "",
    "There are 7,900 unique text values and 987 repeated text values. "
    "Repeated texts have no conflicting labels.",
    "",
    "The sentiment labels are balanced with 3,000 records per class. "
    "The topic labels are strongly imbalanced.",
    "",
    "## 3. Preprocessing Pipeline",
    "",
    "The preprocessing pipeline:",
    "",
    "1. Decodes HTML entities.",
    "2. Decodes escaped Unicode sequences where possible.",
    "3. Replaces URLs with `URLTOKEN`.",
    "4. Replaces mentions with `USERTOKEN`.",
    "5. Normalizes whitespace.",
    "6. Converts text to lowercase.",
    "7. Creates TF-IDF unigram and bigram features.",
    "",
    "TF-IDF used minimum document frequency 2, sublinear term "
    "frequency, and a maximum of 100,000 features.",
    "",
    "## 4. Model Selection",
    "",
    "Two models were compared:",
    "",
    "- Logistic Regression.",
    "- Linear Support Vector Machine.",
    "",
    "Both used the same TF-IDF representation and balanced class weights.",
    "",
    "Models were selected using validation macro F1-score because "
    "macro F1 gives equal importance to every class.",
    "",
    f"Selected sentiment model: **{sentiment['selected_model']}**",
    "",
    f"Selected topic model: **{topic['selected_model']}**",
    "",
    "Final models were saved as:",
    "",
    "```text",
    "round2/models/sentiment_model.pkl",
    "round2/models/topic_model.pkl",
    "```",
    "",
    "## 5. Training Methodology",
    "",
    "| Split | Records |",
    "|---|---:|",
    f"| Training | {sentiment['training_records']} |",
    f"| Validation | {sentiment['validation_records']} |",
    f"| Testing | {sentiment['testing_records']} |",
    "",
    "A group-aware split used the original text as the group. "
    "Therefore identical texts could not cross dataset splits.",
    "",
    f"Train/validation overlap: "
    f"{sentiment.get('train_validation_text_overlap', 0)}",
    "",
    f"Train/test overlap: "
    f"{sentiment.get('train_test_text_overlap', 0)}",
    "",
    f"Validation/test overlap: "
    f"{sentiment.get('validation_test_text_overlap', 0)}",
    "",
    "The selected model was retrained on training plus validation "
    "records and evaluated once on the untouched test set.",
    "",
    "## 6. Evaluation Metrics",
    "",
    "### Sentiment classification",
    "",
)

technical.extend(metric_lines(sentiment["final_test_scores"]))

add(
    technical,
    "",
    "Per-class results:",
    "",
)

technical.extend(
    classification_lines(
        sentiment["classification_report"],
        ["Negative", "Neutral", "Positive"],
    )
)

add(
    technical,
    "",
    "### Topic classification",
    "",
)

technical.extend(metric_lines(topic["final_test_scores"]))

add(
    technical,
    "",
    "Per-class results:",
    "",
)

technical.extend(
    classification_lines(
        topic["classification_report"],
        [
            "Account_Security",
            "Community_Discussion",
            "Feature_Feedback",
            "Technical_Issues",
        ],
    )
)

add(
    technical,
    "",
    "## 7. Confusion Matrices",
    "",
    "### Sentiment",
    "",
    "![Sentiment confusion matrix]"
    "(../figures/sentiment_confusion_matrix.png)",
    "",
    "### Topic",
    "",
    "![Topic confusion matrix]"
    "(../figures/topic_confusion_matrix.png)",
    "",
    "The matrices show strong majority-class performance and "
    "more difficulty with neutral sentiment and minority topics.",
    "",
    "## 8. Error Analysis",
    "",
    "The error files were generated from final test predictions:",
    "",
    "```text",
    "round2/reports/sentiment_errors.csv",
    "round2/reports/topic_errors.csv",
    "```",
    "",
    "### Sentiment error examples",
    "",
)

technical.extend(
    error_lines(
        sentiment_errors,
        "sentiment_label",
    )
)

add(
    technical,
    "",
    "Typical causes include sarcasm, slang, mixed sentiment, "
    "short text, and neutral language containing emotional words.",
    "",
    "### Topic error examples",
    "",
)

technical.extend(
    error_lines(
        topic_errors,
        "topic_category",
    )
)

add(
    technical,
    "",
    "Topic errors are concentrated in minority categories because "
    "those categories contain fewer training examples and share "
    "vocabulary with other topics.",
    "",
    "## 9. Limitations",
    "",
    "The topic dataset is highly imbalanced. The model performs "
    "better on Community Discussion than on the smallest classes.",
    "",
    "TF-IDF cannot fully understand sarcasm, outside context, "
    "world knowledge, or subtle meaning.",
    "",
    "Future improvements could include character features, "
    "transformer embeddings, cross-validation, hyperparameter "
    "tuning, and additional minority-class data.",
    "",
    "## 10. Reproducibility",
    "",
    "Run these commands from the project root:",
    "",
    "```powershell",
    "python \"round2\\src\\inspect_dataset.py\"",
    "python \"round2\\src\\check_text_duplicates.py\"",
    "python \"round2\\src\\train_models.py\"",
    "python \"round2\\src\\generate_reports.py\"",
    "```",
    "",
    "## 11. Conclusion",
    "",
    "This project rebuilds the Social Engine semantic layer using "
    "text normalization, duplicate-aware splitting, TF-IDF features, "
    "model comparison, final test evaluation, confusion matrices, "
    "and error analysis.",
    "",
    "The resulting system performs sentiment recognition and "
    "topic classification with transparent evaluation and documented "
    "limitations.",
)

TECHNICAL_FILE.write_text(
    "\n".join(technical),
    encoding="utf-8",
)


print("REPORTS GENERATED")
print("-----------------")
print(f"Evaluation report: {EVALUATION_FILE}")
print(f"Technical report: {TECHNICAL_FILE}")
