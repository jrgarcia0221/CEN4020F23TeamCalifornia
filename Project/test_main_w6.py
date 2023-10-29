from unittest.mock import patch, MagicMock
import pytest
from io import StringIO
import sys
import main
import databaseInterface
from main import main, postJobAction


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