from config import IMG_PATH
from cv2img import CV2Img
from finder.template_matcher import TemplateMatcher


def test_pyramid_template_matcher():
    source = CV2Img()
    source.load_file(IMG_PATH("screen.png"),-1)

    target = CV2Img()
    target.load_file(IMG_PATH("gmail.png"),-1)

    ratio = min(target.rows / 12, target.cols / 12)

    matcher = TemplateMatcher(source, target, 1, ratio)
    result = matcher.next()
    assert result.score == 1.0

    result_image = source.crop(result)
    assert result_image == target
