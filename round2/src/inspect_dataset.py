from pathlib import Path

import pandas as pd


# ------------------------------------------------------------
# 1. Define the dataset path
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    PROJECT_ROOT
    / "round2"
    / "data"
    / "raw"
    / "Labeled_Social_NLP_Training_Data.csv"
)


# ------------------------------------------------------------
# 2. Check that the dataset exists
# ------------------------------------------------------------

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found at: {DATA_FILE}"
    )


# ------------------------------------------------------------
# 3. Load the dataset
# ------------------------------------------------------------

data = pd.read_csv(
    DATA_FILE,
    encoding="utf-8-sig"
)


# ------------------------------------------------------------
# 4. Display basic dataset information
# ------------------------------------------------------------

print("DATASET OVERVIEW")
print("----------------")
print(f"File: {DATA_FILE}")
print(f"Rows: {data.shape[0]}")
print(f"Columns: {data.shape[1]}")

print()
print("COLUMN NAMES")
print("------------")
for column in data.columns:
    print(column)


# ------------------------------------------------------------
# 5. Display the first five records
# ------------------------------------------------------------

print()
print("FIRST FIVE RECORDS")
print("------------------")
print(data.head().to_string(index=False))


# ------------------------------------------------------------
# 6. Display data types
# ------------------------------------------------------------

print()
print("DATA TYPES")
print("----------")
print(data.dtypes)


# ------------------------------------------------------------
# 7. Check missing values
# ------------------------------------------------------------

print()
print("MISSING VALUES")
print("--------------")
print(data.isna().sum())


# ------------------------------------------------------------
# 8. Check blank text values
# ------------------------------------------------------------

blank_text_count = (
    data["post_text"]
    .fillna("")
    .astype(str)
    .str.strip()
    .eq("")
    .sum()
)

print()
print("BLANK TEXT VALUES")
print("-----------------")
print(f"Blank post_text rows: {blank_text_count}")


# ------------------------------------------------------------
# 9. Check duplicate records
# ------------------------------------------------------------

duplicate_rows = data.duplicated().sum()
duplicate_text_ids = data["text_id"].duplicated().sum()

print()
print("DUPLICATES")
print("----------")
print(f"Duplicate complete rows: {duplicate_rows}")
print(f"Duplicate text_id values: {duplicate_text_ids}")


# ------------------------------------------------------------
# 10. Display sentiment distribution
# ------------------------------------------------------------

print()
print("SENTIMENT LABEL DISTRIBUTION")
print("----------------------------")
print(data["sentiment_label"].value_counts(dropna=False))


# ------------------------------------------------------------
# 11. Display topic distribution
# ------------------------------------------------------------

print()
print("TOPIC CATEGORY DISTRIBUTION")
print("---------------------------")
print(data["topic_category"].value_counts(dropna=False))


# ------------------------------------------------------------
# 12. Calculate text-length statistics
# ------------------------------------------------------------

data["text_length"] = (
    data["post_text"]
    .fillna("")
    .astype(str)
    .str.len()
)

print()
print("TEXT LENGTH STATISTICS")
print("----------------------")
print(data["text_length"].describe())


# ------------------------------------------------------------
# 13. Show the shortest text records
# ------------------------------------------------------------

print()
print("FIVE SHORTEST TEXT RECORDS")
print("--------------------------")
print(
    data[
        [
            "text_id",
            "post_text",
            "sentiment_label",
            "topic_category",
            "text_length",
        ]
    ]
    .sort_values("text_length")
    .head(5)
    .to_string(index=False)
)


# ------------------------------------------------------------
# 14. Show the longest text records
# ------------------------------------------------------------

print()
print("FIVE LONGEST TEXT RECORDS")
print("-------------------------")
print(
    data[
        [
            "text_id",
            "post_text",
            "sentiment_label",
            "topic_category",
            "text_length",
        ]
    ]
    .sort_values("text_length", ascending=False)
    .head(5)
    .to_string(index=False)
)


print()
print("DATASET INSPECTION COMPLETED")
