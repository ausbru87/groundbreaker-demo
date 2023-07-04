from flask import Flask, request
from image_downlinker import ImageDownlinker
import os

app = Flask(__name__)

edgefac_a_var = 'FACILITY_A'
edgefac_b_var = 'FACILITY_B'

# Check if the environment variable exists
if edgefac_a_var in os.environ:
    # Get the value of the environment variable
    edgefac_a_value = os.environ[edgefac_a_var]
    print(f"FACILITY_A is set to: {edgefac_a_value}")
else:
    print(f"{edgefac_a_var} does not exist in the environment.")

# Check if the environment variable exists
if edgefac_b_var in os.environ:
    # Get the value of the environment variable
    edgefac_b_value = os.environ[edgefac_b_var]
    print(f"FACILITY_B is set to: {edgefac_b_value}")
else:
    print(f"{edgefac_a_var} does not exist in the environment.")

images_dir = '/images/in'
downlinker = ImageDownlinker(edgefac_a_value, edgefac_b_value, images_dir)

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
