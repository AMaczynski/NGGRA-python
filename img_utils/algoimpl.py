from copy import copy

import cv2
import numpy as np


def simple_algorithm(frame, hsv_ranges=None):
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # h_range = (0, 80)
    # s_range = (0, 255)
    # v_range = (148, 255)

    h_range = (80, 110)
    s_range = (100, 255)
    v_range = (140, 255)

    if hsv_ranges is not None:
        h_range = hsv_ranges[0]
        s_range = hsv_ranges[1]
        v_range = hsv_ranges[2]
    hsv_min = np.array([h_range[0], s_range[0], v_range[0]])
    hsv_max = np.array([h_range[1], s_range[1], v_range[1]])
    frame_threshed = cv2.inRange(hsv_image, hsv_min, hsv_max)
    frame_threshed_closed = cv2.morphologyEx(frame_threshed, cv2.MORPH_CLOSE,
                                             cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    return frame_threshed_closed


def advanced_algorithm(frame):
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    ycrcb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    output_img = copy(frame)

    for i in range(0, len(hsv_image)):
        for j in range(0, len(hsv_image[0])):
            h = hsv_image[i][j][0] * 2
            s = hsv_image[i][j][1] / 255
            b = frame[i][j][0]
            g = frame[i][j][1]
            r = frame[i][j][2]
            y = ycrcb_image[i][j][0]
            cr = ycrcb_image[i][j][1]
            cb = ycrcb_image[i][j][2]

            if h <= 50.0 and 0.23 <= s <= 0.68 and r > 95 and g > 40 and b > 20 and r > g and r > b and abs(
                    r - g) > 15:
                output_img[i][j] = 255
            elif r > 95 and g > 40 and b > 20 and r > g and r > b and abs(
                    r - g) > 15 and cr > 135 and cb > 85 and y > 80 and ((1.5862 * cb) + 20) >= cr >= (
                    (0.3448 * cb) + 76.2069) and ((-4.5652 * cb) + 234.5652) <= cr <= (
                    (-1.15 * cb) + 301.75) and cr <= ((-2.2857 * cb) + 432.85):
                output_img[i][j] = 255
            else:
                output_img[i][j] = 0

    return output_img
