import re

import subprocess
from cv2img import CV2Img
from keycode import ANDROID_KEYCODE
from robot import Robot

import time
import os

PATH = lambda p: os.path.abspath(p)

KEYCODE = ANDROID_KEYCODE
subp = os.path.join(os.environ["Android_HOME"], "platform-tools", "adb.exe")


class ADBRobot(Robot):
    def open_app(self, appName):
        subprocess.check_output([subp, "shell", "am", "start", "-n", appName ], shell=True)

    def close_app(self, appName):
        subprocess.check_output([subp, "shell", "am", "force-stop", appName], shell=True)

    def send_keys(self, keys):
        for key in keys:
            self.send_key(KEYCODE[key])

    def send_key(self, keycode):
        return subprocess.check_output([subp, "shell", "input", "keyevent", str(keycode)], shell=True)

    def drag_and_drop(self, start_x, start_y, end_x, end_y):
        subprocess.check_output([subp, "shell", "input", "swipe", str(start_x), str(start_y), str(end_x), str(end_y) ], shell=True)

    def screenshot(self):
        path = PATH(os.getcwd() + "/resources/taipeibus")
        os.popen("adb wait-for-device")
        os.popen("adb shell screencap -p /data/local/tmp/tmp.png")
        time.sleep(3)
        if not os.path.isdir(PATH(os.getcwd() + "/resources/taipeibus")):
            os.makedirs(path)
        os.popen("adb pull /data/local/tmp/tmp.png " + str(PATH(path + "/tmp.png")))
        time.sleep(3)
        print("success")
        return "tmp.png"

    def tap(self, x, y, duration=None):
        if duration:
            subprocess.check_output(
                [subp, "shell", "input", "swipe", str(x), str(y), str(x), str(y), str(duration)],
                shell=True)
        else:
            subprocess.check_output(
                [subp, "shell", "input", "tap", str(x), str(y)],
                shell=True)


    def get_uiautomator_dump(self):
        path = PATH(os.getcwd() + "/resources/taipeibus")
        os.popen("adb wait-for-device")
        os.popen("adb shell uiautomator dump /data/local/tmp/uidump.xml")
        time.sleep(3)
        if not os.path.isdir(PATH(os.getcwd() + "/resources/taipeibus")):
            os.makedirs(path)
        os.popen("adb pull /data/local/tmp/uidump.xml " + path + "/uidump.xml")
        time.sleep(3)
        print(path + "/uidump.xml")
        return path + "/uidump.xml"

    # @property
    # def windows_size(self):
    #     """
    #     adb shell dumpsys display | grep mBaseDisplayInfo
    #
    #     :return:
    #     """
    #     #real 1080 X 1920
    #     real_size_pattern = r"real (\d+) x (\d+),"
    #
    #     #density 480 (480.0 x 480.0) dpi,
    #     #density_pattern = re.compile(r"density (\d+) \((\d+.\d+ x \d+.\d+)\) dpi,")
    #
    #     result = grep(adb("shell", "dumpsys", "display"), "mBaseDisplayInfo").__str__()
    #     match = re.search(real_size_pattern, result)
    #     if match:
    #         size = (int(match.group(1)), int(match.group(2)))
    #     else:
    #         size = None
    #
    #     return size