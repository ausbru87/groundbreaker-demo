from flask import Flask, jsonify
from s3_image_uploader import S3ImageUploader
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_to_s3_endpoint():
    try:
        aws_access_key_id = os.environ['AWS_ACCESS_KEY']
        aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
        bucket_name = os.environ['S3_BUCKET']
        image_dir = os.environ['IMAGE_DIR']

        image_uploader = S3ImageUploader(bucket_name)
        image_uploader.upload_png_to_s3(image_dir)

        return jsonify({"message": "PNG files successfully copied to S3."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
