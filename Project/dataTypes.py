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


#Author Grant DeBiase
#Function to create student dictionary
def createStudent(username="JohnDoe", password="Password123!", firstname="John", lastname="Doe", major = "major", university = "uni", settings=createSetting(), friendrequest=None, friends=None):
    return {
        "username": username,
        "password": password,
        "firstname": firstname,
        "lastname": lastname,
        "major": major,
        "university": university,
        "settings": settings,
        "friendrequest": friendrequest or [],
        "friends": friends or []
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