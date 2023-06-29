from flask import Flask
from ImageProcessor import ImageProcessor

app = Flask(__name__)

@app.route('/init-processor', methods=['POST'])
def initialize_sensor():
    global processor
    processor = ImageProcessor(directory_path='/images')
    return 'processor initialized',200

@app.route('/process-images', methods=['POST'])
def find_ships():
    processor.process_directory()
    return 'processed image directory',200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
