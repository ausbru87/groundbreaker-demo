from flask import Flask, request
from image_forwarder import ImageForwarder
import logging
import os

app = Flask(__name__)

aws_receiver_var = 'AWS_RECEIVER'
# TODO: Add azure receiver

if aws_receiver_var in os.environ:
    aws_receiver = os.environ[aws_receiver_var]
else:
    print(f"{aws_receiver_var} does not exist in the environment.")
    # TODO: make this a logging statement (ERROR)

images_dir = '/images/out'
forwarder = ImageForwarder(images_dir, aws_receiver)

@app.route("/forward", methods=["POST"])
def handle_forward():
    global forwarder
    forwarder.flush_forward_queue()
    return "Image forward initiated."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
