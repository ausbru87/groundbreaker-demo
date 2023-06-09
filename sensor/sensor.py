import random
from PIL import Image

# Image Sensor Def
sensor_width = 1080
sensor_height = 480
resolution = (sensor_width, sensor_height)

# Random RGB value
def random_color():
    return (random.randint(0,255), random.randint(0,255), random.randint(0,255))

# Generate Image
img = Image.new('RGB', resolution)
for x in range(sensor_width):
    for y in range(sensor_height):
        img.putpixel((x,y), random_color())

# Output Image
img.save('./image.jpg')
