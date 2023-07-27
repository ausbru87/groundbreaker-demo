import requests
from queue import Queue
import logging
import os

class ImageForwarder:
    def __init__(self, image_dir, destination):
        self.forward_queue = Queue()
        self.destination = destination
        self.image_dir = image_dir

        # Logger instance
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Add a stream handler to log to console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Start enqueuing images
        self.start_enqueuing_images()

    def perform_forward(self, image_data):

        endpoint = self.destination + "/upload"
        try:
            response = requests.post(endpoint, data=image_data)
            if response.status_code == 200:
                self.logger.info("Image successfully forwarded to %s", self.destination)
            else:
                self.logger.warning("Failed to forward image to %s", self.destination)
        except requests.exceptions.RequestException as e:
            self.logger.error("Image forward failed. Error: %s", e)

    def enqueue_image(self, image_path):
        with open(image_path, 'rb') as file:
            image_data = file.read()
            self.forward_queue.put(image_data)

    def start_enqueuing_images(self):
        for filename in os.listdir(self.image_dir):
            if filename.endswith('.jpg') or filename.endswith('.png'):  # Add more extensions if needed
                image_path = os.path.join(self.image_dir, filename)
                self.enqueue_image(image_path)
                # TODO: Make sure the file is forwarded before the deletion of the src file
                os.remove(image_path)

    def flush_forward_queue(self):
        while not self.forward_queue.empty():
            image_data = self.forward_queue.get()
            self.perform_forward(image_data)
