import os
from cv2img import CV2Img
from adb_roboot import ADBRobot
from finder.template_finder import TemplateFinder
from finder.template_matcher import TemplateMatcher


ROOT_DIR = os.path.dirname(__file__)
RESOURCES_DIR = os.path.join(ROOT_DIR, "screenshot_pic")

source_image = None

def IMG_PATH(name):
    return os.path.join(RESOURCES_DIR, name)

def template_finder_Click(target_image):
    robot = ADBRobot()
    source = CV2Img()
    global source_image
    if source_image == None:
        source.load_file(IMG_PATH(robot.screenshot()), 1)
    else:
        source = source_image
    source.show()
    target = CV2Img()
    target.load_PILimage(target_image)
    target.show()
    finder = TemplateFinder(source)
    results = finder.find_all(target, 0.9)

    coordinate_x, coordinate_y = source.coordinate(results[0])
    robot.tap(coordinate_x, coordinate_y)
    source_image = None

def template_finder(target_image):
    robot = ADBRobot()
    source = CV2Img()
    global source_image
    if source_image == None:
        source.load_file(IMG_PATH(robot.screenshot()), 1)
    else:
        source = source_image

    source.show()
    target = CV2Img()
    target.load_PILimage(target_image)
    target.show()
    ratio = min(target.rows / 12, target.cols / 12)

    matcher = TemplateMatcher(source, target, 1, ratio)
    result = matcher.next()

    result_image = source.crop(result)
    if result_image == target:
        source_image = result_image


def assert_finder(target_image):
    robot = ADBRobot()
    source = CV2Img()
    source.load_file(IMG_PATH(robot.screenshot()), 1)

    target = CV2Img()
    target.load_PILimage(target_image)
    target.show()
    ratio = min(target.rows / 12, target.cols / 12)

    matcher = TemplateMatcher(source, target, 1, ratio)
    result = matcher.next()

    result_image = source.crop(result)
    #result_image.show()
    if result_image == target:
        return True
    else:
        return False