import asyncio
import RPi.GPIO as GPIO
import time
from time import sleep

LED = 27  
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  
GPIO.setup(LED, GPIO.OUT)

#Turning it off at the start
GPIO.output(LED, GPIO.LOW)
print("LED is OFF - Initial state.")
 
#Info for intensity
intensityData = 0
from Profile_Manager import userLightThreshold
import Email_Manager
loopSensor = False


#-------------------------EMAIL----------------------------------

def led_control_loop():
    #try:
    print("running loop")
    #while loopSensor:
        # Check the received MQTT message and control the LED based on the message
    if userLightThreshold > intensityData:
        print("LIGHT ON-----------------")
        GPIO.output(LED, GPIO.HIGH)  # Turn on the LED if the message indicates it is dark
        asyncio.run(Email_Manager.send_email_LED())
    elif userLightThreshold < intensityData:
        print("TURN OFF-----------------")
        GPIO.output(LED, GPIO.LOW)  # Turn off the LED if the message indicates it is not dark
    #sleep(1)  # Sleep for 1 second
    #await asyncio.sleep(1)
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
    led_control_loop()