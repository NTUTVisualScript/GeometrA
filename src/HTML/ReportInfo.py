from adbRobot import ADBRobot
import datetime

class Info:
    def __init__(self):
        self.No = ""
        self.stepCount = 0
        self.pWidth = ""
        self.pHeight = ""
        self.result = ""
        self.testDate = ""
        self.exeTime = ""
        self.color = ""

    def setNo(self):
        self.No = ADBRobot().get_devices()

    def setStepCount(self):
        self.stepCount = self.stepCount + 1

    def setDisplay(self):
        self.pWidth, self.pHeight = ADBRobot().get_display()

    def setResult(self):
        if Result == "Error":
            self.Result = '<p class="text-danger"><span class="info-name ">Result:</span>'+ Result + '</p>'
            self.color = "danger"
        else:
            self.Result = '<p class="text-success"><span class="info-name ">Result:</span>'+ Result + '</p>'
            self.color = "primary"

    def getDate(self):
        self.testDate = str(datetime.datetime.now()).split(' ')[0]
        return self.testDate

    def setStartTime(self):
        self.start = str(datetime.datetime.now()).split(' ')[1].split('.')[0].split(':')

    def setEndTime(self):
        self.end = str(datetime.datetime.now()).split(' ')[1].split('.')[0].split(':')

    def setExeTime(self):
        start = self.start[0] * 3600 + self.start[1] *60 + self.start[2]
        end = self.end[0] * 3600 + self.end[1] * 60 + self.end[2]
        exeTime = self.end - self.star
        self.exeTime = str(exeTime//3600) + ':' + str(exeTime%3600//60) + str(exeTime%60)

    def report_info(self):
        infomation = r"""
  <div class="container">
    <div class="panel panel-""" + self.color + """">
      <div class="panel-heading">
        <h4>Base Infomation</h4>
      </div>
      <div class="panel-body">
        <div class="col-md-6">
          <ul class="device-info">
            <li>
              <span class="info-name">SerialNo:</span>""" + self.No + """</li>
            <li>
              <span class="info-name">TestDate:</span>""" + self.testDate + """</li>
            <li>
              <span class="info-name">StepCount:</span>""" + str(self.stepCount) + """</li>
          </ul>
        </div>
        <div class="col-md-6">
          <ul class="device-info">
            <li>
              <span class="info-name">Display:</span>"""+ str(self.pWidth) +" x " + str(self.pHeight) +"""</li>
            <li>
              <span class="info-name">ExecuteTime:</span>"""+ self.exeTime +"""</li>
            <li>
              """+ self.result +"""</li>
          </ul>
        </div>
      </div>
    </div>
    """
        return information
