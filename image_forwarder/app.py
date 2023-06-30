from flask import Flask, request
from image_forwarder import ImageForwarder
import logging
import os

app = Flask(__name__)
destination = 'http://core-facility:9000'
images_dir = '/images/out'
forwarder = ImageForwarder(images_dir, destination)

@app.route("/forward", methods=["POST"])
def handle_forward():
    global forwarder
    forwarder.flush_forward_queue()
    return "Image forward initiated."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
