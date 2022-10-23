# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from services.pbiembedservice import PbiEmbedService
from utils import Utils
from flask import Flask, render_template, send_from_directory, request
import json
import os

import random
import time
import sys
from azure.iot.hub import IoTHubRegistryManager

#####################################################

MESSAGE_COUNT = 1
MSG_TXT = "{\"Service Client Hydraulics Update C2D\": %.2f}"

#CONNECTION_STRING = "HostName=ADAM3600.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=ORKd4f9ro76W1M2uTXSp869Mrni7sz+4/gkEC/DuHU0="
CONNECTION_STRING = "HostName=ADAM3600.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=lsQVvrXgkumu25vlvYczR6BgCNpi1nK9SgykxCpEWlY="
DEVICE_ID = "ADAM-3600"

def iothub_run(dev_str, my_val):
    try:
        # Create IoTHubRegistryManager
        registry_manager = IoTHubRegistryManager(CONNECTION_STRING)

        for i in range(0, MESSAGE_COUNT):

            message = 'Device: {} %d'.format(dev_str)
            print(message)
            #DUMMY_VAR_BOOL = val
            print ( 'Sending Beacon: {0}'.format(i) )
            data = message %(my_val)
            print ( 'LOGIC STATE: {}'.format(data) )

            props={}
            # optional: assign system properties
            props.update(messageId = "message_%d" % i)
            props.update(correlationId = "correlation_%d" % i)
            props.update(contentType = "application/json")

            # optional: assign application properties
            prop_text = "PropMsg_%d" % i
            props.update(testProperty = prop_text)

            registry_manager.send_c2d_message(DEVICE_ID, data, properties=props)


    except Exception as ex:
        print (ex)
        return




#####################################################

# Initialize the Flask app
app = Flask(__name__)

# Load configuration
app.config.from_object('config.BaseConfig')
@app.route('/operator/')
def operator():
    return render_template('operator.html')
@app.route('/admin/')
def admin():
    return render_template('admin.html')

@app.route('/control/', methods=['GET', 'POST'])
def control():

    if request.method == 'POST':
        if request.form.get('b1') == 'START':
            iothub_run('START', 1)
            
        elif  request.form.get('b3') == 'STOP':
            iothub_run('STOP', 1)
    
        elif  request.form.get('b5') == 'RESET':
            iothub_run('RESET', 1)
           
        elif  request.form.get('b7') == 'MQ269-FLUSH':
            iothub_run('MQ269 FLUSH', 1)
           
        elif  request.form.get('b8') == 'MQ161-FORWARD':
            iothub_run('MQ161 FORWARD', 1)

        elif  request.form.get('b9') == 'MQ157-MANUAL':
            iothub_run('MQ157 MANUAL', 1)
        elif  request.form.get('b10') == 'MQ183-AUTOMATIC':
            iothub_run('MQ183 AUTOMATIC', 1)
    
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




