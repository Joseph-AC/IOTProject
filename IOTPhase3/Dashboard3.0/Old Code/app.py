import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import RPi.GPIO as GPIO
import time


LED_PIN = 17  
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  
GPIO.setup(LED_PIN, GPIO.OUT)


GPIO.output(LED_PIN, GPIO.LOW)
print("LED is OFF - Initial state.")

# Email setup
GMAIL_USER = '@gmail.com'  
GMAIL_PASSWORD = 'ukne' 
RECEIVER_EMAIL = '@gmail.com'  

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
        
        # Send email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.sendmail(GMAIL_USER, RECEIVER_EMAIL, message.as_string())
        
        print(f"Email sent: {body}")
    except Exception as e:
        print(f"Error sending email: {e}")

def check_light_intensity():
    """
    Simulate light intensity and handle LED & email logic.
    Adjust the fixed light intensity value as needed for testing.
    """
    
    light_intensity = 300  #change to real value
    
   
    print(f"Light Intensity: {light_intensity}")
    
    if light_intensity < 400:
        GPIO.output(LED_PIN, GPIO.HIGH)  
        print("LED is ON - Light intensity is below threshold.")
        send_email()  
    else:
        GPIO.output(LED_PIN, GPIO.LOW)  
        print("LED is OFF - Light intensity is above threshold.")


try:
    
    print("Checking light intensity.")
    check_light_intensity()
    
except KeyboardInterrupt:
    print("Exiting program.")
finally:
    GPIO.cleanup()  