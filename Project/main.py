import databaseInterface
import menuSystem
import usefulLinks
import re
import sys


#Returns true if password is valid
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


#Handles user create account
#Checks if database is full (capacity is 5)
#User enters username - checks if student is unqiue
#User enters password - checks if password is valid
#User enters first and last name
#Creates account in database
#Returns true if successful login
def createAccount():
  if (databaseInterface.isFull("user")):
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
      break

    print(
        "Password is not valid.  Password must contain one uppercase letter, one digit, one special character, and be between 8 and 12 characters."
    )

  first = input("Enter your first name: ")
  last = input("Enter your last name: ")
  databaseInterface.addStudentAccount(username, password, first, last)
  return True

loggedIn = False
#Handles user login
#No existing accounts - returns to main menu
#User enters username - checks if student exists in database
#User enters password - checks if password is matched
#returns true if successful login
def login():
  print("--------------------------------")

  if databaseInterface.isEmpty("user"):
    print("There are no existing accounts to log into.")
    return False

  while True:
    username = input("Enter your username: ")
    if databaseInterface.studentExists(username):
      break
    else:
      print("Invalid Username. Please try again.")

  while True:
    password = input("Enter your password: ")
    if databaseInterface.login(username, password):
      break
    else:
      print("Invalid Password. Please try again.")

  # save logged in user
  databaseInterface.getCurrentUser(username)


  print("Login successful!")
  return True


def learnSkill():
  print("--------------------------------")
  print("Under construction")
  return True


def jobSearchAction():
  print("Performing job search...")
  print("--------------------------------")
  databaseInterface.displayJobs(postedJobs)
  return True


def postJobAction():
  print("--------------------------------")
  if (databaseInterface.isFull("job")):
    print(
        "All permitted job postings have been created, please come back later")
    return False

  print("Fill out the following entries: ")
  title = input("Title: ")
  desc = input("Description: ")
  employer = input("Employer: ")
  location = input("Location: ")
  salary = input("Salary: ")

  databaseInterface.addJobPost(title, desc, employer, location, salary)
  return True


def watchVideo():
  print("Video is now playing")
  return True


def studentLookup():
  first = input("Enter first name of student to lookup: ")
  last = input("Enter last name of student to lookup: ")

  if databaseInterface.studentNameExists(first, last):
    print("They are part of the InCollege system")
  else:
    print("They are not part of the inCollege system")
  return True


# actions for important links
def copyrightNotice():
  return True

def about():
  return True

def accessibility():
  return True

def userAgreement():
  return True

def privacyPolicy():
  return True

def cookiePolicy():
  return True

def copyrightPolicy():
  return True

def brandPolicy():
  return True

def guestControls():
  return True

def languages():
  return True






importantLinks = menuSystem.menuNode(
    "InCollege Important Links",
    goBack=True,
    children=[
        menuSystem.menuNode("Copyright Notice",
                            goBack=True,
                            action=copyrightNotice),
        menuSystem.menuNode("About",
                            goBack=True,
                            action=about),
        menuSystem.menuNode("Accessibility",
                            goBack=True,
                            action=accessibility),
        menuSystem.menuNode("User Agreement",
                            goBack=True,
                            action=userAgreement),
        menuSystem.menuNode("Privacy Policy",
                            goBack=True,
                            action=privacyPolicy),
        menuSystem.menuNode("Cookie Policy",
                            goBack=True,
                            action=cookiePolicy),
        menuSystem.menuNode("Copyright Policy",
                            goBack=True,
                            action=copyrightPolicy),
        menuSystem.menuNode("Brand Policy",
                            goBack=True,
                            action=brandPolicy),
        menuSystem.menuNode("Guest Controls",
                            goBack=True,
                            action=guestControls),
        menuSystem.menuNode("Languages",
                            goBack=True,
                            action=languages),
])

#Build menu here
#menuNode parameters:
#label - the name of the choice - do not include number of choice
#action=None - function that gets called when menu choice is selected
#children=None - any sub menu this menu will have
#goBack=False - If you want it to have a go back option
def buildMenu():
  root = menuSystem.menuNode(
      "Main Menu",
      children=[
          menuSystem.menuNode("Create an account", action=createAccount),
          menuSystem.menuNode(
              "Login",
              goBack=True,
              action=login,
              children=[
                  menuSystem.menuNode("Find Someone you know",
                                      goBack=True,
                                      action=studentLookup),
                  menuSystem.menuNode("Job search / internship",
                                      goBack=True,
                                      action=jobSearchAction,
                                      children=[
                                          menuSystem.menuNode(
                                              "Post a job",
                                              goBack=True,
                                              action=postJobAction)
                                      ]),
                  menuSystem.menuNode(
                      "Learn a skill",
                      goBack=True,
                      children=[
                          menuSystem.menuNode("Public Speaking",
                                              goBack=True,
                                              action=learnSkill),
                          menuSystem.menuNode("Python",
                                              goBack=True,
                                              action=learnSkill),
                          menuSystem.menuNode("JavaScript",
                                              goBack=True,
                                              action=learnSkill),
                          menuSystem.menuNode("Statistics",
                                              goBack=True,
                                              action=learnSkill),
                          menuSystem.menuNode("Cooking",
                                              goBack=True,
                                              action=learnSkill)
                      ]),
                  usefulLinks.usefulLinksMenu(1),
                  importantLinks
              ]),
          menuSystem.menuNode("Student Lookup",
                              goBack=True,
                              action=studentLookup),
          menuSystem.menuNode("Look for inCollege Friends", goBack=True),
          menuSystem.menuNode("Watch video on why you should join InCollege!",
                              action=watchVideo,
                              goBack=True),
          usefulLinks.usefulLinksMenu(0),
          importantLinks,
          menuSystem.menuNode("Exit", action=lambda: sys.exit(0), goBack=True)
      ])
  return root


#Creates all databases (users, job postings)
def createDatabases():
  databaseInterface.createDatabase()
  databaseInterface.createJobPostingDatabase()

# build main menu tree
def buildMenuTree():
  menuTree = buildMenu()

  while True:
    menuSystem.navigateMenu(menuTree, [])

def main():
  createDatabases()

  #Success Story
  print("Student Success Story: InCollege")

  successStory = "Meet Sarah, a determined college student majoring in Computer Science."
  successStory += " She found inCollege, a platform just for college students, and made an impressive profile."
  successStory += " She connected with peers who shared her interests."
  successStory += " Using inCollege, she got a job at a big tech company and learned a lot from other students she met on the platform."

  print(successStory)

  # Read job postings now so new postings won't be read until next start up
  global postedJobs
  postedJobs = databaseInterface.readJobPosts()

  # build menu tree
  buildMenuTree()


if __name__ == '__main__':
  main()
