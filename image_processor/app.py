from flask import Flask
from image_processor import ImageProcessor

app = Flask(__name__)
processor = ImageProcessor(incoming_path='/images/in', outgoing_path='/images/out')

@app.route('/detect_ships', methods=['POST'])
def detect_ships():
    processor.process_dir_detect()
    return 'processed images to detect ships successfully',200

@app.route('/chip_ships', methods=['POST'])
def chip_ships():
    processor.process_dir_chip()
    return 'processed images, generated chips and saved them successfully',200

@app.route('/label_ships', methods=['POST'])
def label_ships():
    processor.process_dir_label()
    return 'processed chips, generated new chips with ships located and labeled and saved them successfully',200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

