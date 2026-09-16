import paho.mqtt.client as mqtt
from mqtt_init import *

client = mqtt.Client("Lights_Relay_Node")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Relay connected. Waiting for commands...")
        # Subscribe to the relay topic exactly when connected
        client.subscribe(topic_relay)
    else:
        print("Connection failed. Code:", rc)

def on_message(client, userdata, msg):
    command = msg.payload.decode("utf-8")
    print(f"Received command on {msg.topic}: {command}")
    
    # Check what command was received
    if command == "LIGHTS_ON":
        print("--> RELAY ACTIVATED: Calming lights are ON.")
    elif command == "LIGHTS_OFF":
        print("--> RELAY DEACTIVATED: Calming lights are OFF.")

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_ip, broker_port)
print(f"Lights Relay emulator started. Subscribed to: {topic_relay}")

try:
    # loop_forever() keeps the script running and listening for messages
    client.loop_forever() 
except KeyboardInterrupt:
    print("Relay emulator stopped.")
    client.disconnect()