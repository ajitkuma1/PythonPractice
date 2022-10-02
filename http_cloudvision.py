from distutils.log import error
from errno import errorcode
import requests
import json 
import pprint 
from json.decoder import JSONDecodeError
 
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
    headers = {
        'Authorization': 'Bearer ' + auth_token,
        'Cookie': 'access_token=' + auth_token
    }
    return headers

def getDevices (token):
    deviceHostName = input("Please enter device hostname:\t")
    devicesEndpoints = cloudVision+ "/cvpservice/inventory/devices"
    deviceList = requests.request("GET", devicesEndpoints, headers=token )
    for dev in deviceList.json():  
        if deviceHostName.strip() == dev["hostname"]:
            print("Devices HOSTNAME:\t %s" %dev["hostname"])
            print("System MAC Address:\t %s" %dev["systemMacAddress"])
            validateConfigParameters = {"hostname": dev["hostname"], "netElementId": dev["systemMacAddress"]}
            return validateConfigParameters
    print("Devices is not present in the inventory")
    #return deviceList.json()[1]
    

def addConfig(token):
    configEP = cloudVision + "/cvpservice/configlet/addConfiglet.do"
    data = {"config": "hostname  Ajitesh-s2-leaf4 \n interface eth10 \n ip address 1.1.1.1/32 \n" \
                        , "name": "sampleConfigLet1"
    }
    addingConfiglet = requests.request("POST", configEP, headers=token, json=data)
    return addingConfiglet

def getConfiglet(token):
    getConfigletEndpoint = cloudVision + "/cvpservice/configlet/getConfigletByName.do"
    configLet = requests.request("GET", getConfigletEndpoint, headers=token, params={"name" : "sampleConfigLet1"})
    return configLet

def validateConfiglet(token):
    confLetEP = cloudVision + "/cvpservice/configlet/validateConfig.do"
    netElement = getDevices(cloudVisionLogin(userId, password))
    token["Content-Type"]="text/plain" # Adding content type in the token
    #del token["Authorization"]
    payload = {
        "config": "hostname ABC\n interface e1\n ip address 1.1.1.1/32\n",
        "netElementId": netElement["netElementId"]
    }
    try:
        validate = requests.request("POST", confLetEP, headers=token, data=json.dumps(payload))
        v = json.loads(validate.content)
        print("Return valus is of type %s" ,type(validate.text))
        #print("JSON decoding has failed")
        if v["errors"][0]["error"]:
            print("please corrt the following Error:", v["errors"][0]["error"])
        else: 
            print("Configuration is good to apply")
    except TypeError:
        raise("Object is not subscriptable")
    

#devices = getDevices(cloudVisionLogin(userId, password))


#pprint.pprint(getDevices(cloudVisionLogin(userId, password)))
pprint.pprint(validateConfiglet(cloudVisionLogin(userId, password)))
#pprint.pprint(addConfig(cloudVisionLogin(userId, password)))
#k = (getConfiglet(cloudVisionLogin(userId, password))).content
#pprint.pprint(k)
