from adb_roboot import ADBRobot
from keycode import ANDROID_KEYCODE as KEYCODE

import time

"""
Test Environment:

Android Emulator 5.1.1
Device: Nexus 5 (4.95", 1080 X 1920: xxhdpi)
CPU/ABI: Google APIs Intel Atom(x86_64)
"""

def test_capture_screen():
    robot = ADBRobot()
    screenshot = robot.capture_screen()
    assert screenshot is not None

def test_send_key():
    robot = ADBRobot()
    # Get screenshot before send MENU
    before = robot.capture_screen()

    robot.send_key(KEYCODE.MENU)
    time.sleep(1)
    after = robot.capture_screen()
    assert after != before

    # Send HOME key to return home
    robot.send_key(KEYCODE.HOME)
    time.sleep(1)
    return_home = robot.capture_screen()

    assert return_home == before

def test_windows_size():
    robot = ADBRobot()
    w, h = robot.windows_size

    assert w == 1080
    assert h == 1920

def test_tap():
    robot = ADBRobot()

    robot.send_key(KEYCODE.HOME)
    time.sleep(1)
    menu_image = robot.capture_screen()

    robot.send_key(KEYCODE.MENU)
    robot.tap(540, 1850)
    time.sleep(1)
    after_tap = robot.capture_screen()

    assert after_tap == menu_image

