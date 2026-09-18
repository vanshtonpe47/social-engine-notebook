from pathlib import Path
import html
import json
import pickle
import re

import matplotlib.pyplot as plt
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    PROJECT_ROOT
    / "round2"
    / "data"
    / "raw"
    / "Labeled_Social_NLP_Training_Data.csv"
)

MODEL_DIR = PROJECT_ROOT / "round2" / "models"
FIGURE_DIR = PROJECT_ROOT / "round2" / "figures"
REPORT_DIR = PROJECT_ROOT / "round2" / "reports"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. TEXT PREPROCESSING
# ============================================================

def clean_text(value):
    """
    Apply conservative text normalization.

    The original wording is retained while:
    - HTML entities are decoded.
    - Escaped Unicode sequences are decoded where possible.
    - URLs are replaced with a common token.
    - Mentions are replaced with a common token.
    - Whitespace is normalized.
    - Text is converted to lowercase.
    """

    text = str(value)

    # Decode HTML entities such as &amp;.
    text = html.unescape(text)

    # Decode escaped sequences such as literal \\u2019.
    if "\\u" in text or "\\x" in text:
        try:
            text = text.encode("utf-8").decode(
                "unicode_escape"
            )
        except UnicodeDecodeError:
            pass

    # Replace URLs with a common token.
    text = re.sub(
        r"https?://\S+|www\.\S+",
        " URLTOKEN ",
        text,
     )

    # Replace user mentions with a common token.
    text = re.sub(
        r"@\w+",
        " USERTOKEN ",
        text,
    )

    # Normalize whitespace and lowercase.
    text = re.sub(r"\s+", " ", text).strip().lower()

    return text


# ============================================================
# 3. LOAD DATA
# ============================================================

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_FILE}"
    )

data = pd.read_csv(
    DATA_FILE,
    encoding="utf-8-sig",
)

required_columns = {
    "text_id",
    "post_text",
    "sentiment_label",
    "topic_category",
}

missing_columns = required_columns - set(data.columns)

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

data["clean_text"] = data["post_text"].apply(clean_text)

print("DATA LOADED")
print("-----------")
print(f"Total records: {len(data)}")
print(f"Unique text values: {data['post_text'].nunique()}")


# ============================================================
# 4. GROUP-AWARE TRAIN / VALIDATION / TEST SPLIT
# ============================================================

# All identical original texts are assigned to one split only.
# This prevents duplicate text leakage between train and test.

groups = data["post_text"].astype(str)

# First split: 80% temporary training data and 20% final test data.
outer_splitter = GroupShuffleSplit(
    n_splits=1,
    test_size=0.20,
    random_state=42,
)

temporary_indices, test_indices = next(
    outer_splitter.split(
        data,
        groups=groups,
    )
)

temporary_data = data.iloc[temporary_indices].copy()
test_data = data.iloc[test_indices].copy()

temporary_groups = temporary_data["post_text"].astype(str)

# Second split: 75% training and 25% validation inside the
# temporary data. This gives approximately 60/20/20 overall.
inner_splitter = GroupShuffleSplit(
    n_splits=1,
    test_size=0.25,
    random_state=42,
)

train_indices, validation_indices = next(
    inner_splitter.split(
        temporary_data,
        groups=temporary_groups,
    )
)

train_data = temporary_data.iloc[train_indices].copy()
validation_data = temporary_data.iloc[validation_indices].copy()

train_texts = set(train_data["post_text"])
validation_texts = set(validation_data["post_text"])
test_texts = set(test_data["post_text"])

print()
print("DATA SPLIT")
print("----------")
print(f"Training records: {len(train_data)}")
print(f"Validation records: {len(validation_data)}")
print(f"Testing records: {len(test_data)}")
print(
    "Train/validation text overlap:",
    len(train_texts & validation_texts),
)
print(
    "Train/test text overlap:",
    len(train_texts & test_texts),
)
print(
    "Validation/test text overlap:",
    len(validation_texts & test_texts),
)


# ============================================================
# 5. MODEL FACTORIES
# ============================================================

def create_logistic_model():
    return Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=False,
                    ngram_range=(1, 2),
                    min_df=2,
                    sublinear_tf=True,
                    max_features=100000,
                ),
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=2000,
                    class_weight="balanced",
                ),
            ),
        ]
    )


def create_svm_model():
    return Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=False,
                    ngram_range=(1, 2),
                    min_df=2,
                    sublinear_tf=True,
                    max_features=100000,
                ),
            ),
            (
                "classifier",
                LinearSVC(
                    class_weight="balanced",
                ),
            ),
        ]
    )


MODEL_FACTORIES = {
    "logistic_regression": create_logistic_model,
    "linear_svm": create_svm_model,
}


# ============================================================
# 6. MODEL EVALUATION FUNCTIONS
# ============================================================

def calculate_scores(actual, predicted):
    return {
        "accuracy": accuracy_score(
            actual,
            predicted,
        ),
        "macro_precision": precision_score(
            actual,
            predicted,
            average="macro",
            zero_division=0,
        ),
        "macro_recall": recall_score(
            actual,
            predicted,
            average="macro",
            zero_division=0,
        ),
        "macro_f1": f1_score(
            actual,
            predicted,
            average="macro",
            zero_division=0,
        ),
        "weighted_f1": f1_score(
            actual,
            predicted,
            average="weighted",
            zero_division=0,
        ),
    }


def train_and_select_model(
    target_column,
    output_prefix,
):
    print()
    print("=" * 70)
    print(f"TARGET: {target_column}")
    print("=" * 70)

    x_train = train_data["clean_text"]
    y_train = train_data[target_column]

    x_validation = validation_data["clean_text"]
    y_validation = validation_data[target_column]

    x_test = test_data["clean_text"]
    y_test = test_data[target_column]

    validation_results = {}

    # --------------------------------------------------------
    # Select the model using validation data only.
    # --------------------------------------------------------

    for model_name, model_factory in MODEL_FACTORIES.items():

        print()
        print(
            f"Training validation candidate: "
            f"{model_name}"
        )

        model = model_factory()
        model.fit(x_train, y_train)

        validation_predictions = model.predict(
            x_validation
        )

        scores = calculate_scores(
            y_validation,
            validation_predictions,
        )

        validation_results[model_name] = scores

        print(
            f"{model_name}: "
            f"accuracy={scores['accuracy']:.4f}, "
            f"macro_f1={scores['macro_f1']:.4f}, "
            f"weighted_f1={scores['weighted_f1']:.4f}"
        )

    selected_model_name = max(
        validation_results,
        key=lambda name: validation_results[name]["macro_f1"],
    )

    print()
    print(
        "Selected by validation macro F1:",
        selected_model_name,
    )

    # --------------------------------------------------------
    # Retrain the selected model on training + validation data.
    # --------------------------------------------------------

    final_training_data = pd.concat(
        [train_data, validation_data],
        ignore_index=True,
    )

    final_model = MODEL_FACTORIES[
        selected_model_name
    ]()

    final_model.fit(
        final_training_data["clean_text"],
        final_training_data[target_column],
    )

    # --------------------------------------------------------
    # Evaluate once on untouched test data.
    # --------------------------------------------------------

    test_predictions = final_model.predict(x_test)

    final_scores = calculate_scores(
        y_test,
        test_predictions,
    )

    labels = sorted(y_test.unique())

    detailed_report = classification_report(
        y_test,
        test_predictions,
        labels=labels,
        output_dict=True,
        zero_division=0,
    )

    confusion = confusion_matrix(
        y_test,
        test_predictions,
        labels=labels,
    )

    print()
    print("FINAL TEST RESULTS")
    print("------------------")
    print(
        f"Accuracy: {final_scores['accuracy']:.4f}"
    )
    print(
        f"Macro precision: "
        f"{final_scores['macro_precision']:.4f}"
    )
    print(
        f"Macro recall: "
        f"{final_scores['macro_recall']:.4f}"
    )
    print(
        f"Macro F1: "
        f"{final_scores['macro_f1']:.4f}"
    )
    print(
        f"Weighted F1: "
        f"{final_scores['weighted_f1']:.4f}"
    )

    print()
    print("CLASSIFICATION REPORT")
    print("---------------------")
    print(
        classification_report(
            y_test,
            test_predictions,
            labels=labels,
            zero_division=0,
        )
    )

    # --------------------------------------------------------
    # Save final model as .pkl.
    # --------------------------------------------------------

    model_file = (
        MODEL_DIR / f"{output_prefix}_model.pkl"
    )

    with open(model_file, "wb") as file:
        pickle.dump(final_model, file)

    # --------------------------------------------------------
    # Save confusion matrix figure.
    # --------------------------------------------------------

    plt.figure(figsize=(8, 6))
    plt.imshow(confusion, cmap="Blues")
    plt.title(
        f"{output_prefix.title()} Confusion Matrix\n"
        f"Model: {selected_model_name}"
    )
    plt.colorbar()

    plt.xticks(
        range(len(labels)),
        labels,
        rotation=45,
        ha="right",
    )
    plt.yticks(
        range(len(labels)),
        labels,
    )

    plt.xlabel("Predicted label")
    plt.ylabel("True label")

    for row in range(len(labels)):
        for column in range(len(labels)):
            plt.text(
                column,
                row,
                confusion[row, column],
                ha="center",
                va="center",
            )

    plt.tight_layout()

    confusion_file = (
        FIGURE_DIR
        / f"{output_prefix}_confusion_matrix.png"
    )

    plt.savefig(
        confusion_file,
        dpi=180,
        bbox_inches="tight",
    )

    plt.close()

    # --------------------------------------------------------
    # Save misclassified test examples.
    # --------------------------------------------------------

    error_mask = (
        y_test.to_numpy() != test_predictions
    )

    error_data = test_data.loc[
        error_mask,
        [
            "text_id",
            "post_text",
            target_column,
        ],
    ].copy()

    error_data["predicted_label"] = (
        test_predictions[error_mask]
    )

    error_file = (
        REPORT_DIR
        / f"{output_prefix}_errors.csv"
    )

    error_data.to_csv(
        error_file,
        index=False,
    )

    return {
        "target": target_column,
        "selected_model": selected_model_name,
        "training_records": len(train_data),
        "validation_records": len(validation_data),
        "testing_records": len(test_data),
        "train_validation_text_overlap": len(
            train_texts & validation_texts
        ),
        "train_test_text_overlap": len(
            train_texts & test_texts
        ),
        "validation_model_comparison": validation_results,
        "final_test_scores": final_scores,
        "classification_report": detailed_report,
        "confusion_matrix_labels": labels,
        "confusion_matrix": confusion.tolist(),
        "model_file": str(model_file),
        "confusion_matrix_file": str(
            confusion_file
        ),
        "error_file": str(error_file),
    }


# ============================================================
# 7. TRAIN SENTIMENT AND TOPIC MODELS
# ============================================================

results = {
    "sentiment": train_and_select_model(
        target_column="sentiment_label",
        output_prefix="sentiment",
    ),
    "topic": train_and_select_model(
        target_column="topic_category",
        output_prefix="topic",
    ),
}


# ============================================================
# 8. SAVE METRICS JSON
# ============================================================

metrics_file = REPORT_DIR / "metrics.json"

with open(metrics_file, "w", encoding="utf-8") as file:
    json.dump(
        results,
        file,
        indent=2,
    )


print()
print("FINAL MODEL TRAINING COMPLETED")
print("------------------------------")
print(f"Metrics file: {metrics_file}")
print(f"Model directory: {MODEL_DIR}")
print(f"Figure directory: {FIGURE_DIR}")
print(f"Report directory: {REPORT_DIR}")
