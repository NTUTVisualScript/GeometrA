from cv2img import CV2Img
from cv2img import Region

from config import IMG_PATH
import pytest

def test_cv2img_load_image_from_file():
    img = CV2Img()
    img.load_file(IMG_PATH("screen.png"))

    assert img.rows == 1280
    assert img.cols == 768


def test_cv2img_load_image_from_binary():
    img = CV2Img()

    with open(IMG_PATH("screen.png"), 'rb') as img_file:
        binary = img_file.read()

    img.load_binary(binary)

    assert img.rows == 1280
    assert img.cols == 768


def test_cv2img_load_image_from_base64():
    img = CV2Img()

    with open(IMG_PATH("base64-img"), 'rb') as img_file:
        base64 = img_file.read()

    img.load_base64(base64)

    assert img.rows == 1280
    assert img.cols == 768


def test_cv2img_operations():
    img = CV2Img()
    img.load_file(IMG_PATH("screen.png"))

    img2 = CV2Img()
    img2.load_file(IMG_PATH("gmail.png"))

    assert img.is_same_color() == False
    assert img.is_black() == False
    assert img > img2
    assert (img < img2) == False

    # Resize
    img3 = img.resize(0.5)
    assert img3.rows == 640
    assert img3.cols == 384
    assert img.rows == 1280
    assert img.cols == 768

    # Copy
    img4 = img.copy()
    assert img4.rows == img.rows
    assert img4.cols == img.cols

    # Crop
    roi = Region(0, 0, 640, 384)
    img5 = img.crop(roi)
    assert img5.rows == 384
    assert img5.cols == 640

    # Invert
    img6 = img.invert()
    assert img6.rows == 1280
    assert img6.cols == 768

    img7 = img6.invert()
    assert img == img7

def test_cv2img_is_same_color():
    gmail_img = CV2Img()
    gmail_img.load_file(IMG_PATH("gmail.png"))

    assert gmail_img.is_same_color() != True
    assert gmail_img.is_black() != True
