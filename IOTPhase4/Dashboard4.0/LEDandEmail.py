import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import RPi.GPIO as GPIO
import time
from time import sleep

#app = Flask(__name__)

LED = 17  
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  
GPIO.setup(LED, GPIO.OUT)

#Turning it off at the start
GPIO.output(LED, GPIO.LOW)
print("LED is OFF - Initial state.")


#Info for intensity
intensityData = 0
from RFID import userTempThreshold #put this for the light code.
from RFID import userLightThreshold

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

#@app.route('/')
#def index():
#    return render_template('index.html')

#@app.route('/sensor-data')
#def get_sensor_data():
 #   return jsonify({
 #                   'intensity': intensityData,
 #               })

#I need explanation for this --> userThreshold

def led_control_loop():
    try:
        while True:
            # Check the received MQTT message and control the LED based on the message
            if userLightThreshold < intensityData:
                print("LIGHT ON-----------------")
                GPIO.output(LED, GPIO.HIGH)  # Turn on the LED if the message indicates it is dark
                send_email()
            elif userLightThreshold > intensityData:
                print("TURN OFF-----------------")
                GPIO.output(LED, GPIO.LOW)  # Turn off the LED if the message indicates it is not dark
            sleep(1)  # Sleep for 1 second

    except KeyboardInterrupt:
        print("Program interrupted")
    
def LEDData():
    ledData = {
        "intensity": intensityData,
    }
    return ledData

def set_IntensityData(mqtt_message):
    global intensityData
    intensityData = mqtt_message

#if __name__ == '__main__':
    #try:
        # Start MQTT client loop in a new thread
        #mqtt_thread = threading.Thread(target=mqtt_loop)
        #mqtt_thread.daemon = True  # Make the thread exit when the main program exits
        #mqtt_thread.start()

        # Start LED control loop in a separate thread
        #led_thread = threading.Thread(target=led_control_loop)
        #led_thread.daemon = True  # Make the thread exit when the main program exits
        #led_thread.start()

        # Run Flask app
        #app.run(host='0.0.0.0', port=5001)
        #while True:
            #try:
        #        app.run(host='0.0.0.0', port=5001)
        #        time.sleep(10)  # Wait for 10 seconds before the next check
        #   finally:
        #       sensor.exit()
    #finally:
        # Cleanup GPIO and stop MQTT client when exiting
        #GPIO.cleanup()
        #client.loop_stop()  # Stop the MQTT client loop
        #client.disconnect()  # Disconnect from the MQTT broker
