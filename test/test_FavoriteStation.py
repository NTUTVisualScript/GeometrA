import unittest
from cv2img import CV2Img
from adb_roboot import ADBRobot
from finder.template_finder import TemplateFinder
from finder.template_matcher import TemplateMatcher
import time
import os
ROOT_DIR = os.path.dirname(__file__)
RESOURCES_DIR = os.path.join(ROOT_DIR, "resources/taipeibus")

def IMG_PATH(name):
    return os.path.join(RESOURCES_DIR, name)

def _test_template_finder(target_path):
    robot = ADBRobot()
    source = CV2Img()
    source.load_file(robot.screenshot(), 1)
    source.show()
    target = CV2Img()
    target.load_file(IMG_PATH(target_path), 1)
    target.show()
    finder = TemplateFinder(source)
    results = finder.find_all(target, 0.9)

    for item in results :
        coordinate_x, coordinate_y = source.coordinate(item)
        robot.tap(coordinate_x, coordinate_y)

def _test_assert_finder(target_path):
    robot = ADBRobot()
    source = CV2Img()
    source.load_file(robot.screenshot(), -1)

    target = CV2Img()
    target.load_file(IMG_PATH(target_path), -1)

    ratio = min(target.rows / 12, target.cols / 12)

    matcher = TemplateMatcher(source, target, 1, ratio)
    result = matcher.next()

    result_image = source.crop(result)
    assert result_image == target

class MyTestCase(unittest.TestCase):

    # def setUp(self):
    #     robot = ADBRobot()
    #     time.sleep(3)
    #     _test_template_finder(IMG_PATH("TaipeiBus.png"))
    #
    # def tearDown(self):
    #     robot = ADBRobot()
    #     robot.close_app("nexti.android.bustaipei")
    #
    # def test_AssertNearlyStation(self):
    #     time.sleep(2)
    #     _test_template_finder(IMG_PATH("NearlyStation.png"))
    #     time.sleep(3)
    #     _test_assert_finder(IMG_PATH("AssertNearlyStation.png"))

    def test_AssertGuangHuaStation(self):
        time.sleep(2)
        _test_template_finder(IMG_PATH("NearlyStation.png"))
        time.sleep(3)
        _test_template_finder(IMG_PATH("GuangHuaStation.png"))
        time.sleep(1)
        _test_assert_finder(IMG_PATH("AssertGuangHuaStation.png"))

    # def test_AssertAddAllStationToFavorite(self):
    #     time.sleep(2)
    #     robot = ADBRobot()
    #     _test_template_finder(IMG_PATH("NearlyStation.png"))
    #     time.sleep(3)
    #     _test_template_finder(IMG_PATH("GuangHuaStation.png"))
    #     time.sleep(1)
    #     _test_template_finder(IMG_PATH("AddAllStationToFavorite.png"))
    #     time.sleep(1)
    #     _test_assert_finder(IMG_PATH(IMG_PATH("AssertAddAllStationToFavorite.png")))
    #     _test_template_finder(IMG_PATH("Yes.png"))
    #     time.sleep(1)
    #     _test_template_finder(IMG_PATH("back.png"))
    #     time.sleep(1)
    #     _test_template_finder(IMG_PATH("back.png"))
    #     time.sleep(1)
    #     _test_template_finder(IMG_PATH("FavoriteStation.png"))
    #     time.sleep(1)
    #     _test_template_finder(IMG_PATH("ChoiceSetting.png"))
    #     time.sleep(1)
    #     _test_assert_finder(IMG_PATH(IMG_PATH("AssertChoiceSetting.png")))
    #     time.sleep(1)
    #     _test_template_finder(IMG_PATH("StationSort.png"))
    #     time.sleep(1)
    #     robot.drag_and_drop(880, 1020, 880, 585)
    #     time.sleep(1)
    #     _test_template_finder(IMG_PATH("sure.png"))
    #     time.sleep(1)
    #     _test_template_finder(IMG_PATH("ChoiceSetting.png"))
    #     time.sleep(1)
    #     _test_template_finder(IMG_PATH("DeleteGroup.png"))
    #     time.sleep(1)
    #     _test_template_finder(IMG_PATH("sure.png"))
    #     time.sleep(1)
    #     _test_assert_finder(IMG_PATH(IMG_PATH("AssertFavoriteBusStationNull.png")))
    #     _test_template_finder(IMG_PATH("back.png"))

    # def test_AssertFavoriteBusStation(self):
    #     time.sleep(2)
    #     _test_template_finder(IMG_PATH("FavoriteStation.png"))
    #     time.sleep(1)
    #     _test_assert_finder(IMG_PATH("AssertFavoriteBusStation.png"))



if __name__ == '__main__':
    unittest.main()
