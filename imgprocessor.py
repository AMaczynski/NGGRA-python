import math
import os
import threading
from time import sleep
import pyautogui

import cv2

from algoimpl import simple_algorithm, advanced_algorithm
from classifier import Classifier

ALGO_SIMPLE = 0
ALGO_ADV = 1

RIGHT = 1
LEFT = 2
UP = 3
DOWN = 4

COLOR_RED = (66, 66, 244)

STATE_WAITING = 0
STATE_GRABBING = 1


def get_largest_contour(frame):
    ret, thresh = cv2.threshold(frame, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    biggest_contour = None
    biggest_contour_area = -1
    if contours is not None:
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > biggest_contour_area:
                biggest_contour = contour
                biggest_contour_area = area

        if biggest_contour is not None:
            return cv2.boundingRect(biggest_contour)
    return None


def move_mouse2(x_diff, y_diff, x_image_size):
    x_pos, y_pos = pyautogui.position()
    x_screen, y_screen = pyautogui.size()
    scale = x_screen / x_image_size
    x_pos = x_pos - x_diff * scale
    y_pos = y_pos + y_diff * scale
    pyautogui.moveTo(x_pos, y_pos)

    return x_pos, y_pos


def move_mouse(x, y, x_max, y_max):
    x_screen, y_screen = pyautogui.size()

    # tutaj usuwamy efekt odbicia lustrzanego
    x_value=x_screen-(x * math.floor(x_screen / x_max))
    y_value = y * math.floor(y_screen / y_max)

    pyautogui.moveTo(x_value, y_value)

    return x_value, y_value


def mouse_click(x, y):
    pyautogui.click(x, y)


def follow_center(processed_image, even, start, cX1, cX2, cY1, cY2):
    gray_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray_image, 127, 255, 0)
    moments = cv2.moments(thresh)

    if moments["m00"] != 0:
        if even:
            cX1 = int(moments["m10"] / moments["m00"])
            cY1 = int(moments["m01"] / moments["m00"])
        else:
            cX2 = int(moments["m10"] / moments["m00"])
            cY2 = int(moments["m01"] / moments["m00"])

    if even:
        cX_actual = cX1
        cY_actual = cY1
        cX_prev = cX2
        cY_prev = cY2
    else:
        cX_actual = cX2
        cY_actual = cY2
        cX_prev = cX1
        cY_prev = cY1

    for i in range(-4, 5):
        try:
            processed_image[cY_actual + i][cX_actual] = COLOR_RED
        except IndexError:
            print("error")

    for j in range(-4, 5):
        try:
            processed_image[cY_actual][cX_actual + j] = COLOR_RED
        except IndexError:
            print("error")

    if start:
        print(even)
        if cX_actual - cX_prev > 5:
            return RIGHT, cX1, cX2, cY1, cY2
        if cX_prev - cX_actual > 5:
            return LEFT, cX1, cX2, cY1, cY2
        if cY_actual - cY_prev > 5:
            return DOWN, cX1, cX2, cY1, cY2
        if cY_prev - cY_actual > 5:
            return UP, cX1, cX2, cY1, cY2

    return None, cX1, cX2, cY1, cY2


class ImageProcessor:
    def __init__(self, cam, target_scale, mouse_control):
        self.classifier = Classifier()
        self.cam = cam
        self.target_scale = target_scale
        self.custom_simple_ranges = None
        self.mouse_control = mouse_control
        self.wait_complete = True

    # czekanie żeby nie spamowało akcjami cały czas
    # jeden gest na 3 sekundy - jedna akcja
    # żeby użytkownik zdążył zabrać rękę/zmienić gest
    def end_wait(self):
        self.wait_complete = True
        print("wait over")

    def play(self):
        if self.wait_complete:
            pyautogui.press("playpause")
            print("PLAY/PAUSE")
            self.wait_complete = False
            timer = threading.Timer(3.0, self.end_wait)
            timer.start()
        else:
            print("wait not over")

    def next_track(self):
        if self.wait_complete:
            pyautogui.press("nexttrack")
            print("NEXT TRACK")
            self.wait_complete = False
            timer = threading.Timer(3.0, self.end_wait)
            timer.start()
        else:
            print("wait not over")

    def mute(self):
        if self.wait_complete:
            pyautogui.press("volumemute")
            print("MUTE/UNMUTE")
            self.wait_complete = False
            timer = threading.Timer(3.0, self.end_wait)
            timer.start()
        else:
            print("wait not over")

    def redefine_simple_algorithm(self, hsv_ranges):
        self.custom_simple_ranges = hsv_ranges

    def start_loop(self, target_algorithm, detector, display=False):
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

            print(results)
            print(direction)

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
        if self.mouse_control:
            x_image_size = processed_image.shape[1]
            x, y = pyautogui.position()

            if results[0][1] > 0.65 and results[0][0] == 'palm':
                if even:
                    x_diff = cX1 - cX2
                    y_diff = cY1 - cY2
                    x, y = move_mouse2(x_diff, y_diff, x_image_size)
                else:
                    x_diff = cX2 - cX1
                    y_diff = cY2 - cY1
                    x, y = move_mouse2(x_diff, y_diff, x_image_size)

            if results[0][1] > 0.65 and results[0][0] == 'fist':
                mouse_click(x, y)
        # thumb - wyciszenie
        if results[0][1] > 0.65 and results[0][0] == 'thumb':
            self.mute()
        # peace - następny utwór
        if results[0][1] > 0.65 and results[0][0] == 'peace':
            self.next_track()
        # straight - play/pause
        if results[0][1] > 0.8 and results[0][0] == 'straight':
            self.play()

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
                    img_cropped_name = "output_cropped/%s/%s_%d.jpg" % (
                    file_name, file_name, start_number + img_counter)

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
        if target_algorithm == ALGO_SIMPLE:
            processed_image = simple_algorithm(scaled_img, self.custom_simple_ranges)
        elif target_algorithm == ALGO_ADV:
            processed_image = advanced_algorithm(scaled_img)

        processed_image = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2BGR)

        return processed_image
