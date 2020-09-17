import paho.mqtt.client as mqtt

# MQTT setup
MQTT_HOST = "192.168.43.172"
MQTT_PORT = 1883

# When connection is established
def on_connect(client, userdata, flags, rc):
    print("\nConnected with result code " + str(rc) + "\n")
    client.subscribe("/mcu/status")
    print("Subscibed to /mcu/status\n")

# When data under subscribed topic is received
def on_message(client, userdata, msg):
    str_msg = msg.payload.decode('ascii')
    data_values = str_msg.split('_')
    print(f'Room no.: {int(data_values[0])}')
    print(f'Temperature (in celcius): {float(data_values[1]):.2f}')

client = mqtt.Client(client_id="data-logger")
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_HOST, MQTT_PORT, 60)
client.loop_forever()