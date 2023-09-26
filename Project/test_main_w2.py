from unittest.mock import patch, MagicMock
import pytest
from io import StringIO
import sys
import main
import databaseInterface
from main import main, login, watchVideo, studentLookup, createAccount, passwordIsValid, postJobAction
from databaseInterface import isFull, addJobPost



def test_watch_video(capfd):
  expected_output = "Video is now playing\n"
  watchVideo()
  out, err = capfd.readouterr()
  assert out == expected_output

def test_post_job():

  def mock_is_full(job):
    return False

  def mock_add_job_post(title, desc, employer, location, salary):
    return True

  with patch('databaseInterface.isFull', mock_is_full):
    with patch('databaseInterface.addJobPost', mock_add_job_post):
      # Simulate user input for job posting
      with patch('builtins.input',
                 side_effect=[
                     'Analyst', 'Analyze data', 'InCollege', 'CA', '1000/hr'
                 ]):
        assert postJobAction() == True


def test_post_job_full(capsys):

  def mock_is_full(job):
    return True

  with patch('databaseInterface.isFull', mock_is_full):
    # Since the database is full, the function should return False
    assert postJobAction() == False
  # Capture the output
  out, err = capsys.readouterr()
  assert "All permitted job postings have been created, please come back later" in out


# Fixture to simulate that a student exists in the database
@pytest.fixture
def student_exists_in_database(monkeypatch):

  def mock_student_exists_in_database(first, last):
    return True

  monkeypatch.setattr(databaseInterface, "studentNameExists",
                      mock_student_exists_in_database)


# Fixture to simulate that a student does not exists in the database
@pytest.fixture
def student_not_in_database(monkeypatch):

  def mock_student_not_in_database(first, last):
    return False

  monkeypatch.setattr(databaseInterface, "studentNameExists",
                      mock_student_not_in_database)


def test_studentLookup_found(student_exists_in_database, capfd):
  expected_output = "They are part of the InCollege system"
  with patch('builtins.input', side_effect=["John", "Doe"]):
    studentLookup()
  out, err = capfd.readouterr()
  assert out.strip() == expected_output.strip()


def test_studentLookup_not_found(student_not_in_database, capfd):
  expected_output = "They are not part of the inCollege system"
  with patch('builtins.input', side_effect=["Jane", "Smith"]):
    studentLookup()
  out, err = capfd.readouterr()
  assert out.strip() == expected_output.strip()


# Fixture to simulate a database interface with mock methods
@pytest.fixture
def mock_database_interface(monkeypatch):
  mock_db = MagicMock()

  def mock_is_empty(table_name):
    if table_name == "user":
      return False  # Assuming there are accounts in the database
    return True  # For other tables, assume they are empty

  def mock_student_exists(username):
    return True  # Assuming the user exists

  def mock_login(username, password):
    if username == "JohnDoe" and password == "JohnDoe123":
      return True  # Valid login
    return False  # For other cases, assume invalid login

  def mock_get_current_user(username):
    return "JohnDoe"  # Mock the logged-in user

  mock_db.isEmpty.side_effect = mock_is_empty
  mock_db.studentExists.side_effect = mock_student_exists
  mock_db.login.side_effect = mock_login
  mock_db.getCurrentUser.side_effect = mock_get_current_user

  monkeypatch.setattr(databaseInterface, "isEmpty", mock_db.isEmpty)
  monkeypatch.setattr(databaseInterface, "studentExists",
                      mock_db.studentExists)
  monkeypatch.setattr(databaseInterface, "login", mock_db.login)
  monkeypatch.setattr(databaseInterface, "getCurrentUser",
                      mock_db.getCurrentUser)

  return mock_db


# Test case for valid credentials
def test_login_valid_credentials(mock_database_interface, capfd):
  with patch('builtins.input', side_effect=["JohnDoe", "JohnDoe123"]):
    result = login()
  out, err = capfd.readouterr()

  assert result is True  # Check if login is successful
  assert "Login successful!" in out  # Check for the success message in the output


# Test case for invalid password
def test_login_invalid_password(mock_database_interface, capfd):
  # Assuming the username exists but the password is incorrect
  with patch('builtins.input',
             side_effect=["JohnDoe", "Password123!", "JohnDoe", "JohnDoe123"]):
    result = login()
  out, err = capfd.readouterr()

  assert result is True  # Check if login is successful after entering valid credentials
  assert "Invalid Password. Please try again." in out  # Check for the invalid password message in the output


# Test case for creating a valid account
def test_createAccount_valid_account(mock_database_interface, capfd):
  addStudentAcc = MagicMock()
  # Simulate a valid account creation process
  with patch('builtins.input',
             side_effect=["AlexJon", "Password123!", "Alex", "Jon"]):
    with patch('databaseInterface.isFull',
               return_value=False):  # Mock the database not being full
      with patch(
          'databaseInterface.studentExists',
          return_value=False):  
        with patch('databaseInterface.addStudentAccount', addStudentAcc):
          result = createAccount()
  out, err = capfd.readouterr()

  assert result is True 

def test_createAccount_full(capsys):
  def mock_is_full(database):
    return True if database == 'user' else False
  
  expected_output = "All permitted accounts have been created, please come back later\n"

  with patch('databaseInterface.isFull', mock_is_full):
   with patch('builtins.input', side_effect=['test_user', 'Test123!', 'Test', 'User']):
    assert createAccount() == False

  out, err = capsys.readouterr()
  assert expected_output == out

def test_passwordIsValid_fail():
  password_list = [
      'johndoe123!'  # messing capitalized character
      'JohnDoe!'  # messing digits
      'JohnDoe123'  # messing special characters
      'John1!'  #less than 8
      'JohnDoejack123%'  #more than 12
  ]
  for i in password_list:
    password = passwordIsValid(i)
    assert password is False


def test_passwordIsValid_succes():
  password = 'JohnDoe123!'
  value = passwordIsValid(password)
  assert value is True

