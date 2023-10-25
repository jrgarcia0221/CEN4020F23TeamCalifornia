import json
import jsonWrapper
import jsonDB

def createSetting(email="On", sms="On",targetedAdvert="On", language="English"):
    return {
        "email": email,
        "sms": sms,
        "targetedAdvert": targetedAdvert,
        "language":language
    }    


#Author Grant DeBiase.
#Function to create student dictionary
def createStudent(username="JohnDoe", password="Password123!", firstname="John", lastname="Doe", major = "major", university = "uni", settings= None, friendrequest=None, friends=None, profile=None):
    return {
        "username": username,
        "password": password,
        "firstname": firstname,
        "lastname": lastname,
        "major": major,
        "university": university,
        "settings": settings or createSetting(),
        "friendrequest": friendrequest or [],
        "friends": friends or [],
        "profile": profile or {}
    }
    
#Author Grant DeBiase
#Function to create job dictionary
def createJob(title="title", description="description", employer="employer", location="location", salary="salary", firstname="John", lastname="Doe"):
    return {
        "title": title,
        "description": description,
        "employer": employer,
        "location": location,
        "salary": salary,
        "firstname": firstname,
        "lastname": lastname
    }
    
#Author Fatemah Elsewaky
#Function to create student Experience
def createExperience(title=None, employer=None, dateStarted=None, dateEnded=None, location=None, description=None):
    return{
        "title": title,
        "employer": employer,
        "dateStarted": dateStarted,
        "dateEnded": dateEnded,
        "location": location,
        "description": description
    }
    
#Author Fatemah Elsewaky
#Function to create student Education
def createEducation(school= None, degree= None, yearsAttended= None):
    return{
        "school": school,
        "degree": degree,
        "yearsAttended": yearsAttended  
    }
    
#Author Fatemah Elsewaky
#Function to create student "AboutMe"
def createAboutMe(paragraph="", experience= None, education= None):
    return{
        "paragraph": paragraph,
        "experience": experience or [],
        "education": education or []
    }
    
#Author Fatemah Elsewaky
#Function to create student Profile
def createProfile(title="",major = "", university = "", aboutMe= None):
    return{
        "title": title,
        "major": major,
        "university": university,
        "aboutMe": aboutMe or createAboutMe()
    }