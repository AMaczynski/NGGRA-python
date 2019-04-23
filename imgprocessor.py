import os
from time import sleep

import cv2

from algoimpl import simple_algorithm, advanced_algorithm
from classifier import Classifier

ALGO_SIMPLE = 0
ALGO_ADV = 1

STATE_WAITING = 0
STATE_GRABBING = 1


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

    def start_grabber(self, target_algorithm, file_name, grabber_target, grabber_delay):
        grabber_state = STATE_WAITING
        img_counter = 0
        while True:
            processed_image = self.get_processed_image(target_algorithm)
            if processed_image is None:
                break
            cv2.imshow("Show by CV2", processed_image)
            if grabber_state == STATE_GRABBING:
                img_name = "output/%s/%s_%d.jpg" % (file_name, file_name, img_counter)
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
                    if not os.path.exists("output/" + file_name):
                        os.makedirs("output/" + file_name)
                    print("Starting grabbing")
                    grabber_state = STATE_GRABBING
        self.cam.release()
        cv2.destroyAllWindows()

    def get_processed_image(self, target_algorithm):
        ret, frame = self.cam.read()
        new_x, new_y = frame.shape[1] * self.target_scale, frame.shape[0] * self.target_scale
        scaled_img = cv2.resize(frame, (int(new_x), int(new_y)))
        if not ret:
            return None
        processed_image = None
        if target_algorithm == ALGO_SIMPLE:
            processed_image = simple_algorithm(scaled_img, self.custom_simple_ranges)
        elif target_algorithm == ALGO_ADV:
            processed_image = advanced_algorithm(scaled_img)

        return processed_image
