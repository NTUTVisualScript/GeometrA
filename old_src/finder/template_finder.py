from finder.template_matcher import TemplateMatcher
from finder import  ResultGenerator, Finder

class TemplateFinder(Finder):
    DEFAULT_PYRAMID_MIN_TARGET_DIMENSION = 12
    CENTER_REMATCH_THRESHOLD = 0.99

    def __init__(self, source_img=None):
        """
        :param source_img: The Source CV2Img
        """

        self._source_img = source_img
        self._matcher = None

        self._resize_ratio_list = [1, 0.75, 0.5, 0.25]
        self._roi = None

    def set_roi(self, rectangle):
        self._roi = rectangle

    def find(self, target_img, min_similarity=0.9):

        if self._roi:
            source_img = self._source_img.crop(self._roi)
        else:
            source_img = self._source_img

        target_rows, target_cols = target_img.shape[:2]
        matcher = None

        if target_img > source_img:
            return None

        ratio = min(target_img.rows / self.DEFAULT_PYRAMID_MIN_TARGET_DIMENSION,
                    target_img.cols / self.DEFAULT_PYRAMID_MIN_TARGET_DIMENSION)

        return TemplateFinderResultGenerator(source_img, target_img, self._roi, min_similarity, ratio, self._resize_ratio_list)

class TemplateFinderResultGenerator(ResultGenerator):

    def __init__(self, source_img, target_img, roi, min_similarity, ratio, resize_ratio_list):
        self._source_img = source_img
        self._target_img = target_img
        self._roi = roi
        self._min_similarity = min_similarity
        self._ratio = ratio
        self._resize_ratio_list = resize_ratio_list

        self._matcher = None
        self._result_list = None

    def _next_list(self, matcher, size):
        result = []

        for index in range(0, size):
            item = matcher.next()

            if item is None:
                break
            else:
                result.append(item)

        return result

    def _check_result_is_good_enough(self, matcher):
        result_list = []
        result_list.extend(self._next_list(matcher, 5))
        result_list.sort(key=lambda item: item.score, reverse=True)

        # Good enough
        if result_list[0].score >= max(self._min_similarity, TemplateFinder.CENTER_REMATCH_THRESHOLD):
            return result_list

        return None

    def _create_matcher(self):
        # Step 1: Get the resuls by pyramid template matcher with color
        for resize_ratio in self._resize_ratio_list:
            new_ratio = self._ratio * resize_ratio

            if new_ratio >= 1:
                matcher = TemplateMatcher(self._source_img, self._target_img, 1, new_ratio)

                # Good enough
                result_list = self._check_result_is_good_enough(matcher)
                if result_list:
                    return matcher, result_list

        return None, []

    def next(self):
        if self._result_list is None:
            self._matcher, self._result_list = self._create_matcher()

        if len(self._result_list) == 0:
            return None

        elif self._result_list[0].score >= self._min_similarity - 0.0000001:
            result = self._result_list.pop(0)

            if self._roi:
                result.x += self._roi.x
                result.y += self._roi.y

            self._result_list.append(self._matcher.next())
            self._result_list.sort(key=lambda item: item.score, reverse=True)

            return result
