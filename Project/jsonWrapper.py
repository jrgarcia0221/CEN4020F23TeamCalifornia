import json

#Author Grant DeBiase
#converts object to json string
def serialize(obj):
    return json.dumps(obj, indent=4)

#Author Grant DeBiase
#writes json string of object to file
def serializeToFile(obj, fileName):
    with open(fileName, 'w') as file:
        json.dump(obj, file, indent=4)

#Author Grant DeBiase
#converts json string to object
def deserialize(jsonStr):
    return json.loads(jsonStr)

#Author Grant DeBiase
#reads json string from file and converts it to object
def deserializeFromFile(fileName):
    with open(fileName, 'r') as file:
        return json.load(file)
    
def jsonIsValid(jsonStr):
    try:
        json.loads(jsonStr)
        return True
    except json.JSONDecodeError:
        return False
    
def jsonFileisValid(fileName):
    try:
        with open(fileName, 'r') as file:
            json.load(file)
            return True
    except (FileNotFoundError, json.JSONDecodeError):
        return False