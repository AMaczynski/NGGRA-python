import cv2
import pyautogui


def calc_new_mouse_position(x_diff, y_diff, x_image_size):
    x_pos, y_pos = pyautogui.position()
    x_screen, y_screen = pyautogui.size()
    scale = x_screen / x_image_size
    x_pos = x_pos - x_diff * scale * 1.1
    y_pos = y_pos + y_diff * scale * 1.1
    return x_pos, y_pos


def calc_coords_change(cx1, cx2, cy1, cy2, revert):
    if revert:
        return cx2 - cx1, cy2 - cy1
    return cx1 - cx2, cy1 - cy2


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


def vol_up():
    pyautogui.press("volumeup")


def vol_down():
    pyautogui.press("volumedown")


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
