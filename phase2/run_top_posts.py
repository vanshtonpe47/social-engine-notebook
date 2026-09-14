import sqlite3


# Connect to the database
connection = sqlite3.connect("social_engine.db")


# Read the SQL query
with open(
    "sql/top_posts.sql",
    "r",
    encoding="utf-8"
) as file:
    query = file.read()


# Execute the query
result = connection.execute(query)


# Get column names
column_names = [
    column[0]
    for column in result.description
]


print("TOP 5 POSTS WITHIN EACH PLATFORM")
print("---------------------------------")
print(" | ".join(column_names))


# Print the results
for row in result.fetchall():
    values = []

    for value in row:
        if value is None:
            values.append("None")
        else:
            values.append(str(value))

    print(" | ".join(values))


# Close the connection
connection.close()


