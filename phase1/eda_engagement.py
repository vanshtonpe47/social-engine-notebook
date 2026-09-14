import pandas as pd
import matplotlib.pyplot as plt

# Load the cleaned posts dataset
posts = pd.read_csv("cleaned/posts_clean.csv")

# Select engagement columns
engagement_columns = ["likes", "shares", "comments"]

# Print summary statistics
print("ENGAGEMENT SUMMARY")
print("------------------")
print(posts[engagement_columns].describe())

print()
print("Missing engagement values:")
print(posts[engagement_columns].isna().sum())

# Create boxplots
posts[engagement_columns].plot(
    kind="box",
    title="Distribution of Likes, Shares, and Comments"
)

plt.ylabel("Count")
plt.tight_layout()

# Save the chart
plt.savefig("figures/engagement_distribution.png")

# Display the chart
plt.show()
