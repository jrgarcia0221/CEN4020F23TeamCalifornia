from unittest.mock import patch
import pytest
from io import StringIO
import os
from datetime import date, timedelta
import sys
import main
import databaseInterface
from main import postJobAction, handleDeleteJob, createAccount, appliedInPast7Days, applicationNotification, applicationStatusNotification, messageNotifs, profileNotification
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
    currentUser = users_db.read(0)

    with patch("main.currentUser", currentUser), \
        patch("main.users_db", users_db), \
        patch("databaseInterface.usersDB", "mockData.json"), \
        patch("databaseInterface.currentUser", currentUser):
        
        # Mocking input function for testing
        with patch('builtins.input', side_effect=["s4", "Password123!", "s", "4", "cs", "usf", "standard"]):
            # Call the function            
            createAccount()

        users_db = jsonDB("mockData.json")
        users_db.data.remove (users_db.data[-1])

        for student in users_db.data:
            assert("s 4" in student["notis"]["newStudent"])  
    os.remove("MockData.json")

def test_appliedInPast7Days():
    # Mock data setup
    users_db = setupMockData()
    mockJobs = setupMockJobs()

    # Add a recent application for the current user
    currentUser = users_db.read(0)
    recent_application_date = date.today() - timedelta(days=5)
    recent_application = {
        "applicantUsername": "s1",
        "applicationDate": [recent_application_date.year, recent_application_date.month, recent_application_date.day]
    }
    job_with_recent_application = {
        "applications": [recent_application]
    }
    mockJobs.add(job_with_recent_application)

    # Run the appliedInPast7Days function
    with patch('main.currentUser', currentUser):
        with patch('main.jobs_db', mockJobs):
            appliedInPast7Days()

    # Check if the notification is generated
    with patch('main.currentUser', currentUser):
        with patch('main.users_db', users_db):
            with patch('builtins.print') as mock_print:
                applicationNotification()
                mock_print.assert_called_with("Remember - you're going to want to have a job when you graduate. Make sure that you start to apply for jobs today!")
    
    clearMockDatabases()

def test_applicationStatusNotification(capsys):
    # Set up mock data
    users_db = setupMockData()
    jobs_db = setupMockJobs()

    # Create a user profile
    currentUser = users_db.read(0)

    # Add a new job with an application for the user
    job = {
        "title": "Software Engineer",
        "description": "Exciting software engineering position",
        "employer": "Tech Company",
        "location": "City",
        "salary": "Competitive",
        "applications": [{"applicantUsername": "s1"}]
    }
    jobs_db.add(job)

    # Set the current user to the created user
    with patch('main.currentUser', currentUser), patch('main.users_db', users_db), patch('main.jobs_db', jobs_db):
        # Call the applicationStatusNotification function
        applicationStatusNotification()

        # Capture the printed output
        captured = capsys.readouterr()

        # Check if the expected message is in the output
        assert "You have applied for 1 job(s)." in captured.out

    clearMockDatabases()

def test_messageNotifs(capsys):
    # Create a user profile
    users_db = setupMockData()
    currentUser = users_db.read(0)

    # Add a new unread message to the user's inbox
    message = {
        "fromStudent": "s2",
        "message": "Hello",
        "read": False
    }
    currentUser["messages"].append(message)

    # Set the current user to the created user
    with patch('main.currentUser', currentUser), \
            patch('main.users_db', users_db):
        # User has unread messages
        with patch('builtins.input', side_effect=["0"]):
            result = messageNotifs()
            captured = capsys.readouterr()
            assert "You have messages waiting for you." in captured.out
            assert result is True  # The function should return False as the user views the messages

        # User has no unread messages
        currentUser["messages"][0]["read"] = True
        with patch('builtins.input', side_effect=["0"]):
            result = messageNotifs()
            captured = capsys.readouterr()
            assert "You have messages waiting for you." not in captured.out
            assert result is True
    os.remove("mockData.json")

def test_profileNotification(capsys):
    users_db = setupMockData()
    currentUser = users_db.read(0)

    with patch('main.currentUser', currentUser), \
            patch('main.users_db', users_db):
        profileNotification()
        captured = capsys.readouterr()
        assert "Don't forget to create a profile." in captured.out
    os.remove("mockData.json")