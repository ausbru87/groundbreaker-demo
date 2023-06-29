from flask import Flask, request
from PIL import Image
from io import BytesIO
import uuid
import os

app = Flask(__name__)

images_dir = '/images'
@app.route('/upload', methods=['POST'])
def upload_image():

    image_data = request.data

    filename = generate_filename()
    
    save_image(image_data, filename)

    # Return a response indicating successful image processing
    return 'Image uploaded and saved successfully', 200

@app.route('/status', methods=['GET'])
def get_status():
    return 'edgefac is healthy', 200

def generate_filename():
    unique_id = str(uuid.uuid4())
    image_filename = f'downlinked-image_{unique_id}.png'
    return image_filename

def save_image(image_data, filename):
    save_path = os.path.join('/images', filename)
    image = Image.open(BytesIO(image_data))
    image.save(save_path, 'PNG')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)