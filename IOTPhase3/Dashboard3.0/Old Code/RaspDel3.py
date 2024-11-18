import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
from time import sleep  # Import the sleep function from the time module
import paho.mqtt.client as mqtt  # Import the MQTT client library

GPIO.setwarnings(False)  # Ignore warnings for now
GPIO.setmode(GPIO.BCM)  # Use BCM addressing pin numbering

LED = 17  # Define the pin number for the LED
GPIO.setup(LED, GPIO.OUT)  # Set pin 17 to be an output pin

# MQTT Settings
mqtt_broker = "PUT_IP_HERE"  # IP of the MQTT broker (same as in your ESP32 code)
mqtt_port = 1883  # Default MQTT port
mqtt_topic = "IoTlab/SENSOR"  # The topic to subscribe to
mqtt_topic2 = "IoTlab/INTENSITY"  # The topic to subscribe to

##please make an method that converts it to 
intensityData = 0

# This will store the latest message from the MQTT broker
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
        intensityData = int(mqtt_message)
        
# Set up MQTT client and callbacks
client = mqtt.Client()  # Create a new MQTT client instance
client.on_message = on_message  # Define the callback function for incoming messages

# Connect to the MQTT broker
client.connect(mqtt_broker, mqtt_port, 60)

# Subscribe to the topic
client.subscribe(mqtt_topic)
client.subscribe(mqtt_topic2)


# Start a background thread to listen for messages
client.loop_start()

try:
    while True:
        # Check the received MQTT message and control the LED based on the message
        if mqtt_message == "Light:ON":
            GPIO.output(LED, GPIO.HIGH)  # Turn on the LED if the message indicates it is dark
        elif mqtt_message == "Light:OFF":
            GPIO.output(LED, GPIO.LOW)  # Turn off the LED if the message indicates it is not dark
        sleep(1)  # Sleep for 1 second

except KeyboardInterrupt:
    print("Program interrupted")

finally:
    # Cleanup GPIO and stop MQTT client when exiting
    GPIO.cleanup()
    client.loop_stop()  # Stop the MQTT client loop
    client.disconnect()  # Disconnect from the MQTT broker
