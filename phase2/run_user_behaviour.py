import sqlite3


connection = sqlite3.connect("social_engine.db")

with open(
    "sql/user_behaviour.sql",
    "r",
    encoding="utf-8"
) as file:
    query = file.read()

result = connection.execute(query)

column_names = [
    column[0]
    for column in result.description
]

print("USER BEHAVIOUR GROUPS")
print("---------------------")
print(" | ".join(column_names))

rows = result.fetchall()

for row in rows[:30]:
    values = []

    for value in row:
        if value is None:
            values.append("None")
        else:
            values.append(str(value))

    print(" | ".join(values))

print()
print("Rows displayed:", min(30, len(rows)))
print("Total grouped users:", len(rows))

connection.close()


