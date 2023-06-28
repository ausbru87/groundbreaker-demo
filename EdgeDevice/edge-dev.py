from ImageSensor import ImageSensor
from ImageProcessor import ImageProcessor

path = '/home/abruhn/working/groundbreaker/EdgeDevice/images'

sensor = ImageSensor(640, 480)
processor = ImageProcessor(path)
sensor.capture_images()
sensor.store_images(path)

processor.process_directory()