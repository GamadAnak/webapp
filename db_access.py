import sqlite3
import random

DB_NAME = "gamadanak.db"
USERS_TABLE = "users"
GROUPS_TABLE = "groups"
MEMBERSHIPS_TABLE = "memberships"
GIFTS_TABLE = "gifts"
INVITATIONS_TABLE = "invitations"
SETTINGS_TABLE = "settings"
GROUP_ID_COUNTER = "groupIdCounter"
GIFTS_ID_COUNTER = "giftsIdCounter"

## classes
class User:
    """ 
    Represents a user profile in the system 
    """
    def __init__(self, id, firstname, lastname, country, city, address, zip, aboutme, groups, invitations):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.country = country
        self.city = city
        self.address = address
        self.zip = zip
        self.aboutme = aboutme
        self.groups = groups
        self.invitations = invitations

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

class Gift:
    """ 
    Represents a gift in the system 
    """

    def __init__(self, id, url, groupId, giantId, dwarfId, letter):
        self.id = id
        self.url = url
        self.groupId = groupId
        self.giantId = giantId
        self.dwarfId = dwarfId
        self.letter = letter

## functions
def initialize():
    """
    Initializes the database settings, needs to be called before using other functions 
    """
    conn = sqlite3.connect(DB_NAME)

    # check if already initialized
    select_cmd = "SELECT * FROM %s" % (SETTINGS_TABLE)
    cursor = conn.execute(select_cmd)
    if (cursor.fetchone() != None):
        return

    # init group id counter
    insert_cmd = "INSERT INTO %s VALUES('%s', 0)" % (SETTINGS_TABLE, GROUP_ID_COUNTER)
    conn.execute(insert_cmd)

    # init gifts id counter
    insert_cmd = "INSERT INTO %s VALUES('%s', 0)" % (SETTINGS_TABLE, GIFTS_ID_COUNTER)
    conn.execute(insert_cmd)

    conn.commit()
    conn.close()

def doesUserExist(id):
    """
    Checks is a user exists in the system
    """
    conn = sqlite3.connect(DB_NAME)

    # attempt to retrieve user info
    select_cmd = "SELECT * FROM %s WHERE id = %s" % (USERS_TABLE, id)
    cursor = conn.execute(select_cmd)

    if (cursor.fetchone() == None):
        return False

    return True

def createUser(id, firstname, lastname, country, city, address, zip, aboutme):
    """
    Creates a new user profile in the database
    """
    conn = sqlite3.connect(DB_NAME)
    insert_cmd = "INSERT INTO %s VALUES (%s, '%s', '%s', '%s', '%s', '%s', %s, '%s')" \
                 % (USERS_TABLE, id, firstname, lastname, country, city, address, zip, aboutme)
    conn.execute(insert_cmd)
    conn.commit()
    conn.close()

def getUser(id):
    """
    Retrieves a user profile and the groups it is in
    """
    conn = sqlite3.connect(DB_NAME)

    # get user info
    select_cmd = "SELECT * FROM %s WHERE id = %s" % (USERS_TABLE, id)
    cursor = conn.execute(select_cmd)
    for row in cursor:
        ret = User(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], [], [])

    # get user groups
    select_cmd = "SELECT groupid FROM %s WHERE userid = %s" % (MEMBERSHIPS_TABLE, id)
    cursor = conn.execute(select_cmd)
    for row in cursor:
        ret.groups.append(row[0])

    # get user invitations
    select_cmd = "SELECT groupid FROM %s WHERE userid = %s" % (INVITATIONS_TABLE, id)
    cursor = conn.execute(select_cmd)
    for row in cursor:
        ret.invitations.append(row[0])

    conn.close()
    return ret

def createGroup(name, adminid, min ,max):
    """
    Creates a new group in the database
    """
    conn = sqlite3.connect(DB_NAME)

    # get current available group id and increment it
    select_cmd = "SELECT * FROM %s WHERE name = '%s'" % (SETTINGS_TABLE, GROUP_ID_COUNTER)
    cursor = conn.execute(select_cmd)
    for row in cursor:
        group_id = int(row[1]);
    incremented_group_id = group_id + 1;
    update_cmd = "UPDATE %s SET value = %s WHERE name = '%s'" % \
                 (SETTINGS_TABLE, incremented_group_id, GROUP_ID_COUNTER)
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
        insert_cmd = "INSERT INTO %s VALUES (%s, %s, -1, 'FALSE', -1)" \
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

def getAssignment(userid, groupid):
    """
    Gets the assignment of the user in the group
    """
    conn = sqlite3.connect(DB_NAME)

    select_cmd = "SELECT giantid FROM %s WHERE userid = %s AND groupid = %s" % \
                 (MEMBERSHIPS_TABLE, userid, groupid)
    cursor = conn.execute(select_cmd)
    for row in cursor:
        ret = row[0]

    conn.close()
    return ret

def createGift(groupid, url, giantid, dwarfid, letter):
    """
    Creates a new gift in the database
    """
    conn = sqlite3.connect(DB_NAME)

    # get current available gift id and increment it
    select_cmd = "SELECT * FROM %s WHERE name = '%s'" % (SETTINGS_TABLE, GIFTS_ID_COUNTER)
    cursor = conn.execute(select_cmd)
    for row in cursor:
        gift_id = int(row[1]);
    incremented_gift_id = gift_id + 1;
    update_cmd = "UPDATE %s SET value = %s WHERE name = '%s'" % \
                 (SETTINGS_TABLE, incremented_gift_id, GIFTS_ID_COUNTER)
    conn.execute(update_cmd)

    # create new gift
    insert_cmd = "INSERT INTO %s VALUES (%s, '%s', %s, %s, '%s')" \
                 % (GIFTS_TABLE, gift_id, url, giantid, dwarfid, letter)
    conn.execute(insert_cmd)

    # update membership table
    update_cmd = "UPDATE %s SET giftready = 'TRUE', giftid = %s WHERE userid = %s AND groupid = %s" \
    % (MEMBERSHIPS_TABLE, gift_id, dwarfid, groupid)
    conn.execute(update_cmd)

    conn.commit()
    conn.close()

def getGift(giftId):
    """
    Gets the gift info
    """
    conn = sqlite3.connect(DB_NAME)

    # get gift info
    select_cmd = "SELECT * FROM %s WHERE id = %s" % (GIFTS_TABLE, giftId)
    cursor = conn.execute(select_cmd)
    for row in cursor:
        ret = Gift(row[0], row[1], -1, row[2], row[3], row[4])

    # get group id
    select_cmd = "SELECT groupid FROM %s WHERE giftid = %s" % (MEMBERSHIPS_TABLE, giftId)
    cursor = conn.execute(select_cmd)
    for row in cursor:
        ret.groupId = row[0]

    conn.close()
    return ret

def invite(userId, groupId):
    """
    Invites a user to join a group
    """
    conn = sqlite3.connect(DB_NAME)

    # create new invitation
    insert_cmd = "INSERT INTO %s VALUES (%s, %s)" \
                 % (INVITATIONS_TABLE, userId, groupId)
    conn.execute(insert_cmd)

    conn.commit()
    conn.close()

def joinGroup(userId, groupId):
    """
    Joins a user to a group
    """
    conn = sqlite3.connect(DB_NAME)

    # create membership
    insert_cmd = "INSERT INTO %s VALUES (%s, %s, -1, 'FALSE', -1)" \
                     % (MEMBERSHIPS_TABLE, userId, groupId)
    conn.execute(insert_cmd)

    # delete invitation
    delete_cmd = "DELETE FROM %s WHERE userid = %s AND groupid = %s" \
        % (INVITATIONS_TABLE, userId, groupId)
    conn.execute(delete_cmd)

    conn.commit()
    conn.close()

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