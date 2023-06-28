from flask import Flask
from EdgeDevice.ImageSensor.ImageSensor import ImageSensor

images = []
sensor = ImageSensor(width=640,height=640)
app = Flask(__name__)

@app.route('/sensor-data', methods=['POST'])
def acquire_sensor_data():
    # Acquire sensor data
    # Replace this with actual code to capture sensor data
    sensor_data = {'image': 'path/to/image'}
    
    # Send sensor data to Image Processing Microservice
    # Replace with appropriate request to the Image Processing Microservice
    # ...

    return '', 200

@app.route('/init-sensor', methods=['POST'])
def initialize_sensor():
    sensor = ImageSensor(640,640)
    return '',200

@app.route('/capture-images', methods=['POST'])
def capture_images():
    acc = 0
    while acc < 502:
        sensor.capture_image()
        acc += 1
    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
