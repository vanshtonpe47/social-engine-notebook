# Social Engine Recovery — Phase 1

This repository contains the Phase 1 data-recovery, cleaning, validation, and exploratory data analysis workflow for the Data Vortex Social Engine competition.

The objective of Phase 1 was to recover the official datasets from the corrupted Social Engine website, identify data-quality problems, clean the data using documented rules, validate the result, and perform exploratory data analysis.

## Phase 1 workflow

```text
recover datasets
→ preserve raw files
→ inspect corruption
→ clean data
→ validate data
→ perform EDA
→ document findings
```

## Tools used

| Purpose | Tool |
|---|---|
| Programming language | Python |
| Data cleaning | pandas |
| Data visualization | Matplotlib |
| Code editor | Visual Studio Code |
| Documentation | Markdown |
| Version control | Git and GitHub |

## Project structure

```text
social-engine-competition/
│
├── raw/
│   ├── Social_Engine_Users.csv
│   └── Social_Engine_Posts_Corrupted.csv
│
├── cleaned/
│   ├── users_clean.csv
│   └── posts_clean.csv
│
├── figures/
│   ├── posts_by_platform.png
│   ├── daily_post_volume.png
│   └── engagement_distribution.png
│
├── reports/
│   └── phase1_report.md
│
├── inspect_data.py
├── clean_data.py
├── validate_data.py
├── eda_platform.py
├── eda_time.py
├── eda_engagement.py
├── README.md
└── .gitignore
```

## Dataset description

### Users dataset

The users dataset contains one record per user.

| Column | Description |
|---|---|
| `user_id` | Unique user identifier |
| `location` | User location |
| `language` | User language |
| `account_created` | Account creation date |
| `follower_count` | Number of followers |

### Posts dataset

The posts dataset contains one record per social-media post.

| Column | Description |
|---|---|
| `post_id` | Unique post identifier |
| `user_id` | User who created the post |
| `platform` | Social-media platform |
| `text_content` | Post text |
| `timestamp` | Standardized post timestamp |
| `likes` | Number of likes |
| `shares` | Number of shares |
| `comments` | Number of comments |
| `timestamp_original` | Original timestamp before standardization |

The relationship between the datasets is:

```text
users.user_id = posts.user_id
```

One user can create multiple posts.

## Raw-data recovery

The recovery website initially displayed a corrupted Social Engine system.

The system log contained the following clues:

```text
03:42:23 node_07 responded 200 (intermittent)
03:42:26 watchdog last known good node: node_07
03:42:31 watchdog dashboard link to node_07: severed
```

The last known good node was identified as:

```text
node_07
```

The official raw datasets were recovered from the Social Engine website and preserved without manual editing.

## Phase 1 results

The raw data contained:

- 1,500 users
- 12,360 post rows
- 360 exact duplicate post rows
- Missing platform values
- Missing text values
- Missing likes values
- Mixed timestamp formats
- Negative likes
- HTML-encoded text values

After cleaning, the dataset contained:

- 1,500 users
- 12,000 unique posts
- 0 duplicate post IDs
- 0 unknown user IDs
- 0 invalid timestamps
- 0 negative engagement values

The cleaned posts contained:

- 1,784 missing platform values
- 1,688 missing text values
- 2,323 missing likes values

Missing information was preserved rather than fabricated.

## Cleaning decisions

| Problem | Action | Reason |
|---|---|---|
| Exact duplicate post rows | Remove duplicate copies | Prevent double-counting |
| Missing platform | Keep as missing | The correct platform cannot be inferred |
| Missing text | Keep as missing | Text should not be invented |
| Missing likes | Keep as missing | Missing does not mean zero |
| Negative likes | Convert to missing | Likes cannot logically be negative |
| Negative shares or comments | Convert to missing if found | Engagement counts cannot be negative |
| Mixed timestamp formats | Convert to one datetime format | Enables consistent time analysis |
| Original timestamps | Preserve in `timestamp_original` | Maintains traceability |
| HTML entities | Decode into normal characters | Restores readable text |
| Unknown user IDs | Check against users table | Validates the dataset relationship |

The raw files were not overwritten.

## How to install the required libraries

Open the VS Code terminal in the project folder and run:

```powershell
python -m pip install pandas matplotlib
```

If the `python` command does not work, try:

```powershell
py -m pip install pandas matplotlib
```

## How to reproduce the Phase 1 workflow

Run the following commands from the project root.

### 1. Inspect the raw data

```powershell
python inspect_data.py
```

This displays:

- Dataset dimensions
- Column names
- Sample records
- Missing-value counts
- Duplicate post rows

### 2. Clean the data

```powershell
python clean_data.py
```

This creates:

```text
cleaned/users_clean.csv
cleaned/posts_clean.csv
```

The cleaning script:

- Loads the raw CSV files.
- Removes exact duplicate post rows.
- Converts blank and `NULL` values to missing values.
- Decodes HTML entities.
- Converts engagement columns to numeric values.
- Handles invalid negative engagement values.
- Standardizes mixed timestamp formats.
- Preserves original timestamps.
- Checks for unknown user IDs.
- Saves the cleaned datasets.

### 3. Validate the cleaned data

```powershell
python validate_data.py
```

The validation script checks:

- Duplicate rows
- Duplicate identifiers
- Unknown user IDs
- Negative engagement values
- Invalid timestamps
- Data types

Expected validation results include:

```text
Duplicate users: 0
Duplicate posts: 0
Duplicate post IDs: 0
Duplicate user IDs: 0
Posts with unknown user IDs: 0
Negative likes: 0
Negative shares: 0
Negative comments: 0
Invalid timestamps: 0
```

### 4. Perform exploratory data analysis

Run:

```powershell
python eda_platform.py
python eda_time.py
python eda_engagement.py
```

These scripts analyze:

- The number of posts by platform
- Posting activity over time
- The distributions of likes, shares, and comments

The charts are saved in:

```text
figures/
```

## Exploratory findings

### Platform distribution

The cleaned posts were distributed as follows:

| Platform | Posts |
|---|---:|
| Facebook | 2,074 |
| YouTube | 2,073 |
| Twitter | 2,049 |
| Reddit | 2,031 |
| Instagram | 1,989 |
| Missing | 1,784 |

The named platforms have relatively similar post counts. The 1,784 posts without platform values were retained under a separate `Missing` category.

### Time distribution

The cleaned posts cover the period:

```text
5 January 2024 to 4 December 2025
```

The highest daily post volume was:

```text
54 posts on 16 June 2024
```

A high-volume day was not automatically classified as an error because a large value requires contextual investigation.

### Engagement distribution

| Metric | Valid values | Missing values | Mean | Median |
|---|---:|---:|---:|---:|
| Likes | 9,677 | 2,323 | 2,493.51 | 2,502 |
| Shares | 12,000 | 0 | 1,007.17 | 1,018 |
| Comments | 12,000 | 0 | 504.35 | 503 |

The mean and median likes values are close. However, likes are missing for 2,323 posts, representing 19.36% of the cleaned posts.

Missing likes were not changed to zero because:

```text
missing likes ≠ zero likes
```

A missing value means that the information is unavailable. Zero means that the value is known to be zero.

## Phase 1 report

The complete exploratory analysis report is available at:

```text
reports/phase1_report.md
```

The report includes:

- Dataset overview
- Raw-data problems
- Cleaning decisions
- Validation results
- Platform analysis
- Time analysis
- Engagement analysis
- Charts
- Assumptions
- Limitations
- Conclusion

## Evaluation criteria alignment

| Evaluation criterion | How this project addresses it |
|---|---|
| Data Cleaning Accuracy | Duplicate removal, timestamp conversion, invalid-value handling, and validation checks are documented. |
| Data Handling and Preprocessing Logic | Each transformation has a stated reason. |
| EDA Depth and Insight Discovery | Platform, time, engagement, and missingness patterns are analyzed. |
| Data Consistency and Standardisation | Dates, numeric values, text entities, and missing values are standardized. |
| Code Quality and Documentation | The workflow uses readable Python scripts with comments and clear instructions. |
| Insight Interpretation and Clarity | Findings include numerical evidence and limitations. |

## Reproducibility

The complete Phase 1 workflow can be rerun using:

```powershell
python inspect_data.py
python clean_data.py
python validate_data.py
python eda_platform.py
python eda_time.py
python eda_engagement.py
```

The workflow is:

```text
raw CSV files
    ↓
inspect_data.py
    ↓
clean_data.py
    ↓
cleaned CSV files
    ↓
validate_data.py
    ↓
EDA scripts
    ↓
figures and Phase 1 report
```

## Data integrity statement

No data was fabricated.

Missing values were preserved when the correct value could not be determined. Transformations were applied consistently through code, and the original raw files were retained for reference.

## Phase 1 deliverables

The Phase 1 deliverables are:

- Cleaned datasets in `cleaned/`
- EDA charts in `figures/`
- Phase 1 report in `reports/phase1_report.md`
- Cleaning code in the root folder
- Validation code in the root folder
- Reproducible workflow documented in this README