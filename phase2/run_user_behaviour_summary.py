import sqlite3


connection = sqlite3.connect("social_engine.db")

with open(
    "sql/user_behaviour_summary.sql",
    "r",
    encoding="utf-8"
) as file:
    query = file.read()

result = connection.execute(query)

column_names = [
    column[0]
    for column in result.description
]

print("USER BEHAVIOUR SUMMARY")
print("----------------------")
print(" | ".join(column_names))

for row in result.fetchall():
    values = []

    for value in row:
        if value is None:
            values.append("None")
        else:
            values.append(str(value))

    print(" | ".join(values))

connection.close()


