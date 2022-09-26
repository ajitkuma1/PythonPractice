import requests
import json 
import pprint 

# 1 Authenticate 
# 2 Send Request 
userId = "arista"
password = "aristaqyk0"
global cloudVision
cloudVision = "https://cloud-vision-demo-1-31c471ed.topo.testdrive.arista.com"

def cloudVisionLogin(userId, password):
    login_uri = cloudVision + "/cvpservice/login/authenticate.do"
    headers = {
        'content-type' : 'application/json'
        }
    login = requests.request("POST", login_uri, auth=(userId, password ))
    auth_token = login.json()['cookie']['Value']
    return auth_token

def getDevices (token):
    devicesEndpoints = cloudVision+ "/cvpservice/inventory/devices"
    headers = {
        "Authorization": 'Bearer ' + token,
        "Cookie": 'access_token=' + token
    }
    deviceList = requests.request("GET", devicesEndpoints, headers=headers)
    return deviceList.json()

def addConfig(token):
    configEP = cloudVision + "/cvpservice/configlet/addConfiglet.do"
    headers = {
        'Authorization': 'Bearer ' + token,
        'Cookie': 'access_token=' + token
    }
    data = {"config": "hostname Test", "name": "sampleConfigLet"
    }
    addingConfiglet = requests.request("POST", configEP, headers=headers, json=data)
    return addingConfiglet

pprint.pprint(getDevices(cloudVisionLogin(userId, password)))
print(addConfig(cloudVisionLogin(userId, password)))