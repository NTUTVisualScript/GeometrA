import subprocess
from GeometrA.src.ADB.keycode import ANDROID_KEYCODE
from GeometrA.src.ADB.robot import Robot
import os
import re

PATH = lambda p: os.path.abspath(p)

KEYCODE = ANDROID_KEYCODE

def getAppsInfo():
    # Get informations of all apps in aos device.
    getAppsInfoScript = "bash ./GeometrA/static/aos_info.sh"
    subprocess.call(getAppsInfoScript, shell=True)

    # Read the data from of apps
    aosData = []
    with open('aos_info.txt', 'r') as f:
        for line in f:
            aosData.append(line.replace("\n", ""))

    # Generate the dictionary we need
    appsData = {}
    for app in aosData:
        dataStrings = app.split("'")
        # The index of package/app name in dataString is depends on the format of aos_info.txt
        packageName = dataStrings[1]
        appName = dataStrings[5]

        data = {appName: packageName}
        appsData.update(data)
    return appsData

class ADBRobot(Robot):
    def open_app(self, appName):
        appsData = getAppsInfo()
        targetPkg = appsData[appName]
        try:
            command = "adb shell monkey -p " + targetPkg + " -c android.intent.category.LAUNCHER 1"
            subprocess.call(command, shell=True)
            return "Success"
        except:
            return "Error"

    def close_app(self, appName):
        appsData = getAppsInfo()
        targetPkg = appsData[appName]
        try:
            command = "adb shell am force-stop " + targetPkg
            subprocess.check_output(command, shell=True)
            return "Success"
        except:
            return "Error"

    def get_devices(self):
        dList = subprocess.getoutput('adb devices')
        dNames = dList.splitlines()[1]
        return dNames.split('\t')[0]

    def send_keys(self, keys):
        for key in keys:
            self.send_key(KEYCODE[key])

    def send_key(self, keycode):
        command = "adb shell input keyevent " + str(keycode)
        return subprocess.call(command, shell=True)

    def drag_and_drop(self, start_x, start_y, end_x, end_y):
        command = " ".join(["adb shell input swipe", str(start_x), str(start_y), str(end_x), str(end_y)])
        subprocess.call(command, shell=True)

    def getScreenShot(self, path, fileName):
        wait = "adb wait-for-device"
        subprocess.call(wait, shell=True)
        if not os.path.isdir(path):
            os.makedirs(path)
        capture = "adb shell screencap -p ./data/local/tmp/" + fileName
        subprocess.call(capture, shell=True)
        if not os.path.isdir(path):
            os.makedirs(path)
        # capture = "adb exec-out screencap -p > " + path + "/" + fileName
        # subprocess.call(capture, shell=True)
        pull = "adb pull ./data/local/tmp/" + fileName + " " + path
        subprocess.call(pull ,shell=True)

        print("get tmp.png success")
        return path + "/" + fileName

    def screenshot(self):
        path = "./static/screenshot_pic"
        fileName = "tmp.png"
        return self.getScreenShot(path, fileName)

    def before_screenshot(self):
        path = "./static/screenshot_pic"
        fileName = "before.png"
        return self.getScreenShot(path, fileName)

    def after_screenshot(self):
        path = "./static/screenshot_pic"
        fileName = "after.png"
        return self.getScreenShot(path, fileName)

    def tap(self, x, y, duration=None):
        if duration:
            command = " ".join(["adb shell input swipe", str(x), str(y), str(x), str(y), str(3000)])
        else:
            command = " ".join(["adb shell input tap", str(x), str(y)])

        subprocess.call(command, shell=True)

    def input_text(self, text):
        try:
            text = text.replace(' ', '%s')
            command = 'adb shell input text ' + text
            subprocess.call(command, shell=True)

            return "Success"
        except:
            print("Input Text Error", text)
            return "Error"

    def get_uiautomator_dump(self):
        path = "./dumpXML"

        wait = "adb wait-for-device"
        subprocess.call(wait, shell=True)
        fileName = "uidump.xml"
        dump = "adb shell uiautomator dump ./data/local/tmp/" + fileName
        subprocess.call(dump, shell=True)
        if not os.path.isdir(path):
            os.makedirs(path)
        pull = "adb pull ./data/local/tmp/" + fileName + " " + path
        subprocess.call(pull, shell=True)
        print(path + "/uidump.xml")
        return path + "/uidump.xml"

    def get_display(self):
        real_size_pattern = r"real (\d+) x (\d+),"
        result = subprocess.check_output('adb shell dumpsys display | grep mBaseDisplayInfo', shell=True).__str__()
        match = re.search(real_size_pattern, result)
        return (match.group(1), match.group(2))

    def get_device_size(self):
        result = subprocess.getoutput('adb shell wm size')
        sizeList = result.split('\n')
        if len(sizeList) == 1 or sizeList[1] is "":
            sizeList = sizeList[0].split(':') #Only physical size
        else:
            sizeList = sizeList[1].split(':') #Override size
        return sizeList[1]
