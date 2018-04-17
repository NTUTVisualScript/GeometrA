from PIL import Image

from GeometrA.src.Screen.Screenshot import Screen
from GeometrA.src.ADB.DeviceCheck import Check

TMP = ""

def capture():
    if not Check().checkDevices():
        return None
    TMP = Screen().getImagePath()
    return TMP

def cropPhoto(data):
    left,right = (float(data['startX']),float(data['endX'])) if float(data['startX']) <= float(data['endX']) else (float(data['endX']), float(data['startX']))
    top, bottom = (float(data['startY']), float(data['endY'])) if float(data['startY']) <= float(data['endY']) else (float(data['endY']), float(data['startY']))
    coordinate = (int(left), int(top), int(right), int(bottom))
    image = Image.open("./GeometrA/static/screenshot_pic/tmp.png")
    croppedPhoto = image.crop(coordinate)
    croppedPhoto.save("./GeometrA/static/screenshot_pic/cropped.png")
    return "cropped.png"
