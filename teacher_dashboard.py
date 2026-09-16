import tkinter as tk
from tkinter import font
import paho.mqtt.client as mqtt
import time
from mqtt_init import *

# --- Global Cooldown Variable (10 minutes snooze for sport class) ---
last_cleared_time = 0
COOLDOWN_SECONDS = 600  # 10 minutes (10 * 60 seconds)

# --- MQTT Setup ---
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("GUI Connected to broker")
        client.subscribe(topic_pulse)
        client.subscribe(topic_panic)
    else:
        print("Connection failed")

def on_message(client, userdata, msg):
    global last_cleared_time
    topic = msg.topic
    payload = msg.payload.decode("utf-8")
    
    # Update the pulse label
    if topic == topic_pulse:
        try:
            bpm = int(payload.split(":")[1])
            lbl_bpm_value.config(text=f"HEART RATE: {bpm} BPM")
            
            # Check if we are currently inside the 10-minute cooldown (Sport class mode)
            in_cooldown = (time.time() - last_cleared_time) < COOLDOWN_SECONDS
            
            if bpm > hr_threshold and not in_cooldown:
                # High BPM outside of sport class -> Trigger Red Alert!
                lbl_alert.config(text="ALERT: STUDENT 2 HIGH BPM DETECTED!", fg="#D8000C", bg="#FFD2D2")
                alert_frame.config(bg="#FFD2D2")
                lbl_bpm_value.config(bg="#FFD2D2", fg="#D8000C")
                
            elif bpm > hr_threshold and in_cooldown:
                # High BPM DURING sport class (Snoozed) -> Show calm blue/neutral status
                lbl_alert.config(text="Status: Normal (Sport Class - Muted)", fg="#00529B", bg="#BDE5F8")
                alert_frame.config(bg="#BDE5F8")
                lbl_bpm_value.config(bg="#BDE5F8", fg="#00529B")
                
            else:
                # BPM is NORMAL (e.g. dropped back to normal range) -> Automatically turn Green!
                current_status = lbl_alert.cget("text")
                if "PANIC" not in current_status:
                    if in_cooldown:
                        lbl_alert.config(text="Status: Normal (Sport Class - Muted)", fg="#00529B", bg="#BDE5F8")
                        alert_frame.config(bg="#BDE5F8")
                        lbl_bpm_value.config(bg="#BDE5F8", fg="#00529B")
                    else:
                        lbl_alert.config(text="Status: Normal", fg="#4F8A10", bg="#DFF2BF")
                        alert_frame.config(bg="#DFF2BF")
                        lbl_bpm_value.config(bg="#DFF2BF", fg="#4F8A10")
        except:
            pass
            
    # Show panic alert (remains red until manually handled or overridden)
    elif topic == topic_panic:
        lbl_alert.config(text="ALERT: STUDENT 2 PANIC BUTTON PRESSED!", fg="#D8000C", bg="#FFD2D2")
        alert_frame.config(bg="#FFD2D2")
        lbl_bpm_value.config(bg="#FFD2D2", fg="#D8000C")

# --- Button Actions ---
def turn_lights_on():
    client.publish(topic_relay, "LIGHTS_ON")
    lbl_alert.config(text="Intervention: Calming Lights ON", fg="#00529B", bg="#BDE5F8")
    alert_frame.config(bg="#BDE5F8")
    lbl_bpm_value.config(bg="#BDE5F8", fg="#00529B")

def turn_lights_off():
    client.publish(topic_relay, "LIGHTS_OFF")
    lbl_alert.config(text="Status: Normal (Lights OFF)", fg="#4F8A10", bg="#DFF2BF")
    alert_frame.config(bg="#DFF2BF")
    lbl_bpm_value.config(bg="#DFF2BF", fg="#4F8A10")

def clear_alerts():
    global last_cleared_time
    last_cleared_time = time.time()  # Activates the 10-minute sport class snooze!
    
    lbl_alert.config(text="Status: Normal (Snoozed for 10 min)", fg="#00529B", bg="#BDE5F8")
    alert_frame.config(bg="#BDE5F8")
    lbl_bpm_value.config(bg="#BDE5F8", fg="#00529B")

def on_closing():
    client.loop_stop()
    client.disconnect()
    root.destroy()

client = mqtt.Client("Teacher_GUI")
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_ip, broker_port)
client.loop_start() 

# --- GUI Build ---
root = tk.Tk()
root.title("Smart-Sense: Teacher Dashboard")
root.geometry("800x450")
root.configure(bg="#F4F4F9")

# --- Fonts ---
header_font = font.Font(family="Segoe UI", size=16, weight="bold")
alert_font = font.Font(family="Segoe UI", size=14, weight="bold")
normal_font = font.Font(family="Segoe UI", size=11)

# --- Left Panel (Student List) ---
left_frame = tk.Frame(root, bg="#FFFFFF", width=220, relief="flat")
left_frame.pack(side="left", fill="y", padx=10, pady=10)
left_frame.pack_propagate(False) # Keep width fixed

tk.Label(left_frame, text="Students", font=header_font, bg="#FFFFFF", fg="#333333").pack(pady=15)

students = ["Student 1 (Normal)", "Student 2 (Active)", "Student 3 (Normal)", "Student 4 (Normal)"]
for s in students:
    color = "#00529B" if "Active" in s else "#555555"
    weight = "bold" if "Active" in s else "normal"
    s_font = font.Font(family="Segoe UI", size=11, weight=weight)
    tk.Label(left_frame, text=s, font=s_font, bg="#FFFFFF", fg=color).pack(anchor="w", padx=20, pady=8)

# --- Right Panel (Dashboard) ---
right_frame = tk.Frame(root, bg="#F4F4F9")
right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=10)

tk.Label(right_frame, text="Live Monitoring Dashboard", font=header_font, bg="#F4F4F9", fg="#333333").pack(pady=10)

# Alert Card
alert_frame = tk.Frame(right_frame, bg="#DFF2BF", bd=0, relief="flat")
alert_frame.pack(fill="x", pady=15, ipady=30)

lbl_alert = tk.Label(alert_frame, text="Status: Normal", font=alert_font, bg="#DFF2BF", fg="#4F8A10")
lbl_alert.pack(pady=5)

lbl_bpm_value = tk.Label(alert_frame, text="HEART RATE: -- BPM", font=header_font, bg="#DFF2BF", fg="#4F8A10")
lbl_bpm_value.pack(pady=5)

# Control Buttons
btn_frame = tk.Frame(right_frame, bg="#F4F4F9")
btn_frame.pack(pady=20)

btn_style = {"font": normal_font, "fg": "white", "width": 18, "relief": "flat", "bd": 0, "pady": 10, "cursor": "hand2"}

btn_on = tk.Button(btn_frame, text="Turn Lights ON", bg="#007BFF", activebackground="#0056b3", activeforeground="white", command=turn_lights_on, **btn_style)
btn_on.grid(row=0, column=0, padx=10)

btn_off = tk.Button(btn_frame, text="Turn Lights OFF", bg="gray", activebackground="gray", activeforeground="white", command=turn_lights_off, **btn_style)
btn_off.grid(row=0, column=1, padx=10)

btn_clear = tk.Button(btn_frame, text="Clear Alerts", bg="#28A745", activebackground="#1e7e34", activeforeground="white", command=clear_alerts, **btn_style)
btn_clear.grid(row=0, column=2, padx=10)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()