import cv2
import numpy as np

cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()
    imgScale = 0.5
    newX, newY = frame.shape[1] * imgScale, frame.shape[0] * imgScale
    scaled_img = cv2.resize(frame, (int(newX), int(newY)))
    hsv_image = cv2.cvtColor(scaled_img, cv2.COLOR_BGR2HSV)
    ycrcb_image = cv2.cvtColor(scaled_img, cv2.COLOR_BGR2YCrCb)
    bgra = cv2.cvtColor(scaled_img, cv2.COLOR_BGR2BGRA)

    h_range = (0,80)
    s_range = (0,1)
    v_range = (148,255)
    hsv_min = np.array([h_range[0], s_range[0], v_range[0]])
    # hsv_min = cv2.Scalar(h_range[0], s_range[0], v_range[0])
    # hsv_max = cv2.Scalar(h_range[1], s_range[1], v_range[1])
    hsv_max = np.array([h_range[1], s_range[1], v_range[1]])
    frame_threshed = cv2.inRange(hsv_image, hsv_min, hsv_max)
    # frame_threshed_opened = cv2.morphologyEx(frame_threshed, cv2.MORPH_OPEN, 1)
    frame_threshed_closed = cv2.morphologyEx(frame_threshed, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    y_range = (0,80)
    cr_range = (0,80)
    cb_range = (0,80)

    r_range = (0,80)
    g_range = (0,80)
    b_range = (0,80)

    cv2.imshow("Show by CV2", bgra)
    # cv2.imshow("test", frame)
    if not ret:
        break
    k = cv2.waitKey(1)

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print(bgra)

        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()