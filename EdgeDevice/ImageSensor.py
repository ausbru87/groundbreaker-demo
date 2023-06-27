from PIL import Image
import random
import logging
import queue 

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('ImageSensor')

class ImageSensor:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.sensor_size = (self.width, self.height)
        self.capture_count = 0
        self.image_queue = queue.LifoQueue(maxsize=500)
        logger.info(f'sensor initialized width {self.width} height {self.height}')

    def capture_image(self):
        if not self.image_queue.full():
            self.capture_count += 1
            image = Image.new("RGB", self.sensor_size)
            image_pixels = image.load()
            for i in range(image.size[0]):
                for j in range(image.size[1]):
                    image_pixels[i,j] = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
            logger.info(f'image captured {self.sensor_size}, current count: {self.capture_count}')
            self.image_queue.put_nowait(image)
        else:
            logger.warn(f'image queue is currently full, cannot capture current request')

    def set_sensor_size(self, width, height):
        self.width = width
        self.height = height
        self.sensor_size = (self.width, self.height)
        logger.info(f'RESIZED SENSOR: WIDTH = {self.width} HEIGHT = {self.height}')