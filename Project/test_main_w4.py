from unittest.mock import patch
import pytest
from io import StringIO
import sys
import main
import databaseInterface
from main import main, unfriendUser, sendFriendRequest, acceptFriendRequest, rejectFriendRequest
from jsonDB import jsonDB
import dataTypes
from usefulLinks import guestSetting, toggleEmail, toggleSMS, toggleLanguages, toggleTargetedAudience
from databaseInterface import isFull, addJobPost
from csvDatabase import changeRecord
from test_main_w3 import navigation

#Author Grant
def setupMockData():
    mockUsers = jsonDB("mockData.json")
    mockUsers.clear()

    s1 = dataTypes.createStudent("s1", "Password123!", "s", "1", "cs", "usf", friendrequest=[])
    s2 = dataTypes.createStudent("s2", "Password123!", "s", "2", "cs", "usf", friendrequest=[])
    s3 = dataTypes.createStudent("s3", "Password123!", "s", "3", "cs", "usf", friendrequest=[])
    mockUsers.add(s1)
    mockUsers.add(s2)
    mockUsers.add(s3)

    currentUser = s1
    users_db = mockUsers
    matching_students = [s2,s3]

    return currentUser, users_db, matching_students

#Author Grant
def test_sendFriendRequest():
    currentUser, users_db, matching_students = setupMockData()

    with patch("main.currentUser", currentUser), \
        patch("main.users_db", users_db), \
        patch("builtins.input", side_effect=["1", "1"]):
            
        sendFriendRequest(matching_students)

        #index of first match
        index = users_db.read().index(matching_students[0])
        #assert first match has from request from current user
        assert users_db.read(index)["friendrequest"][0] == currentUser["username"]

        #index of second match
        index2 = users_db.read().index(matching_students[1])
        #assert second match has friend request from current user
        assert users_db.read(index2)["friendrequest"][0] == currentUser["username"]
        
        #assert current user does not have a friend request    
        assert len(currentUser["friendrequest"]) == 0 

#Author Grant    
def setupMockData2():
    mockUsers = jsonDB("mockData.json")
    mockUsers.clear()

    s1 = dataTypes.createStudent("s1", "Password123!", "s", "1", "cs", "usf",friends=["s2", "s3"], friendrequest=["s2"])
    s2 = dataTypes.createStudent("s2", "Password123!", "s", "2", "cs", "usf", friends=["s1"], friendrequest=[])
    s3 = dataTypes.createStudent("s3", "Password123!", "s", "3", "cs", "usf", friends=["s1"], friendrequest=[])
    mockUsers.add(s1)
    mockUsers.add(s2)
    mockUsers.add(s3)

    currentUser = s1
    users_db = mockUsers


    return currentUser, users_db

#Author Grant
def test_unfriend():
    currentUser, users_db = setupMockData2()

    #Current User is s1
    #Current User requests to remove S2
    with patch("main.currentUser", currentUser), \
        patch("main.users_db", users_db), \
        patch("builtins.input", side_effect=["1"]):
        unfriendUser()
        
        #Assert s2 is not in s1's friends list
        indexCurrentUser = users_db.read().index(currentUser)
        assert "s2" not in users_db.read(indexCurrentUser)["friends"]
        assert len(users_db.read(indexCurrentUser)["friends"]) == 1

        #Assert s1 is not in s2's friends list
        assert "s1" not in users_db.read(1)["friends"]



#Author Grant    
def setupMockData3():
    mockUsers = jsonDB("mockData.json")
    mockUsers.clear()

    s1 = dataTypes.createStudent("s1", "Password123!", "s", "1", "cs", "usf",friends=[], friendrequest=["s2"])
    s2 = dataTypes.createStudent("s2", "Password123!", "s", "2", "cs", "usf", friends=[], friendrequest=[])
    s3 = dataTypes.createStudent("s3", "Password123!", "s", "3", "cs", "usf", friends=[], friendrequest=[])
    mockUsers.add(s1)
    mockUsers.add(s2)
    mockUsers.add(s3)

    currentUser = s1
    users_db = mockUsers


    return currentUser, users_db

#Author Grant
def test_acceptFriendRequest():
    currentUser, users_db = setupMockData3()

    with patch("main.currentUser", currentUser), \
        patch("main.users_db", users_db):

        acceptFriendRequest(users_db.read(1)["username"])
        #assert s2 is in friends list of s1
        assert "s2" in users_db.read(0)["friends"]

        #assert s1 is in friends list of s2
        assert "s1" in users_db.read(1)["friends"]

        #assert friend request removed from s1
        assert len(users_db.read(0)["friendrequest"]) == 0
    

#Author Grant
def test_rejectFriendRequest():
    currentUser, users_db = setupMockData3()

    with patch("main.currentUser", currentUser), \
        patch("main.users_db", users_db):

        rejectFriendRequest(users_db.read(1)["username"])

        #assert friend request removed from s1
        assert len(users_db.read(0)["friendrequest"]) == 0

#Author Grant
def test_showNetworkOption():
    def mock_login():
        return True
    
    with patch('main.login', side_effect=mock_login):
        navigation(["2"], ["Show my Network"])
