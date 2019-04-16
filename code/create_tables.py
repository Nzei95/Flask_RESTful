import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# use INTEGER to create auto incrementing columns
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

connection.commit()

connection.close()