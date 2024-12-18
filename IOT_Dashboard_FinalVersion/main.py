import asyncio
from flask import Flask, jsonify, render_template

import LED
import TempHum
import Profile_Manager
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
    return jsonify(Profile_Manager.profileData())

@app.route('/temp-hum')
def get_TH_data():
    return jsonify(TempHum.get_sensor_data())

@app.route('/toggle-off')
def fan_off():
    TempHum.toggle_fan("OFF")
    return jsonify({"fan": "OFF"})

if __name__ == '__main__':
    try:
        #Profile_Manager.setJSONPath()
        MQTT_Manager.start_MQTT()
        app.run(host='0.0.0.0', port=5001)
        LED.sensorOn()
        #asyncio.run(LED.led_control_loop())
    except KeyboardInterrupt:
        TempHum.sensorOff()
        LED.sensorOff()
        MQTT_Manager.stop_MQTT()
        exit() 
