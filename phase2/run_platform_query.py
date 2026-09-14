import sqlite3


# Connect to the SQLite database
connection = sqlite3.connect("social_engine.db")


# Read the SQL query from the sql folder
with open(
    "sql/platform_engagement.sql",
    "r",
    encoding="utf-8"
) as file:
    query = file.read()


# Run the query
result = connection.execute(query)


# Get the column names
column_names = [
    column[0]
    for column in result.description
]


print("ENGAGEMENT BY PLATFORM")
print("----------------------")

print(" | ".join(column_names))

# Print the query results
for row in result.fetchall():
    values = []

    for value in row:
        if value is None:
            values.append("None")
        else:
            values.append(str(value))

    print(" | ".join(values))


# Close the database connection
connection.close()


