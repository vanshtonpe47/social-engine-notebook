import sqlite3

# Connect to the SQLite database
connection = sqlite3.connect("social_engine.db")

# Read the SQL file
with open("sql/basic_queries.sql", "r", encoding="utf-8") as file:
    sql_text = file.read()

# Separate individual queries using semicolons
queries = [
    query.strip()
    for query in sql_text.split(";")
    if query.strip()
]

# Run each query
for number, query in enumerate(queries, start=1):
    print()
    print(f"QUERY {number}")
    print("-" * 40)
    print(query)

    result = connection.execute(query)
    column_names = [column[0] for column in result.description]

    print()
    print(" | ".join(column_names))

    for row in result.fetchall():
        print(" | ".join(str(value) for value in row))

# Close the connection
connection.close()


