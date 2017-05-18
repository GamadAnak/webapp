import sqlite3
import random

DB_NAME = "gamadanak.db"
USERS_TABLE = "users"
GROUPS_TABLE = "groups"
MEMBERSHIPS_TABLE = "memberships"
SETTINGS_TABLE = "settings"
GROUP_ID_COUNTER_NAME = "groupIdCounter"

## classes
class User:
    """ 
    Represents a user profile in the system 
    """
    def __init__(self, id, firstname, lastname, country, city, address, zip):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.country = country
        self.city = city
        self.address = address
        self.zip = zip
        return;

class Group:
    """ 
    Represents a group in the system 
    """
    def __init__(self, id, name, adminId, min, max, closed, memberIds):
        self.id = id
        self.name = name
        self.adminId = adminId
        self.min = min
        self.max = max
        self.closed = closed
        self.memberIds = memberIds
        return;

## functions
def initialize():
    """
    Initializes the database settings, needs to be called before using other functions 
    """
    conn = sqlite3.connect(DB_NAME)
    insert_cmd = "INSERT INTO %s VALUES('%s', 0)" % (SETTINGS_TABLE, GROUP_ID_COUNTER_NAME)
    conn.execute(insert_cmd)
    conn.commit()
    conn.close()

def createUser(id, firstname, lastname, country, city, address, zip):
    """
    Creates a new user profile in the database
    """
    conn = sqlite3.connect(DB_NAME)
    insert_cmd = "INSERT INTO %s VALUES (%s, '%s', '%s', '%s', '%s', '%s', %s)" \
                 % (USERS_TABLE, str(id), firstname, lastname, country, city, address, str(zip))
    conn.execute(insert_cmd)
    conn.commit()
    conn.close()

def getUser(id):
    """
    Retrieves a user profile 
    """
    conn = sqlite3.connect(DB_NAME)
    select_cmd = "SELECT * FROM %s WHERE id = %s" % (USERS_TABLE, id)
    cursor = conn.execute(select_cmd)
    for row in cursor:
        user = User(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
    conn.close()
    return user

def createGroup(name, adminid, min ,max):
    """
    Creates a new group in the database
    """
    conn = sqlite3.connect(DB_NAME)

    # get current available group id and increment it
    select_cmd = "SELECT * FROM %s WHERE name = '%s'" % (SETTINGS_TABLE, GROUP_ID_COUNTER_NAME)
    cursor = conn.execute(select_cmd)
    for row in cursor:
        group_id = int(row[1]);
    incremented_group_id = group_id + 1;
    update_cmd = "UPDATE %s SET value = %s WHERE name = '%s'" % \
                 (SETTINGS_TABLE, incremented_group_id, GROUP_ID_COUNTER_NAME)
    conn.execute(update_cmd)

    # create new group
    insert_cmd = "INSERT INTO %s VALUES (%s, '%s', '%s', %s, %s, 'FALSE')" \
                 % (GROUPS_TABLE, group_id, name, adminid, min, max)
    conn.execute(insert_cmd)
    conn.commit()
    conn.close()

def getGroup(groupId):
    """
    Gets the group info and its members ids
    """
    conn = sqlite3.connect(DB_NAME)

    # get group info
    select_cmd = "SELECT * FROM %s WHERE id = %s" % (GROUPS_TABLE, groupId)
    cursor = conn.execute(select_cmd)
    for row in cursor:
        ret = Group(row[0], row[1], row[2], row[3], row[4], row[5], [])

    # get group members
    select_cmd = "SELECT userid FROM %s WHERE groupid = %s" % (MEMBERSHIPS_TABLE, groupId)
    cursor = conn.execute(select_cmd)
    for row in cursor:
        ret.memberIds.append(row[0])

    conn.close()
    return ret

def addUsersToGroup(userIds, groupId):
    """
    Adds the users to the group 
    """
    conn = sqlite3.connect(DB_NAME)
    for id in userIds:
        insert_cmd = "INSERT INTO %s VALUES (%s, '%s', -1)" \
                     % (MEMBERSHIPS_TABLE, id, groupId)
        conn.execute(insert_cmd)
    conn.commit()
    conn.close()

def assignGiants(groupId):
    """
    Assigns giants to each of the group members
    """
    conn = sqlite3.connect(DB_NAME)

    # get group users
    select_cmd = "SELECT * FROM %s WHERE groupid = %s" % (MEMBERSHIPS_TABLE, groupId)
    cursor = conn.execute(select_cmd)
    users = []
    for row in cursor:
        users.append(row[0])

    # assign giants
    assignments = permutationWithoutFixedPoints(users)

    # update memberships table
    for i in range(len(users)):
        update_cmd = "UPDATE %s SET giantid = %s WHERE userid = %s AND groupid = %s" \
            % (MEMBERSHIPS_TABLE, assignments[i], users[i], groupId)
        conn.execute(update_cmd)

    conn.commit()
    conn.close()

    return assignments

def permutationWithoutFixedPoints(numbers):
    """
    Given a list of unique numbers returns a permutation without fixed points 
    """
    randomized_list = numbers[:]
    while True:
        random.shuffle(randomized_list)
        for a, b in zip(numbers, randomized_list):
            if a == b:
                break
        else:
            return randomized_list