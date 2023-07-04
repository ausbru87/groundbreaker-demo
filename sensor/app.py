from flask import Flask
from image_sensor import ImageSensor
import os
import requests


in_path = '/images/in'
out_path = '/images/out'

if not os.path.exists(out_path):
    os.mkdir(out_path)

if not os.path.exists(in_path):
    os.mkdir(in_path)

app = Flask(__name__)


sensor = ImageSensor(width=640, height=480, queue_size=500, images_dir=in_path)

@app.route('/capture_images', methods=['POST'])
def capture_images():
    sensor.capture_images()
    sensor.store_images()
    response = requests.post('http://192.168.5.108:8082/detect_ships')
    if response == 200:
        return 'captured images successfully and sent processing command to processor successfully',200
    return 'captured images successfully',200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
