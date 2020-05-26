from pymongo import MongoClient

client
db

def connect():
    try:
        client = MongoClient("mongodb://root:root@localhost/?authSource=Simpy&authMechanism=SCRAM-SHA-256")
        print("Connected to db successfully")
        db = client["mydatabase"]
    except Exception as e:
        print(e)


def add(collectionName, doc):
    try:
        collection = db[str(collectionName)]
        x = collection.insert_one(doc)
        print("Successfully inserted: %S, in: %s" + %(x.inserted_id, collectionName))
    except Exception as e:
        print(e)


def delete(collectionName, doc):
    try:
        collection = db[str(collectionName)]
        collection.delete_one(doc)
        print("Successfully deleted: %S, from: %s" + %(doc, collectionName))
    except Exception as e:
        print(e)


def find(collectionName, doc)):
    collection = db[str(collectionName)]
    x = collection.find_one(doc)
    if x:
        return x
    else:
        print("Document not found in %s"+ % collectionName)
        return None
