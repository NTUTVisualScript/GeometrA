import subprocess

class Check:
    def __init__(self):
        self.getDevice()

    def getDevice(self):
        deviceInfo = subprocess.getoutput('adb devices')
        devices = deviceInfo.splitlines()
        self.findDevices = []
        for i in range (len(devices)):
            if devices[i].find("emulator") >= 0:
                subprocess.check_call('adb kill-server')
                return self.getDevice()

            if devices[i].find("device") >= 0:
                self.findDevices.append(devices[i])
        self.findDevices.pop(0)

    def checkDevices(self):
        if len(self.findDevices) == 0:
            return False
        else:
            return True
