from pathlib import Path
import json
import pandas as pd

BASE = Path(__file__).parent
CLEANED = BASE / "cleaned"
OUTPUT = CLEANED / "social_engine_cleaned.json"

users_path = CLEANED / "users_clean.csv"
posts_path = CLEANED / "posts_clean.csv"

users = pd.read_csv(users_path)
posts = pd.read_csv(posts_path)

# Convert missing values to valid JSON null values.
users_records = json.loads(
    users.to_json(orient="records", date_format="iso")
)

posts_records = json.loads(
    posts.to_json(orient="records", date_format="iso")
)

submission = {
    "users": users_records,
    "posts": posts_records,
}

with open(OUTPUT, "w", encoding="utf-8") as file:
    json.dump(
        submission,
        file,
        ensure_ascii=False,
        separators=(",", ":"),
    )

print("Valid combined JSON created.")
print(f"Users included: {len(users_records)}")
print(f"Posts included: {len(posts_records)}")
print(f"File size: {OUTPUT.stat().st_size / (1024 * 1024):.2f} MB")
print(f"Output: {OUTPUT}")
