import paho.mqtt.client as mqtt
import time
from mqtt_init import *

# Setup MQTT client
client = mqtt.Client("Data_Manager_Node")

def log_to_db(alert_type, value):
    try:
        with open("system_db.txt", "a") as file:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"[{timestamp}] ALERT: {alert_type} - {value}\n")
        print("--> Alert saved to local database (system_db.txt)")
    except Exception as e:
        print("Failed to save to DB:", e)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Data Manager connected successfully.")
        client.subscribe(topic_pulse)
        client.subscribe(topic_panic)
        print(f"Listening to Pulse ({topic_pulse}) and Panic ({topic_panic})")
    else:
        print("Connection failed. Code:", rc)

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode("utf-8")
    
    # Handle Pulse Sensor Data
    if topic == topic_pulse:
        try:
            bpm = int(payload.split(":")[1])
            if bpm > hr_threshold:
                print(f"[ALARM] High Heart Rate! ({bpm} BPM)")
                client.publish(topic_relay, "LIGHTS_ON")
                log_to_db("High Heart Rate", f"{bpm} BPM")
        except:
            pass
            
    # Handle Panic Button Data
    elif topic == topic_panic:
        print("[ALARM] Panic Button Pressed!")
        client.publish(topic_relay, "LIGHTS_ON")
        log_to_db("Panic Button", "Pressed")

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_ip, broker_port)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Data Manager stopped.")
    client.disconnect()