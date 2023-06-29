import cv2

class ShipFinder:
    def __init__(self, image_path):
        self.image_path = image_path

    def find_ships(self):
        # Load the image using OpenCV
        image = cv2.imread(self.image_path)

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply edge detection to find edges in the image
        edges = cv2.Canny(gray, 50, 150)

        # Find contours of the objects in the image
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # Approximate the contour to a polygon
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)

            # If the polygon has 4 vertices, it is likely a rectangle (ship)
            if len(approx) == 4:
                return True

        return False
