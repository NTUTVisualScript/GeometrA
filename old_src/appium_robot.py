from cv2img import CV2Img
from keycode import ANDROID_KEYCODE
from robot import Robot

KEYCODE = ANDROID_KEYCODE

class AppiumRobot(Robot):
    def __init__(self, driver):
        """
        :param driver: Appium webdriver
        """
        self._driver = driver

    def send_keys(self, keys):
        for key in keys:
            self._driver.keyevent(KEYCODE[key])

    def send_key(self, keycode):
        self._driver.keyevent(keycode)

    def drag_and_drop(self, start_x, start_y, end_x, end_y, duration=None):
        self._driver.swipe(start_x, start_y, end_x, end_y, duration)

    def capture_screen(self):
        img = CV2Img()
        return img.load_base64(self._driver.get_screenshot_as_base64())

    def tap(self, x, y, duration):
        self._driver.tap([(x, y)], duration)

    @property
    def windows_size(self):
        return self._driver.get_windows_size()
