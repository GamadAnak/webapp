import db_access

# initialize
db_access.initialize()

# create users
db_access.createUser(1, 'Guy', 'Shiran', 'Israel', 'Jerusalem', 'HaYabok 24', 123456)
db_access.createUser(2, 'Amit', 'Benski', 'Israel', 'Jerusalem', 'HaYabok 24', 123456)
db_access.createUser(3, 'Erez', 'Levanon', 'Israel', 'Jerusalem', 'IDK', 11111)
db_access.createUser(4, 'Ori', 'B', 'Israel', 'Jerusalem', 'IDK2', 11211)
db_access.createUser(5, 'Tal', 'S', 'Israel', 'Jerusalem', 'IDK3', 21111)
db_access.createUser(6, 'Yael', 'B', 'Israel', 'Jerusalem', 'IDK4', 18111)

# create group and assign members
users = [1, 2, 3, 4, 5, 6]
db_access.createGroup('Team6', 1, 50, 60)
db_access.addUsersToGroup(users, 0)

# get group
group = db_access.getGroup(0)
print(group.memberIds)

# assign giants
db_access.assignGiants(1)