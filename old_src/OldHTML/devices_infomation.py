from TestReport import Report

class HTML_divices_Info:
    def __init__(self):
        self.SerialNo = ""
        self.StepCount = ""
        self.DisplayW = ""
        self.DisplayH = ""
        self.Result = ""
        self.start_time = ""
        self.end_time = ""
        self.color = ""


    def set_SerialNo(self, SerialNo):
        self.SerialNo = SerialNo

    def set_StepCount(self, StepCount):
        self.StepCount = StepCount

    def set_Display(self,DisplayW , DisplayH):
        self.DisplayW, self.DisplayH = DisplayW, DisplayH

    def set_Result(self, Result):
        if Result == "Error":
            self.Result = '<p class="text-danger"><span class="info-name ">Result:</span>'+ Result + '</p>'
            self.color = "danger"
        else:
            self.Result = '<p class="text-success"><span class="info-name ">Result:</span>'+ Result + '</p>'
            self.color = "primary"

    def set_start_time(self, time):
        self.start_time = time

    def set_end_time(self, time):
        self.end_time = time

    def report_Info(self):
        report = Report.getReport()
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
              <span class="info-name">SerialNo:</span>""" + self.SerialNo + """</li>
            <li>
              <span class="info-name">Start:</span>""" + self.start_time + """</li>
            <li>
              <span class="info-name">StepCount:</span>""" + str(self.StepCount) + """</li>
          </ul>
        </div>
        <div class="col-md-6">
          <ul class="device-info">
            <li>
              <span class="info-name">Display:</span>"""+ str(self.DisplayW) +" x " + str(self.DisplayH) +"""</li>
            <li>
              <span class="info-name">End:</span>"""+ self.end_time +"""</li>
            <li>
              """+ self.Result +"""</li>
          </ul>
        </div>
      </div>
    </div>
    """
        report.insert(infomation)