from jsonDB import jsonDB
from dataTypes import createJob, createSetting, createStudent

usersDB = "users.json"
jobsDB = "jobs.json"
guestSettingsDB = "guestSettings.json"
currentUser = {}

#returns true if student record exists
def studentExists(username):    
    db = jsonDB(usersDB)
    conditions = [jsonDB.createQueryCondition("username", username)]
    return len(db.query(conditions)) > 0

#returns true if student record exists by first and last name
def studentNameExists(firstName, lastName):    
    db = jsonDB(usersDB)
    conditions = [
        jsonDB.createQueryCondition("firstname", firstName),
        jsonDB.createQueryCondition("lastname", lastName)
    ]
    return len(db.query(conditions)) > 0

#returns true if student record exists by first and last name
def studentlastNameExists(lastName):    
    db = jsonDB(usersDB)
    conditions = [jsonDB.createQueryCondition("lastname", lastName)]
    return len(db.query(conditions)) > 0

#returns true if database is empty
def isEmpty(db):
    if db == "user":
        db = jsonDB(usersDB)
    elif db == "job":
        db = jsonDB(jobsDB)
    data = db.read()
    return len(data) == 0
#returns true if database if full
def isFull(db):
    if db == "user":
        db = jsonDB(usersDB)
    elif db == "job":
        db = jsonDB(jobsDB)
    data = db.read()
    return len(data) >= 10

#Adds Student Account
def addStudentAccount(username, password, firstname, lastname, major, university, tier):
    db = jsonDB(usersDB)
    data = db.read()
    if not studentExists(username) and not isFull("user"):
        settings = createSetting()  # Create student settings
        new_student = createStudent(username, password, firstname, lastname, major, university, settings, tier=tier)
        db.add(new_student)
        return True
    return False

                    
#Gets password of student
#Returns None if password does not exist
def getPassword(username):
    db = jsonDB(usersDB)
    conditions = [jsonDB.createQueryCondition("username", username)]
    user_record = db.query(conditions)
    if user_record:
        return user_record[0]["password"]
    return None

#Returns true if username and password are in database
def login(username, password):
    return getPassword(username) == password

def addGuestSettings(username):
    db = jsonDB(guestSettingsDB)
    new_settings = createSetting()  # Create guest settings
    new_settings["username"] = username
    db.add(new_settings)

def lookForGuestSetting():
    db = jsonDB(guestSettingsDB)
    if "username" in currentUser:  # Check if "username" is a key in the dictionary
        username = currentUser["username"]
        conditions = [jsonDB.createQueryCondition("username", username)]
        user_settings = db.query(conditions)
        if user_settings:
            return user_settings[0]
    return None

# current user
def getCurrentUser(user):
    global currentUser
    db = jsonDB(usersDB)
    conditions = [jsonDB.createQueryCondition("username", user)]
    user_record = db.query(conditions)
    if user_record:
        currentUser = user_record[0]
    else:
        print(f"User '{user}' not found in the database.")

        
# Adds job posting
def addJobPost(title, desc, employer, location, salary):
    db = jsonDB(jobsDB)    
    job = createJob(title, desc, employer, location, salary, currentUser['firstname'], currentUser['lastname'], currentUser['username'])
    if not isFull("job"):
        db.add(job)        
    return False

# Read current posted jobs
def readJobPosts():
    db = jsonDB(jobsDB)
    data = db.read()
    print("---------------------------------------------")
    if data:
        for job in data:
            print(job['title'])
            for key, value in job.items():
                if key in ['description', 'employer', 'location', 'salary']:
                    print(f"   {key}: {value}")
            print()
    return data

# Displays job postings (excluding poster's name)
def displayJobs(jobs):
    print("Available Jobs:")
    for job in jobs:
        applied = currentUser['username'] in [app['applicantUsername'] for app in job.get("applications", [])]
        print(job['title'])
        for key in job:
            if key in ['description', 'employer', 'location', 'salary']:
                print(f'  {key}: {job[key]}')
        if applied:
            print("---> Applied by You")
    
    # user_notifications = currentUser.get("notifications", [])
    # for notification in user_notifications:
    #     print(notification)

def createNameNotification(fullName):
    db = jsonDB(usersDB)
    users = db.read()
   
    for index, user in enumerate(users):
        if 'notis' not in user:
            user['notis'] = {}
        if 'newStudent' not in user['notis']:
            user['notis']['newStudent'] = []
            
        user["notis"]["newStudent"].append(fullName)
        db.update(index,user)
    return True

def createJobNotification(jobTitle,currentUserName):
    db = jsonDB(usersDB)
    users = db.read()
    
    for index, user in enumerate(users):
            if currentUserName == user["username"]:
                continue
            if 'notis' not in user:
                user['notis'] = {}
            if "newStudent" not in user["notis"]:
                user['notis']['newJob'] = []
                
            user["notis"]["newJob"].append(jobTitle)
            db.update(index,user)
    return True