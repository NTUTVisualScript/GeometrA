from cv2img import CV2Img
from adb_roboot import ADBRobot
from finder.template_finder import TemplateFinder
from finder.template_matcher import TemplateMatcher
from screen import Screen
import time
import os
import pytest
ROOT_DIR = os.path.dirname(__file__)
RESOURCES_DIR = os.path.join(ROOT_DIR, "resources/taipeibus")

def find():
    src = cv2.imread("lena.jpg", cv2.CV_LOAD_IMAGE_GRAYSCALE)
    roiImg = cv2.imread("temp.jpg", cv2.CV_LOAD_IMAGE_GRAYSCALE)
    displayImg = src.clone()
    result = cv2.create(src.rows - roiImg.rows + 1, src.cols - roiImg.cols + 1, cv2.CV_32FC1)

    cv2.matchTemplate(src, roiImg, result, cv2.CV_TM_SQDIFF)


def IMG_PATH(name):
    return os.path.join(RESOURCES_DIR, name)

def _test_template_finder(target_path):
    robot = ADBRobot()
    source = CV2Img()
    source.load_file(robot.screenshot(), 1)

    target = CV2Img()
    target.load_file(IMG_PATH(target_path), 1)

    finder = TemplateFinder(source)
    results = finder.find_all(target, 0.9)

    for item in results :
        coordinate_x, coordinate_y = source.coordinate(item)
        robot.tap(coordinate_x, coordinate_y)

def _test_assert_finder(target_path):
    robot = ADBRobot()
    source = CV2Img()
    source.load_file(robot.screenshot(), 1)

    target = CV2Img()
    target.load_file(IMG_PATH(target_path), 1)

    ratio = min(target.rows / 12, target.cols / 12)

    matcher = TemplateMatcher(source, target, 1, ratio)
    result = matcher.next()

    result_image = source.crop(result)

    assert result_image == target


def test_FavoriteStation():
    robot = ADBRobot()

    _test_template_finder(IMG_PATH("NearlyStation.png"))
    time.sleep(3)
    _test_assert_finder(IMG_PATH(IMG_PATH("AssertNearlyStation.png")))

    _test_template_finder(IMG_PATH("GuangHuaStation.png"))
    time.sleep(1)
    _test_assert_finder(IMG_PATH(IMG_PATH("AssertGuangHuaStation.png")))

    _test_template_finder(IMG_PATH("AddAllStationToFavorite.png"))
    time.sleep(1)

    _test_assert_finder(IMG_PATH(IMG_PATH("AssertAddAllStationToFavorite.png")))

    _test_template_finder(IMG_PATH("Yes.png"))
    time.sleep(1)

    _test_template_finder(IMG_PATH("back.png"))
    time.sleep(1)

    _test_assert_finder(IMG_PATH(IMG_PATH("AssertNearlyStation.png")))

    _test_template_finder(IMG_PATH("back.png"))
    time.sleep(1)

    #_test_assert_finder(IMG_PATH(IMG_PATH("AssertTaipeiBus.png")))

    _test_template_finder(IMG_PATH("FavoriteStation.png"))
    time.sleep(1)

    _test_assert_finder(IMG_PATH(IMG_PATH("AssertFavoriteBusStation.png")))

    _test_template_finder(IMG_PATH("ChoiceSetting.png"))
    time.sleep(1)

    #_test_assert_finder(IMG_PATH(IMG_PATH("AssertChoiceSetting.png")))

    _test_template_finder(IMG_PATH("StationSort.png"))
    time.sleep(1)

    #_test_assert_finder(IMG_PATH(IMG_PATH("AssertBefortSwip.png")))

    #_test_template_finder(IMG_PATH("BusStationSort.png"))
    robot.drag_and_drop(880, 1020, 880, 585)
    time.sleep(1)

    #_test_assert_finder(IMG_PATH(IMG_PATH("AssertAfterSwip.png")))

    _test_template_finder(IMG_PATH("sure.png"))
    time.sleep(1)

    _test_template_finder(IMG_PATH("ChoiceSetting.png"))
    time.sleep(1)

    _test_template_finder(IMG_PATH("DeleteGroup.png"))
    time.sleep(1)

    _test_template_finder(IMG_PATH("sure.png"))
    time.sleep(1)

    _test_assert_finder(IMG_PATH(IMG_PATH("AssertFavoriteBusStationNull.png")))

    _test_template_finder(IMG_PATH("back.png"))

