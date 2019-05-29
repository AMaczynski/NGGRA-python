import cv2

COLOR_RED = (66, 66, 44)


class FollowShapeCenter:
    def __init__(self):
        self.start = False
        self.even = True
        self.cX1 = 0
        self.cX2 = 0
        self.cY1 = 0
        self.cY2 = 0

    def follow_center(self, processed_image):
        gray_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray_image, 127, 255, 0)
        moments = cv2.moments(thresh)

        if moments["m00"] != 0:
            if self.even:
                self.cX1 = int(moments["m10"] / moments["m00"])
                self.cY1 = int(moments["m01"] / moments["m00"])
            else:
                self.cX2 = int(moments["m10"] / moments["m00"])
                self.cY2 = int(moments["m01"] / moments["m00"])
        if self.even:
            cX_actual = self.cX1
            cY_actual = self.cY1
            cX_prev = self.cX2
            cY_prev = self.cY2
        else:
            cX_actual = self.cX2
            cY_actual = self.cY2
            cX_prev = self.cX1
            cY_prev = self.cY1

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

        self.even = not self.even

        if self.start:
            if cX_actual - cX_prev > 5:
                return self.even, self.cX1, self.cX2, self.cY1, self.cY2
            if cX_prev - cX_actual > 5:
                return self.even, self.cX1, self.cX2, self.cY1, self.cY2
            if cY_actual - cY_prev > 5:
                return self.even, self.cX1, self.cX2, self.cY1, self.cY2
            if cY_prev - cY_actual > 5:
                return self.even, self.cX1, self.cX2, self.cY1, self.cY2

        self.start = True

        return self.even, self.cX1, self.cX2, self.cY1, self.cY2
