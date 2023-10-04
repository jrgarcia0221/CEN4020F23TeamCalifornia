import csvDatabase

usersDB = "users.csv"
jobsDB = "jobs.csv"
guestSettingsDB = "guestSettings.csv"
currentUser = []

#Creates Database
def createDatabase():
    csvDatabase.createDatabase(usersDB, ['username', 'password', 'firstname', 'lastname'])
    return True

#returns true if student record exists
def studentExists(username):    
    return csvDatabase.lookupRecord(usersDB, 1, username) != None

#returns true if student record exists by first and last name
def studentNameExists(firstName, lastName):    
    return (csvDatabase.lookupRecord(usersDB, 3, firstName) != None) and (csvDatabase.lookupRecord(usersDB, 4, lastName) != None)

#returns true if database is empty
def isEmpty(db):
    if db == "user":
        return csvDatabase.getRecordCount(usersDB) == 0
    elif db == "job":
        return csvDatabase.getRecordCount(jobsDB) == 0

#returns true if database if full
def isFull(db):
    if db == "user":
        return csvDatabase.getRecordCount(usersDB) >= 10
    elif db == "job":
        return csvDatabase.getRecordCount(jobsDB) >= 10

#Adds Student Account
def addStudentAccount(username, password, firstname, lastname):
    if (not studentExists(username) and not isFull("user")):
        csvDatabase.addRecord(usersDB, [username, password, firstname, lastname])
        return True
    return False
                
#Gets password of student
#Returns None if password does not exist
def getPassword(username):
    return csvDatabase.lookupRecord(usersDB, 1, username)[1]

#Returns true if username and password are in database
def login(username, password):
    return getPassword(username) == password

# Creates Job Posting Database
def createJobPostingDatabase():
    csvDatabase.createDatabase(jobsDB, ['title', 'description', 'employer', 'location', 'salary', 'firstname', 'lastname'])
    return True

#creates a database with guest settings
def createGuestSettingsDatabase():
    csvDatabase.createDatabase(guestSettingsDB, ['username', 'email', 'sms', 'targetedadvertising', 'language'])
    return True

def addGuestSettings(username):
    csvDatabase.addRecord(guestSettingsDB, [username, "On", "On","On","English"])

def lookForGuestSetting():
    arr = csvDatabase.lookupRecord(guestSettingsDB, 1, currentUser[0])
    return arr

# current user
def getCurrentUser(user):
    global currentUser 
    currentUser = csvDatabase.lookupRecord(usersDB, 1, user)

# Adds job posting
def addJobPost(title, desc, employer, location, salary):
    if (not isFull("job")):
        csvDatabase.addRecord(jobsDB, [title, desc, employer, location, salary, currentUser[2], currentUser[3]])
        return True
    return False

# Read current posted jobs
def readJobPosts():
    return csvDatabase.displayRecord(jobsDB)

# Displays job postings (excluding poster's name)
def displayJobs(jobs):
    print("Available Jobs:")
    for job in jobs:
        print(job[0])
        for i in range(1, len(job)-2):
            print('  '+job[i])
