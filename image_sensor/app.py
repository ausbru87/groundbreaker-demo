from flask import Flask
from image_sensor import ImageSensor
import os


in_path = '/images/in'
out_path = '/images/out'

if not os.path.exists(out_path):
    os.mkdir(out_path)

if not os.path.exists(in_path):
    os.mkdir(in_path)

app = Flask(__name__)


sensor = ImageSensor(width=640, height=480, queue_size=500, images_dir=in_path)

@app.route('/capture-images', methods=['POST'])
def capture_images():
    sensor.capture_images()
    return '',200

@app.route('/store-images', methods=['POST'])
def store_images():
    sensor.store_images()
    return '',200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
