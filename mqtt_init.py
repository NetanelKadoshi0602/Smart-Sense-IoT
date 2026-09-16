import socket

# Broker settings (0 for HIT broker, 1 for HiveMQ)
broker_choice = 1 

brokers = [socket.gethostbyname('vmm1.saaintertrade.com'), socket.gethostbyname('broker.hivemq.com')]
ports = [80, 1883]

broker_ip = brokers[broker_choice]
broker_port = ports[broker_choice]

# Smart-Sense MQTT Topics
base_topic = 'smartsense/class1/'

topic_pulse = base_topic + 'pulse'
topic_panic = base_topic + 'panic_button'
topic_relay = base_topic + 'lights_relay'
topic_alarm = base_topic + 'alarms'

# Application thresholds and settings
hr_threshold = 120 # BPM
sensor_delay = 5 # seconds