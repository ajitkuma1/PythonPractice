import requests
from requests.exceptions import ConnectionError
from urllib3.exceptions import NewConnectionError
from socket import error, gaierror
from flask import request, url_for, redirect, request, session, render_template
import json 
import pprint
import os

class CloudConnect:
    def __init__(self,userId, password, cvaddress):
        """
        
        Define cloud vision url and credentials.
        
        """
        self.cvaddress = cvaddress
        self.userId = userId
        self.password = password 
        self.app = Flask(__name__)
    
    def login(self) -> dict:
        print(self.cvaddress)
        login_uri = self.cvaddress + "/cvpservice/login/authenticate.do"
        headers = {
        'content-type' : 'application/json'
        }
        #pprint.pprint(json.loads(login.content))
        self.login = requests.request("POST", login_uri, auth=(self.userId, self.password )) 
        try: 
            if self.login.status_code == 200 and json.loads(self.login.content)['sessionId']:
                auth_token = self.login.json()['sessionId']
                headers = {
                    'Authorization': 'Bearer ' + auth_token,
                    'Cookie': 'access_token=' + auth_token
                }
                #pprint.pprint(headers)
                return headers
        except KeyError:
            return "Please pass the valid credentials. Status Code: {}".format(json.loads(self.login.content)['errorCode'])
        except requests.exceptions.ConnectionError: 
            print("Cloud vision  not up")
            return (ConnectionError)

    
    def fetchsessioninfo(self) -> str:
        """
        Fetching Login session Info to check if user is active
        """
        if self.login.status_code == 200:
            sessionInfo = {}
            sessionInfo["user"] = json.loads(self.login.content)['user']['userId']
            sessionInfo["sessionId"] = json.loads(self.login.content)['sessionId']
            sessionInfo["Expires"] = json.loads(self.login.content)['cookie']['Expires']
            sessionInfo["MaxAge"] = json.loads(self.login.content)['cookie']['MaxAge']
            return json.dumps(sessionInfo)
        else: 
            return f"Unsuccessful Login attempt, Status Code: {self.login.status_code}"


    def writeSessionInfo (self):
        parentdir = "/tmp"
        if self.login.status_code == 200:
            self.fileName =  os.path.join(parentdir, json.loads(self.login.content)['user']['userId'] + ".txt")
            print(f"Creating session state:\n User:\t{json.loads(self.login.content)['user']['userId']}\n Session Info File:\t{self.fileName} ")
            print(f"Writing user session info in {self.fileName}")
            with open (self.fileName, "w") as fd:
                fd.write(self.fetchsessioninfo())
            return self.fileName

    def checkActiveSessions(self,file):
        """ 
        Check whether the user session is active, if it is active
        get the return the session ID value. Otherwise call login function.

        :file = Username

        """
        parentdir = "/tmp"
        fileN = parentdir + file + ".txt"
        if os.path.exists(fileN):
            with open (fileN) as f:
                expireTime = json.load(f)['Expires']
                sessionId = json.load(f)['sessionId']
                maxAge = json.load(f)['MaxAge']


userId = "arista"
password = "aristaqyk0"
cloudVision = "https://cloud-vision-demo-1-31c471ed.topo.testdrive.arista.com"

a = CloudConnect(userId, password, cloudVision )
b = a.login()
c = a.writeSessionInfo()
print(b)
print(f"File path is {c}")