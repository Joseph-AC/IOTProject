import paho.mqtt.client as mqtt
from flask import Flask, jsonify, render_template

import RFID
import LED

mqtt_broker = "192.168.1.30"  # IP of the MQTT broker (insert)
mqtt_port = 1883  
mqtt_topic_ID = "IoTProject/ID"  # The topic to subscribe  for the sensor 
mqtt_topic_LED = "IoTlab/INTENSITY"

# Define the callback function that will be called when a message is received
def on_message(client, userdata, message):
    global mqtt_message
    mqtt_message = message.payload.decode("utf-8")  # Decode the MQTT message
    if message.topic == "IoTProject/ID":
        print(f"Received ID: {mqtt_message}")
        #global userID
        RFID.set_UserID(mqtt_message)
    if message.topic =="IoTlab/INTENSITY":
        print(f"Intensity: {mqtt_message} (From {message.topic})")
        LED.set_IntensityData(int(mqtt_message))

# Set up MQTT client and callbacks
client = mqtt.Client()  # Create a new MQTT client instance
client.on_message = on_message  # Define the callback function for incoming messages

# Connect to the MQTT broker
def start_MQTT():
    client.connect(mqtt_broker, mqtt_port, 60)

    # Subscribe to the topic
    client.subscribe(mqtt_topic_ID)
    client.subscribe(mqtt_topic_LED)

    client.loop_start()
        
def stop_MQTT():
    client.loop_stop()  # Stop the MQTT client loop
    client.disconnect()  # Disconnect from the MQTT broker

