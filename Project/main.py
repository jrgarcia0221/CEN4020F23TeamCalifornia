import databaseInterface
import menuSystem
import usefulLinks
import re
import sys
from jsonDB import jsonDB
import dataTypes

currentUser = None
users_db = jsonDB("users.json")
jobs_db = jsonDB("jobs.json")

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
# Handles user create account
#Checks if database is full (capacity is 5)
#User enters username - checks if student is unique
#User enters password - checks if password is valid
#User enters first and last name
#Creates account in database
#Returns true if successful login
def createAccount():
  #Uncomment this automatically create 3 test accounts
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
  global users_db 
  users_db = jsonDB("users.json")

  return True

#Author Grant DeBiase
# Handles user login
#No existing accounts - returns to main menu
#User enters username - checks if student exists in database
#User enters password - checks if password is matched
#returns true if successful login
def login():
  global username
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

  #usefulLinks.initializeGuestArray(guestSettingArr)

   
  conditions = []
  conditions.append(jsonDB.createQueryCondition("username", username ))
  #returns the user
  global currentUser
  currentUser = users_db.query(conditions)[0] 

  usefulLinks.initializeGuestArray(guestSettingArr, currentUser)

  print("Login successful!")  
  friendRequest() 

  return True

# def login():
#     global currentUser, username, guestSettingArr

#     print("--------------------------------")

#     if databaseInterface.isEmpty("user"):
#         print("There are no existing accounts to log into.")
#         return False

#     while True:
#         username = input("Enter your username: ")
#         if databaseInterface.studentExists(username):
#             break
#         else:
#             print("Invalid Username. Please try again.")

#     while True:
#         password = input("Enter your password: ")
#         if databaseInterface.login(username, password):
#             # Save logged in user
#             currentUser = databaseInterface.getCurrentUser(username)
#             if currentUser:
#                 guestSettingArr = databaseInterface.lookForGuestSetting()
#                 usefulLinks.initializeGuestArray(guestSettingArr, currentUser)
#                 print("Login successful!")
#                 friendRequest()
#                 return True
#             else:
#                 print("Error: Unable to retrieve user data.")
#                 return False
#         else:
#             print("Invalid Password. Please try again.")

  
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
  global jobs_db 
  jobs_db = jsonDB("jobs.json")

  global postedJobs 
  postedJobs = databaseInterface.readJobPosts()

  return False

#Author Grant DeBiase
#Note - not in use
def deleteJobAction():
    print("--------------------------------")
    currentUsername = currentUser['username']
    myJobs = jobs_db.query([jsonDB.createQueryCondition("postedby", currentUsername)])

    i = 0
    for myJob in myJobs:
        i = i + 1
        print(f"Enter {i} to delete job - {myJob['title']}")        

    if i > 0:
        ans = input("Enter number: ")

        if (int(ans)>=1 and int(ans)<=i):
            jobToDelete = myJobs[int(ans)-1]
            jobToDeleteIndex = jobs_db.read().index(jobToDelete)
            jobs_db.delete(jobToDeleteIndex)
    else:
        print("You have no jobs to delete")

    return False

#Author Grant
def displayJob(job):    
    print(job['title'])

    for key in job:
        if key in ['title', 'description', 'employer', 'location', 'salary']:
            print(f'  {key}: {job[key]}')

#Author Grant
def displaySavedJobsAction():
    print("--------------------------------")
    currentUsername = currentUser['username']
    jobs = jobs_db.read()

    for job in jobs:
        users = job["savedby"]
        
        if currentUsername in users:
            displayJob(job)

    return False

#Author Grant
def displayAppliedJobsAction():
    print("--------------------------------")
    currentUsername = currentUser['username']
    jobs = jobs_db.read()

    for job in jobs:        
        applications = job["applications"]
        if any(obj.get("applicantUsername") == currentUsername for obj in applications):
            displayJob(job)

    return False

#Author Grant
def displayUnAppliedJobsAction():
    print("--------------------------------")
    currentUsername = currentUser['username']
    jobs = jobs_db.read()

    for job in jobs:
        applications = job["applications"]
        if any(obj.get("applicantUsername") == currentUsername for obj in applications):
            continue

        if job["postedby"] == currentUsername:
            continue

        displayJob(job)

    return False



#Author Grant DeBiase
#Deletes Job at index
def handleDeleteJob(job, index): 
    job_title = job["title"]
    
    # Iterate through applicants and notify each user
    applicants = job.get("applications", [])
    for applicant in applicants:
        applicant_username = applicant["applicantUsername"]
        
        # Add a notification to the user
        conditions = [jsonDB.createQueryCondition("username", applicant_username)]
        user_record = users_db.query(conditions)
        user= user_record[0]
        notification = f"Job '{job_title}' has been deleted."
        user["notifications"].append(notification)
        users_db.update(users_db.read().index(user), user)

    jobs_db.delete(index)
    global postedJobs 
    postedJobs = databaseInterface.readJobPosts()

#Author Grant DeBiase
#Adds current user to job's savedby array
def handleSaveJob(job, index):
    job["savedby"].append(currentUser["username"])
    jobs_db.update(index, job)

#Author Grant DeBiase
#Removes current user from job's savedby array
def handleUnSaveJob(job, index):
    job["savedby"].remove(currentUser["username"])
    jobs_db.update(index, job)

#Author Grant DeBiase
#Adds application to job's applications array
def handleApplyJob(job, index):
    gradDate = input("Enter Graduation Date: ")
    workDate = input("Enter Date You Can Start Working: ")
    paragraph = input("Enter paragraph on why you think you would be a good fit for this job: ")

    application = dataTypes.createJobApplication(gradDate, workDate, paragraph, currentUser["username"])

    job["applications"].append(application)
    jobs_db.update(index, job)

#Author Grant DeBiase
#Lets user select a job
def selectJobAction():
    i = 0
    for job in jobs_db.read():
        i = i + 1
        print(f"Enter {i} to select job - {job['title']}")    

    if i > 0:
        ans = input("Enter number: ")
        ans = int(ans)

        if (ans>=1 and ans<=i):
            selectedJobIndex = ans - 1
            selectedJob = jobs_db.read(selectedJobIndex)

            print (f"Selected job: {selectedJob['title']} {selectedJob['description']} {selectedJob['employer']} {selectedJob['location']} {selectedJob['salary']}")

            delFlag = False
            saveFlag = False
            applyFlag = False
            unSaveFlag = False
            user = currentUser["username"]
            if (user == selectedJob["postedby"]):
                print("Enter del to delete job")
                delFlag = True
            else:
                if (not user in selectedJob["savedby"]):
                    print ("Enter save to save job for later")
                    saveFlag = True

                if (user in selectedJob["savedby"]):
                    print ("Enter unsave to unsave job")
                    unSaveFlag = True

                jobApplications = selectedJob["applications"]
                userInApplicationlist = any(obj.get("applicantUsername") == username for obj in jobApplications)
                if (not userInApplicationlist):
                    print("Enter apply to apply to job")
                    applyFlag = True

            if (delFlag or saveFlag or applyFlag or unSaveFlag):
                ans = input("Enter value or back to go back: ")

                if (ans == "del"):
                    handleDeleteJob(selectedJob, selectedJobIndex)
                elif (ans == "save"):
                    handleSaveJob(selectedJob, selectedJobIndex)
                elif (ans == "unsave"):
                    handleUnSaveJob(selectedJob, selectedJobIndex)
                elif (ans == "apply"):
                    handleApplyJob(selectedJob, selectedJobIndex)
                elif (ans == "back"):
                    return False
                else:
                    print ("Invalid Value")
    else:
        print("There are no job postings")

    return False


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


def capitalizeFirstLetter(input_string):
    words = input_string.split()  # Split the input string into words
    capitalized_words = [word.capitalize() for word in words]  # Capitalize the first letter of each word
    output_string = " ".join(capitalized_words)  # Join the words back into a string
    return output_string

def manageProfile ():
      while True:
            # check if the user already have a profile
            if currentUser.get("profile") and any(currentUser["profile"].values()):
                print("\nYou already have a profile.")
                print("1. Edit profile")
                print("2. Create a new profile")
                choice = input("Enter your choice (1-2): ")

                if choice == "1":
                      editProfile()
                      break
                elif choice == "2":
                      createProfile()
                      break  
                else:
                      print("Invalid choice. Please try again.\n")
                      
            else:
                  createProfile()
                  break

                  
def createProfile():
      
      print("\nCreate Profile")
      print("-----------------------------------------")
      
      # Initialize an empty profile
      index = users_db.data.index(currentUser)
      currentUser["profile"] = dataTypes.createProfile()      
      users_db.update(index, currentUser)
      
      title = input("Enter a title or 0 to exit: ")
      if title == '0':
            return 
      currentUser["profile"]["title"] = title
      index = users_db.data.index(currentUser)
      users_db.update(index, currentUser)
            
      major = input("Enter your major or 0 to exit: ")
      if major == '0':
            return 
      currentUser["profile"]["major"] = capitalizeFirstLetter(major)
      index = users_db.data.index(currentUser)
      users_db.update(index, currentUser)
      
      university = input("Enter your university or 0 to exit: ")
      if university == '0':
            return 
      currentUser["profile"]["university"] = capitalizeFirstLetter(university)
      index = users_db.data.index(currentUser)
      users_db.update(index, currentUser)
      
      # Create aboutMe dictionary
      print("\nAbout Me:")
      paragraph = input("Enter a brief about yourself or 0 to exit: ")
      if paragraph == '0':
            return
      currentUser["profile"]["aboutMe"]["paragraph"] = paragraph
      index = users_db.data.index(currentUser)
      users_db.update(index, currentUser)
      
      print("\nExperiences:")
      experiences = []
      while len(experiences)<3:
            exp_title = input("\nEnter job title or 0 to exit: ")
            if exp_title == '0':
                  break
            employer = input("Enter employer: ")
            date_started = input("Enter start date: ")
            date_ended = input("Enter end date: ")
            location = input("Enter location: ")
            description = input("Enter job description: ")
            experience = dataTypes.createExperience(exp_title, employer, date_started, date_ended, location, description)
            experiences.append(experience)
            
      currentUser["profile"]["aboutMe"]["experience"] = experiences
      index = users_db.data.index(currentUser)
      users_db.update(index, currentUser)
      
      print("\nEducations:")
      educations = []
      while True:
        school = input("\nEnter school/university name or 0 to exit: ")
        if school == '0':
            break
        degree = input("Enter degree: ")
        years_attended = input("Enter years attended: ")
        education = dataTypes.createEducation(school, degree, years_attended)
        educations.append(education)
        
      currentUser["profile"]["aboutMe"]["education"] = educations
      index = users_db.data.index(currentUser)
      users_db.update(index, currentUser) 
      
      print("Profile created/updated successfully!")
      
      while True:
        print("\nWould you like to view your profile?")
        print("1. Yes")
        print("2. No")
        choice = input("Enter your choice (1-2): ")

        if choice == "1":
              if "profile" in currentUser:
                    full_name = f"{currentUser['firstname']} {currentUser['lastname']}"
                    viewProfile(currentUser["profile"],full_name)
              else:
                  print("Profile not found. Please create your profile first.")
                  
        elif choice == "2":
              break
        else:
              print("Invalid choice. Please try again.")

def editProfile():

    print("\nEdit Profile")
    print("-----------------------------------------")
    

    while True:
        full_name = f"{currentUser['firstname']} {currentUser['lastname']}"
        viewProfile(currentUser["profile"],full_name)
        
        print("\nProfile Options:")
        print("1. Edit Title")
        print("2. Edit Major")
        print("3. Edit University")
        print("4. Edit About Me pargraph")
        print("5. Edit Experiences")
        print("6. Edit Education")
        print("7. Go Back")
        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            currentUser["profile"]["title"] = input("Enter a new title: ")
            index = users_db.data.index(currentUser)
            users_db.update(index, currentUser)
        elif choice == "2":
            currentUser["profile"]["major"] = capitalizeFirstLetter(input("Enter updated major: "))
            index = users_db.data.index(currentUser)
            users_db.update(index, currentUser)
        elif choice == "3":
            currentUser["profile"]["university"] = capitalizeFirstLetter(input("Enter updated university: "))
            index = users_db.data.index(currentUser)
            users_db.update(index, currentUser)
        elif choice == "4":
              currentUser["profile"]["aboutMe"]["paragraph"] = input("Enter new paragraph: ")
              index = users_db.data.index(currentUser)
              users_db.update(index, currentUser)
        elif choice == "5":
              editExperiences()
        elif choice == "6":
              editEducation()
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")
            continue
          
        print("\nProfile updated successfully!")
        
def editExperiences():
    experiences = currentUser["profile"]["aboutMe"]["experience"]
    while True:
        print("\nExperiences:")
        for i, experience in enumerate(experiences, start=1):
            print(f"{i}. {experience['title']} at {experience['employer']}")
        print("\na. Add Experience")
        print("b. Edit Experience")
        print("c. Delete Experience")
        print("d. Go Back")
        choice = input("Enter your choice (a-d): ")

        if choice == "a":
            if len(experiences) >= 3:
                print("You can't add more than 3 experiences.")
            else:
                title = input("Enter job title: ")
                employer = input("Enter employer: ")
                location = input("Enter location: ")
                dateStarted = input("Enter start date: ")
                dateEnded = input("Enter end date: ")
                description = input("Enter job description: ")
                experience = dataTypes.createExperience(title, employer, dateStarted, dateEnded, location, description)
                experiences.append(experience)
        elif choice == "b":
            # check if there is no existing Experience
            if not experiences:
                print("No Experience records found to edit.")
                continue
            index = input("Enter the number of the experience to edit: ")
            if index.isdigit() and 1 <= int(index) <= len(experiences):
                index = int(index) - 1
                title = input("Enter new job title: ")
                employer = input("Enter new employer: ")
                location = input("Enter new location: ")
                dateStarted = input("Enter new start date: ")
                dateEnded = input("Enter new end date: ")
                description = input("Enter new job description: ")
                experiences[index] = dataTypes.createExperience(title, employer, dateStarted, dateEnded, location, description)
                print("Experience updated successfully.")
            else:
                print("Invalid input. Please enter a valid number.")
        elif choice == "c":
            # check if there is no existing Experience
            if not experiences:
                print("No Experience records found to delete.")
                continue
            index = input("Enter the number of the experience to delete: ")
            if index.isdigit() and 1 <= int(index) <= len(experiences):
                del experiences[int(index) - 1]
            else:
                print("Invalid input. Please enter a valid number.")
        elif choice == "d":
            break
        else:
            print("Invalid choice. Please try again.")
            
        currentUser["profile"]["aboutMe"]["experience"] = experiences
        index = users_db.data.index(currentUser)
        users_db.update(index, currentUser)

def editEducation():
    educations = currentUser["profile"]["aboutMe"]["education"]
    while True:
        print("\nEducation:")
        for i, education in enumerate(educations, start=1):
            print(f"{i}. {education['school']}, {education['degree']}")
        print("a. Add Education")
        print("b. Edit Education")
        print("c. Delete Education")
        print("d. Go Back")
        choice = input("Enter your choice (a-d): ")

        if choice == "a":
            school = input("Enter school/university name: ")
            degree = input("Enter degree: ")
            yearsAttended = input("Enter years attended: ")
            education = dataTypes.createEducation(school, degree, yearsAttended)
            educations.append(education)
        elif choice == "b":
            # check if there is no existing education
            if not educations:
                print("No education records found to edit.")
                continue
            index = input("Enter the number of the education to edit: ")
            if index.isdigit() and 1 <= int(index) <= len(educations):
                index = int(index) - 1
                school = input("Enter new school/university name: ")
                degree = input("Enter new degree: ")
                yearsAttended = input("Enter new years attended: ")
                educations[index] = dataTypes.createEducation(school, degree, yearsAttended)
                print("Education updated successfully.")
            else:
                print("Invalid input. Please enter a valid number.")
        elif choice == "c":
            # check if there is no existing education
            if not educations:
                print("No education records found to delete.")
                continue
            index = input("Enter the number of the education to delete: ")
            if index.isdigit() and 1 <= int(index) <= len(educations):
                del educations[int(index) - 1]
            else:
                print("Invalid input. Please enter a valid number.")
        elif choice == "d":
            break
        else:
            print("Invalid choice. Please try again.")
            
        currentUser["profile"]["aboutMe"]["education"] = educations
        index = users_db.data.index(currentUser)
        users_db.update(index, currentUser)

def callviewProfile():
    while True:
        print("-----------------------------------------")
        print("Which profile would you like to view?")
        print("1.View My Profile")
        print("2.Look up a Friend's Profile")
        print("3.Go back")
        choice = input("Enter your choice (1-3): ")
        print("-----------------------------------------")

        if choice == "1":
            if "profile" in currentUser:
                full_name = f"{currentUser['firstname']} {currentUser['lastname']}"
                viewProfile(currentUser["profile"],full_name)
            else:
                print("Profile not found. Please create your profile first.") 
            
            
        elif choice == "2":
              
            if not currentUser["friends"]:
              print("You have no connections")
              return
            
            print("List of Friends:")
            for x, friend in enumerate(currentUser["friends"], start=1):
                print(f"{x}. {friend}")
                
            friend_choice = input(f"\nSelect a friend to view their profile (1-{len(currentUser['friends'])}) or enter '0' to go back: ")
            try:
                friend_index = int(friend_choice) - 1
                if 0 <= friend_index < len(currentUser["friends"]):
                    friend_username = currentUser["friends"][friend_index]
                    friend_profile = getUserProfile(friend_username)
                    if friend_profile:
                        full_name = getUserFullName(friend_username)
                        viewProfile(friend_profile, full_name)
                    else:
                        print("Friend does not have a profile.")
                elif friend_index == -1:
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

def getUserProfile(username):
    for user in users_db.data:
        if user["username"] == username and "profile" in user:
            return user["profile"]
    return None
  
def getUserFullName(username):
    for user in users_db.data:
        if user["username"] == username:
            full_name = f"{user['firstname']} {user['lastname']}"
            return full_name
           
def viewProfile(profile, full_name):
    print(f"\n{full_name}'s Profile\n")
    
    name_padding = (100 - len(full_name)) // 2
    print(f"{'-'*100}")
    print(f"{' '*name_padding}{full_name}{' '*name_padding}")
    print(f"{'-'*100}")
    
    print(f"\n{'Title:':<10} {profile['title']:^20}")
    print(f"{'Major:':<10} {profile['major']:^20}")
    print(f"{'University:':<10} {profile['university']:^20}")
    print(f"{'-'*50}")
    
    print("\nAbout Me:")
    print(f"{profile['aboutMe']['paragraph']}\n")
    
    print("Experiences:")
    print(f"{'-'*50}")
    
    for exp in profile['aboutMe']['experience']:
        print(f"- Title: {exp['title']} at {exp['employer']}")
        print(f"  Employer: {exp['employer']}")
        print(f"  Start Date: {exp['dateStarted']} | End Date: {exp['dateEnded']}")
        print(f"  Location: {exp['location']}")
        print(f"  Description: {exp['description']}\n")

        
    print("\nEducations:")
    print(f"{'-'*50}")

    for edu in profile['aboutMe']['education']:
        print(f"- School: {edu['school']}")
        print(f"  Degree: {edu['degree']}")
        print(f"  Years Attended: {edu['yearsAttended']}\n")


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
                                              action=postJobAction),                                              
                                              menuSystem.menuNode(
                                              "Select a job",
                                              goBack=True,
                                              action=selectJobAction),
                                              menuSystem.menuNode(
                                              "Display Saved Jobs",
                                              goBack=True,
                                              action=displaySavedJobsAction),
                                              menuSystem.menuNode(
                                              "Display Jobs Applied for",
                                              goBack=True,
                                              action=displayAppliedJobsAction),
                                              menuSystem.menuNode(
                                              "Display Jobs Not Applied For",
                                              goBack=True,
                                              action=displayUnAppliedJobsAction)
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
                  usefulLinks.buildImportantLinksMenu(True),
                  menuSystem.menuNode(
                      "My Profile",
                      goBack=True,
                      children=[
                          menuSystem.menuNode("Create/Manage Profile",
                                              goBack=True,
                                              action=manageProfile),
                          menuSystem.menuNode("View Profile",
                                              goBack=True,
                                              action=callviewProfile)  
                  ])
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


# build main menu tree
def buildMenuTree():
  menuTree = buildMenu()

  while True:
    menuSystem.navigateMenu(menuTree, [])

def main():
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