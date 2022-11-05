import sys, time

from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod, CloudToDeviceMethodResult, Twin

CONNECTION_STRING = "HostName=ADAM3600.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=ORKd4f9ro76W1M2uTXSp869Mrni7sz+4/gkEC/DuHU0="
DEVICE_ID = "ADAM-3600"

METHOD_NAME = "rebootDevice"
METHOD_PAYLOAD = "{\"method_number\":\"42\"}"
TIMEOUT = 60
WAIT_COUNT = 10

def iothub_devicemethod_sample_run():
    try:
        # Create IoTHubRegistryManager
        registry_manager = IoTHubRegistryManager(CONNECTION_STRING)

        print ( "" )
        print ( "Invoking device to reboot..." )

        # Call the direct method.
        deviceMethod = CloudToDeviceMethod(method_name=METHOD_NAME, payload=METHOD_PAYLOAD)
        response = registry_manager.invoke_device_method(DEVICE_ID, deviceMethod)

        print ( "" )
        print ( "Successfully invoked the device to reboot." )

        print ( "" )
        print ( response.payload )

        while True:
            print ( "" )
            print ( "IoTHubClient waiting for commands, press Ctrl-C to exit" )

            status_counter = 0
            while status_counter <= WAIT_COUNT:
                twin_info = registry_manager.get_twin(DEVICE_ID)

                if twin_info.properties.reported.get("rebootTime") != None :
                    print ("Last reboot time: " + twin_info.properties.reported.get("rebootTime"))
                else:
                    print ("Waiting for device to report last reboot time...")

                time.sleep(5)
                status_counter += 1

    except Exception as ex:
        print ( "" )
        print ( "Unexpected error {0}".format(ex) )
        return
    except KeyboardInterrupt:
        print ( "" )
        print ( "IoTHubDeviceMethod sample stopped" )

if __name__ == '__main__':
    print ( "Starting the IoT Hub Service Client DeviceManagement Python sample..." )
    print ( "    Connection string = {0}".format(CONNECTION_STRING) )
    print ( "    Device ID         = {0}".format(DEVICE_ID) )

    iothub_devicemethod_sample_run()
