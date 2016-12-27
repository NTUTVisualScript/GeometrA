import unittest
from cv2img import CV2Img
from adb_roboot import ADBRobot
import time
import os
ROOT_DIR = os.path.dirname(__file__)
RESOURCES_DIR = os.path.join(ROOT_DIR, "resources/taipeibus")

def IMG_PATH(name):
    return os.path.join(RESOURCES_DIR, name)


class MyTestCase(unittest.TestCase):

    def setUp(self):
        robot = ADBRobot()
        time.sleep(3)


    def tearDown(self):
        robot = ADBRobot()
        robot.close_app("nexti.android.bustaipei")

    def test_AssertNearlyStation(self):
        time.sleep(2)




if __name__ == '__main__':
    unittest.main()
