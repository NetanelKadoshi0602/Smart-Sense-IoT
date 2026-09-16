import paho.mqtt.client as mqtt
import time
import random
from mqtt_init import *

# Setup MQTT client
client = mqtt.Client("Pulse_Sensor_Node") 

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker successfully!")
    else:
        print("Failed to connect. Return code:", rc)

client.on_connect = on_connect
client.connect(broker_ip, broker_port)
client.loop_start()

print(f"Starting pulse simulation. Publishing to topic: {topic_pulse}")

try:
    while True:
        # Simulate pulse (mostly normal, sometimes high stress)
        current_pulse = random.randint(70, 90)
        
        # 20% chance to simulate a stress event for testing
        if random.random() > 0.8:
            current_pulse = random.randint(125, 140)
            
        payload = f"BPM:{current_pulse}"
        print(f"Sending: {payload}")
        
        client.publish(topic_pulse, payload)
        time.sleep(sensor_delay) 

except KeyboardInterrupt:
    print("Simulation stopped by user.")

client.loop_stop()
client.disconnect()