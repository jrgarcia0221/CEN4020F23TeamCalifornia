from unittest.mock import patch
import pytest
from io import StringIO
import os
import sys
import main
import databaseInterface
from main import postJobAction, handleDeleteJob, createAccount
from jsonDB import jsonDB
import dataTypes

#Author Grant
def setupMockData():
    mockUsers = jsonDB("mockData.json")
    mockUsers.clear()

    s1 = dataTypes.createStudent("s1", "Password123!", "s", "1", "cs", "usf")
    s2 = dataTypes.createStudent("s2", "Password123!", "s", "2", "cs", "usf")
    s3 = dataTypes.createStudent("s3", "Password123!", "s", "3", "cs", "usf")
    mockUsers.add(s1)
    mockUsers.add(s2)
    mockUsers.add(s3)    

    return mockUsers

#Author Grant
def setupMockJobs():
    mockJobs = jsonDB("mockDataJobs.json")
    return mockJobs

#Author Grant
def clearMockDatabases():
    os.remove("mockData.json")
    os.remove("mockDataJobs.json")

#Author Grant
#Tests new job adds new job notification
def test_newJobPostNotification():
    users_db = setupMockData()
    jobs_db = setupMockJobs()
    currentUser = users_db.read(0)

    with patch("main.currentUser", currentUser), \
        patch("main.users_db", users_db), \
        patch("main.jobs_db", jobs_db), \
        patch("databaseInterface.usersDB", "mockData.json"), \
        patch("databaseInterface.jobsDB", "mockDataJobs.json"), \
        patch("databaseInterface.currentUser", currentUser):
        
        # Mocking input function for testing
        with patch('builtins.input', side_effect=["Test Title", "Test Description", "Test Employer", "Test Location", "Test Salary"]):
            # Call the function            
            postJobAction()

        users_db = jsonDB("mockData.json")

        assert("Test Title" in users_db.read(1)["notis"]["newJob"])
        assert("Test Title" in users_db.read(2)["notis"]["newJob"])
    clearMockDatabases()

#Author Grant
#Tests new job adds new job notification
def test_newJobPostNotification():
    users_db = setupMockData()
    jobs_db = setupMockJobs()
    currentUser = users_db.read(0)

    with patch("main.currentUser", currentUser), \
        patch("main.users_db", users_db), \
        patch("main.jobs_db", jobs_db), \
        patch("databaseInterface.usersDB", "mockData.json"), \
        patch("databaseInterface.jobsDB", "mockDataJobs.json"), \
        patch("databaseInterface.currentUser", currentUser):
        
        # Mocking input function for testing
        with patch('builtins.input', side_effect=["Test Title", "Test Description", "Test Employer", "Test Location", "Test Salary"]):
            # Call the function            
            postJobAction()

        users_db = jsonDB("mockData.json")

        assert("Test Title" in users_db.read(1)["notis"]["newJob"])
        assert("Test Title" in users_db.read(2)["notis"]["newJob"])
    clearMockDatabases()


#Author Grant
#Tests deleted job that was applied for sends notifications to user who applied
def test_deletedAppliedForJobNotification():
    users_db = setupMockData()
    jobs_db = setupMockJobs()
    currentUser = users_db.read(0)

    application = dataTypes.createJobApplication("t", "t", "str", "s2")
    job = dataTypes.createJob(title="jobTitle", postedby="s1", applications=[application])
    jobs_db.add(job)

    with patch("main.currentUser", currentUser), \
        patch("main.users_db", users_db), \
        patch("main.jobs_db", jobs_db), \
        patch("databaseInterface.usersDB", "mockData.json"), \
        patch("databaseInterface.jobsDB", "mockDataJobs.json"), \
        patch("databaseInterface.currentUser", currentUser):
        
        handleDeleteJob(job, 0)

        users_db = jsonDB("mockData.json")

        assert("jobTitle" in users_db.read(1)["notis"]["deletedJob"])       
    clearMockDatabases()

#Tests account creation adds notications
def test_createAccountNotifications():
    users_db = setupMockData()
    jobs_db = setupMockJobs()
    currentUser = users_db.read(0)

    with patch("main.currentUser", currentUser), \
        patch("main.users_db", users_db), \
        patch("main.jobs_db", jobs_db), \
        patch("databaseInterface.usersDB", "mockData.json"), \
        patch("databaseInterface.jobsDB", "mockDataJobs.json"), \
        patch("databaseInterface.currentUser", currentUser):
        
        # Mocking input function for testing
        with patch('builtins.input', side_effect=["s4", "Password123!", "s", "4", "cs", "usf", "standard"]):
            # Call the function            
            createAccount()

        users_db = jsonDB("mockData.json")
        users_db.data.remove(users_db.data[-1])

        for student in users_db.data:
            assert("s 4" in student["notis"]["newStudent"])            
    clearMockDatabases()