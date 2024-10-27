
import time
import board
import adafruit_dht
from flask import Flask, jsonify, render_template
import psutil

app = Flask(__name__)

# Kill any existing libgpiod processes that might interfere
for process in psutil.process_iter():
    if process.name() in ['libgpiod_pulsein', 'libgpiod_plsei']:
        process.kill()

# Initialize sensor after killing interfering processes
DHTPin = board.D27  # Use GPIO 27 for the DHT11 sensor
sensor = adafruit_dht.DHT11(DHTPin)



#if (temp>24){ send email  if(yes) turn on fan -> codde to turn on fan and fan icon on html





@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sensor-data')
def get_sensor_data():
    try:
        # Read temperature and humidity
        temp = sensor.temperature
        humidity = sensor.humidity

        # Log the values
        print(f"Temperature: {temp}°C, Humidity: {humidity}%")

        # Return the data as JSON
        return jsonify({
            'temperature': temp,
            'humidity': humidity
        })
    except RuntimeError as error:
        # Handle sensor reading errors
        print(f"Sensor Error: {str(error)}")
        return jsonify({
            'error': str(error)
        }), 500

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5001)
    finally:
        sensor.exit()
