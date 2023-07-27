import requests
from queue import Queue
import threading
import logging
import os

class ImageDownlinker:
    def __init__(self, facility_a, facility_b, image_dir):
        self.facility_a = facility_a
        self.facility_b = facility_b
        self.image_dir = image_dir
        self.active_facility = facility_a
        self.online_state_a = True
        self.online_state_b = True
        self.downlink_queue = Queue()

        # Logger instance
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Add a stream handler to log to console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Start monitoring facilities
        self.monitor_thread = threading.Thread(target=self.monitor_facilities, daemon=True)
        self.monitor_thread.start()

    def perform_downlink(self, image_data):
        if not self.active_facility:
            return

        endpoint = self.active_facility + "/upload"
        try:
            response = requests.post(endpoint, data=image_data)
            if response.status_code == 200:
                self.logger.info("Image successfully downlinked to %s", self.active_facility)
            else:
                self.logger.warning("Failed to downlink image to %s", self.active_facility)
        except requests.exceptions.RequestException as e:
            self.logger.error("Image downlink failed. Error: %s", e)

    def monitor_facilities(self):
        while True:
            self.check_facility_status(self.facility_a, "a")
            self.check_facility_status(self.facility_b, "b")

    def check_facility_status(self, facility, facility_name):
        try:
            response = requests.get(facility + "/status")
            online_state = response.status_code == 200
        except requests.exceptions.RequestException:
            online_state = False

        if facility_name == "a":
            self.online_state_a = online_state
        elif facility_name == "b":
            self.online_state_b = online_state

        if facility == self.active_facility and not online_state:
            self.switch_facility()

    def switch_facility(self):
        if self.active_facility == self.facility_a and not self.online_state_b:
            self.active_facility = None
            self.logger.info("Both facilities are offline.")
        elif self.active_facility == self.facility_b and not self.online_state_a:
            self.active_facility = None
            self.logger.info("Both facilities are offline.")
        elif self.active_facility == self.facility_a and self.online_state_b:
            self.active_facility = self.facility_b
            self.logger.info("Switched to facility B")
        elif self.active_facility == self.facility_b and self.online_state_a:
            self.active_facility = self.facility_a
            self.logger.info("Switched to facility A")


    def enqueue_image(self, image_path):
        with open(image_path, 'rb') as file:
            image_data = file.read()
            self.downlink_queue.put(image_data)

    def start_enqueuing_images(self):
        for filename in os.listdir(self.image_dir):
            if filename.endswith('.jpg') or filename.endswith('.png'):  # Add more extensions if needed
                image_path = os.path.join(self.image_dir, filename)
                self.enqueue_image(image_path)
                # TODO: Make sure the file is saved before the deletion of the src file
                os.remove(image_path)

    def flush_downlink_queue(self):
        while not self.downlink_queue.empty():
            image_data = self.downlink_queue.get()
            self.perform_downlink(image_data)
