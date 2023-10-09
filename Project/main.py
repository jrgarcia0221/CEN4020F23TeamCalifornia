import databaseInterface
import menuSystem
import usefulLinks
import re
import sys
import jsonDB
import dataTypes

currentUser = None
users_db = jsonDB.jsonDB("users.json")

#Author Grant DeBiase
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

#Author Grant DeBiase
#Creates 3 test accounts for testing purposes
def create3TestAccounts():
   for i in range(3):
      username = "g" + str(i)
      first = "g"
      last = str(i)
      major = "cs"
      uni = "usf"
      password = "Password123!"

      databaseInterface.addGuestSettings(username)
      databaseInterface.addStudentAccount(username, password, first, last, major, uni)
      #json 
      new_user = dataTypes.createStudent(username, password, first, last, major, uni)
      users_db.add(new_user)

#Author Grant DeBiase
# andles user create account
#Checks if database is full (capacity is 5)
#User enters username - checks if student is unique
#User enters password - checks if password is valid
#User enters first and last name
#Creates account in database
#Returns true if successful login
def createAccount():
  #Uncomment this to automatically create 3 test accounts
  # create3TestAccounts()  
  # return                

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
  major = input("Enter your major: ")
  uni = input("Enter your university: ")
  databaseInterface.addGuestSettings(username)
  databaseInterface.addStudentAccount(username, password, first, last, major, uni)
  #json 
  new_user = dataTypes.createStudent(username, password, first, last, major, uni)
  users_db.add(new_user)

  return True

#Author Grant DeBiase
# Handles user login
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

  global guestSettingArr
  guestSettingArr = databaseInterface.lookForGuestSetting()

  usefulLinks.initializeGuestArray(guestSettingArr)

   
  conditions = []
  conditions.append(jsonDB.jsonDB.createQueryCondition("username", username ))
  #returns the user
  global currentUser
  currentUser = users_db.query(conditions)[0] 



  print("Login successful!")

  
  friendRequest() 

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

def studentLookupLog():
  print("Choose the option you would like to find someone you know.")
  return True




def LastNameLookup():
    last = input("Enter the last name of student to lookup: ")
    matching_students = []

    for user in users_db.read():
        if user["lastname"].lower() == last.lower() and (user["username"] != currentUser["username"]) and (user["username"] not in currentUser["friends"]):
            matching_students.append(user)

    if not matching_students:
        print("No students found with the specified last name.")
        return False

    print("Students found:")
    print("No.\tUsername\tFirstname\tLast Name")
    for index, student in enumerate(matching_students, start=1):
          print(f"{index}\t{student['username']:<10}\t{student['firstname']:<10}\t{student['lastname']}")


    sendFriendRequest(matching_students)  
    return False
  
def universityLookup():
      uni = input("Enter the university of student to lookup: ")
      matching_students = []

      for user in users_db.read():
        if user["university"].lower() == uni.lower() and (user["username"] != currentUser["username"]) and (user["username"] not in currentUser["friends"]):
              matching_students.append(user)

      if not matching_students:
          print("No students found with the specified university.")
          return False

      print("Students found:")
      print("No.\tUsername\tFirstname\tUniversity")
      for index, student in enumerate(matching_students, start=1):
            print(f"{index}\t{student['username']:<10}\t{student['firstname']:<10}\t{student['university']}")

      sendFriendRequest(matching_students)  

      return True

def majorLookup():
    major = input("Enter the major of student to lookup: ")
    matching_students = []

    for user in users_db.read():
        if user["major"].lower() == major.lower() and (user["username"] != currentUser["username"]) and (user["username"] not in currentUser["friends"]):
            matching_students.append(user)

    if not matching_students:
        print("No students found with the specified major.")
        return False

    print("Students found:")
    print("No.\tUsername\tFirstname\tMajor")
    for index, student in enumerate(matching_students, start=1):
          print(f"{index}\t{student['username']:<10}\t{student['firstname']:<10}\t{student['major']}")


    sendFriendRequest(matching_students)  
    return True


def sendFriendRequest(matching_students):
    for student in matching_students:
        if currentUser["username"] not in student["friendrequest"]:
            print(f"Send a friend request to {student['username']}?")
            print("Select\n(1) Yes\n(2) No")
            choice = input("Enter your choice (1-2): ")

            if choice == "1":
                student["friendrequest"].append(currentUser["username"])
                print(f"Friend request sent to {student['username']}.")
            else:
                print(f"No friend request sent to {student['username']}.")

            index = users_db.data.index(student)
            users_db.update(index, student)


            



def acceptFriendRequest(friend):
    print(f"Accepting friend request from {friend}.")
    # Update sender's friend list
    for user in users_db.data:
        if user["username"] == friend:
            user["friends"].append(currentUser["username"])
            break
    
    # Update current user's friend and friend request lists
    currentUser["friends"].append(friend)
    currentUser["friendrequest"].remove(friend)
    index = users_db.data.index(currentUser)
    users_db.update(index, currentUser)

    
    
def rejectFriendRequest(friend):
    print(f"Rejecting friend request from {friend}.")
    currentUser["friendrequest"].remove(friend)
    index = users_db.data.index(currentUser)
    users_db.update(index, currentUser) 



def friendRequest():
    print("-----------------------------------------")
    
    while currentUser["friendrequest"]:
        print(f"\nYou have a friend request from: {currentUser['friendrequest'][0]}")
        count = input("Select (1) to accept or (2) to reject, or enter '0' to go back: ")

        if count == "1":
            acceptFriendRequest(currentUser['friendrequest'][0])
        elif count == "2":
            rejectFriendRequest(currentUser['friendrequest'][0])
        elif count == "0":
            return True
        else:
            print("Invalid choice. No friend request accepted or rejected.")
    
    print("You have no pending friend requests.")
    return True


def showNetwork():
    print("-----------------------------------------")
    print("\n1. Display Pending Friend Requests")
    print("2. Display Friends List")
    print("3. Go Back")
    choice = input("Enter your choice (1-3): ")

    if choice == "1":
        displayPendingFriendRequests()
    elif choice == "2":
        displayFriendsList()
    elif choice == "3":
        return True
    else:
        print("Invalid choice. Please try again.")

def displayPendingFriendRequests():
    print("\nPending Friend Requests")
    print("-----------------------------------------")
    if not currentUser["friendrequest"]:
        print("No pending friend requests.")
        return
    friendRequest()

def displayFriendsList():
    print("\nYour Friends List")
    print("-----------------------------------------")
    if not currentUser["friends"]:
        print("No Connections")
        return

    for x, friend in enumerate(currentUser["friends"], start=1):
        print(f"{x}. {friend}")

    print("\nOptions:")
    print("1. Unfriend a user")
    print("2. Go Back")
    choice = input("Enter your choice (1-2): ")

    if choice == "1":
        unfriendUser()
    elif choice == "2":
        return
    else:
        print("Invalid choice. Please try again.")



def unfriendUser():
    print("\nYour Friends List")
    print("-----------------------------------------")
    if not currentUser["friends"]:
        print("No Connections")
        return

    for x, friend in enumerate(currentUser["friends"], start=1):
        print(f"{x}. {friend}")

    try:
        friend_number = int(input("Enter the number of the friend to unfriend (or enter 0 to go back): "))

        if 1 <= friend_number <= len(currentUser["friends"]):
            friend = currentUser["friends"][friend_number - 1]
            currentUser["friends"].remove(friend)

            # Update the friend's list of the unfriended user 
            for user in users_db.data:
                if user["username"] == friend:
                    user["friends"].remove(currentUser["username"])
                    print(f"You have unfriended {friend}.")
                    users_db.update(users_db.data.index(user), user)
                    break

            # Update the current user's data in the database
            users_db.update(users_db.data.index(currentUser), currentUser)
        elif friend_number == 0:
            return True
        else:
            print("Invalid friend number. Please try again.")
    except ValueError:
        print("Invalid input. Please enter a number.")





#Author Grant DeBiase
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
                                      action=studentLookupLog,
                                      children=[
                                        menuSystem.menuNode(
                                              "Search by Last Name",
                                              goBack=True,
                                              action=LastNameLookup),
                                        menuSystem.menuNode(
                                              "Search by Major",
                                              goBack=True,
                                              action=majorLookup),
                                        menuSystem.menuNode(
                                              "Search by University",
                                              goBack=True,
                                              action=universityLookup)
                                      ]),
                  menuSystem.menuNode("Show my Network",
                                      goBack=True,
                                      action=showNetwork,
                                      #implment the menu systems for the showNetwork function
                                      # children=[
                                      #   menuSystem.menuNode(
                                      #         "Display Pending Friend Requests",
                                      #         goBack=True,
                                      #         action=displayPendingFriendRequests),
                                      #   menuSystem.menuNode(
                                      #         "Display Friends List",
                                      #         goBack=True,
                                      #         action=displayFriendsList),
                                      # ]
                                      ),
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
                  usefulLinks.buildUsefulLinksMenu(True),
                  usefulLinks.buildImportantLinksMenu(True)
              ]),
          menuSystem.menuNode("Student Lookup",
                              goBack=True,
                              action=studentLookup),
          menuSystem.menuNode("Look for inCollege Friends", goBack=True),
          menuSystem.menuNode("Watch video on why you should join InCollege!",
                              action=watchVideo,
                              goBack=True),
          usefulLinks.buildUsefulLinksMenu(False),
          usefulLinks.buildImportantLinksMenu(False),
          menuSystem.menuNode("Exit", action=lambda: sys.exit(0), goBack=True)
      ])
  return root


#Creates all databases (users, job postings)
def createDatabases():
  databaseInterface.createDatabase()
  databaseInterface.createJobPostingDatabase()
  databaseInterface.createGuestSettingsDatabase()


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
