from time import sleep

import cv2
import pyautogui

from config_utils.ConfigManager import *
from img_utils.algoimpl import simple_algorithm, advanced_algorithm
from img_utils.classifier import Classifier
from img_utils.followvideocenter import FollowShapeCenter
from app_utils.functions import get_largest_contour, calc_new_mouse_position

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
        self.fvc = FollowShapeCenter()
        self.detector = None
        self.gesture_move = None
        self.gesture_click = None

    def attach_detector(self, detector):
        self.detector = detector

    def set_gesture_move(self, gesture_move):
        self.gesture_move = gesture_move

    def set_gesture_click(self, gesture_click):
        self.gesture_click = gesture_click

    def redefine_simple_algorithm(self, hsv_ranges):
        self.custom_simple_ranges = hsv_ranges

    def start_loop(self, target_algorithm, display=False):

        while True:
            ret, frame = self.cam.read()
            if not ret:
                break
            processed_image = self.get_processed_image(frame, target_algorithm)
            if processed_image is None:
                break

            results = self.start_tensorflow_analyser(processed_image)

            self.controls(processed_image, results)

            if display:
                cv2.imshow("Show by CV2", processed_image)
                k = cv2.waitKey(1)
                if k % 256 == 27:  # ESC
                    print("Escape hit, closing...")
                    break
        self.cam.release()
        cv2.destroyAllWindows()

    def controls(self, processed_image, results):
        gesture = results[0][0]
        probability = results[0][1]
        if probability < 0.65 or gesture == GESTURE_NONE:
            return

        cx_diff, cy_diff = self.fvc.follow_center(processed_image)
        if self.gesture_move is not None and gesture == self.gesture_move:
            x_image_size = processed_image.shape[1]
            new_mouse_position = calc_new_mouse_position(cx_diff, cy_diff, x_image_size)
            self.detector.on_gesture_move(new_mouse_position[0], new_mouse_position[1])

        if self.gesture_click is not None and gesture == self.gesture_click:
            mouse_position = pyautogui.position()
            self.detector.on_gesture_click(mouse_position[0], mouse_position[1])

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
                    img_name = "test_data/test_%s_%d.jpg" % (file_name, start_number + img_counter)
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
