import pandas as pd
import matplotlib.pyplot as plt

# Load the cleaned posts dataset
posts = pd.read_csv("cleaned/posts_clean.csv")

# Convert timestamp text back into datetime values
posts["timestamp"] = pd.to_datetime(posts["timestamp"])

# Count posts by date
daily_posts = posts.groupby(
    posts["timestamp"].dt.date
).size()

print("POSTING ACTIVITY")
print("----------------")
print("First date:", daily_posts.index.min())
print("Last date:", daily_posts.index.max())
print("Highest number of posts on one day:", daily_posts.max())
print()
print("Dates with the highest post counts:")
print(daily_posts.sort_values(ascending=False).head(10))

# Create the chart
daily_posts.plot(
    kind="line",
    title="Daily Number of Posts",
    xlabel="Date",
    ylabel="Number of Posts"
)

plt.tight_layout()

# Save the chart
plt.savefig("figures/daily_post_volume.png")

# Display the chart
plt.show()