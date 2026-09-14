# Social Engine Competition — Data Recovery and SQL Analysis

This repository contains the complete working project for the Data Vortex Social Engine competition.

The project is organized into two phases:

- **Phase 1:** Dataset recovery, cleaning, validation, and exploratory data analysis.
- **Phase 2:** SQL table creation, analytical queries, output screenshots, logic explanations, and insight reporting.

Both phases are maintained in this single repository so that the workflow remains traceable and reproducible.

---

## Repository structure

```text
social-engine-notebook/
│
├── README.md
│
├── phase1/
│   ├── raw/
│   │   ├── Social_Engine_Users.csv
│   │   └── Social_Engine_Posts_Corrupted.csv
│   │
│   ├── cleaned/
│   │   ├── users_clean.csv
│   │   ├── posts_clean.csv
│   │   └── social_engine_cleaned.json
│   │
│   ├── figures/
│   │   ├── posts_by_platform.png
│   │   ├── daily_post_volume.png
│   │   └── engagement_distribution.png
│   │
│   ├── reports/
│   │   ├── phase1_report.md
│   │   └── phase1_report.pdf
│   │
│   ├── inspect_data.py
│   ├── clean_data.py
│   ├── validate_data.py
│   ├── eda_platform.py
│   ├── eda_time.py
│   ├── eda_engagement.py
│   └── submission_json.py
│
└── phase2/
    ├── sql/
    │   ├── basic_queries.sql
    │   ├── trend_query.sql
    │   ├── platform_engagement.sql
    │   ├── top_posts.sql
    │   ├── user_behaviour.sql
    │   ├── user_behaviour_summary.sql
    │   ├── follower_correlation.sql
    │   └── missingness_by_platform.sql
    │
    ├── screenshots/
    │   ├── trend_output.png
    │   ├── platform_output.png
    │   ├── top_posts_output.png
    │   ├── behaviour_output.png
    │   ├── correlation_output.png
    │   └── missingness_output.png
    │
    ├── reports/
    │   ├── phase2_report.md
    │   └── phase2_report.pdf
    │
    ├── setup_database.py
    ├── run_basic_queries.py
    ├── run_trend_query.py
    ├── run_platform_query.py
    ├── run_top_posts.py
    ├── run_user_behaviour.py
    ├── run_user_behaviour_summary.py
    ├── run_follower_correlation.py
    └── run_missingness.py
```

The SQLite database is generated locally by `setup_database.py` and does not need to be permanently stored in GitHub.

---

## Technologies

| Purpose | Technology |
|---|---|
| Programming language | Python |
| Data cleaning | pandas |
| Data visualization | Matplotlib |
| Database | SQLite |
| Analytical queries | SQL |
| Documentation | Markdown |
| Version control | Git and GitHub |

---

# Phase 1 — Data recovery, cleaning, and EDA

## Objective

Phase 1 focused on recovering the official datasets, preserving the raw files, cleaning corrupted values, validating the results, and performing exploratory data analysis.

## Phase 1 workflow

```text
raw datasets
    ↓
inspect_data.py
    ↓
clean_data.py
    ↓
cleaned datasets
    ↓
validate_data.py
    ↓
EDA scripts
    ↓
charts and Phase 1 report
```

## Phase 1 recovery

The recovery logs contained clues identifying the last known good node:

```text
03:42:23 node_07 responded 200 (intermittent)
03:42:26 watchdog last known good node: node_07
03:42:31 watchdog dashboard link to node_07: severed
```

The raw datasets were recovered and preserved in:

```text
phase1/raw/
```

The raw files were not manually overwritten.

## Phase 1 cleaning

The cleaning workflow:

- Removes exact duplicate post rows.
- Converts invalid blank values to missing values.
- Decodes HTML entities in text.
- Converts engagement fields to numeric values.
- Handles invalid negative engagement values.
- Standardizes mixed timestamp formats.
- Preserves original timestamps.
- Checks for unknown user IDs.
- Saves the cleaned datasets.

### Cleaning principles

| Problem | Action | Reason |
|---|---|---|
| Exact duplicate posts | Remove duplicate copies | Prevent double-counting |
| Missing platform | Preserve as missing | Do not infer unsupported values |
| Missing text | Preserve as missing | Do not invent text |
| Missing likes | Preserve as missing | Missing does not mean zero |
| Negative engagement | Convert to missing | Engagement cannot logically be negative |
| Mixed timestamps | Standardize to datetime | Enables consistent time analysis |
| Original timestamps | Preserve separately | Maintains traceability |
| Unknown user IDs | Validate against users | Checks table consistency |

No data was fabricated.

## Phase 1 results

After cleaning:

- 1,500 users remain.
- 12,000 unique posts remain.
- 360 duplicate post rows were removed.
- There are no duplicate post IDs.
- There are no unknown user IDs.
- There are no invalid timestamps.
- There are no negative engagement values.

The cleaned posts contain:

- 1,784 missing platform values.
- 1,688 missing text values.
- 2,323 missing likes values.

Missing values were preserved because unavailable information cannot be reliably reconstructed.

## Run Phase 1

From the repository root:

```powershell
cd phase1
python inspect_data.py
python clean_data.py
python validate_data.py
python eda_platform.py
python eda_time.py
python eda_engagement.py
cd ..
```

The outputs are saved in:

```text
phase1/cleaned/
phase1/figures/
phase1/reports/
```

The Phase 1 report is:

```text
phase1/reports/phase1_report.pdf
```

---

# Phase 2 — SQL analytical core

## Objective

Phase 2 converts the cleaned datasets into SQL tables and uses reproducible queries to analyze:

- Posting trends.
- Platform engagement.
- High-performing posts.
- User behaviour.
- Follower-count correlation.
- Data-quality missingness.

## Phase 2 workflow

```text
phase1/cleaned CSV files
    ↓
setup_database.py
    ↓
SQLite users and posts tables
    ↓
SQL query files
    ↓
generated outputs
    ↓
screenshots and insight report
```

## Database schema

The database contains two tables.

### Users table

| Column | Description |
|---|---|
| `user_id` | Unique user identifier |
| `location` | User location |
| `language` | User language |
| `account_created` | Account creation date |
| `follower_count` | Number of followers |

### Posts table

| Column | Description |
|---|---|
| `post_id` | Unique post identifier |
| `user_id` | User who created the post |
| `platform` | Social-media platform |
| `text_content` | Post text |
| `timestamp` | Standardized timestamp |
| `likes` | Number of likes |
| `shares` | Number of shares |
| `comments` | Number of comments |
| `timestamp_original` | Original timestamp |

The relationship is:

```text
users.user_id = posts.user_id
```

## Phase 2 query mapping

| Analysis | SQL file |
|---|---|
| Basic database checks | `phase2/sql/basic_queries.sql` |
| Monthly posting trend | `phase2/sql/trend_query.sql` |
| Engagement by platform | `phase2/sql/platform_engagement.sql` |
| Top posts by platform | `phase2/sql/top_posts.sql` |
| Detailed user behaviour | `phase2/sql/user_behaviour.sql` |
| Behaviour summary | `phase2/sql/user_behaviour_summary.sql` |
| Follower correlation | `phase2/sql/follower_correlation.sql` |
| Missingness by platform | `phase2/sql/missingness_by_platform.sql` |

The queries use reproducible SQL techniques including:

- Common Table Expressions.
- Aggregations.
- `CASE` expressions.
- Window functions.
- `ROW_NUMBER()`.
- `LAG()`.
- `PARTITION BY`.
- Joins.
- Conditional aggregation.

Outputs are generated from the database and are not hardcoded.

## Run Phase 2

From the repository root:

```powershell
cd phase2
python setup_database.py
python run_basic_queries.py
python run_trend_query.py
python run_platform_query.py
python run_top_posts.py
python run_user_behaviour.py
python run_user_behaviour_summary.py
python run_follower_correlation.py
python run_missingness.py
cd ..
```

Expected database counts:

```text
Users table rows: 1500
Posts table rows: 12000
```

The Phase 2 report is:

```text
phase2/reports/phase2_report.pdf
```

The output screenshots are stored in:

```text
phase2/screenshots/
```

## Phase 2 submission requirements

The Phase 2 deliverables include:

- SQL query files.
- Output screenshots.
- Schema design explanation.
- Query logic explanations.
- Findings and limitations.
- Phase 2 insight report in PDF format.

These are documented in:

```text
phase2/reports/phase2_report.pdf
```

---

## Reproducibility and integrity

The complete project is reproducible because:

1. Raw data is preserved.
2. Cleaning transformations are implemented in code.
3. Validation checks are documented.
4. SQL tables are created from the cleaned data.
5. Queries generate the analytical results.
6. Screenshots are captured from generated outputs.
7. Reports explain assumptions and limitations.

No analytical outputs were hardcoded into the SQL workflow.

---

## Competition deliverables

### Phase 1

- Cleaned dataset.
- EDA report.
- Cleaning code.
- Documentation.
- Reproducible workflow.

### Phase 2

- SQL queries.
- Output screenshots.
- Schema explanation.
- Query logic explanation.
- Phase 2 insight report PDF.

Both phases are maintained in this repository:

```text
https://github.com/vanshtonpe47/social-engine-notebook
```
