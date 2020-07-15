import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import datetime
import os

cred = credentials.Certificate('./serviceAccount.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': os.environ['FIRESTORAGE_BUCKET']
})
bucket = storage.bucket()




def uploadRetrievedImages(customer_name, project_name):
    #here we don't use os.path.join to enable firebase to create folders
    path = "dataset"+"/"+customer_name+"/"+project_name
    for imgName in os.listdir(path):
        imgName = path+"/"+imgName
        blob = storage.bucket(os.environ['FIRESTORAGE_BUCKET']).blob(imgName) # intended name of file in Firebase Storage
        blob.upload_from_filename(imgName) # path to file on local disk

def uploadIndexes(customer_name, project_name):
    #here we don't use os.path.join to enable firebase to create folders
    path = "indexes"+"/"+customer_name+"/"+project_name
    for indexFile in os.listdir(path):
        indexFile = path+"/"+indexFile
        blob = storage.bucket(os.environ['FIRESTORAGE_BUCKET']).blob(indexFile) # intended name of file in Firebase Storage
        blob.upload_from_filename(indexFile) # path to file on local disk

def uploadQueryImage(customer_name, project_name):
    #here we don't use os.path.join to enable firebase to create folders
    path = "queries"+"/"+customer_name+"/"+project_name
    for img in os.listdir(path):
        img = path+"/"+img
        blob = storage.bucket(os.environ['FIRESTORAGE_BUCKET']).blob(img) # intended name of file in Firebase Storage
        blob.upload_from_filename(img) # path to file on local disk


def getImage(imgPath):
    blob = storage.bucket(os.environ['FIRESTORAGE_BUCKET']).blob(imgPath) 
    return(blob.generate_signed_url(datetime.timedelta(weeks=30000), method='GET'))
