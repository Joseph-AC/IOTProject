
from flask import Flask, jsonify, render_template

import RFID
import LED
import MQTT_Manager

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/LED')
def get_sensor_data():
    return jsonify(LED.LEDData())

@app.route('/profile')
def get_profile_data():
    return jsonify(RFID.profileData())

if __name__ == '__main__':
    try:
        MQTT_Manager.start_MQTT()
        app.run(host='0.0.0.0', port=5001)

    finally:
        MQTT_Manager.stop_MQTT()
