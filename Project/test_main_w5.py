import pytest
from unittest.mock import patch
from jsonDB import jsonDB
import json
import databaseInterface
from databaseInterface import addStudentAccount, studentNameExists, getPassword, login, addGuestSettings, getCurrentUser, lookForGuestSetting, addJobPost, readJobPosts, displayJobs
from dataTypes import createExperience, createEducation, createAboutMe, createProfile
from main import capitalizeFirstLetter, buildMenuTree, main, watchVideo, studentLookup, createAccount, passwordIsValid, postJobAction, sendFriendRequest
import sys
from io import StringIO
import main

# test new functions in dataTypes
experienceOutput = createExperience('Analyst', 'InCollege', 'June 6, 2020', 'May 12, 2023', 'CA', 'Analyze data')
educationOutput = createEducation('USF', 'BSCS', '2018-2022')
aboutMeOutput = createAboutMe("I am an Analyst...", experienceOutput, educationOutput)

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

def test_createExperience():
  expected_output = {'title': 'Analyst', 'employer': 'InCollege', 'dateStarted': 'June 6, 2020', 'dateEnded': 'May 12, 2023', 'location': 'CA', 'description': 'Analyze data'}
  assert expected_output == experienceOutput

def test_createEducation():
  expected_output = {'school': 'USF', 'degree': 'BSCS', 'yearsAttended': '2018-2022'}
  assert expected_output == educationOutput

def test_createAboutMe():
  expected_output = {'paragraph': 'I am an Analyst...', 'experience': {'title': 'Analyst', 'employer': 'InCollege', 'dateStarted': 'June 6, 2020', 'dateEnded': 'May 12, 2023', 'location': 'CA', 'description': 'Analyze data'}, 'education': {'school': 'USF', 'degree': 'BSCS', 'yearsAttended': '2018-2022'}}
  assert expected_output == aboutMeOutput

def test_createProfile():
  expected_output = {'title': 'Analyst', 'major': 'CSE', 'university': 'USF', 'aboutMe': {'paragraph': 'I am an Analyst...', 'experience': {'title': 'Analyst', 'employer': 'InCollege', 'dateStarted': 'June 6, 2020', 'dateEnded': 'May 12, 2023', 'location': 'CA', 'description': 'Analyze data'}, 'education': {'school': 'USF', 'degree': 'BSCS', 'yearsAttended': '2018-2022'}}}
  output = createProfile('Analyst', 'CSE', 'USF', aboutMeOutput)
  assert expected_output == output


def test_capitalizeFirstLetter():
  expected_output = "Computer Science"
  output = capitalizeFirstLetter("compuTER sCIENCE")
  assert expected_output == output

def test_capitalizeFirstLetter1():
  expected_output = "Computer Engineering"
  output = capitalizeFirstLetter("comPuTer ENGINEERING")
  assert expected_output == output

def test_capitalizeFirstLetterOfUniversity():
  expected_output = "University Of South Florida"
  output = capitalizeFirstLetter("university of south florida")
  assert expected_output == output

def test_capitalizeFirstLetterOfUniversity2():
  expected_output = "Hillsborough Community College"
  output = capitalizeFirstLetter("hiLlsboroUGH coMMunity CoLLEGE")
  assert expected_output == output

def test_showMyProfileOption():
    def mock_login():
      return True
    
    with patch('main.login', side_effect=mock_login):
      navigation(["2"], ["My Profile"])

def test_showOptionsInProfile():
    def mock_login():
      return True
    
    with patch('main.login', side_effect=mock_login):
      navigation(["2", "7"], ["Create/Manage Profile", "View Profile"])

def test_viewProfileViewOption():
    def mock_login():
      return True
    
    with patch('main.login', side_effect=mock_login):
      navigation(["2", "7", "2"], ["View My Profile", "Look up a Friend's Profile"])


def readDB(db):
  with open(db) as f:
    data = json.load(f)
    return data

users = jsonDB("users.json")

def test_addStudentAccount():
  users.clear()
  expected_output = [True, False]
  output = [addStudentAccount('s1', "Password123!", "s", "1", "cs", "usf"),
            addStudentAccount('s1', "Password123!", "s", "1", "cs", "usf")]

  expected = [{'username': 's1', 'password': 'Password123!', 'firstname': 's', 'lastname': '1', 'major': 'cs', 'university': 'usf', 'settings': {'email': 'On', 'sms': 'On', 'targetedAdvert': 'On', 'language': 'English'}, 'friendrequest': [], 'friends': [], 'profile': {}}]
  result = readDB("users.json")
  assert output == expected_output
  assert expected == result

# test is student name exists
def test_studentNameExists():
  expected_output = [True, False]
  # name exists due to previous test
  output = [studentNameExists('s', '1'), studentNameExists('s', '2')]
  assert output == expected_output

def test_getPassword():
  expected_output = ["Password123!", None]
  output = [getPassword('s1'), getPassword('s2')]
  assert expected_output == output

def test_login():
  expected_output = [True, False]
  output = [login('s1', 'Password123!'), login('s1', '"Password124!')]
  assert output == expected_output

guestSettings = "guestSettings.json"
def test_addGuestSettings():
  jsonDB(guestSettings).clear()
  addGuestSettings('s1')
  result = readDB(guestSettings)
  expected = [{'email': 'On', 'sms': 'On', 'targetedAdvert': 'On', 'language': 'English', 'username': 's1'}]
  assert result == expected

current = {}
def test_getCurrentUser(capfd):
  expected_output = "User 's2' not found in the database.\n"
  expected = {'username': 's1', 'password': 'Password123!', 'firstname': 's', 'lastname': '1', 'major': 'cs', 'university': 'usf', 'settings': {'email': 'On', 'sms': 'On', 'targetedAdvert': 'On', 'language': 'English'}, 'friendrequest': [], 'friends': [], 'profile': {}}
  getCurrentUser('s1')
  assert databaseInterface.currentUser == expected

  getCurrentUser('s2')
  out, err = capfd.readouterr()
  assert out.strip() == expected_output.strip()


def test_lookForGuestSetting():
  expected_output = {'email': 'On', 'sms': 'On', 'targetedAdvert': 'On', 'language': 'English', 'username': 's1'}
  output = lookForGuestSetting()
  assert expected_output == output

jobs = "jobs.json"
def test_addJobPost():
  jsonDB(jobs).clear()
  expected_ouput = True
  output = addJobPost('Analyst', 'Analyze data', 'InCollege', 'CA', '1000/hr')
  assert expected_ouput == output

  expected_result = [{"title": "Analyst", "description": "Analyze data", "employer": "InCollege",
        "location": "CA", "salary": "1000/hr", "firstname": "s", "lastname": "1"}]
  result = readDB(jobs)
  assert expected_result == result

def test_readJobPosts(capfd):
  expected_output = "---------------------------------------------\n"
  expected_output += "title: Analyst\n"
  expected_output += "description: Analyze data\n"
  expected_output += "employer: InCollege\n"
  expected_output += "location: CA\n"
  expected_output += "salary: 1000/hr\n"
  expected_output += "firstname: s\n"
  expected_output += "lastname: 1\n\n"

  readJobPosts()

  out, err = capfd.readouterr()
  assert out.strip() == expected_output.strip()

