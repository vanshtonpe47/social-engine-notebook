import sqlite3


# Open the SQLite database
connection = sqlite3.connect("social_engine.db")


# Read the trend query
with open(
    "sql/trend_query.sql",
    "r",
    encoding="utf-8"
) as file:
    query = file.read()


# Execute the query
result = connection.execute(query)


# Get the column names
column_names = [
    column[0]
    for column in result.description
]


# Print the title
print("MONTHLY POSTING TREND")
print("---------------------")

# Print the column names
print(" | ".join(column_names))

# Print each result row
for row in result.fetchall():
    formatted_row = []

    for value in row:
        if value is None:
            formatted_row.append("None")
        else:
            formatted_row.append(str(value))

    print(" | ".join(formatted_row))


# Close the connection
connection.close()


