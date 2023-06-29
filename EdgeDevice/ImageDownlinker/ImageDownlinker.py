import os
import requests
import time
from io import BytesIO

class ImageDownlinker:
    def __init__(self):
        self.current_downlink_site = 'edgefacility-a'
        self.api_check_interval = 10  # seconds
        self.image_directory = '/path/to/images'
        self.endpoint_a = 'http://127.0.0.1:8085/upload'
        self.endpoint_b = 'http://127.0.0.1:8086/upload'

    def monitor_services(self):
        while True:
            api_status_a = self.check_api_status('edgefacility-a')
            api_status_b = self.check_api_status('edgefacility-b')

            if self.current_downlink_site == 'edgefacility-a' and not api_status_a:
                print("Switching downlink site to edgefacility-b...")
                self.current_downlink_site = 'edgefacility-b'

            if self.current_downlink_site == 'edgefacility-b' and not api_status_b:
                print("Switching downlink site to edgefacility-a...")
                self.current_downlink_site = 'edgefacility-a'

            time.sleep(self.api_check_interval)

    def check_api_status(self, edgefacility):
        try:
            response = requests.get(f"https://{edgefacility}.api.example.com/status")
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def perform_downlink(self):
        while True:
            if self.current_downlink_site == 'edgefacility-a':
                api_status = self.check_api_status('edgefacility-a')
                if not api_status:
                    print("Switching downlink site to edgefacility-b...")
                    self.current_downlink_site = 'edgefacility-b'
                    continue

                target_endpoint = self.endpoint_a

            if self.current_downlink_site == 'edgefacility-b':
                api_status = self.check_api_status('edgefacility-b')
                if not api_status:
                    print("Switching downlink site to edgefacility-a...")
                    self.current_downlink_site = 'edgefacility-a'
                    continue

                target_endpoint = self.endpoint_b

            # Loop through the images in the directory
            for image_file in os.listdir(self.image_directory):
                if not image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    continue  # Skip non-image files

                image_path = os.path.join(self.image_directory, image_file)

                with open(image_path, 'rb') as f:
                    image_data = f.read()

                # Create an in-memory buffer for image data
                image_buffer = BytesIO(image_data)

                print(f"Performing downlink to {self.current_downlink_site} - Image: {image_file}...")

                # Perform HTTP POST request to send the image data
                try:
                    response = requests.post(target_endpoint, files={'image': image_buffer})
                    if response.status_code == 200:
                        print("Image upload successful!")
                    else:
                        print(f"Image upload failed. Status Code: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    print(f"Image upload failed. Error: {e}")

            break  # Break the loop after processing all images
