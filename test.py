import cv2

from imgprocessor import ImageProcessor, follow_center

ALGO_SIMPLE = 0
ALGO_ADV = 1

algorithm = ALGO_SIMPLE
capture_name = "none"
images_to_capture = 10
capture_delay = 0.5

save_raw = True
save_bin = True
save_cropped_bin = True
grab_test = True

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    # ImageProcessor(cam reference, image scale)
    ip = ImageProcessor(cam, 0.5,False)
    start_number = 0

    custom_hsv_ranges = ((80, 110),  # H
                         (100, 255),  # S
                         (140, 255))  # V

    ip.redefine_simple_algorithm(custom_hsv_ranges)
    # follow_center(ALGO_SIMPLE)
