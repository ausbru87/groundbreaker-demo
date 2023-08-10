from flask import Flask
from image_sensor import ImageSensor
import os
import requests


in_path = '/images/in'
out_path = '/images/out'
processor_url = 'http://192.168.5.108:8082'

if not os.path.exists(out_path):
    os.mkdir(out_path)

if not os.path.exists(in_path):
    os.mkdir(in_path)

app = Flask(__name__)


sensor = ImageSensor(width=640, height=480, queue_size=500, images_dir=in_path)

@app.route('/capture_images', methods=['POST'])
def capture_images():
    capture = True
    while capture:
        sensor.capture_image()
        sensor.stream_image(processor_service)
        if response == 200:
            return f'sent image to processor: {processor_service}',200
        else:
            return f'there was an error in capturing and sending image to processor, ending captures', 505
            capture = False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
