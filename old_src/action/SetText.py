from adb_roboot import ADBRobot

class SetText:
    def __init__(self):
        self.robot = ADBRobot()

    def InputValue(self, index):
        return self.robot.input_text(self.value[index])