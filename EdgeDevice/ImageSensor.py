from PIL import Image, ImageDraw, ImageFont
from queue import LifoQueue
import io
import random
import logging
import queue
import time

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('ImageSensor')

class ImageSensor:
    def __init__(self, width, height):
        self.min_width = 400
        self.max_width = 1920
        self.min_height = 400
        self.max_height = 1080
        self.width = width
        self.height = height
        self.sensor_size = (self.width, self.height)
        self.capture_count = 0
        self.image_queue = LifoQueue(maxsize=500)
        logger.info(f'sensor initialized width {self.width} height {self.height}')

    def generate_ship_image(self):
        background_color = (58, 110, 165)  # Darker blue background
        object_color = (105, 105, 105)  # Dark gray objects
        text_color = (0, 0, 0)  # Black text color
        size = self.sensor_size
        # Create a new image with the specified size and background color
        image = Image.new("RGB", size, background_color)
        draw = ImageDraw.Draw(image)

        # Randomly generate the size and position of the ship objects (ellipses in this case)
        object_width = random.randint(80, 120)
        object_height = random.randint(30, 70)
        object_x = random.randint(0, size[0] - object_width)
        object_y = random.randint(0, size[1] - object_height)
        draw.ellipse((object_x, object_y, object_x + object_width, object_y + object_height), fill=object_color)

        # Add the text "SHIP" in the middle of the ellipse
        text = "SHIP"
        text_width, text_height = draw.textsize(text)
        text_x = object_x + (object_width - text_width) // 2
        text_y = object_y + (object_height - text_height) // 2
        draw.text((text_x, text_y), text, fill=text_color)

        # Save image data to in-memory buffer
        image_buffer = io.BytesIO()
        image.save(image_buffer, format='PNG')
        image_data = image_buffer.getvalue()
        
        self.image_queue.put((image_data, 1))
        return {'message': 'Geospatial image of ship generated and stored successfully'}

    def generate_null_image(self):
        background_color = (58, 110, 165)  # Darker blue background
        size = self.sensor_size
        # Create a new image with the specified size and background color
        image = Image.new("RGB", size, background_color)
        
        # Save image data to in-memory buffer
        image_buffer = io.BytesIO()
        image.save(image_buffer, format='PNG')
        image_data = image_buffer.getvalue()
        
        self.image_queue.put((image_data, 0))
        return {'message': 'Geospatial image of military base generated and stored successfully'}

    def capture_images(self):
        if self.image_queue.full():
            logger.warn('Unable to capture image because the queue is full')
            return {'message': 'Unable to capture image because the queue is full'}
        while not self.image_queue.full():
            selected_function = random.choice([self.generate_ship_image, self.generate_null_image])
            selected_function()
            self.randomize_sensor_size()

    def randomize_sensor_size(self):
        self.width = random.randint(self.min_width, self.max_width)
        self.height = random.randint(self.min_height, self.max_height)
        self.sensor_size = (self.width, self.height)
        logger.info(f'resized sensor: {self.sensor_size}')
    
    def get_image(self):
        if image_queue.empty():
            logger.warn('No images available')
            return jsonify({'message': 'No images available'})
        image_data = image_queue.get()
        logger.debug('image retrieved')
        return  jsonify({'image': image_data.decode})
    
    def send_images(self):
        while not self.image_queue.empty():
            image_data = self.image_queue.get()
            if image_data[1] == 1:
                image = Image.open(io.BytesIO(image_data[0]))

                image.save(f"./images/generated-image_{self.capture_count}.png", "PNG")
                self.capture_count += 1

