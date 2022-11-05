# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from services.pbiembedservice import PbiEmbedService
from utils import Utils
from flask import Flask, render_template, send_from_directory, request, make_response
import json
import os

import sys, time

from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod, CloudToDeviceMethodResult, Twin

CONNECTION_STRING = "HostName=ADAM3600.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=ORKd4f9ro76W1M2uTXSp869Mrni7sz+4/gkEC/DuHU0="
DEVICE_ID = "ADAM-3600"

#METHOD_NAME = "rebootDevice"
METHOD_NAME = ""

#METHOD_PAYLOAD = "{\"method_number\":\"42\"}"
METHOD_PAYLOAD = ""

TIMEOUT = 60
WAIT_COUNT = 10

def iot_invoke_run(METHOD_NAME, METHOD_PAYLOAD ):
    try:
        # Create IoTHubRegistryManager
        registry_manager = IoTHubRegistryManager(CONNECTION_STRING)

        print ( "" )
        print ( "Invoking device..." )

        # Call the direct method.
        deviceMethod = CloudToDeviceMethod(method_name=METHOD_NAME, payload=METHOD_PAYLOAD)
        response = registry_manager.invoke_device_method(DEVICE_ID, deviceMethod)

        print ( "" )
        print ( "Successfully invoked the device." )

        print ( "" )
        print ( response.payload )

        while True:
            print ( "" )
            print ( "IoTHubClient waiting for commands, press Ctrl-C to exit" )

            status_counter = 0
            while status_counter <= WAIT_COUNT:
                twin_info = registry_manager.get_twin(DEVICE_ID)

                if twin_info.properties.reported.get("rebootTime") != None :
                    print ("Get current time: " + twin_info.properties.reported.get("rebootTime"))
                else:
                    print ("Waiting for device to invoke...")

                time.sleep(5)
                status_counter += 1

    except Exception as ex:
        print ( "" )
        print ( "Unexpected error {0}".format(ex) )
        return

        
#####################################################

# Initialize the Flask app
app = Flask(__name__)

# Load configuration
app.config.from_object('config.BaseConfig')
@app.route('/operator/')
def operator():
    if request.authorization and request.authorization.username == 'operator':
        return render_template('operator.html')
    elif request.authorization and request.authorization.username == 'admin' and request.authorization.password == 'admin123':
        return render_template('operator.html')
    else:
        return make_response('Could not verifiy!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})
    return render_template('operator.html')
@app.route('/admin/')
def admin():
    if request.authorization and request.authorization.username == 'admin' and request.authorization.password == 'admin123':
        return render_template('admin.html')
    else:
        return make_response('Could not verifiy!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})
    return render_template('admin.html')

@app.route('/control/', methods=['GET', 'POST'])
def control():
    if request.authorization and request.authorization.username == 'admin' and request.authorization.password == 'admin123':
        if request.method == 'POST':
            if request.form.get('b1') == 'START':
                iot_invoke_run("startInvoke", "\"method_number\":\"1\"}")
                               
            elif  request.form.get('b3') == 'STOP':
                iot_invoke_run("stopInvoke", "\"method_number\":\"2\"}")
                
            elif  request.form.get('b5') == 'RESET':
                iot_invoke_run("resetInvoke", "\"method_number\":\"3\"}")
                
            elif  request.form.get('b7') == 'MQ269-FLUSH':
                iot_invoke_run("flushInvoke", "\"method_number\":\"4\"}")
                
            elif  request.form.get('b8') == 'MQ161-FORWARD':
                iot_invoke_run("forwardInvoke", "\"method_number\":\"5\"}")
                
            elif  request.form.get('b9') == 'MQ157-MANUAL':
                iot_invoke_run("manualInvoke", "\"method_number\":\"6\"}")

            elif  request.form.get('b10') == 'MQ183-AUTOMATIC':
                iot_invoke_run("automaticInvoke", "\"method_number\":\"7\"}")

            return render_template('control.html')
    else:
        return make_response('Could not verifiy!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})
    return render_template('control.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    '''Returns a static HTML page'''
    return render_template('index.html')

@app.route('/getembedinfo', methods=['GET'])
def get_embed_info():
    '''Returns report embed configuration'''

    config_result = Utils.check_config(app)
    if config_result is not None:
        return json.dumps({'errorMsg': config_result}), 500

    try:
        embed_info = PbiEmbedService().get_embed_params_for_multiple_reports(app.config['WORKSPACE_ID'], app.config['REPORT_ID'])
        return embed_info
    except Exception as ex:
        return json.dumps({'errorMsg': str(ex)}), 500

@app.route('/favicon.ico', methods=['GET'])
def getfavicon():
    '''Returns path of the favicon to be rendered'''

    return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run()




