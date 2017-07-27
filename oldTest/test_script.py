import time

from adb_roboot import ADBRobot
from screen import Screen
from img_db import ImgDB


def test_script():
    db = ImgDB("./resources").browser
    screen = Screen(ADBRobot())

    # Home image
    screen.home()
    home_img = screen.image

    # Go to browser
    browser_img = db.home.browser.load()
    screen.find(browser_img).click()
    time.sleep(1)

    # Browser
    google_logo_img = db.browser_google.load()
    result = screen.find(google_logo_img)
    assert result is not None

    # Browser - all tab
    all_tab_btn_img = db.browser_all_tab_btn.load()
    close_btn_img = db.browser_all_tab_close_btn.load()

    screen.find(all_tab_btn_img).click()
    time.sleep(1)

    screen.find(close_btn_img).click()
    time.sleep(2)

    result_img = screen.image
    assert result_img == home_img
