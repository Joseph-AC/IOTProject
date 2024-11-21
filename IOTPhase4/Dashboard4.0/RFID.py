mqtt_broker = ""  # IP of the MQTT broker (insert)
mqtt_port = 1883  
mqtt_topic = "IoTlab/RFID"  # The topic to subscribe  for the sensor itself (ON/OFF)


#Info for intensity + MQTT message
intensityData = 0
mqtt_message = ""

# Define the callback function that will be called when a message is received
def on_message(client, userdata, message):
    global mqtt_message
    mqtt_message = message.payload.decode("utf-8")  # Decode the MQTT message
    if message.topic !="IoTlab/INTENSITY":
        print(f"Received message: {mqtt_message} on topic: {message.topic}")
    else:
        print(f"Intensity: {mqtt_message} (From {message.topic}) (2000 = treshold)")
        #this could be used to translate it to % for the web
        
# Set up MQTT client and callbacks
client = mqtt.Client()  # Create a new MQTT client instance
client.on_message = on_message  # Define the callback function for incoming messages

# Connect to the MQTT broker
client.connect(mqtt_broker, mqtt_port, 60)

# Subscribe to the topic
client.subscribe(mqtt_topic)