from flask import Flask, request, jsonify, render_template
import atexit
import threading
import time
#import paho.mqtt.client as mqtt    #uncomment when u want to run 
import phase2  
import phase3
import phase4

app = Flask(__name__)

# Shared state for the sensor data and fan status
current_sensor_data = {
    'temperature': None,
    'humidity': None,
    'fan': False
}

# Define the user light threshold globally, you can adjust this value
userLightThreshold = 1600  # Example threshold for the light sensor

# MQTT Client setup (to be run in the background)
mqtt_client = mqtt.Client()

# Set up the MQTT connection
mqtt_client.connect("mqtt_broker_address")  # Replace with actual broker address
mqtt_client.subscribe("topic")  # Replace with actual topic

# Start the MQTT loop in a separate thread (non-blocking)
mqtt_thread = threading.Thread(target=mqtt_client.loop_forever)
mqtt_thread.daemon = True
mqtt_thread.start()

# Start the LED control loop in a separate thread
led_thread = threading.Thread(target=phase3.led_control_loop, args=(userLightThreshold,))
led_thread.daemon = True
led_thread.start()

def update_sensor_data():
    """Background task to update sensor data every 5 seconds."""
    global current_sensor_data
    while True:
        # Fetch new sensor data
        sensor_data = phase2.get_sensor_data()  # Fetch data from phase2
        
        # Update shared state
        current_sensor_data['temperature'] = sensor_data.get('temperature')
        current_sensor_data['humidity'] = sensor_data.get('humidity')
        current_sensor_data['fan'] = sensor_data.get('fan')
        
        time.sleep(5)  # Update every 5 seconds

@app.route("/")
def home():
    # Render the home page with the latest sensor data
    return render_template('index.html', data=current_sensor_data)

@app.route('/toggle_fan', methods=['POST'])
def toggle_fan():
    data = request.json
    fan_state = data.get('state', False)  # Get fan state from JSON body
    print(f"Toggling fan. Desired state: {fan_state}")  # Debug print
    # Toggle fan using Phase 2 function
    fan_status = phase2.toggle_fan(fan_state)
    print(f"Fan status after toggle: {fan_status}")  # Debug print
    return jsonify({"success": True, "fan_on": fan_status})

@app.route('/get_sensor_data')
def return_sensor_data():
    # Return current sensor data as JSON response
    return jsonify(current_sensor_data)

@app.route('/get_email_data')
def return_email_data():
    # Get temperature from Phase 2 sensor data
    sensor_data = phase2.get_sensor_data()
    temp = sensor_data.get('temperature')
    print(f"Temperature for email: {temp}")  # Debug print

    # Ensure that temp is passed to the email alert function in a thread
    email_thread = threading.Thread(target=phase2.send_email_alert, args=(temp,))
    email_thread.start()

    return jsonify({"success": True, "message": "Email alert thread started."})

@app.route('/get_status')
def get_status():
    # Return the current status including fan, temperature, and humidity
    return jsonify(current_sensor_data)

@app.route('/temp-hum')
def get_temp_hum():
    # Return the latest temperature and humidity
    return jsonify(current_sensor_data)

# Route to set intensity data (triggered by MQTT or other methods)
@app.route('/set_intensity', methods=['POST'])
def set_intensity():
    # Receive intensity data from the request body
    data = request.json
    intensity = data.get('intensity', 0)  # Get intensity from JSON body (default to 0)
    
    print(f"Setting intensity to: {intensity}")
    
    # Update intensity data in phase3 and control LED
    phase3.set_intensity_data(intensity)  # Pass intensity to phase3's set_intensity_data
    phase3.led_control()  # Control LED based on the intensity
    
    # Return success response
    return jsonify({"success": True, "intensity": intensity})

# Route to get the current LED intensity
@app.route('/LED', methods=['GET'])
def get_led():
    # Get the current LED intensity from phase3
    led_intensity = phase3.get_led_intensity()
    
    # Return the current intensity as a JSON response
    return jsonify({"led_intensity": led_intensity})

@app.route('/profile')
def get_profile():
    if last_scanned_rfid:
        # Retrieve user profile data based on the last scanned RFID tag
        user_profile = USER_PROFILES.get(last_scanned_rfid)
        if user_profile:
            # If the user profile exists, return it as a JSON response
            return jsonify(user_profile)
        else:
            # If the user profile doesn't exist, return an error message
            return jsonify({"error": "User profile not found"}), 404
    else:
        # If no RFID tag has been scanned yet, return an error
        return jsonify({"error": "No RFID scanned yet"}), 400

if __name__ == "__main__":
    # Start the background thread to update sensor data
    threading.Thread(target=update_sensor_data, daemon=True).start()
    
    # Start Flask app
    app.run(host='0.0.0.0', port=5001)
