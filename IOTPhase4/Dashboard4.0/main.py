from flask import Flask, jsonify, render_template

app = Flask(__name__)

intensityData = 300

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sensor-data')
def get_sensor_data():
    return jsonify({
                    'intensity': intensityData,
                })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
