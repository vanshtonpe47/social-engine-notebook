import pandas as pd

# Load the cleaned datasets
users = pd.read_csv("cleaned/users_clean.csv")
posts = pd.read_csv("cleaned/posts_clean.csv")

print("CLEANED DATA VALIDATION")
print("-----------------------")

# 1. Check duplicate rows
print("Duplicate users:", users.duplicated().sum())
print("Duplicate posts:", posts.duplicated().sum())

# 2. Check whether post IDs are unique
print("Duplicate post IDs:", posts["post_id"].duplicated().sum())

# 3. Check whether user IDs are unique
print("Duplicate user IDs:", users["user_id"].duplicated().sum())

# 4. Check that every post belongs to a known user
unknown_users = posts[~posts["user_id"].isin(users["user_id"])]

print("Posts with unknown user IDs:", len(unknown_users))

# 5. Check invalid engagement values
print("Negative likes:", (posts["likes"] < 0).sum())
print("Negative shares:", (posts["shares"] < 0).sum())
print("Negative comments:", (posts["comments"] < 0).sum())

# 6. Check timestamp conversion
posts["timestamp"] = pd.to_datetime(
    posts["timestamp"],
    errors="coerce"
)

print("Invalid timestamps:", posts["timestamp"].isna().sum())

# 7. Display cleaned data types
print()
print("DATA TYPES")
print(posts.dtypes)
