import paho.mqtt.client as mqtt
import time
from mqtt_init import *

# Setup MQTT client
client = mqtt.Client("Panic_Button_Node")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Panic Button connected to broker.")
    else:
        print("Connection failed. Code:", rc)

client.on_connect = on_connect
client.connect(broker_ip, broker_port)
client.loop_start()

print(f"Panic Button emulator ready. Publishing to: {topic_panic}")
print("Type 'p' and press Enter to simulate a panic button press. Type 'q' to quit.")

try:
    while True:
        user_input = input(">> ")
        if user_input.lower() == 'p':
            payload = "STATUS:PANIC_PRESSED"
            print("Button pressed! Sending panic alert to broker...")
            client.publish(topic_panic, payload)
        elif user_input.lower() == 'q':
            break
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
print("Panic button emulator stopped.")