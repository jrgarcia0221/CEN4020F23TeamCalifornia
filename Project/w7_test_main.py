import pytest
from unittest.mock import patch
from main import buildMenuTree, createAccount
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


def test_createStudent_standardTire():
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
    
def test_createStudent_plusTire():
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