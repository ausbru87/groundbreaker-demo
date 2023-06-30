import cv2
import numpy as np

class ShipDetector:
    def __init__(self, image_path):
        self.image_path = image_path

    def detect_ship(self, image):
        image = cv2.imread(self.image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)

        # Find contours of the objects in the image
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # Approximate the contour to a polygon
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
            if len(approx) == 4:
                return True
        
        return False

    def chip_ship(self):
        image = cv2.imread(self.image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)

        # Find contours of the objects in the image
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # Approximate the contour to a polygon
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)
                chip = image[y:y+h, x:x+w]
                return chip
        
        return None

    def label_ship(self):
        chip = cv2.imread(self.image_path)
        label = "SHIP"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        color = (255, 255, 255)  # White color
        thickness = 2

        x, y, w, h = 10, 30, 20 * len(label) + 20, 50
        cv2.rectangle(chip, (x, y), (x + w, y + h), (0, 255, 0), -1)  # Light green rectangle
        cv2.putText(chip, label, (x + 10, y + 35), font, font_scale, color, thickness, cv2.LINE_AA)

        return chip
