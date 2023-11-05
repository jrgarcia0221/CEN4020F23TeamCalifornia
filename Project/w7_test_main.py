import pytest
import sys
import io
from io import StringIO
from unittest.mock import patch
from main import buildMenuTree, createAccount, sendMessage, jsonDB, messageNotifs, viewMessagesInterface
from dataTypes import createStudent, createSetting


def navigation(userInputs, expectedLabels):
    # Keeps track of all console outputs
    consoleOutput = []
    
    with patch('builtins.input', side_effect=userInputs):
        with patch('builtins.print', side_effect=lambda *args, **kwargs: consoleOutput.append(" ".join(map(str, args)))):
            
            try: 
                buildMenuTree()
            except StopIteration:
                pass
    for expectedLabel in expectedLabels:
        assert any(expectedLabel in output for output in consoleOutput)

def test_showMessagesOption():
    def mock_login():
      return True
    
    with patch('main.login', side_effect=mock_login):
      navigation(["2"], ["Messages"])
      
      

standard_output = createStudent("JohnDoe", "Password123!", "John", "Doe", "CS", "USF", {}, [], [], {}, [],"standard", [])
plus_output = createStudent("JohnDoe", "Password123!", "John", "Doe", "CS", "USF", None, None, None, None, None,"plus", None)


def test_createStudent_standardTier():
    expected_output = {
        "username": "JohnDoe",
        "password": "Password123!",
        "firstname": "John",
        "lastname": "Doe",
        "major": "CS",
        "university": "USF",
        "settings": createSetting(),
        "friendrequest": [],
        "friends": [],
        "profile": {},
        "notifications": [],
        "tier": "standard",
        "messages": []
    }
    assert expected_output == standard_output
    
def test_createStudent_plusTier():
    expected_output = {
        "username": "JohnDoe",
        "password": "Password123!",
        "firstname": "John",
        "lastname": "Doe",
        "major": "CS",
        "university": "USF",
        "settings": createSetting(),
        "friendrequest": [],
        "friends": [],
        "profile": {},
        "notifications": [],
        "tier": "plus",
        "messages": []
    }
    assert expected_output == plus_output

def test_standardMessaging(capsys):
    # Create a standard user and another user
    user1 = createStudent("User1", "Password123!", "User", "One", "CS", "University1", "standard")
    user2 = createStudent("User2", "Password123!", "User", "Two", "CS", "University2", "standard")

    # Add the user profiles to the users_db
    users_db = jsonDB('users.json')
    users_db.add(user1)
    users_db.add(user2)

    # Add user2 to user1's friends list
    user1["friends"].append("User2")
    user2["friends"].append("User1")
    # User1 sends a message to user2 (a friend)
    with patch('main.currentUser', user1):
        message_content = "Hello User2!"
        sendMessage("User1", "User2", message_content)
        assert "Your message has been sent" in capsys.readouterr().out

  # User2 attempts to send a message to user1 (a friend)
    with patch('main.currentUser', user2):
        message_content = "Hello User1!"
        sendMessage("User2", "User1", message_content)
        assert "Your message has been sent" in capsys.readouterr().out


def test_messageNotifs(capsys):
    # Create a user profile
    user = createStudent("User1", "Password123!", "John", "Doe", "CS", "University1", "standard")
    users_db = jsonDB('users.json')
    users_db.add(user)
    # Add a new message to the user's inbox
    message = {
        "fromStudent": "Sender",
        "message": "Hello",
        "read": False
    }
    user["messages"].append(message)

    # Set the current user to the created user
    with patch('main.currentUser', user):
        with patch('builtins.input', side_effect=["0"]):
            result = messageNotifs()
            assert result == True

    user["messages"] = [] 
    with patch('main.currentUser', user):
        messageNotifs()
        captured = capsys.readouterr()
        assert "You have no messages." in captured.out


# def test_readMessageOptions(capsys):
#     # Create a user profile
#     user = createStudent("User1", "Password123!", "John", "Doe", "CS", "University1", "standard")
#     users_db = jsonDB('users.json')
#     users_db.add(user)

#     # Add a new message to the user's inbox
#     message = {
#         "fromStudent": "Sender",
#         "message": "Hello",
#         "read": False
#     }
#     user["messages"].append(message)
#     # Set the current user to the created user
#     with patch('main.currentUser', user):
#         # User selects to reply to the message
#         with patch('builtins.input', side_effect=["1", "1", "reply", "hi"]):
#             viewMessagesInterface()
#             captured = capsys.readouterr()
#             assert "Your message has been sent" in captured.out

#         # User selects to delete the message
#         user["messages"] = []  # Clear messages for the next part of the test
#         with patch('builtins.input', side_effect=["del"]):
#             viewMessagesInterface()
#             captured = capsys.readouterr()
#             assert "No Messages" in captured.out

def test_plusMessaging(capsys):
    users_db = jsonDB('users.json')
    users_db.add(plus_output)
    users_db.add(standard_output)

    def mock_login():
      return True
    
    with patch('main.currentUser', plus_output):
        with patch('main.login', side_effect=mock_login):
            navigation(["2", "1", "1", "test"], ["Messages", "Message any Student"])



