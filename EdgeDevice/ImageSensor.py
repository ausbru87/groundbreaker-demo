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
        background_color = (135, 206, 250)  # Light blue background
        object_color = (0, 0, 0)  # Black ship object color
        size = self.sensor_size

        # Create a new image with the specified size and background color
        image = Image.new("RGB", size, background_color)
        draw = ImageDraw.Draw(image)

        # Randomly generate the size and position of the ship objects (rectangles in this case)
        object_width = random.randint(80, 120)
        object_height = random.randint(30, 70)
        object_x = random.randint(0, size[0] - object_width)
        object_y = random.randint(0, size[1] - object_height)

        # Draw the ship object as a rectangle
        draw.rectangle((object_x, object_y, object_x + object_width, object_y + object_height), fill=object_color)

    
        # Save image data to in-memory buffer
        image_buffer = io.BytesIO()
        image.save(image_buffer, format='PNG')
        image_data = image_buffer.getvalue()
        
        self.image_queue.put(image_data)
        logger.info('generated NON-SHIP image')
        return {'message': 'image of ship generated and stored in local buffer successfully'}

    def generate_null_image(self):
        background_color = (58, 110, 165)  # Darker blue background
        size = self.sensor_size
        # Create a new image with the specified size and background color
        image = Image.new("RGB", size, background_color)
        
        # Save image data to in-memory buffer
        image_buffer = io.BytesIO()
        image.save(image_buffer, format='PNG')
        image_data = image_buffer.getvalue()
        
        self.image_queue.put(image_data)
        logger.info('generated ocean only image')
        return {'message': 'image of ocean generated and stored in local buffer successfully'}

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
    
    def store_images(self, image_dir_path):
        while not self.image_queue.empty():
            image_data = self.image_queue.get()
            image = Image.open(io.BytesIO(image_data))

            image.save(f"{image_dir_path}/generated-image_{self.capture_count}.png", "PNG")
            logger.info(f"successfully stored: {image_dir_path}/generated-image_{self.capture_count}.png")
            self.capture_count += 1

