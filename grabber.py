import sys

import cv2
from imgprocessor import ImageProcessor

ALGO_SIMPLE = 0
ALGO_ADV = 1

algorithm = ALGO_SIMPLE
capture_name = "palm"
images_to_capture = 300
capture_delay = 0.1

# usage: python grabber.py <gesture_name>
if __name__ == '__main__':
    if len(sys.argv) >= 2:
        capture_name = sys.argv[1]

    cam = cv2.VideoCapture(0)

    # ImageProcessor(cam reference, image scale)
    ip = ImageProcessor(cam, 0.5)

    if algorithm is ALGO_SIMPLE:
        # custom_hsv_ranges = ((0, 90), # H
        #                      (0,255), # S
        #                      (120,255)) # V
        custom_hsv_ranges = ((80, 110),  # H
                             (100, 255),  # S
                             (140, 255))  # V
        ip.redefine_simple_algorithm(custom_hsv_ranges)
        ip.start_grabber(ALGO_SIMPLE, capture_name, images_to_capture, capture_delay)
    elif algorithm is ALGO_ADV:
        ip.start_grabber(ALGO_ADV, capture_name, images_to_capture, capture_delay)
