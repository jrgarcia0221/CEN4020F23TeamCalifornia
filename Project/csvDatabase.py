import csv
import os

#Creates CSV File if it does not exist
#fileName: name of csv file
#header: first row of csv
def createDatabase(fileName, header):
    path = os.path.realpath(fileName)
    if not os.path.isfile(path):
        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)

#Adds record to csv file
#fileName: name of csv file
#record: string array representing the csv record
def addRecord(fileName, record):
    with open(fileName, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(record)

#Returns number of records in csv
#fileName: name of csv file
def getRecordCount(fileName):
    with open(fileName, 'r') as csvfile:
        reader = csv.reader(csvfile)
        return sum(1 for _ in reader) - 1

#Looks up record
#Returns record - string array representing csv record
#Returns None if no record is found
#fileName: name of csv file
#col: column number of lookup - for example, if you are looking up username input the number of the username column.  First column is 1 not 0
#lookupValue: value you are looking up
def lookupRecord(filename, col, lookupValue):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            if (len(row) < col):
                raise Exception("Row does not have " + col + " columns")
            if row[col-1] == lookupValue:
                return row
    return None  # Return None if record is not found

# Displays record
def displayRecord(filename):
    record = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) # skip header row
        for row in reader:
            record.append(row)
    return record