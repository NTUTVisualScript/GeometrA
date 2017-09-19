import subprocess
from keycode import ANDROID_KEYCODE
from robot import Robot
import os

PATH = lambda p: os.path.abspath(p)

KEYCODE = ANDROID_KEYCODE
subp = os.path.join(os.environ["Android_HOME"], "platform-tools", "adb.exe")


class ADBRobot(Robot):
    def open_app(self, appName):
        subprocess.check_output([subp, "shell", "am", "start", "-n", appName ], shell=True)

    def close_app(self, appName):
        subprocess.check_output([subp, "shell", "am", "force-stop", appName], shell=True)

    def get_devices(self):
        return subprocess.check_output('adb devices')

    def send_keys(self, keys):
        for key in keys:
            self.send_key(KEYCODE[key])

    def send_key(self, keycode):
        return subprocess.call([subp, "shell", "input", "keyevent", str(keycode)], shell=True)

    def drag_and_drop(self, start_x, start_y, end_x, end_y):
        subprocess.call([subp, "shell", "input", "swipe", str(start_x), str(start_y), str(end_x), str(end_y) ], shell=True)

    def screenshot(self):
        path = PATH(os.getcwd() + "/screenshot_pic")
        subprocess.call([subp, "wait-for-device"], shell=True)
        subprocess.call([subp, "shell", "screencap", "-p", "/data/local/tmp/tmp.png"], shell=True)
        if not os.path.isdir(PATH(os.getcwd() + "/screenshot_pic")):
            os.makedirs(path)
        subprocess.call([subp, "pull", "/data/local/tmp/tmp.png", str(PATH(path + "/tmp.png"))], shell=True)
        print("success")
        return path + "/tmp.png"

    def before_screenshot(self):
        path = PATH(os.getcwd() + "/screenshot_pic")
        subprocess.call([subp, "wait-for-device"], shell=True)
        subprocess.call([subp, "shell", "screencap", "-p", "/data/local/tmp/before.png"], shell=True)
        if not os.path.isdir(PATH(os.getcwd() + "/screenshot_pic")):
            os.makedirs(path)
        subprocess.call([subp, "pull", "/data/local/tmp/before.png", str(PATH(path + "/before.png"))], shell=True)
        print("success")
        return path + "/before.png"

    def after_screenshot(self):
        path = PATH(os.getcwd() + "/screenshot_pic")
        subprocess.call([subp, "wait-for-device"], shell=True)
        subprocess.call([subp, "shell", "screencap", "-p", "/data/local/tmp/after.png"], shell=True)
        if not os.path.isdir(PATH(os.getcwd() + "/screenshot_pic")):
            os.makedirs(path)
        subprocess.call([subp, "pull", "/data/local/tmp/after.png", str(PATH(path + "/after.png"))], shell=True)
        print("success")
        return path + "/after.png"

    def tap(self, x, y, duration=None):
        if duration:
            subprocess.call(
                [subp, "shell", "input", "swipe", str(x), str(y), str(x), str(y), str(3000)],
                shell=True)
        else:
            subprocess.call(
                [subp, "shell", "input", "tap", str(x), str(y)],
                shell=True)

    def input_text(self, inputtext):
        text = list(inputtext)
        #print("text =" + str(text))
        try:
            for i in range(len(text)):
                print(text[i])
                if text[i] == " ":
                    subprocess.call([subp, "shell", "input", "text", "%s"], shell=True)
                else:
                    subprocess.call([subp, "shell", "input", "text", text[i]], shell=True)

            return "Success"
        except:
            print("Input Text Error", inputtext)
            return "Error"

    def get_uiautomator_dump(self):
        path = PATH(os.getcwd() + "/dumpXML")
        subprocess.call([subp, "wait-for-device"], shell=True)
        subprocess.call([subp, "shell", "uiautomator", "dump", "/data/local/tmp/uidump.xml"], shell=True)
        if not os.path.isdir(PATH(os.getcwd() + "/dumpXML")):
            os.makedirs(path)
        subprocess.call([subp, "pull", "/data/local/tmp/uidump.xml", path + "/uidump.xml"], shell=True)
        print(path + "/uidump.xml")
        return path + "/uidump.xml"

    def get_display(self):
        print(subprocess.call([subp, "shell", "dumpsys", "display"], shell=True))

    # @property
    # def windows_size(self):
    #     """
    #     adb shell dumpsys display | grep mBaseDisplayInfo
    #
    #     :return:
    #     """
    #     #real 1080 X 1920
    #     real_size_pattern = r"real (\d+) x (\d+),"
    #
    #     #density 480 (480.0 x 480.0) dpi,
    #     #density_pattern = re.compile(r"density (\d+) \((\d+.\d+ x \d+.\d+)\) dpi,")
    #
    #     result = grep(adb("shell", "dumpsys", "display"), "mBaseDisplayInfo").__str__()
    #     match = re.search(real_size_pattern, result)
    #     if match:
    #         size = (int(match.group(1)), int(match.group(2)))
    #     else:
    #         size = None
    #
    #     return size