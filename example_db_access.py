import db_access

# initialize
db_access.initialize()

# create users
db_access.createUser(1, 'Guy', 'Shiran', 'Israel', 'Jerusalem', 'HaYabok 24', 123456, 'i')
db_access.createUser(2, 'Amit', 'Benski', 'Israel', 'Jerusalem', 'HaYabok 24', 123456, 'love')
db_access.createUser(3, 'Erez', 'Levanon', 'Israel', 'Jerusalem', 'IDK', 11111, 'big')
db_access.createUser(4, 'Ori', 'B', 'Israel', 'Jerusalem', 'IDK2', 11211, 'butts')
db_access.createUser(5, 'Tal', 'S', 'Israel', 'Jerusalem', 'IDK3', 21111, 'no')
db_access.createUser(6, 'Yael', 'B', 'Israel', 'Jerusalem', 'IDK4', 18111, 'lie')

# create group and assign members
users = [1, 2, 3, 4, 5, 6]
db_access.createGroup('Team6', 1, 50, 60)
db_access.addUsersToGroup(users, 0)

# get group
group = db_access.getGroup(0)
print(group.memberIds)

# assign giants
assignments = db_access.assignGiants(0)
print(assignments)

# get assignments
for user in users:
    assignment = db_access.getAssignment(user, 0)
    print(assignment)

# set gift
db_access.createGift(0, 'www.amazon.com/crap', 4, 2, 'hope you like big butts')
gift = db_access.getGift(0)
print(gift.url)

# get user profile and groups
user = db_access.getUser(3)
print(user.firstname)
print(user.aboutme)
print(user.groups)