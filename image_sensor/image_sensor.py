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
    def __init__(self):
        self.min_width = 400
        self.max_width = 1920
        self.min_height = 400
        self.max_height = 1080
        self.width = 0
        self.height = 0
        self.sensor_size = (self.width, self.height)
        self.capture_count = 0
        self.image = None
        self.randomize_sensor_size()
        logger.info(f'sensor initialized width {self.width} height {self.height}')


    def generate_ship_image(self):
        background_color = (135, 206, 250)  # Light blue background
        object_color = (0, 0, 0)  # Black ship object color

        # Create a new image with the specified size and background color
        self.capture_count += 1
        self.image = Image.new("RGB", self.sensor_size, background_color)
        draw = ImageDraw.Draw(image)

        # Randomly generate the size and position of the ship objects (rectangles in this case)
        object_width = random.randint(80, 120)
        object_height = random.randint(30, 70)
        object_x = random.randint(0, size[0] - object_width)
        object_y = random.randint(0, size[1] - object_height)

        # Draw the ship object as a rectangle
        draw.rectangle((object_x, object_y, object_x + object_width, object_y + object_height), fill=object_color)
        logger.debug(f'generated ship image: image_{self.capture_count}')
        
        return {'message': f'Captured Image: image_{self.capture_count}'}

    def generate_null_image(self):
        background_color = (58, 110, 165)  # Darker blue background
        
        # Create a new image with the specified size and background color
        self.capture_count += 1
        self.image = Image.new("RGB", self.sensor_size, background_color)
        logger.debug(f'generated ocean only image: image_{self.capture_count}')

        return {'message': f'Captured Image: image_{self.capture_count}'}

    def capture_image(self):
        selected_function = random.choice([self.generate_ship_image, self.generate_null_image])
        selected_function()
        self.randomize_sensor_size()

    def randomize_sensor_size(self):
        self.width = random.randint(self.min_width, self.max_width)
        self.height = random.randint(self.min_height, self.max_height)
        self.sensor_size = (self.width, self.height)
        logger.info(f'resized sensor: {self.sensor_size}')
    
    def stream_image(self):
        
        
        

