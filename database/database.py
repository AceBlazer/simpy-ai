from pymongo import MongoClient
import os

client = None
db = None

def connect():
    try:
        client = MongoClient(os.environ["SIMPY_CONNECTION_STRING"])
        print("Connected to db successfully")
        global db
        db = client["mydatabase"]
    except Exception as e:
        print(e)


def add(collectionName, doc):
    try:
        print("here")
        collection = db[str(collectionName)]
        x = collection.insert_one(doc)
        print("Successfully inserted: "+str(x.inserted_id)+", to: "+  str(collectionName))
        return x
    except Exception as e:
        print(e)
        return None


def delete(collectionName, doc):
    try:
        collection = db[str(collectionName)]
        collection.delete_one(doc)
        print("Successfully deleted: "+str(doc)+", from: "+  str(collectionName))
    except Exception as e:
        print(e)


def find(collectionName, doc):
    collection = db[str(collectionName)]
    x = collection.find_one(doc)
    if x:
        return x
    else:
        print("Document not found in: "+ str(collectionName))
        return None


def findCustomerByName(name):
    collection = db["customers"]
    return collection.find_one({"name": name})

def findCustomerByEmail(email):
    collection = db["customers"]
    return collection.find_one({"email": email})

def findCustomerById(id):
    collection = db["customers"]
    return collection.find_one({"_id": id})

def deleteCustomerById(id):
    collection = db["customers"]
    return collection.delete_one({"_id": id})

def findProjectsOfCustomer(customerId):
    #no populate in pymongo :(
    try:
        projects = []
        customer = findCustomerById(customerId)

        for pid in customer["projects"]:
            projects.append(db["projects"].find_one({"_id": pid}))
        return projects 
    except Exception as e:
        print(e)
        return None


