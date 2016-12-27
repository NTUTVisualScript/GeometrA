import cv2
import numpy as np

from utils import FindResult

class MultiScaleTemplateMatcher:
    def __init__(self, source_img, target_img):
        self.source_img = source_img.gray()
        self.target_img = target_img.gray().canny(50, 200)

    def find(self, min_scale=0.8, max_scale=1.2, interval=0.01):
        found = None

        sample_num = (max_scale - min_scale) / interval

        for scale in np.linspace(min_scale, max_scale, sample_num)[::-1]:
            # resize the image according to the scale, and keep track
            # of the ratio of the resizing
            r = 1 / scale
            resized_source = self.source_img.resize(scale)

            # if the resized image is smaller than the template, then break
            # from the loop
            if resized_source < self.target_img:
                break

            edged = resized_source.canny(50, 200)
            result = cv2.matchTemplate(edged.source, self.target_img.source, cv2.TM_CCOEFF_NORMED)
            _, maxVal, _, maxLoc = cv2.minMaxLoc(result)
            if found is None or maxVal > found[0]:
                found = (maxVal, maxLoc, r)

        maxVal, maxLoc, r = found

        x, y = maxLoc
        x *= r
        y *= r


        return FindResult(x, y, self.target_img.cols * r, self.target_img.rows * r, maxVal)
