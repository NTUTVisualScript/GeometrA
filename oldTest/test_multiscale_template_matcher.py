import numpy as np
import pytest

from config import IMG_PATH
from cv2img import CV2Img
from finder.multiscale_template_matcher import MultiScaleTemplateMatcher
from finder.template_finder import TemplateFinder

size_list = np.arange(0.7, 1, 0.01)
error = 10 #px

@pytest.mark.parametrize("size", size_list)
def test_multiscale_template_matcher(size):
    source = CV2Img()
    source.load_file(IMG_PATH("screen.png"))

    target = CV2Img()
    target.load_file(IMG_PATH("gmail.png"))

    # Use finder to get the location of target
    finder = TemplateFinder(source)
    result_generator = finder.find(target, 0.9)
    result = result_generator.next()
    assert result.score == 1.0

    # Resize the target image and use multiple scale template matcher to find the location
    target = target.resize(size)
    matcher = MultiScaleTemplateMatcher(source, target)
    result2 = matcher.find(0.7, 1, 0.01)

    print(result2.score)
    assert result2.x >= result.x - error and result2.x <= result.x + error
    assert result2.y >= result.y - error and result2.y <= result.y + error
    assert result2.w >= result.w - error and result2.w <= result.w + error
    assert result2.h >= result.h - error and result2.h <= result.h + error


