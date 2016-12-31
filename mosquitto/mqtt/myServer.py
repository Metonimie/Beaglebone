import paho.mqtt.client as mqtt
import smarthome
#
# Mosquitto client for my personal BeagleBone Black.
# Author: Denis Nutiu
#

# Sensitive data make sure this doesn't end up in git.
client_id       = 'a'
client_username = 'b'
client_password = 'c'

server_address = 'd'
server_port    = 8883

# Invalid path will raise OSError.
certificate_path = '/etc/ssl/certs/ca-certificates.crt'

subscription_dict = {
    "smarthome/#" : smarthome.denis_room_aws
}

def on_connect(client, userdata, flags, rc):
    print("Connection established: {}".format(server_address))
    for topic, listener in subscription_dict.items():
        client.subscribe(topic)
        client.message_callback_add(topic, listener)

def on_disconnect(client, userdata, rc):
    print("Disconnect, reason: " + str(rc))
    print("Disconnect, reason: " + str(client))

client = mqtt.Client(client_id)

# If we use encrypted connection set the certificates.
if server_port == 8883:
    client.tls_set(certificate_path)

# Setting the username and password.
client.username_pw_set(client_username, client_password)

# Setting the connect and disconnect handlers.
client.on_connect = on_connect
client.on_disconnect = on_disconnect

client.connect(server_address, server_port)

# Handles reconnecting
client.loop_forever()
