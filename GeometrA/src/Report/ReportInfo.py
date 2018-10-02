from GeometrA.src.ADB.adbRobot import ADBRobot
import datetime

class Info:
    def __init__(self):
        self.setNo()
        self.stepCount = 0
        self.setDisplay()
        self.result = ""
        self.getDate()
        self.setStartTime()
        self.exeTime = ""
        self.color = ""

    def setNo(self):
        self.No = ADBRobot().get_devices()

    def setStepCount(self, n):
        self.stepCount = n

    def setDisplay(self):
        self.screenSize = ADBRobot().get_device_size()

    def setResult(self, result):
        if result == "Success":
            self.result = result
            self.color = "success"
        else:
            self.result = result
            self.color = "danger"

    def getDate(self):
        self.testDate = str(datetime.datetime.now()).split('.')[0]
        return self.testDate

    def setStartTime(self):
        self.start = str(datetime.datetime.now()).split(' ')[1].split('.')[0].split(':')

    def setEndTime(self):
        self.end = str(datetime.datetime.now()).split(' ')[1].split('.')[0].split(':')

    def setExeTime(self):
        start = int(self.start[0]) * 3600 + int(self.start[1]) *60 + int(self.start[2])
        end = int(self.end[0]) * 3600 + int(self.end[1]) * 60 + int(self.end[2])
        exeTime = end-start
        self.exeTime = ' ' + str(exeTime//3600) + ':' + str(exeTime%3600//60) + ':' + str(exeTime%60)

    def report_info(self):
        self.setExeTime()
        information = r"""<!-- Body -->
  <div class="container">

    <!-- Information -->
    <div class="panel panel-""" + str(self.color) + """">
      <div class="panel-heading">
        <h4>Base Information</h4>
      </div>
      <div class="panel-body">
        <div class="col-md-6">
          <ul class="device-info">
            <li>
              <span class="info-name">SerialNo:</span>""" + str(self.No) + """</li>
            <li>
              <span class="info-name">Start:</span>""" + str(self.testDate) + """</li>
            <li>
              <span class="info-name">StepCount:</span>""" + str(self.stepCount) + """</li>
          </ul>
        </div>
        <div class="col-md-6">
          <ul class="device-info">
            <li>
              <span class="info-name">Display:</span>"""+ self.screenSize +"""</li>
            <li>
              <span class="info-name">Execution Time:</span>"""+ str(self.exeTime) +"""</li>
            <li>
              <p class="text-""" + self.color + """"><span class=info-name ">Result:</span>"""+ str(self.result) +"""</p></li>
          </ul>
        </div>
      </div>
    </div>
"""
        return information
