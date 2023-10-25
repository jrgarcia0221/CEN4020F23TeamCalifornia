import jsonWrapper
import os

#Author Grant DeBiase
class jsonDB:

    #Author Grant DeBiase
    #if json file exists, loads it.
    def __init__(self, fileName):
        loadedData = None

        if jsonWrapper.jsonFileisValid(fileName):
            loadedData = jsonWrapper.deserializeFromFile(fileName)

        self.fileName = fileName        
        self.data = loadedData or []
    
    #Author Grant DeBiase
    #appends item to database
    def add(self, item):
        self.data.append(item)
        jsonWrapper.serializeToFile(self.data, self.fileName)

    #Author Grant DeBiase
    #returns item at index
    #returns copy of database if index is not provided
    def read(self, index=None):
        if index is not None:
            #if index is out of range
            if not (0 <= index < len(self.data)):
                raise IndexError("Index out of range")
            return self.data[index]
        else:
            return self.data.copy()   
        
    #Author Grant DeBiase
    #updates index with newItem
    def update(self, index, newItem):
        #if index is out of range
        if not (0 <= index < len(self.data)):
            raise IndexError("Index out of range")
        
        self.data[index] = newItem
        jsonWrapper.serializeToFile(self.data, self.fileName)

    #Queries data based on conditions
    #conditions is an array, use createQueryCondition funtion to create condtion, append condition to conditions array
    def query(self, conditions):
        result = []

        for item in self.data:
            allConditionsMet = True

            for condition in conditions:
                key = condition['key']
                value = condition['value']
                operator = condition['operator']

                if key not in item:
                    allConditionsMet = False
                    break

                itemValue = item[key]

                if operator == '==':
                    if itemValue != value:
                        allConditionsMet = False
                        break
                elif operator == '!=':
                    if itemValue == value:
                        allConditionsMet = False
                        break
                elif operator == '<':
                    if not (itemValue < value):
                        allConditionsMet = False
                        break
                elif operator == '>':
                    if not (itemValue > value):
                        allConditionsMet = False
                        break
                elif operator == '<=':
                    if not (itemValue <= value):
                        allConditionsMet = False
                        break
                elif operator == '>=':
                    if not (itemValue >= value):
                        allConditionsMet = False
                        break
                else:
                    raise ValueError(f"Invalid operator: {operator}")

            if allConditionsMet:
                result.append(item)

        return result

    #Author Grant DeBiase
    #returns size of database
    def size(self):
        return len(self.data)

    #Author Grant DeBiase
    #deletes index
    def delete(self, index):
        #if index is out of range
        if not (0 <= index < len(self.data)):
            raise IndexError("Index out of range")        
        del self.data[index]  
        jsonWrapper.serializeToFile(self.data, self.fileName)  

    #Author Grant DeBiase
    #clears all data
    def clear(self):
        if not os.path.exists(self.fileName):
            return
        
        with open(self.fileName, 'w') as file:
            file.truncate(0)
            self.data = []

    @staticmethod
    def createQueryCondition(key, value, operator="=="):
        return {
            "key": key,
            "value": value,
            "operator": operator
        }