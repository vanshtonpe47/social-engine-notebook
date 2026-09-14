import pandas as pd
import matplotlib.pyplot as plt

# Load the cleaned posts dataset
posts = pd.read_csv("cleaned/posts_clean.csv")

# Count posts for each platform
platform_counts = posts["platform"].fillna("Missing").value_counts()

print("POSTS BY PLATFORM")
print("-----------------")
print(platform_counts)

# Create a bar chart
platform_counts.plot(
    kind="bar",
    title="Number of Posts by Platform",
    xlabel="Platform",
    ylabel="Number of Posts"
)

plt.tight_layout()

# Save the chart
plt.savefig("figures/posts_by_platform.png")

# Display the chart
plt.show()
