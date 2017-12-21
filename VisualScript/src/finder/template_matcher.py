import cv2
import numpy as np

from VisualScript.src.finder.utils import FindResult
from VisualScript.src.finder.rectangle import Rectangle


class TemplateMatcher:
    def __init__(self, source_img, target_img, level, factor):
        self.source_img = source_img
        self.target_img = target_img
        self.factor = factor
        self.level = level
        self.lower_pyramid = None
        self.cache_result = None

        if self.source_img < self.target_img:
            return

        if level > 0:
            self.lower_pyramid = self._create_small_matcher()

    def _create_small_matcher(self):
        return TemplateMatcher(
            self.source_img.resize(1 / self.factor),
            self.target_img.resize(1 / self.factor),
            self.level - 1,
            self.factor
        )

    def next(self):

        if self.source_img < self.target_img:    #
            return FindResult(0, 0, 0, 0, -1)

        if self.lower_pyramid != None:
            return self._next_from_lower_pyramid()

        if self.cache_result is None:
            detection_score, detection_loc = self._find_best()
        else:
            _, detection_score, _, detection_loc = cv2.minMaxLoc(self.cache_result)

        x_margin = int(self.target_img.cols / 3)
        y_margin = int(self.target_img.rows / 3)
        detection_x, detection_y = detection_loc

        self._erase_result(detection_x,
                           detection_y,
                           x_margin,
                           y_margin)

        result = FindResult(detection_x,
                            detection_y,
                            self.target_img.cols,
                            self.target_img.rows,
                            detection_score)

        return result

    def _find_best(self, roi=None):
        source_img = self.source_img
        target_img = self.target_img

        if roi:
            source_img = source_img.crop(roi)

        if target_img.is_same_color():
            if target_img.is_black():
                source_img = source_img.invert()
                target_img = target_img.invert()

            result = cv2.matchTemplate(source_img.source,
                                       target_img.source,
                                       cv2.TM_SQDIFF_NORMED)

            result = np.ones(result.size(), np.float32) - result
        else:
            result = cv2.matchTemplate(source_img.source,
                                       target_img.source,
                                       cv2.TM_CCOEFF_NORMED)

        self.cache_result = result
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(self.cache_result)

        return maxVal, maxLoc

    def _erase_result(self, x, y, x_margin, y_margin):
        x0 = max(x - x_margin, 0)
        y0 = max(y - y_margin, 0)

        rows, cols = self.cache_result.shape
        x1 = min(x + x_margin, cols)
        y1 = min(y + y_margin, rows)

        self.cache_result[y0:y1, x0:x1] = 0

    def _next_from_lower_pyramid(self):
        match = self.lower_pyramid.next()

        x = int(match.x * self.factor)
        y = int(match.y * self.factor)

        # Convert factor from float to int
        factor = int(self.factor)

        # Compute the parameter to define the neighborhood rectangle
        x0 = max(x - factor, 0)
        y0 = max(y - factor, 0)

        x1 = min(x + self.target_img.cols + factor, self.source_img.cols)
        y1 = min(y + self.target_img.rows + factor, self.source_img.rows)

        roi = Rectangle(x0, y0, x1 - x0, y1 - y0)

        detection_score, detection_loc = self._find_best(roi)

        detection_x, detection_y = detection_loc
        detection_x += roi.x
        detection_y += roi.y

        return FindResult(
            detection_x,
            detection_y,
            self.target_img.cols,
            self.target_img.rows,
            detection_score)
