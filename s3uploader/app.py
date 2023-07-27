import os
import boto3
from flask import Flask, jsonify

app = Flask(__name__)

def upload_image_to_s3(bucket_name, object_key, file_path):
    s3 = boto3.client('s3')

    with open(file_path, 'rb') as file:
        content = file.read()

    response = s3.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=content
    )

    print(f"Uploaded {file_path} to S3. Response:", response)

@app.route('/upload_images', methods=['POST'])
def upload_images():
    bucket_name = 'groundbreaker-images'  # Replace with your S3 bucket name

    # Directory containing image files to upload
    image_directory = '/images/out'

    # List all files in the directory
    image_files = os.listdir(image_directory)
    uploaded_images = []

    for image_file in image_files:
        file_path = os.path.join(image_directory, image_file)
        object_key = f'images/{image_file}'  # Object key in S3, you can modify this as needed
        upload_image_to_s3(bucket_name, object_key, file_path)
        uploaded_images.append(image_file)
        # TODO: Make sure the file is saved before the deletion of the src file
        os.remove(file_path)


    return jsonify({"uploaded_images": uploaded_images})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8080)
