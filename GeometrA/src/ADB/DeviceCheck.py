import subprocess
from GeometrA.src.ADB.adbRobot import ADBRobot

class Check:
    def __init__(self):
        self.findDevices = ADBRobot().get_devices_list()

    def checkDevices(self):
        if len(self.findDevices) == 0:
            return False
        else:
            return True
