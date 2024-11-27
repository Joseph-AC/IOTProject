import paho.mqtt.client as mqtt

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
        global userID
        userID = mqtt_message
    
def profileData():
    userData = {
        "userID": userID,
        "tempThreshold": userTempThreshold,
        "lightThreshold": userLightThreshold,
        "mqtt_message": mqtt_message
    }
    return userData
        
# Set up MQTT client and callbacks
client = mqtt.Client()  # Create a new MQTT client instance
client.on_message = on_message  # Define the callback function for incoming messages

# Connect to the MQTT broker
client.connect(mqtt_broker, mqtt_port, 60)

# Subscribe to the topic
client.subscribe(mqtt_topic)

client.loop_start()
