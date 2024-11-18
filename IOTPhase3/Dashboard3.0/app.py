import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import RPi.GPIO as GPIO
import time
from time import sleep
import paho.mqtt.client as mqtt
from flask import Flask, jsonify, render_template


app = Flask(__name__)

LED = 17  
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  
GPIO.setup(LED, GPIO.OUT)

#Turning it off at the start
GPIO.output(LED, GPIO.LOW)
print("LED is OFF - Initial state.")

#-------------------------MQTT_SERVER----------------------------------

#Info for MQTTSettings
# MQTT Settings
mqtt_broker = ""  # IP of the MQTT broker (insert)
mqtt_port = 1883  
mqtt_topic = "IoTlab/SENSOR"  # The topic to subscribe  for the sensor itself (ON/OFF)
mqtt_topic2 = "IoTlab/INTENSITY"  # The topic to subscribe for the intensity (1023)


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
        global intensityData
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
#client.loop_start()
#-------------------------MQTT_SERVER----------------------------------

#-------------------------EMAIL----------------------------------

# Email setup
GMAIL_USER = 'seconddummytwo@gmail.com'  
GMAIL_PASSWORD = 'yucp cxwh gycz pena' 
RECEIVER_EMAIL = 'templatebuttondown@gmail.com'  


def send_email():
    """Send an email notification."""
    try:
        
        current_time = datetime.now().strftime("%H:%M")
        subject = "Light Notification"
        body = f"The Light is ON at {current_time}."
        
        # Create the email
        message = MIMEText(body)
        message["Subject"] = subject
        message["From"] = GMAIL_USER
        message["To"] = RECEIVER_EMAIL
        print("EMAIL SENDING")
        # Send email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.sendmail(GMAIL_USER, RECEIVER_EMAIL, message.as_string())
        
        print(f"Email sent: {body}")
    except Exception as e:
        print(f"Error sending email: {e}")

#-------------------------EMAIL----------------------------------

#THIS wont be used because the arduino already has that methord (its the reason why it gives ON/OFF)

# def check_light_intensity():
#     """
#     Simulate light intensity and handle LED & email logic.
#     Adjust the fixed light intensity value as needed for testing.
#     """
    
#     light_intensity = intensityData  #Reusing the intensity data
    
   
#     #print(f"Light Intensity: {light_intensity}") (this is printed already)
    
#     if light_intensity < 1600:
#         GPIO.output(LED_PIN, GPIO.HIGH)  
#         print("LED is ON - Light intensity is below threshold.")
#         send_email()  
#     else:
#         GPIO.output(LED_PIN, GPIO.LOW)  
#         print("LED is OFF - Light intensity is above threshold.")

# 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sensor-data')
def get_sensor_data():
    return jsonify({
                    'intensity': intensityData,
                })

try:
    while True:
        # Check the received MQTT message and control the LED based on the message
        if mqtt_message == "Light:ON":
            GPIO.output(LED, GPIO.HIGH)  # Turn on the LED if the message indicates it is dark
            send_email()
        elif mqtt_message == "Light:OFF":
            print("TURN OFF-----------------")
            GPIO.output(LED, GPIO.LOW)  # Turn off the LED if the message indicates it is not dark
        sleep(1)  # Sleep for 1 second

except KeyboardInterrupt:
    print("Program interrupted")
    


finally:
    # Cleanup GPIO and stop MQTT client when exiting
    GPIO.cleanup()
    client.loop_stop()  # Stop the MQTT client loop
    client.disconnect()  # Disconnect from the MQTT broker
    
if __name__ == '__main__':
    while True:
        try:
            app.run(host='0.0.0.0', port=5001)
            time.sleep(10)  # Wait for 10 seconds before the next check
        finally:
            sensor.exit()