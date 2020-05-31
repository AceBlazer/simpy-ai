from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import base64
import os
import datetime
from search import run
from index import indexNow
import pycron
import time
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import database.database as db
from bson.objectid import ObjectId
from flask_bcrypt import Bcrypt
import json
from bson.json_util import dumps


app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
db.connect()





'''
******************************************************************
*************  Routes interacting with db (mostly for the website)
******************************************************************
'''

#get customer name, project name (later api key), given the shop url, to the frontend to  be able to call us
@app.route('/shop-info', methods=['GET'])
def shopInfo():
    try:
        url = request.args['url']
        p = db.findProjectByUrl(url)
        if p:
            c = db.findCustomerByProject(p["_id"])
            resp = {
                "customer_name": c["company"],
                "project_name": p["name"],
                "email": c["email"]
            }
            return resp
        else:
            return Response("{'error':'Cannot find a project with this URL.'}", status=500, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response("{'error':'Error occured when getting shop info.'}", status=500, mimetype='application/json')

#get cust by id or del customer by id
@app.route('/customer', methods=['GET', 'DELETE'])
def customer():
    try: 
        customer = request.args['id']
        if request.method == 'GET':
            x = db.findCustomerById(ObjectId(customer))
            if x:
                return dumps(x)
            else:
                return Response("{'error':'Customer not found.'}", status=500, mimetype='application/json')
        else:
            x = db.deleteCustomerById(ObjectId(customer))
            if x:
                return Response("customer successfully deleted.", status=200, mimetype='application/json')
            else:
                return Response("{'error':'Customer not deleted.'}", status=500, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response("{'error':'Error occured when adding/deleting customer.'}", status=500, mimetype='application/json')


#get project, add project to customerId, delete project
@app.route('/project', methods=['GET', 'POST', 'DELETE'])
def project():
    try: 
        if request.method == 'GET':
            projectId = request.args['id']
            x = db.findProjectById(projectId)
            if x:
                return dumps(x)
            else:
                return Response("{'error':'Project not found.'}", status=500, mimetype='application/json')
        elif request.method == 'POST':
            project_info = {
                "name": request.json["name"],
                "url": request.json["url"]
            }
            xproject = db.add("projects", project_info)
            print(type(xproject.inserted_id))
            x = db.addProjectToCustomer(ObjectId(request.json["customerId"]), xproject.inserted_id)
            if x:
                return Response("project successfully added.", status=200, mimetype='application/json')
            else:
                return Response("{'error':'Project not added.'}", status=500, mimetype='application/json')

        else:
            #todo: update all customers projects field if its not automatically done by pymongo
            projectId = request.args['id']
            x = db.deleteProjectById(ObjectId(projectId))
            if x:
                return Response("project successfully deleted.", status=200, mimetype='application/json')
            else:
                return Response("{'error':'Project not deleted.'}", status=500, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response("{'error':'Error occured when adding/deleting project.'}", status=500, mimetype='application/json')


#get projects of customer ID
@app.route('/projects', methods=['GET'])
def projects():
    try: 
        customerId = request.args['id']
        projects = db.findProjectsOfCustomer(ObjectId(customerId))
        if len(projects)>0:
            resp = []
            for project in projects:
                resp.append(project)
            print(resp)
            return dumps(resp)
        else:
            return Response("{'error':'No projects found.'}", status=500, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response("{'error':'Error occured when getting project.'}", status=500, mimetype='application/json')

@app.route('/register', methods=['POST'])
def register():
    try: 
        address_info = {
            "country": request.json["country"],
            "state": request.json["state"],
            "city": request.json["city"],
            "street": request.json["street"],
            "zipCode": int(request.json["zipCode"])
        }
        xaddress = db.add("addresses", address_info)
        
        customer_info = {
            "firstName": request.json["firstName"],
            "lastName": request.json["lastName"],
            "email": request.json["email"],
            "password": str(bcrypt.generate_password_hash(request.json["password"], 10).decode("utf-8")),
            "function": request.json["function"],
            "company": request.json["name"],
            "url": request.json["url"],
            "address": ObjectId(str(xaddress.inserted_id)),
            "sector": request.json["sector"],
            "specialty": request.json["specialty"],
            "tel": request.json["tel"],
            "projects": []
        }
        xcustomer = db.add("customers", customer_info)
  
        if xcustomer: 
            return Response("customer successfully added.", status=200, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response("{'error':'Error occured when registering customer.'}", status=500, mimetype='application/json')
        

@app.route('/login', methods=['POST'])
def login():
    try:
        email = request.json["email"]
        password = request.json["password"]
        x = db.findCustomerByEmail(email)
        if x:
            if bcrypt.check_password_hash(x["password"], password):
                return dumps(x)
            else:
                return Response("{'error':'Wrong credentials.'}", status=500, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response("{'error':'Error occured when finding customer.'}", status=500, mimetype='application/json')




'''
*****************************************
*************  Routes interacting with AI
*****************************************
'''

@app.route('/index', methods=['POST'])
def index():
    try:
        pathIndex = os.path.join("indexes", request.json["project_name"])
        pathIndex = os.path.join(pathIndex, request.json["customer_name"])
        pathIndex = os.path.join(pathIndex, "index.csv")
        reciever = request.json["email"]
        if not os.path.exists(os.path.dirname(pathIndex)):
                try:
                    os.makedirs(os.path.dirname(pathIndex))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
        indexNow("dataset", pathIndex)
        sendEmail(reciever, request.json["project_name"])
        #return ("Images indexed successfully.")
        return Response("Images indexed successfully.", status=200, mimetype='application/javascript')
    except Exception as e:
        print(e)
        sendErrorEmail(reciever, request.json["project_name"])
        return Response("{'error':'Error occured when indexing your images.'}", status=500, mimetype='application/javascript')


@app.route('/search', methods=['POST'])
def search():
    if request.json and len(request.json) > 0:
        try:
            base64_img = str(request.json['image']).split(',')[1]
            base64_img_bytes = base64_img.encode('utf-8')
            currentDT = datetime.datetime.now().isoformat()
            imgname = str(currentDT).replace(":","-").replace(".","_")+".jpg"
            path = os.path.join("queries", request.json["project_name"])
            path = os.path.join(path, request.json["customer_name"])
            path = os.path.join(path, imgname)
            if not os.path.exists(os.path.dirname(path)):
                try:
                    os.makedirs(os.path.dirname(path))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            with open(path, 'wb') as file_to_save:
                decoded_image_data = base64.decodebytes(base64_img_bytes)
                file_to_save.write(decoded_image_data)
                pathIndex = os.path.join("indexes", request.json["project_name"])
                pathIndex = os.path.join(pathIndex, request.json["customer_name"])
                pathIndex = os.path.join(pathIndex, "index.csv")
                similars = run(path, pathIndex)
                return {"similars": similars}
        except Exception as e:
             print(str(e))
             return Response("{'error':'Please check the image you sent.'}", status=500, mimetype='application/json')
    else:
        return Response("{'error':'Please check the image you sent.'}", status=500, mimetype='application/json')









'''
***************************************************
*************  Routes interacting with Email module
***************************************************
'''

def sendEmail(reciever, project_name):
    try:
        msg = MIMEMultipart()
        msg['from'] = "customer.simpy@gmail.com"
        msg['to'] = str(reciever)
        password = os.environ['GMPW']
        msg['subject'] = "Indexing complete"
        body = "<p>The image indexing from the project: "+project_name+" is completed successfully.</p>"
        msg.attach(MIMEText(body, "html"))
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(msg['from'], str(password))
        server.sendmail(msg['from'], msg['to'], msg.as_string())
        server.quit()
    except Exception as e:
        print(e)


def sendErrorEmail(reciever, project_name):
    try:
        print(os.environ['GMPW'])
        msg = MIMEMultipart()
        msg['from'] = "customer.simpy@gmail.com"
        msg['to'] = str(reciever)
        password = os.environ['GMPW']
        msg['subject'] = "Indexing problem"
        body = "<p>It appears to be that the image indexing for the project: "+project_name+" got an error and has not completed.</p><p>We will check that as soon as possible.</p>"
        msg.attach(MIMEText(body, "html"))
        print(msg)
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(msg['from'], str(password))
        server.sendmail(msg['from'], msg['to'], msg.as_string())
        server.quit()
    except Exception as e:
        print(e)









'''
*******************************************
*************  Routes interacting with CRON
*******************************************
'''


'''
#to leave untill later time bc crons/schedules are hard in windows
@app.route('/start_cron', methods=['POST'])
def startCron():
    '''
    


'''
@app.route('/stop_cron', methods=['POST'])
def stopCron(): '''





