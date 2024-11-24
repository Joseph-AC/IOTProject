mqtt_broker = ""  # IP of the MQTT broker (insert)
mqtt_port = 1883  
mqtt_topic = "IoTProject/ID"  # The topic to subscribe  for the sensor 


#Info for intensity + MQTT message
userID = ""
userTempThreshold = 35 #base value
userLightThreshold = 2000 #base value
mqtt_message = ""

# Define the callback function that will be called when a message is received
def on_message(client, userdata, message):
    global mqtt_message
    mqtt_message = message.payload.decode("utf-8")  # Decode the MQTT message
    if message.topic == "IoTProject/ID":
        print(f"Received ID: {mqtt_message}")
        userID = mqtt_message
    # the database...
    if userID == "d62d21ae":
        userTempThreshold = 20
        userLightThreshold = 1500
        print(f"thresholds: Light({userLightThreshold}) and Temp({userTempThreshold})")
    
        
# Set up MQTT client and callbacks
client = mqtt.Client()  # Create a new MQTT client instance
client.on_message = on_message  # Define the callback function for incoming messages

# Connect to the MQTT broker
client.connect(mqtt_broker, mqtt_port, 60)

# Subscribe to the topic
client.subscribe(mqtt_topic)