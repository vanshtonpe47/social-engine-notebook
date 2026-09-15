from pathlib import Path
import sqlite3
import pandas as pd


# ------------------------------------------------------------
# 1. Define project paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PHASE2_DIR = Path(__file__).resolve().parent

USERS_FILE = PROJECT_ROOT / "phase1" / "cleaned" / "users_clean.csv"
POSTS_FILE = PROJECT_ROOT / "phase1" / "cleaned" / "posts_clean.csv"

SQL_DIR = PHASE2_DIR / "sql"
RESULTS_DIR = PHASE2_DIR / "results"
DATABASE_FILE = PHASE2_DIR / "social_engine_phase2.db"

RESULTS_DIR.mkdir(exist_ok=True)


# ------------------------------------------------------------
# 2. Check that required input files exist
# ------------------------------------------------------------

required_files = [
    USERS_FILE,
    POSTS_FILE,
    SQL_DIR / "E3_average_engagement_by_platform.sql",
    SQL_DIR / "M2_follower_groups.sql",
    SQL_DIR / "H3_platform_anomalies.sql",
]

for file_path in required_files:
    if not file_path.exists():
        raise FileNotFoundError(f"Required file not found: {file_path}")


# ------------------------------------------------------------
# 3. Load cleaned datasets
# ------------------------------------------------------------

users = pd.read_csv(USERS_FILE)
posts = pd.read_csv(POSTS_FILE)

print("CLEANED DATA LOADED")
print("-------------------")
print(f"Users rows: {len(users)}")
print(f"Posts rows: {len(posts)}")


# ------------------------------------------------------------
# 4. Create SQLite database and tables
# ------------------------------------------------------------

if DATABASE_FILE.exists():
    DATABASE_FILE.unlink()

connection = sqlite3.connect(DATABASE_FILE)

users.to_sql(
    "users",
    connection,
    if_exists="replace",
    index=False
)

posts.to_sql(
    "posts",
    connection,
    if_exists="replace",
    index=False
)

print()
print("DATABASE CREATED")
print("-----------------")
print(f"Users table rows: {len(users)}")
print(f"Posts table rows: {len(posts)}")


# ------------------------------------------------------------
# 5. Define the three selected questions
# ------------------------------------------------------------

selected_queries = [
    (
        "E3",
        "E3_average_engagement_by_platform.sql",
        "E3 - Average Engagement by Platform"
    ),
    (
        "M2",
        "M2_follower_groups.sql",
        "M2 - Do High Follower Users Get More Engagement?"
    ),
    (
        "H3",
        "H3_platform_anomalies.sql",
        "H3 - Platform Performance Compared With Its Own Average"
    ),
]


# ------------------------------------------------------------
# 6. Execute each SQL query dynamically
# ------------------------------------------------------------

for question_code, sql_filename, question_title in selected_queries:

    sql_file = SQL_DIR / sql_filename
    sql_query = sql_file.read_text(encoding="utf-8")

    result = pd.read_sql_query(sql_query, connection)

    csv_output = RESULTS_DIR / f"{question_code}_result.csv"
    text_output = RESULTS_DIR / f"{question_code}_result.txt"

    result.to_csv(csv_output, index=False)

    with open(text_output, "w", encoding="utf-8") as output_file:
        output_file.write(question_title + "\n")
        output_file.write("=" * len(question_title) + "\n\n")
        output_file.write(result.to_string(index=False))
        output_file.write("\n")

    print()
    print(question_title.upper())
    print("-" * len(question_title))
    print(result.to_string(index=False))
    print()
    print(f"CSV saved to: {csv_output}")
    print(f"Text output saved to: {text_output}")


# ------------------------------------------------------------
# 7. Close the database connection
# ------------------------------------------------------------

connection.close()

print()
print("ALL SELECTED QUERIES COMPLETED")
print("------------------------------")
print(f"Database: {DATABASE_FILE}")
print(f"Results folder: {RESULTS_DIR}")
