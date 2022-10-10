from distutils.log import error
from errno import errorcode
import json 
import pprint 
from json.decoder import JSONDecodeError
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import requests
from datetime import timedelta 

userId = "arista"
password = "aristaqyk0"
global cloudVision
cloudVision = "https://cloud-vision-demo-1-31c471ed.topo.testdrive.arista.com"
app = Flask(__name__)
port = 5005
app.secret_key = "aaaa12333122"
#SECRET_KEY = 'development key'

#app.config.from_object(__name__)
#app.config.update(SECRET_KEY='osd(99092=36&462134kjKDhuIS_d23',ENV='development')
#Session(app) 
#app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_TYPE"] = "filesystem"



@app.route("/authUser", methods=["GET", "POST"])
def authenticateUsers():
    #global is_authenticated 
    #is_authenticated = "unauthenticated"
    global loginToken
    if request.method == "GET" and session["logged_in"] == False:
        return render_template ("login.html")
    elif request.method == "POST" and request.form["username"] and request.form["password"]:
        loginToken = cloudVisionLogin(request.form["username"], request.form["password"])
        print("Login Token: {}".format(loginToken))
        #is_authenticated = "authenticated"
        session["logged_in"] = True
        return redirect(url_for(session["url"]))
    elif session["logged_in"]:
        #is_authenticated = "authenticated"
        return redirect(url_for(session["url"]))


@app.route("/", methods=["GET", "POST"])
def login():
    global loginToken
    if request.method == "GET":
        return render_template ("login.html")
    elif request.form["username"] and request.form["password"]:
        loginToken= cloudVisionLogin(request.form["username"], request.form["password"])
        session["loginToken"] = loginToken
        session["logged_in"] = True
        if loginToken["Authorization"] != "" and loginToken["Cookie"] != "":
            return redirect(url_for('returnRadios'))

@app.route("/loginTemplate", methods=["GET", "POST"])
def loginTemp():
    if request.method == "GET":
        return render_template("login.html")

def cloudVisionLogin(userId, password):
    print("I am cloud vision")
    login_uri = cloudVision + "/cvpservice/login/authenticate.do"
    headers = {
        'content-type' : 'application/json'
        }
    login = requests.request("POST", login_uri, auth=(userId, password ))
    print("Login:".format(login ))
    try:
        if login.status_code == 200 and json.loads(login.content)['sessionId'] != "":
            auth_token = login.json()['cookie']['Value']
            headers = {
                'Authorization': 'Bearer ' + auth_token,
                'Cookie': 'access_token=' + auth_token
            }
            session["loginToken"] = headers
            print(headers)
            return headers
    except KeyError:
        return "Please pass the valid credentials. Status Code: {}".format(json.loads(login.content)['errorCode'])

@app.route("/options", methods=["GET", "POST"])
def returnRadios():
    error = None
    if request.method == "GET":
        return render_template ("radio.html")
    elif request.method == "POST":
        print(request.form)
        if request.form["operations"] == "Validate Configuration":
            return redirect(url_for('validateConfig'))
        elif request.form["operations"] == "Configure Configlet":
            return redirect(url_for ('addConfig'))
        else:
            return error

def getDevices(deviceName):
    deviceHostName = deviceName
    #deviceHostName = "Ajitesh-s2-leaf4"
    #deviceHostName = input("Please enter device hostname:\t")
    devicesEndpoints = cloudVision+ "/cvpservice/inventory/devices"
    deviceList = requests.request("GET", devicesEndpoints, headers=session["loginToken"] )
    for dev in deviceList.json():  
        if deviceHostName.strip() == dev["hostname"]:
            print("Devices HOSTNAME:\t %s" %dev["hostname"])
            print("System MAC Address:\t %s" %dev["systemMacAddress"])
            validateConfigParameters = {"hostname": dev["hostname"], "netElementId": dev["systemMacAddress"]}
            return validateConfigParameters
    return "Devices is not present in the inventory"
    #return deviceList.json()[1]

@app.route("/add_configlet", methods=["GET","POST"])
def addConfig():
    configEP = cloudVision + "/cvpservice/configlet/addConfiglet.do"
    session["url"] = "addConfig"
    if request.method == "GET" and session.get("logged_in"):
        return render_template ("Configlet.html")
    elif request.method == "GET" and session.get("logged_in") == False:
        return redirect (url_for("authenticateUsers"))
    elif request.method == "POST" and session.get("logged_in") == False:
        return redirect (url_for("authenticateUsers"))
    if request.method == "POST" and session.get("logged_in"):
        data = {"config": request.form['freeform'], "name": request.form['cname']}
        addingConfiglet = requests.request("POST", configEP, headers=session["loginToken"], json=data)
        if addingConfiglet.status_code == 200:
            return "Configlet {} Added Successfully".format(request.form['cname'])
        else: 
            return addingConfiglet.status_code
    return 'Configlet could not be added'

@app.route("/validateConfig", methods=["GET","POST"])
def validateConfig():
    session["url"] = "validateConfig"
    confLetEP = cloudVision + "/cvpservice/configlet/validateConfig.do"
    
    if request.method == "GET" and session.get("logged_in"):
        return render_template ("ValidateConfig.html")
    elif request.method == "GET" and session.get("logged_in") == False:
        return redirect (url_for("authenticateUsers"))
    elif request.method == "POST" and session.get("logged_in") == False:
        return redirect (url_for("authenticateUsers"))
    session["loginToken"]["Content-Type"]="text/plain" # Adding content type in the token
    #payload = {"config": request.form['configuration'], "name": request.form['dname']}
   
    try:
        if request.method == "POST" and session.get("logged_in"):
            netElement = getDevices(request.form["dname"])
            #payload = {
            #    "config": "hostname ABC\n interface e1\n ip address 1.1.1.1/24\n",
            #    "netElementId": netElement["netElementId"]
            #    }   
            #payload = {"config": request.form['configuration'], "name": request.form['dname']}
            payload = {"config": request.form['configuration'], "netElementId": netElement["netElementId"]}
            validate = requests.request("POST", confLetEP, headers=session["loginToken"], data=json.dumps(payload))
            if validate.status_code == 200:
                v = json.loads(validate.content)
                pprint.pprint(v)
                #return v
                try:
                    if v["errors"][0]["error"]:
                        return ("please correct the following Error {}:".format(v["errors"][0]["error"]))
                except KeyError:
                    print("Configuration is good to apply")
                    return (v['result'][0]['messages'])
    except TypeError:
        raise("Object is not subscriptable")


    
app.run(host="0.0.0.0", port=port, debug=True)