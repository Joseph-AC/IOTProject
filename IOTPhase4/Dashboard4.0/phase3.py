import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import RPi.GPIO as GPIO
import time
from time import sleep
from flask import jsonify

# GPIO setup
LED = 17  
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  
GPIO.setup(LED, GPIO.OUT)

# Turning it off at the start
GPIO.output(LED, GPIO.LOW)
print("LED is OFF - Initial state.")

# Info for intensity
intensityData = 0
from RFID import userTempThreshold  # User temperature threshold
from RFID import userLightThreshold  # User light threshold

#-------------------------EMAIL----------------------------------

# Email setup
GMAIL_USER = 'seconddummytwo@gmail.com'  
GMAIL_PASSWORD = 'yucp cxwh gycz pena' 
RECEIVER_EMAIL = 'templatebuttondown@gmail.com'  

def send_email():
    """Send an email notification when LED is turned on."""
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

#-------------------------LED Control----------------------------------

def led_control():
    """Control LED based on intensity data and user threshold."""
    global intensityData
    if userLightThreshold < intensityData:
        print("LIGHT ON-----------------")
        GPIO.output(LED, GPIO.HIGH)  # Turn on the LED if intensity is below threshold
        send_email()  # Send email if the LED is turned on
    elif userLightThreshold > intensityData:
        print("TURN OFF-----------------")
        GPIO.output(LED, GPIO.LOW)  # Turn off the LED if intensity is above threshold

def set_intensity_data(mqtt_message):
    """Set the intensity data received from MQTT."""
    global intensityData
    intensityData = mqtt_message

def get_led_intensity():
    """Return the current LED intensity."""
    return {"intensity": intensityData}
