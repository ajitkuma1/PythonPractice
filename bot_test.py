import os
from webexteamsbot import TeamsBot
from distutils.log import error
from errno import errorcode
import requests
import json 
import pprint 
from json.decoder import JSONDecodeError
import http_cloudvision
 
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

def getDevices(devicename):
    token = cloudVisionLogin(userId, password)
    #deviceHostName = devicename
    deviceHostName = "Ajitesh-s2-leaf4"
    #deviceHostName = input("Please enter device hostname:\t")
    devicesEndpoints = cloudVision+ "/cvpservice/inventory/devices"
    deviceList = requests.request("GET", devicesEndpoints, headers=token )
    for dev in deviceList.json():  
        if deviceHostName.strip() == dev["hostname"]:
            print("Devices HOSTNAME:\t %s" %dev["hostname"])
            print("System MAC Address:\t %s" %dev["systemMacAddress"])
            validateConfigParameters = {"hostname": dev["hostname"], "netElementId": dev["systemMacAddress"]}
            return "Device net element id is {}" .format(validateConfigParameters["netElementId"])
    return "Devices is not present in the inventory"
    #return deviceList.json()[1]

# Retrieve required details from environment variables
bot_email = os.getenv("TEAMS_BOT_EMAIL")
teams_token = os.getenv("TEAMS_BOT_TOKEN")
bot_url = os.getenv("TEAMS_BOT_URL")
bot_app_name = os.getenv("TEAMS_BOT_APP_NAME")

# Create a Bot Object
bot = TeamsBot(
    bot_app_name,
    teams_bot_token=teams_token,
    teams_bot_url=bot_url,
    teams_bot_email=bot_email,
)

# A simple command that returns a basic string that will be sent as a reply
def do_something(incoming_msg):
    """
    Sample function to do some action.
    :param incoming_msg: The incoming message object from Teams
    :return: A text or markdown based reply
    """
    return "i did what you said - {}".format(incoming_msg.text)

def get_devices():
    """
    Sample function to do some action.
    :param incoming_msg: The incoming message object from Teams
    :return: A text or markdown based reply
    """
    t = http_cloudvision.cloudVisionLogin(http_cloudvision.userId, http_cloudvision.password)
    d = http_cloudvision.getDevices(t)
    return d
    #return "Configuration is  - {}".format(d)

# Add new commands to the box.
bot.add_command("do_something", "help for do something", do_something)
bot.add_command("/Get Device", "Get the devices from the inventory", getDevices)
#bot.add_command(do_something("Test"))

if __name__ == "__main__":
    # Run Bot
    bot.run(host="0.0.0.0", port=5005)
