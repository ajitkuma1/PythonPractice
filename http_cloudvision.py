import requests
import json 
import pprint 

# 1 Authenticate 
# 2 Send Request 

def cloudVisionLogin(cloudVision, userId, password):
    login_uri = cloudVision + "cvpservice/login/authenticate.do"
    headers = {
        'content-type' : 'application/json'
        }
    login = requests.request("POST", login_uri, auth=(userId, password ))
    auth_token = login.json()['cookie']['Value']
    return auth_token

def getDevices (token):
    devicesEndpoints ="https://cloud-vision-demo-1-31c471ed.topo.testdrive.arista.com/cvpservice/inventory/devices"
    headers = {
        "Authorization": 'Bearer ' + token,
        "Cookie": 'access_token=' + token
    }
    deviceList = requests.request("GET", devicesEndpoints, headers=headers)
    return deviceList.json()

#uri = "https://cloud-vision-demo-1-31c471ed.topo.testdrive.arista.com/cvpservice/login/authenticate.do"
cv = "https://cloud-vision-demo-1-31c471ed.topo.testdrive.arista.com"
userId = "arista"
password = "aristaqyk0"

pprint.pprint(getDevices(cloudVisionLogin(cv, userId, password)))