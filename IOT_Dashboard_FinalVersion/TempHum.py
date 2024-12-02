import time
import adafruit_dht
import board
import smtplib
import imaplib
import email
import RPi.GPIO as GPIO
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from Profile_Manager import userTempThreshold

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# DHT11 Sensor configuration
DHTPin = board.D17  # GPIO pin for DHT11 sensor GPIO 17
sensor = adafruit_dht.DHT11(DHTPin)

# Motor control configuration
Motor1 = 22  # Enable Pin
Motor2 = 18  # Input Pin
Motor3 = 26  # Input Pin
GPIO.setup(Motor1, GPIO.OUT)
GPIO.setup(Motor2, GPIO.OUT)
GPIO.setup(Motor3, GPIO.OUT)
GPIO.output(Motor1, GPIO.LOW)
GPIO.output(Motor2, GPIO.LOW)
GPIO.output(Motor3, GPIO.LOW)

# Gmail configuration
GMAIL_USER = 'seconddummytwo@gmail.com'  
GMAIL_PASSWORD = 'yucp cxwh gycz pena' 
RECEIVER_EMAIL = 'templatebuttondown@gmail.com'  

fan_on = False
email_sent = False
last_temp = None
last_humidity = None

def sensorOff():
    sensor.exit()
    GPIO.cleanup()

def get_sensor_data():
    """Fetch temperature and humidity from the DHT11 sensor."""
    global last_temp, last_humidity
    retries = 5

    for _ in range(retries):
        try:
            # Uncomment and use the actual sensor readings for temp and humidity
            print(userTempThreshold)
            temp = sensor.temperature
            humidity = sensor.humidity

            print(f"{email_sent}============================================D")
            if temp and humidity:
                last_temp, last_humidity = temp, humidity  # Cache successful readings
                print(f"Temperature: {temp}°C, Humidity: {humidity}%, Fan Status: {'ON' if fan_on else 'OFF'}")

                # Send email alert if the temperature exceeds 18°C
                if temp > userTempThreshold:
                    send_email_alert(temp)  # Ensure the temperature is passed to the function
                    print("SEND FAN MAIL")

                if email_sent:
                    check_for_yes_reply()
                    
                return {
                    'temperature': temp,
                    'humidity': humidity,
                    'fan': fan_on
                }

        except RuntimeError as error:
            print(f"Sensor Error: {str(error)} - Retrying...")
            time.sleep(1)

    if last_temp is not None and last_humidity is not None:
        print("Returning last known good readings.")
        return {
            'temperature': last_temp,
            'humidity': last_humidity,
            'fan': fan_on
        }

    else:
        print("Failed to read sensor data.")
        return {'error': 'Failed to read sensor data.'}

def send_email_alert(temp):
    """Send an email alert if the temperature exceeds a threshold."""
    global email_sent
    try:
        subject = "Temperature Alert - Fan Control"
        body = f"The current temperature is {temp}°C. Please reply 'YES' to turn on the fan."

        message = MIMEMultipart()
        message['From'] = GMAIL_USER
        message['To'] = GMAIL_USER
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, GMAIL_USER, message.as_string())
        server.quit()

        print("Alert email sent.")
        email_sent = True
    except Exception as e:
        print(f"Error sending email: {e}")

def check_for_yes_reply():
    """Check for 'YES' email replies and toggle the fan if received."""
    global fan_on, email_sent
    try:
        print("Connecting to Gmail to check for replies...")
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(GMAIL_USER, GMAIL_PASSWORD)
        mail.select('inbox')

        # Search for unseen messages with the specific subject or no subject
        status, messages = mail.search(None, '(UNSEEN SUBJECT "Temperature Alert - Fan Control")')
        if status != 'OK' or not messages[0]:
            status, messages = mail.search(None, '(UNSEEN)')
        print("Checking for unread 'YES' replies...")
        print(messages)

        for msg_num in messages[0].split():
            print(f"Checking message number: {msg_num}")  # Debug message
            status, msg_data = mail.fetch(msg_num, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    print(f"Processing email: {msg}")  # Debug message
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == 'text/plain':
                                body = part.get_payload(decode=True).decode().strip()
                                print(f"Email body received: '{body}'")  # Debug message
                                first_line = body.splitlines()[0].strip().lower()  # Get first line and normalize
                                print(f"First line extracted: '{first_line}'")  # Debug message
                                if first_line == "yes":
                                    print("Found 'YES' reply! Turning on the fan...")
                                    mail.store(msg_num, '+FLAGS', '\\Seen')  # Mark as read
                                    fan_on = True  # Turn the fan on
                                    toggle_fan("ON")
                                    #global email_sent
                                    email_sent = False  # Reset email sent status
                                    print("Fan status updated to ON.")
                                    mail.logout()
                                    return True
                                else:
                                    print("Reply was not 'YES'.")  # Debug message
                    else:
                        body = msg.get_payload(decode=True).decode().strip()
                        print(f"Email body received (not multipart): '{body}'")  # Debug message
                        first_line = body.splitlines()[0].strip().lower()  # Get first line and normalize
                        print(f"First line extracted: '{first_line}'")  # Debug message
                        if first_line == "yes":
                            print("Found 'YES' reply! Turning on the fan...")
                            mail.store(msg_num, '+FLAGS', '\\Seen')  # Mark as read
                            fan_on = True  # Turn the fan on
                            toggle_fan("ON")
                            email_sent = False  # Reset email sent status
                            print("Fan status updated to ON.")
                            mail.logout()
                            return True
                        else:
                            print("Reply was not 'YES'.")  # Debug message
        mail.logout()
        print("No 'YES' reply found.")
        return False
    except Exception as e:
        print(f"Error checking emails: {e}")
        return False


def toggle_fan(state):
    """Turn the fan on or off based on the provided state."""
    global fan_on
    if state == "ON":
        GPIO.output(Motor1, GPIO.HIGH)
        GPIO.output(Motor2, GPIO.LOW)
        GPIO.output(Motor3, GPIO.HIGH)
        fan_on = True
        print("Fan turned ON.")
        print("Fan turned ON TRUE UNLIMITED FAN WORKS")
        email_sent = False
    elif state == "OFF" and fan_on:
        GPIO.output(Motor1, GPIO.LOW)
        GPIO.output(Motor2, GPIO.LOW)
        GPIO.output(Motor3, GPIO.LOW)
        fan_on = False
        email_sent = False
        print("Fan turned OFF.")
def toggle_fan_ON():
    """Turn the fan on."""
    global fan_on
    GPIO.output(Motor1, GPIO.HIGH)
    GPIO.output(Motor2, GPIO.LOW)
    GPIO.output(Motor3, GPIO.HIGH)
    fan_on = True
    print("Fan turned ON.")