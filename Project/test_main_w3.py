from unittest.mock import patch
import pytest
from io import StringIO
import sys
import main
import databaseInterface
from main import main, buildMenuTree, login, watchVideo, studentLookup, createAccount, passwordIsValid, postJobAction
from usefulLinks import guestSetting, toggleEmail, toggleSMS, toggleLanguages, toggleTargetedAudience
from databaseInterface import isFull, addJobPost
from csvDatabase import changeRecord

guestSetting.append("name")
guestSetting.append("On")
guestSetting.append("On")
guestSetting.append("On")
guestSetting.append("Spanish")

#Used to test navigation of menu
#Author Grant
#expected labels are labels that the menu should output
#userInputs are the keys a user enters to get to a menu
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


#Author Grant
def toggle(colNum, toggleValue, func):
    def mock_change_record(filename, col, lookupvalue, toggle):
        assert filename == "guestSettings.csv"
        assert col == colNum
        assert lookupvalue == "name"
        assert toggle == toggleValue
    
    # Patch the csvDatabase.changeRecord method with the mock
    with patch('csvDatabase.changeRecord', mock_change_record):
        result = func()
    
    #Assert that the result is True
    assert result is True

#Author Grant
def test_toggleEmail():
    toggle(1, "Off", toggleEmail)

#Author Grant
def test_toggleSMS():
    toggle(2, "Off", toggleSMS)

#Author Grant
def test_toggleTargetedAudience():
    toggle(3, "Off", toggleTargetedAudience)

#Author Grant
def test_toggleLanguages():
    toggle(4, "English", toggleLanguages)

#Author Grant
def test_usefulLinks():
    navigation(["6"], ["Useful Links", "General", "Browse InCollege", "Business Solutions", "Directories"])

#Author Grant
def test_usefulLinks_general():
    navigation(["6", "1"], ["Useful Links", "General", "Sign Up", "Help Center", "About", "Press", "Blog", "Careers", "Developers"])

#Author Grant
def test_login_usefulLinks():
    def mock_login():
        return True    
    with patch('main.login', side_effect=mock_login):
        navigation(["2", "4"], ["Useful Links", "General", "Browse InCollege", "Business Solutions", "Directories"])

#Author Grant
def test_login_importantLinks():
    def mock_login():
        return True
    
    with patch('main.login', side_effect=mock_login):
        navigation(["2", "5"], ["InCollege Important Links", "Copyright Notice", "About", "Accessibility", "User Agreement", "Privacy Policy", "Cookie Policy", "Copyright Policy", "Brand Policy", "Languages"])

#Author Grant
def test_login_importantLinks_guestControls():
    def mock_login():
        return True
    
    with patch('main.login', side_effect=mock_login):
        navigation(["2", "5", "5"], ["InCollege Important Links", "Copyright Notice", "About", "Accessibility", "User Agreement", "Privacy Policy", "Cookie Policy", "Copyright Policy", "Brand Policy", "Languages", "Guest Controls"])