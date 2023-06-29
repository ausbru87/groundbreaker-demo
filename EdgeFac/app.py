from flask import Flask, request
from PIL import Image
from io import BytesIO
import uuid
import os

app = Flask(__name__)

images_dir = '/images'
@app.route('/upload', methods=['POST'])
def upload_image(downlink_count):
    if 'image' not in request.files:
        return 'No image file provided', 400

    image_file = request.files['image']
    image_data = image_file.read()

    # Convert the image data bytes into an image object using Pillow
    image = Image.open(BytesIO(image_data))

    # Generate a unique ID for the image
    unique_id = str(uuid.uuid4())

    # Create the image filename with the desired naming convention
    image_filename = f'downlinked-image_{unique_id}.png'

    # Save the processed image to the '/images' directory
    save_path = os.path.join('/images', image_filename)
    image.save(save_path, 'PNG')

    # Return a response indicating successful image processing
    return 'Image uploaded and saved successfully', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
