from cv2img import CV2Img
from adb_roboot import ADBRobot
from finder.template_finder import TemplateFinder

import time
import os
import pytest
ROOT_DIR = os.path.dirname(__file__)
RESOURCES_DIR = os.path.join(ROOT_DIR, "resources/taipeibus")

def IMG_PATH(name):
    return os.path.join(RESOURCES_DIR, name)

def _test_template_finder(source_path, target_path, result_len):
    source = CV2Img()
    source.load_file(IMG_PATH(source_path), 0)

    target = CV2Img()
    target.load_file(IMG_PATH(target_path), 0)

    finder = TemplateFinder(source)
    results = finder.find_all(target, 0.9)

    for item in results:
        result = source.crop(item)
        coordinate_x, coordinate_y = source.coordinate(item)
        return coordinate_x, coordinate_y


def test_searchBus():
    robot = ADBRobot()
    time.sleep(2)
    coordinate_x, coordinate_y = _test_template_finder(IMG_PATH("TaipeiBus.png"), IMG_PATH("searchPath.png"), 1)
    robot.tap(coordinate_x, coordinate_y)
    time.sleep(2)
    coordinate_x, coordinate_y = _test_template_finder(IMG_PATH("searchBus.png"), IMG_PATH("two.png"), 1)
    robot.tap(coordinate_x, coordinate_y)
    #robot.tap(758, 1378)
    time.sleep(1)
    coordinate_x, coordinate_y = _test_template_finder(IMG_PATH("searchBus2.png"), IMG_PATH("nine.png"), 1)
    robot.tap(coordinate_x, coordinate_y)
    #obot.tap(975, 1690)
    time.sleep(1)
    coordinate_x, coordinate_y = _test_template_finder(IMG_PATH("searchBus29.png"), IMG_PATH("nine.png"), 1)
    robot.tap(coordinate_x, coordinate_y)
    #robot.tap(975, 1690)
    time.sleep(1)
    coordinate_x, coordinate_y = _test_template_finder(IMG_PATH("busStation.png"), IMG_PATH("FJUtoYC.png"), 1)
    robot.tap(coordinate_x, coordinate_y)
    #robot.tap(245, 405)
    time.sleep(1)
    coordinate_x, coordinate_y = _test_template_finder(IMG_PATH("Bus299.png"), IMG_PATH("FJUstation.png"), 1)
    robot.tap(coordinate_x, coordinate_y)
    #robot.tap(405, 830)
    time.sleep(1)
    coordinate_x, coordinate_y = _test_template_finder(IMG_PATH("Station.png"), IMG_PATH("AddFavoriteStation.png"), 1)
    robot.tap(coordinate_x, coordinate_y)
    #robot.tap(505, 435)
    time.sleep(1)
    coordinate_x, coordinate_y = _test_template_finder(IMG_PATH("checkAddFavorite.png"), IMG_PATH("sure.png"), 1)
    robot.tap(coordinate_x, coordinate_y)
    #robot.tap(840, 1230)
    time.sleep(1)
    coordinate_x, coordinate_y = _test_template_finder(IMG_PATH("Bus299.png"), IMG_PATH("back.png"), 1)
    robot.tap(coordinate_x, coordinate_y)
    time.sleep(1)
    coordinate_x, coordinate_y = _test_template_finder(IMG_PATH("busStation.png"), IMG_PATH("back.png"), 1)
    robot.tap(coordinate_x, coordinate_y)
    time.sleep(1)
    coordinate_x, coordinate_y = _test_template_finder(IMG_PATH("TaipeiBus.png"), IMG_PATH("FavoriteStation.png"), 1)
    robot.tap(coordinate_x, coordinate_y)
    time.sleep(1)
    coordinate_x, coordinate_y = _test_template_finder(IMG_PATH("FavoriteBusStation.png"), IMG_PATH("FJUstation.png"), 1)
    robot.tap(coordinate_x, coordinate_y)
    #robot.tap(395, 420)
    time.sleep(1)
    coordinate_x, coordinate_y = _test_template_finder(IMG_PATH("FavoriteBusSomething.png"), IMG_PATH("removeStation.png"), 1)
    robot.tap(coordinate_x, coordinate_y)
    #robot.tap(480, 520)
    time.sleep(1)
    coordinate_x, coordinate_y = _test_template_finder(IMG_PATH("checkRemoveStation.png"), IMG_PATH("Yes.png"), 1)
    robot.tap(coordinate_x, coordinate_y)
    #robot.tap(845, 1140)
    time.sleep(1)
    coordinate_x, coordinate_y = _test_template_finder(IMG_PATH("FavoriteBusStationNull.png"), IMG_PATH("back.png"), 1)
    robot.tap(coordinate_x, coordinate_y)