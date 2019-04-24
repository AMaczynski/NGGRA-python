import os
from time import sleep

import cv2

from algoimpl import simple_algorithm, advanced_algorithm
from classifier import Classifier

ALGO_SIMPLE = 0
ALGO_ADV = 1

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


class ImageProcessor:
    def __init__(self, cam, target_scale):
        self.cam = cam
        self.target_scale = target_scale
        self.custom_simple_ranges = None

    def redefine_simple_algorithm(self, hsv_ranges):
        self.custom_simple_ranges = hsv_ranges

    def start_tensorflow_analyser(self, target_algorithm, detector, display = False):
        self.classifier = Classifier()
        while True:
            processed_image = self.get_processed_image(target_algorithm)
            if processed_image is None:
                break
            results = self.classifier.label_image(processed_image)
            print(results)
            if results[0][1] > 0.7:
                detector.on_gesture(results[0][0])
            else:
                detector.on_gesture(None)
            if display:
                cv2.imshow("Show by CV2", processed_image)
                k = cv2.waitKey(1)
                if k % 256 == 27:  # ESC
                    print("Escape hit, closing...")
                    break

        self.cam.release()
        cv2.destroyAllWindows()

    def start_grabber(self, target_algorithm, file_name, grabber_target, grabber_delay, start_number):
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
            if grabber_state == STATE_GRABBING:
                img_name = "output/%s/%s_%d.jpg" % (file_name, file_name, start_number + img_counter)
                img_raw_name = "output_raw/%s/%s_%d.jpg" % (file_name, file_name, start_number + img_counter)
                img_cropped_name = "output_cropped/%s/%s_%d.jpg" % (file_name, file_name, start_number + img_counter)

                contours = get_largest_contour(processed_image)
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
                k = cv2.waitKey(1)

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

        return processed_image

