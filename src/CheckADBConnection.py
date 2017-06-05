import subprocess
from MessageUI import Message

class checkADB_Connection:
    def check(self):
        message = Message.getMessage(self)
        try:
            deviceInfo = subprocess.getoutput('adb devices')
            deviceNames = deviceInfo.splitlines()
            print(deviceNames)
            finddevices = []
            for i in range(len(deviceNames)):
                if deviceNames[i].find("emulator") >= 0:
                    subprocess.check_call('adb kill-server')
                    self.check()

                if deviceNames[i].find("device") >= 0:
                    finddevices.append(deviceNames[i])

            finddevices.pop(0)

            if len(finddevices) == 0:
                message.InsertText("No Devices connect...\n")
                return "No Connect"
            else:
                message.InsertText("Get devices :\n")
                for i in range(len(finddevices)):
                    message.InsertText(finddevices[i] + "\n\n\n")
                return "Connect"

        except subprocess.CalledProcessError as e:
            message.InsertText(e.returncode)