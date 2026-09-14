import sqlite3
import pandas as pd

# Load the cleaned CSV files
users = pd.read_csv("../phase1/../phase1/cleaned/users_clean.csv")
posts = pd.read_csv("../phase1/../phase1/cleaned/posts_clean.csv")

# Create or open a SQLite database file
connection = sqlite3.connect("social_engine.db")

# Write the DataFrames into SQL tables
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

# Check how many rows were loaded
users_count = pd.read_sql(
    "SELECT COUNT(*) AS total_users FROM users",
    connection
)

posts_count = pd.read_sql(
    "SELECT COUNT(*) AS total_posts FROM posts",
    connection
)

print("DATABASE CREATED")
print("----------------")
print("Users table rows:", users_count.iloc[0]["total_users"])
print("Posts table rows:", posts_count.iloc[0]["total_posts"])

# Close the database connection
connection.close()


