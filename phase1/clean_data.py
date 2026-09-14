import pandas as pd
import html
# 1. Load the raw datasets
users = pd.read_csv("raw/Social_Engine_Users.csv")
posts = pd.read_csv("raw/Social_Engine_Posts_Corrupted.csv")

# 2. Show the original number of rows
print("Original users:", len(users))
print("Original posts:", len(posts))

# 3. Remove exact duplicate post rows
posts = posts.drop_duplicates()

print("Posts after removing duplicates:", len(posts))

# 4. Convert blank strings to missing values
users = users.replace(r"^\s*$", pd.NA, regex=True)
posts = posts.replace(r"^\s*$", pd.NA, regex=True)

# 5. Convert the literal word NULL to a missing value
users = users.replace("NULL", pd.NA)
posts = posts.replace("NULL", pd.NA)

# Decode HTML entities in text content
posts["text_content"] = posts["text_content"].apply(
    lambda value: html.unescape(value)
    if pd.notna(value)
    else value
)
# 6. Convert likes, shares, and comments to numbers
posts["likes"] = pd.to_numeric(posts["likes"], errors="coerce")
posts["shares"] = pd.to_numeric(posts["shares"], errors="coerce")
posts["comments"] = pd.to_numeric(posts["comments"], errors="coerce")

# 7. Negative likes are invalid, so mark them as missing
posts.loc[posts["likes"] < 0, "likes"] = pd.NA

# 8. Convert different timestamp formats to one standard format

# Preserve the original value for traceability
posts["timestamp_original"] = posts["timestamp"]

raw_timestamp = posts["timestamp"].astype("string").str.strip()

# Identify Unix timestamps, which contain 10 digits
unix_mask = raw_timestamp.str.fullmatch(r"\d{10}")

# Create an empty datetime column
standard_timestamp = pd.Series(
    pd.NaT,
    index=posts.index,
    dtype="datetime64[ns]"
)

# Convert Unix timestamps
standard_timestamp.loc[unix_mask] = pd.to_datetime(
    pd.to_numeric(raw_timestamp.loc[unix_mask]),
    unit="s",
    errors="coerce"
)

# Convert normal date and ISO datetime values
standard_timestamp.loc[~unix_mask] = pd.to_datetime(
    raw_timestamp.loc[~unix_mask],
    format="mixed",
    dayfirst=True,
    errors="coerce"
)

# Replace the original timestamp with the standardized timestamp
posts["timestamp"] = standard_timestamp


# 9. Save the cleaned datasets
users.to_csv("cleaned/users_clean.csv", index=False)
posts.to_csv("cleaned/posts_clean.csv", index=False)

# 10. Print a cleaning summary
print()
print("CLEANING SUMMARY")
print("----------------")
print("Clean users:", len(users))
print("Clean posts:", len(posts))
print()
print("Missing values in cleaned posts:")
print(posts.isna().sum())
