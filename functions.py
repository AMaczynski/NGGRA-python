import cv2
import pyautogui

COLOR_RED = (66, 66, 44)

RIGHT = 1
LEFT = 2
UP = 3
DOWN = 4


def calc_new_mouse_position(x_diff, y_diff, x_image_size):
    x_pos, y_pos = pyautogui.position()
    x_screen, y_screen = pyautogui.size()
    scale = x_screen / x_image_size
    x_pos = x_pos - x_diff * scale
    y_pos = y_pos + y_diff * scale
    return x_pos, y_pos


def move_mouse(x_pos, y_pos):
    pyautogui.moveTo(x_pos, y_pos)


def mouse_click(x, y):
    pyautogui.click(x, y)


def mute():
    pyautogui.press("volumemute")


def next_track():
    pyautogui.press("nexttrack")


def play():
    pyautogui.press("playpause")


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
        # print(even)
        if cX_actual - cX_prev > 5:
            return RIGHT, cX1, cX2, cY1, cY2
        if cX_prev - cX_actual > 5:
            return LEFT, cX1, cX2, cY1, cY2
        if cY_actual - cY_prev > 5:
            return DOWN, cX1, cX2, cY1, cY2
        if cY_prev - cY_actual > 5:
            return UP, cX1, cX2, cY1, cY2

    return None, cX1, cX2, cY1, cY2
