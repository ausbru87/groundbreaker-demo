from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
sensor_initialized = False

@app.route('/')
def index():
    return render_template('index.html', sensor_initialized=sensor_initialized)

@app.route('/capture-images', methods=['POST'])
def capture_images():
    # Handles the POST request for capturing images
    # TODO: POST request to ImageSensor service
    return 'Images captured successfully!'

@app.route('/init-sensor', methods=['POST'])
def init_sensor():
    global sensor_initialized
    # Handles the POST request for initializing the sensor
    # TODO: POST request to ImageSensor service
    sensor_initialized = True  # Update sensor status
    return redirect(url_for('index'))


@app.route('/get-image', methods=['POST'])
def get_image():
    # Handles the POST request for getting an image
    # TODO: Add the ability to get the processed images?
    return 'Image retrieved successfully!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)