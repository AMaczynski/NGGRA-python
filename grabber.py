import os

import cv2

from imgprocessor import ImageProcessor

ALGO_SIMPLE = 0
ALGO_ADV = 1

algorithm = ALGO_SIMPLE
capture_name = "thumb"
images_to_capture = 1000
capture_delay = 0.01

save_raw = True
save_bin = True
save_cropped_bin = True
grab_test = False

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    # ImageProcessor(cam reference, image scale)
    ip = ImageProcessor(cam, 0.5)
    start_number = 0
    if grab_test:
        dir_path = "test"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        else:
            files = os.listdir(dir_path)
            for file in files:
                number = int(file.split("_")[-1][:-4])
                if number > start_number:
                    start_number = number
            start_number += 1
    else:
        dir_path = "output/%s" % capture_name
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        else:
            files = os.listdir(dir_path)
            for file in files:
                number = int(file.split("_")[-1][:-4])
                if number > start_number:
                    start_number = number
            start_number += 1
        dir_path = "output_cropped/%s" % capture_name
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        dir_path = "output_raw/%s" % capture_name
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    if algorithm is ALGO_SIMPLE:
        # custom_hsv_ranges = ((20, 50), # H
        #                      (0,255), # S
        #                      (0,120)) # V
        custom_hsv_ranges = ((80, 110),  # H
                             (100, 255),  # S
                             (140, 255))  # V
        ip.redefine_simple_algorithm(custom_hsv_ranges)
        ip.start_grabber(ALGO_SIMPLE, capture_name, images_to_capture, capture_delay, start_number, grab_test)
    elif algorithm is ALGO_ADV:
        ip.start_grabber(ALGO_ADV, capture_name, images_to_capture, capture_delay, start_number, grab_test)
