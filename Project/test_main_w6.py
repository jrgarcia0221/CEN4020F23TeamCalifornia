import pytest
from unittest.mock import patch, Mock
from jsonDB import jsonDB
import json
import databaseInterface
from databaseInterface import addStudentAccount, studentNameExists, getPassword, login, addGuestSettings, getCurrentUser, lookForGuestSetting, addJobPost, readJobPosts, displayJobs
from dataTypes import createExperience, createEducation, createAboutMe, createProfile
from main import capitalizeFirstLetter, buildMenuTree, main, watchVideo, studentLookup, createAccount, passwordIsValid, postJobAction, sendFriendRequest, selectJobAction, handleSaveJob
import sys
from io import StringIO
import main
import dataTypes


def test_post_job_full(capsys):

  def mock_is_full(job):
    return True

  with patch('databaseInterface.isFull', mock_is_full):
    # Since the database is full, the function should return False
    assert postJobAction() == False
  # Capture the output
  out, err = capsys.readouterr()
  assert "All permitted job postings have been created, please come back later" in out


def test_unsuccessful_11th_jobposting():
    for i in range(10):
        databaseInterface.currentUser = {
        'firstname': 's'+str(i+1),
        'lastname': 'l'+str(i+1),
        'username': 'sl'+str(i+1)
        }
        databaseInterface.addJobPost('t'+str(i+1), 'desc'+str(i+1), 'e'+str(i+1), 'location', str(i+1))
    result = databaseInterface.isFull('job')

    
    assert result == True



def setupMockData():
    mockUsers = jsonDB("mockData.json")
    mockJobs = jsonDB("mockJobs.json")
    mockUsers.clear()
    mockJobs.clear()

    s1 = dataTypes.createStudent("s1", "Password123!", "s", "1", "cs", "usf", friendrequest=[])
    s2 = dataTypes.createStudent("s2", "Password123!", "s", "2", "cs", "usf", friendrequest=[])
    s3 = dataTypes.createStudent("s3", "Password123!", "s", "3", "cs", "usf", friendrequest=[])
    mockUsers.add(s1)
    mockUsers.add(s2)
    mockUsers.add(s3)

    job = dataTypes.createJob('research intern', 'good internship', 'alex garcia', 'orlando', '20.00 hr', 's', '2','s2')
    mockJobs.add(job)
    
    currentUser = s1
    users_db = mockUsers
    jobs_db = mockJobs

    return currentUser, users_db, jobs_db

def test_saveJob():
  currentUser, users_db, jobs_db = setupMockData()
  with patch("main.currentUser", currentUser), \
        patch("main.users_db", users_db), \
        patch("main.jobs_db", jobs_db),\
        patch("builtins.input", side_effect=[]):
    
        handleSaveJob(jobs_db.read(0), 0)

        assert "s1" in jobs_db.read(0)["savedby"]
        assert "s2" not in jobs_db.read(0)["savedby"]

def test_selectJob():
  currentUser, users_db, jobs_db = setupMockData()
  selectedJob = jobs_db.read(0)
  expected_output = f"Selected job: {selectedJob['title']} {selectedJob['description']} {selectedJob['employer']} {selectedJob['location']} {selectedJob['salary']}\n"
  expected_output += "Enter save to save job for later\n" 
  expected_output += "Enter apply to apply to job\n"
  # expected_output += ""
  with patch("main.currentUser", currentUser), \
        patch("main.users_db", users_db), \
        patch("main.jobs_db", jobs_db),\
        patch("builtins.input", side_effect=[1]):
    
        selectJobAction()

        out, err = capfd.readouterr()
        assert out.strip() == expected_output.strip()
        
