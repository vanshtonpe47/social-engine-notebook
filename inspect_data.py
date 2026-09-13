import pandas as pd

# Load the original raw files
users = pd.read_csv("raw/Social_Engine_Users.csv")
posts = pd.read_csv("raw/Social_Engine_Posts_Corrupted.csv")

print("USERS DATASET")
print("----------------")
print("Rows and columns:", users.shape)
print("Columns:", list(users.columns))
print()

print("First five user records:")
print(users.head())
print()

print("Missing values in users:")
print(users.isna().sum())
print()

print("POSTS DATASET")
print("----------------")
print("Rows and columns:", posts.shape)
print("Columns:", list(posts.columns))
print()

print("First five post records:")
print(posts.head())
print()

print("Missing values in posts:")
print(posts.isna().sum())
print()

print("Duplicate post rows:", posts.duplicated().sum())