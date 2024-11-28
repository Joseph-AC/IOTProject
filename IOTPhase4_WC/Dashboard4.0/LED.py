import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import asyncio
import RPi.GPIO as GPIO
import time
from time import sleep

LED = 17  
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  
GPIO.setup(LED, GPIO.OUT)

#Turning it off at the start
GPIO.output(LED, GPIO.LOW)
print("LED is OFF - Initial state.")


#Info for intensity
intensityData = 0
from Profile_Manager import userLightThreshold

loopSensor = False
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

async def led_control_loop():
    #try:
    while loopSensor:
        # Check the received MQTT message and control the LED based on the message
        if userLightThreshold < intensityData:
            print("LIGHT ON-----------------")
            GPIO.output(LED, GPIO.HIGH)  # Turn on the LED if the message indicates it is dark
            send_email()
        elif userLightThreshold > intensityData:
            print("TURN OFF-----------------")
            GPIO.output(LED, GPIO.LOW)  # Turn off the LED if the message indicates it is not dark
        sleep(1)  # Sleep for 1 second
    await asyncio.sleep(1)
    #except KeyboardInterrupt:
      #  print("Program interrupted")
    
def LEDData():
    ledData = {
        "intensity": intensityData,
    }
    return ledData

def sensorOn():
    global loopSensor
    loopSensor = True

def sensorOff():
    global loopSensor
    loopSensor = False

def set_IntensityData(mqtt_message):
    global intensityData
    intensityData = mqtt_message