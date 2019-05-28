from time import sleep

import cv2
import pyautogui

from ConfigManager import *
from algoimpl import simple_algorithm, advanced_algorithm
from classifier import Classifier
from functions import follow_center, get_largest_contour, calc_new_mouse_position

ALGORITHM_SIMPLE = 0
ALGORITHM_ADV = 1

STATE_WAITING = 0
STATE_GRABBING = 1


class ImageProcessor:
    def __init__(self, cam, target_scale):
        self.classifier = Classifier()
        self.cam = cam
        self.target_scale = target_scale
        self.custom_simple_ranges = None
        self.mouse_control = False

        self.detector = None
        self.gesture_move = None
        self.gesture_click = None

    def attach_detector(self, detector):
        self.detector = detector

    def enable_mouse_control(self):
        self.mouse_control = True

    def set_gesture_move(self, gesture_move):
        self.gesture_move = gesture_move

    def set_gesture_click(self, gesture_click):
        self.gesture_click = gesture_click

    def redefine_simple_algorithm(self, hsv_ranges):
        self.custom_simple_ranges = hsv_ranges

    def start_loop(self, target_algorithm, display=False):
        even = True
        start = False
        cX1 = 0
        cX2 = 0
        cY1 = 0
        cY2 = 0

        while True:
            ret, frame = self.cam.read()
            if not ret:
                break
            processed_image = self.get_processed_image(frame, target_algorithm)
            if processed_image is None:
                break

            results = self.start_tensorflow_analyser(processed_image)
            direction, cX1, cX2, cY1, cY2 = follow_center(processed_image, even, start, cX1, cX2, cY1, cY2)

            self.controls(cX1, cX2, cY1, cY2, even, processed_image, results)

            start = True
            even = not even

            if display:
                cv2.imshow("Show by CV2", processed_image)
                k = cv2.waitKey(1)
                if k % 256 == 27:  # ESC
                    print("Escape hit, closing...")
                    break
        self.cam.release()
        cv2.destroyAllWindows()

    def controls(self, cX1, cX2, cY1, cY2, even, processed_image, results):
        gesture = results[0][0]
        probability = results[0][1]
        if self.mouse_control:
            x_image_size = processed_image.shape[1]
            x, y = pyautogui.position()
            if probability > 0.65 and gesture == self.gesture_move:
                if even:
                    x_diff = cX1 - cX2
                    y_diff = cY1 - cY2
                    x, y = calc_new_mouse_position(x_diff, y_diff, x_image_size)
                    self.detector.on_gesture_move(x, y)
                else:
                    x_diff = cX2 - cX1
                    y_diff = cY2 - cY1
                    x, y = calc_new_mouse_position(x_diff, y_diff, x_image_size)
                    self.detector.on_gesture_move(x, y)

            if probability > 0.65 and gesture == self.gesture_click:
                self.detector.on_gesture_click(x, y)

        if probability > 0.65 and gesture != NONE:
            self.detector.on_gesture(gesture)

    def start_tensorflow_analyser(self, processed_image):
        return self.classifier.label_image(processed_image)

    def start_grabber(self, target_algorithm, file_name, grabber_target, grabber_delay, start_number, grab_test=False):
        grabber_state = STATE_WAITING
        img_counter = 0
        while True:
            ret, frame = self.cam.read()
            if not ret:
                break
            processed_image = self.get_processed_image(frame, target_algorithm)
            if processed_image is None:
                break
            cv2.imshow("Show by CV2", processed_image)
            k = cv2.waitKey(1)

            if grabber_state == STATE_GRABBING:
                if grab_test:
                    img_name = "test/test_%s_%d.jpg" % (file_name, start_number + img_counter)
                    cv2.imwrite(img_name, processed_image)
                else:
                    img_name = "output/%s/%s_%d.jpg" % (file_name, file_name, start_number + img_counter)
                    img_raw_name = "output_raw/%s/%s_%d.jpg" % (file_name, file_name, start_number + img_counter)
                    img_cropped_name = "output_cropped/%s/%s_%d.jpg" % (file_name, file_name,
                                                                        start_number + img_counter)

                    gray_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
                    contours = get_largest_contour(gray_image)
                    if contours is not None:
                        x, y, w, h = contours
                        cropped_img = processed_image[y:y + h, x:x + w]
                        cv2.imwrite(img_cropped_name, cropped_img)

                    cv2.imwrite(img_raw_name, frame)
                    cv2.imwrite(img_name, processed_image)
                print("{} written!".format(img_name))
                img_counter += 1
                sleep(grabber_delay)
                if img_counter == grabber_target:
                    break
            else:

                if k % 256 == 27:  # ESC
                    print("Escape hit, closing...")
                    break
                elif k % 256 == 32:  # space
                    print("Starting grabbing")
                    grabber_state = STATE_GRABBING
        self.cam.release()
        cv2.destroyAllWindows()

    def get_processed_image(self, frame, target_algorithm):
        new_x, new_y = frame.shape[1] * self.target_scale, frame.shape[0] * self.target_scale
        scaled_img = cv2.resize(frame, (int(new_x), int(new_y)))

        processed_image = None
        if target_algorithm == ALGORITHM_SIMPLE:
            processed_image = simple_algorithm(scaled_img, self.custom_simple_ranges)
        elif target_algorithm == ALGORITHM_ADV:
            processed_image = advanced_algorithm(scaled_img)

        processed_image = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2BGR)

        return processed_image
