import sys
sys.path.append('/usr/local/lib/python3.5/site-packages')

import cv2
import numpy as np
#from matplotlib import pyplot as plt
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

def _test_template_finder(source_path=None, target_path=None, result_len=None):
    source = CV2Img()
    source.load_file(IMG_PATH(source_path))

    target = CV2Img()
    target.load_file(IMG_PATH(target_path))

    finder = TemplateFinder(source)
    results = finder.find_all(target, 0.9)

    for item in results:
        result = source.crop(item)
        coordinate_x, coordinate_y = source.coordinate(item)
        return coordinate_x, coordinate_y


def test_searchBus():
    robot = ADBRobot()
    time.sleep(2)
    print()
    coordinate_x, coordinate_y = _test_template_finder(IMG_PATH("TaipeiBus.png"), IMG_PATH("searchPath.png"), 1)
    robot.tap(coordinate_x, coordinate_y)
    time.sleep(2)
    coordinate_x, coordinate_y = _test_template_finder(cv2.Sobel(cv2.imread(IMG_PATH("searchBus.png"),0),cv2.CV_8U,1,0), cv2.Sobel(cv2.imread(IMG_PATH("two.png"),0),cv2.CV_8U,1,0), 1)
    robot.tap(coordinate_x, coordinate_y)
    time.sleep(1)
    coordinate_x, coordinate_y = _test_template_finder(IMG_PATH("nine.png"), IMG_PATH("searchBus2.png"), 1)
    robot.tap(coordinate_x, coordinate_y)
    time.sleep(1)
    coordinate_x, coordinate_y = _test_template_finder(IMG_PATH("nine.png"), IMG_PATH("searchBus29.png"), 1)
    robot.tap(coordinate_x, coordinate_y)
    time.sleep(1)
    coordinate_x, coordinate_y = _test_template_finder(IMG_PATH("FJUtoYC.png"), IMG_PATH("busStation.png"), 1)
    robot.tap(coordinate_x, coordinate_y)
    time.sleep(1)
    coordinate_x, coordinate_y = _test_template_finder(IMG_PATH("FJUstation.png"), IMG_PATH("Bus299.png"), 1)
    robot.tap(coordinate_x, coordinate_y)
    time.sleep(1)
    coordinate_x, coordinate_y = _test_template_finder(IMG_PATH("AddFavoriteStation.png"), IMG_PATH("Station.png"), 1)
    robot.tap(coordinate_x, coordinate_y)
    time.sleep(1)
    coordinate_x, coordinate_y = _test_template_finder(IMG_PATH("sure.png"), IMG_PATH("checkAddFavorite.png"), 1)
    robot.tap(coordinate_x, coordinate_y)
    time.sleep(1)
    coordinate_x, coordinate_y = _test_template_finder(IMG_PATH("back.png"), IMG_PATH("Bus299.png"), 1)
    robot.tap(coordinate_x, coordinate_y)
    time.sleep(1)
    coordinate_x, coordinate_y = _test_template_finder(IMG_PATH("back.png"), IMG_PATH("busStation.png"), 1)
    robot.tap(coordinate_x, coordinate_y)
    time.sleep(1)
    coordinate_x, coordinate_y = _test_template_finder(IMG_PATH("FavoriteStation.png"), IMG_PATH("searchPath.png"), 1)
    robot.tap(coordinate_x, coordinate_y)
    time.sleep(1)
    coordinate_x, coordinate_y = _test_template_finder(IMG_PATH("FJUstation.png"), IMG_PATH("FavoriteBusStation.png"), 1)
    robot.tap(coordinate_x, coordinate_y)
    time.sleep(1)
    coordinate_x, coordinate_y = _test_template_finder(IMG_PATH("FJUstation.png"), IMG_PATH("FavoriteBusStation.png"), 1)
    robot.tap(coordinate_x, coordinate_y)
    time.sleep(1)
    coordinate_x, coordinate_y = _test_template_finder(IMG_PATH("removeStation.png"), IMG_PATH("FavoriteBusSomething.png"), 1)
    robot.tap(coordinate_x, coordinate_y)
    time.sleep(1)
    coordinate_x, coordinate_y = _test_template_finder(IMG_PATH("Yes.png"), IMG_PATH("checkRemoveStation.png"), 1)
    robot.tap(coordinate_x, coordinate_y)
    time.sleep(1)
    coordinate_x, coordinate_y = _test_template_finder(IMG_PATH("back.png"), IMG_PATH("FavoriteBusStationNull.png"), 1)
    robot.tap(coordinate_x, coordinate_y)

#def toCV_8U(img):
