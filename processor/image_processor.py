from ship_detector import ShipDetector
import os
import logging
import cv2
import time

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('ImageProcessor')

class ImageProcessor:
    def __init__(self, incoming_path, outgoing_path):
        self.incoming_path = incoming_path
        self.outgoing_path = outgoing_path
        self.processed_count = 0

    def process_dir_detect(self):
        for filename in os.listdir(self.incoming_path):
            if filename.endswith(".png"):
                self.processed_count += 1
                image_path = os.path.join(self.incoming_path, filename)
                ship_detector = ShipDetector(image_path)
                has_ship = ship_detector.detect_ship()
                logger.info('detecting ships in image')
                logger.info(f"Processed {self.processed_count} Image -- Image: {filename}, Ship Found: {has_ship}")
                if not has_ship:
                    logger.info(f"Removing Image: {filename} - No ship found")
                    os.remove(image_path)
    
    def process_dir_chip(self):
        for filename in os.listdir(self.incoming_path):
            if filename.endswith(".png"):
                self.processed_count += 1
                image_path = os.path.join(self.incoming_path, filename)
                logger.debug(f'image_path: {image_path}')
                ship_detector = ShipDetector(image_path)
                chip_data = ship_detector.chip_ship()
                logger.info("Processed {self.processed_count} Image -- Chipping ship image")
                self.save_images(type='chip',image_data=chip_data)
                # TODO: Make sure the file is saved before the deletion of the src file
                os.remove(image_path)

    def process_dir_label(self):
        for filename in os.listdir(self.incoming_path):
            if filename.endswith(".png"):
                self.processed_count += 1
                image_path = os.path.join(self.incoming_path, filename)
                ship_detector = ShipDetector(image_path)
                label_data = ship_detector.label_ship()
                logger.info("Processed {self.processed_count} Image -- Labeling ship object in image")
                self.save_images(type='labeled',image_data=label_data)
                # TODO: Make sure the file is saved before the deletion of the src file
                os.remove(image_path)

    def save_images(self, type, image_data):
        file_path = self.generate_filenmae(type)
        cv2.imwrite(file_path, image_data, [cv2.IMWRITE_PNG_COMPRESSION, 0])
        logger.info("successfully saved {file_path}")
    
    def generate_filenmae(self, type):
        ms_epoch = round(time.time() * 1000)
        filename = f'ship_{type}_{ms_epoch}.png'
        file_path = os.path.join(self.outgoing_path, filename)
        return file_path
