import sqlite3

DB_NAME = r"gamadanak.db"

conn = sqlite3.connect(DB_NAME)

print("Opened database: " + DB_NAME)

conn.execute("DROP TABLE IF EXISTS users")
conn.execute("DROP TABLE IF EXISTS groups")
conn.execute("DROP TABLE IF EXISTS memberships")
conn.execute("DROP TABLE IF EXISTS gifts")
conn.execute("DROP TABLE IF EXISTS invitations")
conn.execute("DROP TABLE IF EXISTS settings")

print("Dropped tables: users, groups, memberships")

conn.execute("CREATE TABLE users( \
              id INT PRIMARY KEY NOT NULL, \
              firstname TEXT NOT NULL, \
              lastname TEXT NOT NULL, \
              country TEXT NOT NULL, \
              city TEXT NOT NULL, \
              address TEXT NOT NULL, \
              zip INT NOT NULL, \
              aboutme TEXT NOT NULL)")

conn.execute("CREATE TABLE groups( \
              id INT PRIMARY KEY NOT NULL, \
              name TEXT NOT NULL, \
              adminid INT NOT NULL, \
              min FLOAT NOT NULL, \
              max FLOAT NOT NULL, \
              closed BOOLEAN NOT NULL, \
              image TEXT NOT NULL, \
              FOREIGN KEY (adminid) REFERENCES users(adminid))")

conn.execute("CREATE TABLE memberships( \
              userid INT NOT NULL, \
              groupid INT NOT NULL, \
              giantid INT NOT NULL, \
              giftready BOOLEAN NOT NULL, \
              giftid INT NOT NULL, \
              FOREIGN KEY (userid) REFERENCES users(userid), \
              FOREIGN KEY (groupid) REFERENCES groups(groupid), \
              FOREIGN KEY (giantid) REFERENCES groups(giantid), \
              FOREIGN KEY (giftid) REFERENCES gifts(giftid), \
              UNIQUE(userid, groupid))")

conn.execute("CREATE TABLE gifts( \
              id INT PRIMARY KEY NOT NULL, \
              url TEXT NOT NULL, \
              letter TEXT NOT NULL, \
              giantid INT NOT NULL, \
              dwarfid INT NOT NULL, \
              FOREIGN KEY (giantid) REFERENCES users(giantid), \
              FOREIGN KEY (dwarfid) REFERENCES users(dwarfid))")

conn.execute("CREATE TABLE invitations( \
              userid INT NOT NULL, \
              groupid INT NOT NULL, \
              UNIQUE(userid, groupid))")

conn.execute("CREATE TABLE settings( \
              name TEXT PRIMARY KEY NOT NULL, \
              value TEXT NOT NULL)")

print("Created tables: users, groups, memberships, gifts, settings")

conn.close()

print("finished!")