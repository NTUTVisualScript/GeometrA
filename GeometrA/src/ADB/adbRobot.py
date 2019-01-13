import os
import re
import platform
import subprocess
from GeometrA.src.ADB.keycode import ANDROID_KEYCODE
from GeometrA.src.ADB.robot import Robot
from GeometrA.src.path import GEOMETRA_ROOT, RESOURCE_PATH

if (platform.system() == 'Windows'):
    PATH = GEOMETRA_ROOT + '\\screenshot_pic\\'
    ADB_COMMAND = 'adb'
else:
    PATH = GEOMETRA_ROOT + '/screenshot_pic/'
    ADB_COMMAND = RESOURCE_PATH + '/adb_resources/mac/adb'

KEYCODE = ANDROID_KEYCODE


def getAppsInfo():
    # Get informations of all apps in aos device.
    if (platform.system() == 'Windows'):
        getAppsInfoBatch = [r'.\\GeometrA\\static\\aos_info.bat']
        subprocess.call(getAppsInfoBatch)
    else:
        getAppsInfoScript = "export GEOMETRA_RESOURCE=" + RESOURCE_PATH + " && bash " + RESOURCE_PATH + "/aos_info.sh"
        subprocess.call(getAppsInfoScript, shell=True)

    # Read the data from of apps
    aosData = []
    with open(GEOMETRA_ROOT + '/aos_info.txt', 'r', encoding='utf8') as f:
        for line in f:
            aosData.append(line.replace("\n", ""))

    # Generate the dictionary we need
    appsData = {}
    for app in aosData:
        if (app.isspace()):
            continue
        dataStrings = app.split("'")
        # The index of package/app name in dataString is depends on the format of aos_info.txt
        packageName = dataStrings[1]
        appName = dataStrings[5]

        data = {appName: packageName}
        appsData.update(data)
    return appsData


class ADBRobot(Robot):
    def open_app(self, appName):
        try:
            appsData = getAppsInfo()
            targetPkg = appsData[appName]
            command = ADB_COMMAND + " shell monkey -p " + targetPkg + " -c android.intent.category.LAUNCHER 1"
            subprocess.call(command, shell=True)
            return "Success"
        except:
            return "Error"

    def close_app(self, appName):
        appsData = getAppsInfo()
        targetPkg = appsData[appName]
        try:
            command = ADB_COMMAND + " shell am force-stop " + targetPkg
            subprocess.check_output(command, shell=True)
            return "Success"
        except:
            return "Error"

    def get_devices(self):
        dList = subprocess.getoutput(ADB_COMMAND + ' devices')
        print(dList)
        dNames = dList.splitlines()[1]
        print('dNames' + str(dNames))
        return dNames.split('\t')[0]

    def send_keys(self, keys):
        for key in keys:
            self.send_key(KEYCODE[key])

    def send_key(self, keycode):
        command = ADB_COMMAND + " shell input keyevent " + str(keycode)
        return subprocess.call(command, shell=True)

    def drag_and_drop(self, start_x, start_y, end_x, end_y):
        command = " ".join([ADB_COMMAND + " shell input swipe", str(start_x), str(start_y), str(end_x), str(end_y)])
        subprocess.call(command, shell=True)

    def getScreenShot(self, fileName):
        path = PATH
        wait = ADB_COMMAND + " wait-for-device"
        subprocess.call(wait, shell=True)
        if not os.path.isdir(path):
            os.makedirs(path)
        capture = ADB_COMMAND + " shell screencap -p ./data/local/tmp/" + fileName
        subprocess.call(capture, shell=True)
        if not os.path.isdir(path):
            os.makedirs(path)
        # capture = "adb exec-out screencap -p > " + path + "/" + fileName
        # subprocess.call(capture, shell=True)
        pull = ADB_COMMAND + " pull ./data/local/tmp/" + fileName + " " + path
        subprocess.call(pull ,shell=True)

        print("get tmp.png success")
        return path + fileName

    def screenshot(self):
        fileName = "tmp.png"
        return self.getScreenShot(fileName)

    def before_screenshot(self):
        fileName = "before.png"
        return self.getScreenShot(fileName)

    def after_screenshot(self):
        fileName = "after.png"
        return self.getScreenShot(fileName)

    def tap(self, x, y, duration=None):
        if duration:
            command = " ".join([ADB_COMMAND + " shell input swipe", str(x), str(y), str(x), str(y), str(3000)])
        else:
            command = " ".join([ADB_COMMAND + " shell input tap", str(x), str(y)])

        subprocess.call(command, shell=True)

    def input_text(self, text):
        try:
            text = text.replace(' ', '%s')
            command = ADB_COMMAND + ' shell input text ' + text
            subprocess.call(command, shell=True)

            return "Success"
        except:
            print("Input Text Error", text)
            return "Error"

    def get_uiautomator_dump(self):
        path = GEOMETRA_ROOT + "/dumpXML"

        wait = ADB_COMMAND + " wait-for-device"
        subprocess.call(wait, shell=True)
        fileName = "uidump.xml"
        dump = ADB_COMMAND + " shell uiautomator dump ./data/local/tmp/" + fileName
        subprocess.call(dump, shell=True)
        if not os.path.isdir(path):
            os.makedirs(path)
        pull = ADB_COMMAND + " pull ./data/local/tmp/" + fileName + " " + path
        subprocess.call(pull, shell=True)
        print(path + "/uidump.xml")
        return path + "/uidump.xml"

    def get_display(self):
        real_size_pattern = r"real (\d+) x (\d+),"
        result = subprocess.check_output(ADB_COMMAND + ' shell dumpsys display | grep mBaseDisplayInfo', shell=True).__str__()
        match = re.search(real_size_pattern, result)
        return (match.group(1), match.group(2))

    def get_device_size(self):
        result = subprocess.getoutput(ADB_COMMAND + ' shell wm size')
        sizeList = result.split('\n')
        if len(sizeList) == 1 or sizeList[1] is "":
            sizeList = sizeList[0].split(':') #Only physical size
        else:
            sizeList = sizeList[1].split(':') #Override size
        return sizeList[1]

    def get_devices_list(self):
        deviceInfo = subprocess.getoutput(ADB_COMMAND + ' devices')
        return deviceInfo
        devices = deviceInfo.splitlines()
        findDevices = []
        for i in range (len(devices)):
            if devices[i].find("emulator") >= 0:
                subprocess.check_call(ADB_COMMAND + ' kill-server')
                return self.get_devices_list()

            if devices[i].find("device") >= 0:
                findDevices.append(devices[i])
        findDevices.pop(0)
        return findDevices
