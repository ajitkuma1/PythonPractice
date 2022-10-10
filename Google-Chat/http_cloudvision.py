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
token = getDevices(cloudVisionLogin(userId, password) 

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

tok = getDevices(cloudVisionLogin(userId, password) 
global tok
def getDevices():
    deviceHostName = "Ajitesh-s2-leaf4"
    #deviceHostName = input("Please enter device hostname:\t")
    devicesEndpoints = cloudVision+ "/cvpservice/inventory/devices"
    deviceList = requests.request("GET", devicesEndpoints, headers=tok )
    for dev in deviceList.json():  
        if deviceHostName.strip() == dev["hostname"]:
            print("Devices HOSTNAME:\t %s" %dev["hostname"])
            print("System MAC Address:\t %s" %dev["systemMacAddress"])
            validateConfigParameters = {"hostname": dev["hostname"], "netElementId": dev["systemMacAddress"]}
            return validateConfigParameters
    return "Devices is not present in the inventory"
    #return deviceList.json()[1]
    

def addConfig():
    configEP = cloudVision + "/cvpservice/configlet/addConfiglet.do"
    data = {"config": "hostname  Ajitesh-s2-leaf4 \n interface eth10 \n ip address 1.1.1.1/32 \n" \
                        , "name": "sampleConfigLet1"
    }
    addingConfiglet = requests.request("POST", configEP, headers=tok, json=data)
    return addingConfiglet

def getConfiglet():
    getConfigletEndpoint = cloudVision + "/cvpservice/configlet/getConfigletByName.do"
    configLet = requests.request("GET", getConfigletEndpoint, headers=tok, params={"name" : "sampleConfigLet1"})
    return configLet

def validateConfiglet():
    confLetEP = cloudVision + "/cvpservice/configlet/validateConfig.do"
    netElement = getDevices(cloudVisionLogin(userId, password))
    token["Content-Type"]="text/plain" # Adding content type in the token
    payload = {
        "config": "hostname ABC\n interface e1\n ip address 1.1.1.1/24\n",
        "netElementId": netElement["netElementId"]
    }
    try:
        validate = requests.request("POST", confLetEP, headers=tok, data=json.dumps(payload))
        if validate.status_code == 200:
            v = json.loads(validate.content)
            pprint.pprint(v)
            try:
                if v["errors"][0]["error"]:
                    print("please correct the following Error:", v["errors"][0]["error"])  
            except KeyError:
                print("Configuration is good to apply")
                print(v['result'][0]['messages'])
    except TypeError:
        raise("Object is not subscriptable")
#devices = getDevices(cloudVisionLogin(userId, password))


#pprint.pprint(getDevices(cloudVisionLogin(userId, password)))
#pprint.pprint(validateConfiglet(cloudVisionLogin(userId, password)))
#pprint.pprint(addConfig(cloudVisionLogin(userId, password)))
#k = (getConfiglet(cloudVisionLogin(userId, password))).content
#pprint.pprint(k)
