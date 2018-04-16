from GeometrA.src.Screen.Screenshot import Screen
from GeometrA.src.ADB.DeviceCheck import Check

def capture():
    if not Check().checkDevices():
        return None
    return Screen().getImagePath()
