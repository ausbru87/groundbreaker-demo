from ShipFinder import ShipFinder
import os
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('ImageProcessor')

class ImageProcessor:
    def __init__(self, directory_path):
        self.directory_path = directory_path

    def process_directory(self):
        for filename in os.listdir(self.directory_path):
            if filename.endswith(".png") or filename.endswith(".jpg"):
                image_path = os.path.join(self.directory_path, filename)
                ship_finder = ShipFinder(image_path)
                has_ship = ship_finder.find_ships()
                logger.info(f"Image: {filename}, Ship Found: {has_ship}")
                if not has_ship:
                    logger.info(f"Removing Image: {filename} - No ship found")
                    os.remove(image_path)
