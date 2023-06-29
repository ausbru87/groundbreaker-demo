from flask import Flask, request
from ImageDownlinker import ImageDownlinker
import logging
import os

app = Flask(__name__)
facility_a = 'http://192.168.92.140:8085'
facility_b = 'http://192.168.92.140:8086'
images_dir = '/images'
downlinker = ImageDownlinker(facility_a, facility_b, images_dir)

@app.route("/downlink", methods=["POST"])
def handle_downlink():
    global downlinker

    if downlinker.active_facility:
        downlinker.flush_downlink_queue()
        return "Image downlink initiated."
    else:
        return "No active facility available for downlink."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
