from ImageSensor import ImageSensor
from ImageProcessor import ImageProcessor

path = '/home/abruhn/working/groundbreaker/EdgeDevice/images'
sensor = ImageSensor(width=640, height=480, queue_size=500, image_dir=path)
processor = ImageProcessor(path)
sensor.capture_images()
sensor.store_images(path)

processor.process_directory()