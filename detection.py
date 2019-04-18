import cv2
import numpy as np

cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()
    imgScale = 1
    newX, newY = frame.shape[1] * imgScale, frame.shape[0] * imgScale
    scaled_img = cv2.resize(frame, (int(newX), int(newY)))
    hsv_image = cv2.cvtColor(scaled_img, cv2.COLOR_BGR2HSV)
    ycrcb_image = cv2.cvtColor(scaled_img, cv2.COLOR_BGR2YCrCb)
    bgra = cv2.cvtColor(scaled_img, cv2.COLOR_BGR2BGRA)

    output_im = cv2.resize(frame, (int(newX), int(newY)))
    output_img = cv2.cvtColor(output_im, cv2.COLOR_BGR2GRAY)

    h_range = (0, 80)
    s_range = (0, 255)
    v_range = (148, 255)
    hsv_min = np.array([h_range[0], s_range[0], v_range[0]])
    hsv_max = np.array([h_range[1], s_range[1], v_range[1]])
    frame_threshed = cv2.inRange(hsv_image, hsv_min, hsv_max)
    frame_threshed_closed = cv2.morphologyEx(frame_threshed, cv2.MORPH_CLOSE,
                                             cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    y_range = (0, 80)
    cr_range = (0, 80)
    cb_range = (0, 80)

    r_range = (0, 80)
    g_range = (0, 80)
    b_range = (0, 80)

    cv2.imshow("Show by CV2", frame_threshed_closed)
    # cv2.imshow("test", frame)
    if not ret:
        break
    k = cv2.waitKey(1)

    if k % 256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k % 256 == 32:
        print("%d x %d" % (len(hsv_image), len(hsv_image[0])))
        # print(hsv_image[239])
        h_table = []
        s_table = []
        for i in range(0, len(hsv_image)):
            for j in range(0, len(hsv_image[0])):
                h = hsv_image[i][j][0] * 2
                s = hsv_image[i][j][1] / 255
                b = scaled_img[i][j][0]
                g = scaled_img[i][j][1]
                r = scaled_img[i][j][2]
                y = ycrcb_image[i][j][0]
                cr = ycrcb_image[i][j][1]
                cb = ycrcb_image[i][j][2]

                if h <= 50.0 and 0.23 <= s <= 0.68 and r > 95 and g > 40 and b > 20 and r > g and r > b and abs(
                        r - g) > 15:
                    output_img[i][j] = 255
                elif r > 95 and g > 40 and b > 20 and r > g and r > b and abs(
                        r - g) > 15 and cr > 135 and cb > 85 and y > 80 and cr <= ((1.5862 * cb) + 20) and cr >= (
                        (0.3448 * cb) + 76.2069) and cr >= ((-4.5652 * cb) + 234.5652) and cr <= (
                        (-1.15 * cb) + 301.75) and cr <= ((-2.2857 * cb) + 432.85):
                    output_img[i][j] = 255
                else:
                    output_img[i][j] = 0

        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, output_img)
        # print(bgra)
        #
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()
