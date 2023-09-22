import databaseInterface
import re
import pytest
import re

def createAccount():
    if (databaseInterface.isFull()):
        print("All permitted accounts have been created, please come back later")
        return False

    while True:
        username = input("Enter your username: ")
        #if account is unique end the loop
        if not databaseInterface.studentExists(username):
            break
        print("Username already exists.  Please try a different username.")
        
    while True:
        password = input("Enter your password: ")

        if passwordIsValid(password):
            databaseInterface.addStudentAccount(username,password)
            return True
            
        print("Password is not valid.  Password must contain one uppercase letter, one digit, one special character, and be between 8 and 12 characters.")        
    
    return False

# Function for logging in a user
def login(username, password):
    if not databaseInterface.studentExists(username):
        return False           

    if databaseInterface.login(username, password):
        return True

    return False

# Refactored main function to accept user input as arguments
def main(choice, username=None, password=None):
    # Create Database if it does not exist
    databaseInterface.createDatabase()
    print("--------------------------------")
    print("Welcome to InCollege!\n")

    # If user selects login
    if choice == '1':
        if login(username, password):
            return "Login successful"
        else:
            return "Login failed"
    elif choice == '2':            
            if (createAccount()):
                print("Account created successfully!")
            

# Pytest test case for the login functionality
def test_login_existing_account_successful():
    databaseInterface.createDatabase()
    databaseInterface.addStudentAccount("JohnDoe", "JohnDoe123")

    result = main('1', 'JohnDoe', 'JohnDoe123')

    assert result == "Login successful"


def test_login_existing_account_successful1():
    databaseInterface.addStudentAccount("AlexG", "Password123!")

    result = main('1', 'AlexG', 'Password123!')

    assert result == "Login successful"

def test_login_existing_account_successful2():
    databaseInterface.addStudentAccount('jane00', 'Doe123456&')

    result = main('1', 'jane00', 'Doe123456&')

    assert result == "Login successful"



def test_login_existing_account_successful4():
    databaseInterface.addStudentAccount('kate123', 'Martinez1#')

    result = main('1','kate123', 'Martinez1#')

    assert result == "Login successful"

def test_login_existing_account_successful5():
    databaseInterface.addStudentAccount('userName', '012345Pass%')

    result = main('1','userName', '012345Pass%')

    assert result == "Login successful"

#test case for bad password
def test_login_existing_account_unsuccessful1():

    result = main('1', 'JohnDoe', 'JohnDoe123!')

    assert result == "Login failed"



#Test case for second wrong password
def test_login_existing_account_unsuccessful2():

    result = main('1', 'AlexG', 'Password!')

    assert result == "Login failed"

#Test case for wrong username
def test_login_existing_account_unsuccessful3():

    result = main('1', 'jane01', 'Doe123456&')

    assert result == "Login failed"

#Test case for second wrong username
def test_login_existing_account_unsuccessful4():

    result = main('1', 'kate', 'Martinez1#')

    assert result == "Login failed"

#Test case for both username and pasword being wrong
def test_login_existing_account_unsuccessful5():

    result = main('1', 'Name', '1234Pass%')

    assert result == "Login failed"

#the function returns true when there is a 6th account, just need one case
def test_unsuccessful_6th_account():
    #result = main('2')
    result = databaseInterface.isFull()
    assert result == True

def passwordIsValid(password):
    #Password must be between 8 and 12 characters
    if not 8 <= len(password) <= 12:
        return False
    
    #Password must contain at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False

    #Password must contain at least one digit
    if not re.search(r'\d', password):
        return False

    #Password must contain at least one special character
    if not re.search(r'[!@#$%^&*()_+{}|:"<>?~]', password):
        return False

    #Password is valid
    return True


def test_passwordIsValid1():
    output = passwordIsValid("Ee0022")
    assert output == False

def test_passwordIsValid2():
    output = passwordIsValid("0000000")
    assert output == False

def test_passwordIsValid3():
    output = passwordIsValid("passWo101010")
    assert output == False

def test_passwordIsValid4():
    output = passwordIsValid("wWwWWWWWWWWWWWWWW")
    assert output == False

def test_passwordIsValid5():
    output = passwordIsValid("helloA01!")
    assert output == True

def test_passwordIsValid6():
    output = passwordIsValid("0000000A!")
    assert output == True

def test_passwordIsValid7():
    output = passwordIsValid("AAAAAAAAAa2#")
    assert output == True

def test_passwordIsValid8():
    output = passwordIsValid("Password123!")
    assert output == True

if __name__ == "__main__":
    main()