from flask import Flask
from image_processor import ImageProcessor
import os
import requests

app = Flask(__name__)

in_path = '/images/in'
out_path = '/images/out'
downlinker_url = 'http://192.168.5.108:8083'
forwarder_url = 'http://forwarder:8080'
s3uploader_url = 'http://s3uploader:8080'


if not os.path.exists(out_path):
    os.mkdir(out_path)

if not os.path.exists(in_path):
    os.mkdir(in_path)

processor = ImageProcessor(incoming_path=in_path, outgoing_path=out_path)

@app.route('/detect_ships', methods=['POST'])
def detect_ships():
    processor.process_dir_detect()
    response = requests.post(f'{downlinker_url}/downlink')
    if response == 200:
        return 'sent downlink command successfully and detected ships successfully',200
    return 'detected ships successfully',200

@app.route('/chip_ships', methods=['POST'])
def chip_ships():
    processor.process_dir_chip()
    response = requests.post(f'{forwarder_url}/forward')
    return 'processed images, generated chips and began forwarding images to core',200

@app.route('/label_ships', methods=['POST'])
def label_ships():
    processor.process_dir_label()
    response = requests.post(f'{s3uploader_url}/upload_images')
    return 'processed chips, generated new chips with ships located and labeled and saved them successfully',200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

