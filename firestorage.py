import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import datetime
import os
from multiprocessing import Process


cred = credentials.Certificate('./serviceAccount.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': os.environ['FIRESTORAGE_BUCKET']
})
bucket = storage.bucket()



def uploadRetrievedImagesCore(customer_name, project_name):
    #here we don't use os.path.join to enable firebase to create folders
    path = "dataset"+"/"+customer_name+"/"+project_name
    for imgName in os.listdir(path):
        imgName = path+"/"+imgName
        if os.path.isfile(imgName):
            blob = storage.bucket(os.environ['FIRESTORAGE_BUCKET']).blob(imgName) # intended name of file in Firebase Storage
            blob.upload_from_filename(imgName) # path to file on local disk
        else:
            # imgName is a directory
            for img in os.listdir(imgName):
                img = imgName+"/"+img
                blob = storage.bucket(os.environ['FIRESTORAGE_BUCKET']).blob(img) # intended name of file in Firebase Storage
                blob.upload_from_filename(img) # path to file on local disk 

def uploadRetrievedImages(customer_name, project_name):
    try:
        p = Process(target=uploadRetrievedImagesCore, args=(customer_name, project_name))
        p.start()
    except Exception as e:
        print("Error when uploading to firebase: %s" %e)




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
    return(blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET'))
