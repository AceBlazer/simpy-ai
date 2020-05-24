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
import os


app = Flask(__name__)
CORS(app)


@app.route('/index', methods=['POST'])
def index():
    try:
        pathIndex = os.path.join("indexes", "project_name")
        pathIndex = os.path.join(pathIndex, "customer_name")
        pathIndex = os.path.join(pathIndex, "index.csv")
        reciever = "saanoun.jasser21@gmail.com"
        if not os.path.exists(os.path.dirname(pathIndex)):
                try:
                    os.makedirs(os.path.dirname(pathIndex))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
        indexNow("dataset", pathIndex)
        sendEmail(reciever)
        return ("Images indexed successfully.")
    except:
        sendErrorEmail(reciever)
        return Response("{'error':'Error occured when indexing your images.'}", status=500, mimetype='application/json')


@app.route('/search', methods=['POST'])
def search():
    if request.json and len(request.json) > 0:
        try:
            base64_img = str(request.json['image']).split(',')[1]
            base64_img_bytes = base64_img.encode('utf-8')
            currentDT = datetime.datetime.now().isoformat()
            imgname = str(currentDT).replace(":","-").replace(".","_")+".jpg"
            path = os.path.join("queries", "project_name")
            path = os.path.join(path, "customer_name")
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
                pathIndex = os.path.join("indexes", "project_name")
                pathIndex = os.path.join(pathIndex, "customer_name")
                pathIndex = os.path.join(pathIndex, "index.csv")
                similars = run(path, pathIndex)
                return {"similars": similars}
        except Exception as e:
             print(str(e))
             return Response("{'error':'Please check the image you sent.'}", status=500, mimetype='application/json')
    else:
        return Response("{'error':'Please check the image you sent.'}", status=500, mimetype='application/json')




def sendEmail(reciever):
    try:
        print(os.environ['GMPW'])
        msg = MIMEMultipart()
        msg['from'] = "customer.simpy@gmail.com"
        msg['to'] = str(reciever)
        password = os.environ['GMPW']
        msg['subject'] = "Indexing complete"
        body = "<p>The image indexing from the project: xxx is completed successfully.</p>"
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


def sendErrorEmail(reciever):
    try:
        print(os.environ['GMPW'])
        msg = MIMEMultipart()
        msg['from'] = "customer.simpy@gmail.com"
        msg['to'] = str(reciever)
        password = os.environ['GMPW']
        msg['subject'] = "Indexing problem"
        body = "<p>It appears to be that the image indexing for the project: xxx got an error and has not completed.</p><p>We will check that as soon as possible.</p>"
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
#to leave untill later time bc crons/schedules are hard in windows
@app.route('/start_cron', methods=['POST'])
def startCron():
    '''
    


'''
@app.route('/stop_cron', methods=['POST'])
def stopCron(): '''





