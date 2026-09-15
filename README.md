# Social Engine Competition Project

This repository contains the reproducible recovery, cleaning, validation, exploratory analysis, and SQL analysis work for the Data Vortex 2026 Social Engine challenge.

The repository is organized into two clearly separated phases:

- **Phase 1:** Data recovery, cleaning, validation, and exploratory data analysis.
- **Phase 2:** One selected SQL challenge from each difficulty level, with separate SQL, screenshot, logic explanation, and insight-report deliverables.

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
│   ├── clean_data.py
│   ├── inspect_data.py
│   ├── validate_data.py
│   ├── eda_platform.py
│   ├── eda_time.py
│   └── eda_engagement.py
│
└── phase2/
    ├── sql/
    │   ├── E3_average_engagement_by_platform.sql
    │   ├── M2_follower_groups.sql
    │   └── H3_platform_anomalies.sql
    │
    ├── screenshots/
    │   ├── E3_platform_engagement.jpeg
    │   ├── M2_follower_groups.jpeg
    │   └── H3_platform_anomalies.jpeg
    │
    ├── results/
    │   ├── E3_result.csv
    │   ├── E3_result.txt
    │   ├── M2_result.csv
    │   ├── M2_result.txt
    │   ├── H3_result.csv
    │   └── H3_result.txt
    │
    ├── reports/
    │   ├── sql_queries.md
    │   ├── sql_queries.pdf
    │   ├── logic_explanation.md
    │   ├── logic_explanation.pdf
    │   ├── phase2_insight_report.md
    │   └── phase2_insight_report.pdf
    │
    ├── run_selected_queries.py
    └── create_screenshots.py
```

The generated SQLite database is intentionally not committed because it can be recreated using the Python query runner.

---

# Phase 1 — Data Recovery, Cleaning, and EDA

## Objective

Phase 1 focused on recovering the corrupted Social Engine datasets, cleaning and validating the data, and performing exploratory data analysis.

## Phase 1 workflow

```text
Raw datasets
    ↓
Data inspection
    ↓
Cleaning and transformation
    ↓
Validation
    ↓
Exploratory data analysis
    ↓
Cleaned datasets, figures, and report
```

## Phase 1 cleaning actions

The cleaning process:

- Removed exact duplicate post rows.
- Standardized mixed timestamp formats.
- Decoded HTML entities in text fields.
- Converted engagement columns to numeric values.
- Identified invalid negative engagement values.
- Preserved missing values instead of fabricating replacements.
- Preserved original timestamp values for traceability.
- Checked that every post refers to a valid user.

## Phase 1 results

After cleaning:

- 1,500 users remained.
- 12,000 unique posts remained.
- 360 duplicate post rows were removed.
- No duplicate post IDs remained.
- No unknown user IDs remained.
- No invalid timestamps remained.
- No negative engagement values remained.

The cleaned datasets are stored under:

```text
phase1/cleaned/
```

The Phase 1 report is stored under:

```text
phase1/reports/phase1_report.pdf
```

---

# Phase 2 — Selected SQL Challenges

The official Phase 2 instructions require one question from each difficulty level.

## Selected questions

| Difficulty | Selected question |
|---|---|
| Easy | E3 — Average Engagement by Platform |
| Medium | M2 — Do High Follower Users Get More Engagement? |
| Hard | H3 — Platform Performance Compared With Its Own Average |

---

## Easy — E3: Average Engagement by Platform

The E3 query calculates average likes, shares, comments, and total engagement for each named platform.

Posts with missing platforms are excluded from the platform comparison.

Result:

```text
Reddit has the highest average total engagement:
3,550.43 interactions per post
```

SQL source:

```text
phase2/sql/E3_average_engagement_by_platform.sql
```

---

## Medium — M2: Do High Follower Users Get More Engagement?

Users are divided into two groups:

- High follower users: follower count greater than or equal to 25,000.
- Low follower users: follower count below 25,000.

The query compares their average engagement per post.

Results:

| Follower group | Average engagement per post |
|---|---:|
| Low follower users | 3,535.84 |
| High follower users | 3,508.45 |

SQL source:

```text
phase2/sql/M2_follower_groups.sql
```

---

## Hard — H3: Platform Performance Compared With Its Own Average

The H3 query identifies posts whose total engagement is at least twice the average engagement of their own platform.

Result:

```text
139 exceptional posts were identified.
```

SQL source:

```text
phase2/sql/H3_platform_anomalies.sql
```

---

# Phase 2 Submission Deliverables

The official Phase 2 submission materials are separated as required.

| Requirement | File or folder |
|---|---|
| SQL Query PDF | `phase2/reports/sql_queries.pdf` |
| Output screenshots | `phase2/screenshots/*.jpeg` |
| Logic Explanation PDF | `phase2/reports/logic_explanation.pdf` |
| Phase 2 Insight Report PDF | `phase2/reports/phase2_insight_report.pdf` |

Supporting source files are also available:

```text
phase2/sql/
phase2/results/
phase2/reports/*.md
```

The screenshots are stored in JPEG format as required by the competition instructions.

---

# Reproducible workflow

From the repository root, run:

```powershell
python "phase2\run_selected_queries.py"
```

This script:

1. Loads the cleaned Phase 1 CSV files.
2. Creates the SQLite database.
3. Creates the `users` and `posts` tables.
4. Reads the three SQL files.
5. Executes E3, M2, and H3 dynamically.
6. Writes CSV and text result files under `phase2/results/`.

Then generate the screenshots:

```powershell
python "phase2\create_screenshots.py"
```

This creates:

```text
phase2/screenshots/E3_platform_engagement.jpeg
phase2/screenshots/M2_follower_groups.jpeg
phase2/screenshots/H3_platform_anomalies.jpeg
```

---

# Data-handling assumptions

The analysis uses the following assumptions:

- Total engagement is calculated as `likes + shares + comments`.
- Missing likes are treated as zero only for total-engagement calculations.
- Individual average-like calculations use SQL `AVG(likes)`, which ignores missing likes.
- Posts with missing platforms are excluded from platform-specific comparisons.
- No missing values were manually fabricated.
- The cleaned source datasets are not modified during SQL analysis.
- All analytical outputs are generated dynamically from the cleaned data and SQL queries.

---

# Technologies

| Purpose | Technology |
|---|---|
| Programming language | Python |
| Data cleaning | pandas |
| Visualization | Matplotlib |
| Database | SQLite |
| Analysis | SQL |
| Documentation | Markdown and PDF |
| Version control | Git and GitHub |

---

## Repository

GitHub repository:

```text
https://github.com/vanshtonpe47/social-engine-notebook
```