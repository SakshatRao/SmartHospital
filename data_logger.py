import paho.mqtt.client as mqtt
import sqlite3
from datetime import datetime

# Setup
MQTT_HOST = "192.168.43.172"
MQTT_PORT = 1883
NUM_STATUS_PER_PATIENT = 100                                        # Number of health status entries allowed per patient

# Creating an SQLite connection
conn = sqlite3.connect("SmartHospitalServer/db.sqlite3")
conn.execute('pragma foreign_keys = on')
conn.commit()
cur = conn.cursor()

# When connection is established
def on_connect(client, userdata, flags, rc):
    print("\nConnected with result code " + str(rc) + "\n")
    client.subscribe("/mcu/status")
    print("Subscibed to /mcu/status\n")

# When data under subscribed topic is received
def on_message(client, userdata, msg):

    # Process incoming data
    str_msg = msg.payload.decode('ascii')
    data_values = str_msg.split('_')
    recv_data = {
        'room_number': int(data_values[0].strip()),
        'temperature': float(data_values[1].strip()) / 10,
        'spO2': float(data_values[2].strip()) / 10,
        'bpm': float(data_values[3].strip()) / 10,
        'recorded_time': datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    }
    print(recv_data)
    
    # Identifying patient
    cur.execute("SELECT * FROM accounts_patient WHERE room_number = ?", [recv_data['room_number']])
    patient_info = cur.fetchall()
    if(len(patient_info) != 0):
        
        # Check whether health status limit has crossed
        patient_id = patient_info[0][0]
        recv_data['patient_id'] = patient_id
        cur.execute("SELECT * FROM patient_health_status WHERE patient_id = ?", [patient_id])
        patient_status = cur.fetchall()
        if(len(patient_status) < NUM_STATUS_PER_PATIENT):
            # If not crossed, add an entry into the patient's health status database
            cur.execute(
                "INSERT INTO patient_health_status (temperature, spO2, bpm, recorded_time, patient_id) VALUES (?, ?, ?, ?, ?)", [
                    recv_data['temperature'],
                    recv_data['spO2'],
                    recv_data['bpm'],
                    recv_data['recorded_time'],
                    recv_data['patient_id']
                ]
            )
            conn.commit()
        else:
            # Else, replace the earliest entry of the patient's health status database
            cur.execute("SELECT MIN(recorded_time) FROM patient_health_status WHERE patient_id = ?", [patient_id])
            min_time = cur.fetchone()[0]
            cur.execute(
                "UPDATE patient_health_status SET temperature = ?, spO2 = ?, bpm = ?, recorded_time = ? WHERE patient_id = ? AND recorded_time = ?", [
                    recv_data['temperature'],
                    recv_data['spO2'],
                    recv_data['bpm'],
                    recv_data['recorded_time'],
                    patient_id,
                    min_time
                ]
            )
            conn.commit()

# Establishing connection with MQTT Broker
client = mqtt.Client(client_id="data-logger")
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_HOST, MQTT_PORT, 60)
client.loop_forever()