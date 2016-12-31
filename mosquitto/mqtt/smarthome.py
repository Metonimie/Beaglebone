#
# SmartHome callbacks.
# Author: Denis Nutiu
#
import subprocess
import json
import copy


# Required json schema for updating Aws IoT
# {
#     "state":  {
#       "reported": {
#           "smarthome": {
#               "denis_room": {
#                   "temperature":24,
#                   "humidity":43
#               }
#           }
#        }
#     }
# }
JSON_SCHEMA = {"state": {"reported": {"smarthome":{}}}}

# Do not include forward slash!
SCRIPT_PATH = "/home/denis/awspy"

def dump(text):
    file = open("data.json", "w")
    file.write(text)
    file.close()

def call_script(name):
    """
        This function will execute a shell script and pass the params to it.
        Script must have #!/bin/sh also everything must be absolute in it.
    :param name: The name of the shell script
    :param params: The argument vector as a string, that will be passed to the shell script.
    """

    path = "{}/{}".format(SCRIPT_PATH, name)
    try:
        subprocess.call(path)
    except Exception as e:
        print("Something bad happened.")
        print(e)

def denis_room_aws(client, userdata, message):
    print("Topic {}".format(message.topic))
    print("Payload: {}".format(message.payload))
    payload = message.payload.decode()
    jsonObject = json.loads(payload)

    # Extract the values from the json.
    temperature = jsonObject["temperature"]
    humidity    = jsonObject["humidity"]

    # Create new json
    newJson = copy.deepcopy(JSON_SCHEMA)
    newJson["state"]["reported"]["smarthome"]["denis_room"] \
        = { "temperature" : temperature, "humidity" : humidity }
    encodedJson = json.dumps(newJson)

    print("Encoded payload: {}".format(encodedJson))
    #Dump to file
    dump(encodedJson)

    # Call the script that updates the shadow on AwS IoT
    call_script("updateShadow.sh")
