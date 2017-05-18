import sqlite3

DB_NAME = r"gamadanak.db"

conn = sqlite3.connect(DB_NAME)

print("Opened database: " + DB_NAME)

conn.execute("DROP TABLE IF EXISTS users")
conn.execute("DROP TABLE IF EXISTS groups")
conn.execute("DROP TABLE IF EXISTS memberships")

print("Dropped tables: users, groups, memberships")

conn.execute("CREATE TABLE users( \
              id INT PRIMARY KEY NOT NULL, \
              firstname TEXT NOT NULL, \
              lastname TEXT NOT NULL, \
              country TEXT NOT NULL, \
              city TEXT NOT NULL, \
              address TEXT NOT NULL, \
              zip INT NOT NULL)")

conn.execute("CREATE TABLE groups( \
              id INT PRIMARY KEY NOT NULL, \
              name TEXT NOT NULL, \
              admin INT NOT NULL)")

conn.execute("CREATE TABLE memberships( \
              userid INT PRIMARY KEY NOT NULL, \
              groupid INT NOT NULL, \
              giantid INT NOT NULL)")

print("Created tables: users, groups, memberships")

conn.close()

print("finished!")