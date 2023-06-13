from PIL import Image
import random

class ImageSensor:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.sensor_size = (self.width, self.height)
        self.image = None
    
    def capture_image(self):
        self.image = Image.new("RGB", self.sensor_size)
        image_pixels = self.image.load()
        for i in range(self.image.size[0]):
            for j in range(self.image.size[1]):
                image_pixels[i,j] = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    
    def set_sensor_size(self, width, height):
        self.width = width
        self.height = height
        self.sensor_size = (self.width, self.height)

    def get_image(self):
        return self.image
    
    def write_image_file(self):
        self.image.save()
        # TODO: add save info /images/raw and format