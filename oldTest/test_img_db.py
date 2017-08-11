from img_db import ImgDB
from cv2img import CV2Img
from rectangle import Rectangle
import pytest


def test_img_db():
    home_image = CV2Img().load_file("./resources/browser/home.png")
    browser_image = home_image.crop(Rectangle(640, 1550, 210, 185))

    db = ImgDB("./resources")
    home = db.browser.home
    assert home_image == home.load()
    assert browser_image == home.browser.load()

