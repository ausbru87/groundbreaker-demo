import os
import boto3

class S3ImageUploader:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3')

    def upload_png_to_s3(self, image_dir):
        for root, _, files in os.walk(image_dir):
            for filename in files:
                if filename.lower().endswith('.png'):
                    local_path = os.path.join(root, filename)
                    s3_path = os.path.join('labeled_ship_images', filename)
                    self.upload_to_s3(local_path, s3_path)

    def upload_to_s3(self, local_path, s3_path):
        try:
            self.s3_client.upload_file(local_path, self.bucket_name, s3_path)
            print(f"{local_path} uploaded to S3 as {s3_path}")
        except Exception as e:
            print(f"Failed to upload {local_path} to S3: {e}")
