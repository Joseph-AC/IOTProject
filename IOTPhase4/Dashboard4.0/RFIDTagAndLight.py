import serial
import threading
import time
import board
import adafruit_dht

# Serial communication with Arduino
arduino = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
arduino.flush()

# DHT11 Sensor Configuration
DHTPin = board.D26  # GPIO pin for DHT11 sensor
sensor = adafruit_dht.DHT11(DHTPin)

# Hardcoded user profiles
USER_PROFILES = {
    "23c3ccf7": {"user_id": 1, "temp": None, "light_intensity": None},
    "12b3456f": {"user_id": 2, "temp": None, "light_intensity": None},
    "89d4567a": {"user_id": 3, "temp": None, "light_intensity": None},
}

def update_user_profile(rfid_tag, light_intensity):
    # Convert RFID tag to lowercase to ensure case-insensitivity
    rfid_tag = rfid_tag.lower()

    # Check if RFID tag exists in the user profiles
    user = USER_PROFILES.get(rfid_tag)
    if not user:
        print(f"Unknown RFID tag: {rfid_tag}")
        return "Unknown RFID tag"

    try:
        # Read temperature from the DHT11 sensor
        temp = sensor.temperature
        if temp is None:
            raise ValueError("Failed to read temperature from DHT11 sensor.")

        # Update user profile with current temperature and light intensity
        user['temp'] = temp
        user['light_intensity'] = light_intensity
        print(f"Updated user {user['user_id']} - Temp: {temp}°C, Light: {light_intensity} lux")
        return f"User {user['user_id']} updated: Temp={temp}°C, Light={light_intensity} lux"

    except Exception as e:
        print(f"Error updating user: {e}")
        return "Failed to update user"

# Thread function for serial data handling
def read_serial_data():
    while True:
        if arduino.in_waiting > 0:
            try:
                # Read data from Arduino and decode with 'ignore' to handle invalid characters
                data = arduino.readline().decode('utf-8', errors='ignore').strip()
                
                if data:
                    print(f"Received data: {data}")

                    # Ensure the data is in the expected format (rfid_tag, light_intensity)
                    if ',' in data:
                        rfid_tag, light_intensity = data.split(',')
                        try:
                            # Call the update function to update the user profile
                            response = update_user_profile(rfid_tag, float(light_intensity))
                            print(response)
                        except ValueError as e:
                            print(f"Invalid light intensity value: {e}")
                    else:
                        print(f"Invalid data format: {data}")
            except Exception as e:
                print(f"Error processing data: {e}")

# Main function
def main():
    # Start the serial reading in a separate thread
    serial_thread = threading.Thread(target=read_serial_data)
    serial_thread.daemon = True
    serial_thread.start()

    while True:
        # Main thread can do other tasks here if needed, for example, logging or waiting
        time.sleep(1)  # To prevent the main thread from terminating immediately

if __name__ == "__main__":
    main()
