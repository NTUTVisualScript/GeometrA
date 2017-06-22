from TestReport import Report
import base64
import io

class HtmlTestStep:
    __single = None
    def __init__(self):
        if HtmlTestStep.__single:
            raise HtmlTestStep.__single
            HtmlTestStep.__single = self
        self.HTMLStep = "<h3>Test Step</h3>"
        self.afterImg_base64 = ""
        self.beforeImg_base64 = ""
        self.actionvalue = ""

    def getHtmlTestStep():
        if not HtmlTestStep.__single:
            HtmlTestStep.__single = HtmlTestStep()
        return HtmlTestStep.__single

    def step_before(self, imagepath):
        data_uri = base64.b64encode(open(imagepath, 'rb').read()).decode('utf-8').replace('\n', '')
        self.beforeImg_base64 = """<img data-src="holder.js/140x140" class="img-responsive" src="data:image/jpg;base64,%s"  data-holder-rendered="true" style="width: 500px;">""" % data_uri

    def step_after(self, imagepath):
        data_uri = base64.b64encode(open(imagepath, 'rb').read()).decode('utf-8').replace('\n', '')
        self.afterImg_base64 = """<img data-src="holder.js/140x140" class="img-responsive" src="data:image/jpg;base64,%s"  data-holder-rendered="true" style="width: 500px;">""" % data_uri

    def step_IMG(self, image):
        jpeg_image_buffer = io.BytesIO()
        image.save(jpeg_image_buffer, format="JPEG")
        base64_encoded_result = base64.b64encode(jpeg_image_buffer.getvalue())
        imgStr = base64_encoded_result.decode('utf-8')
        return """<img data-src="holder.js/140x140" class="img-responsive" src="data:image/jpg;base64,%s"  data-holder-rendered="true" style="height: 100px;">""" % imgStr


    def clearstep(self):
        self.HTMLStep = "<h3>Test Step</h3>"

    def report_step(self):
        report = Report.getReport()

        self.HTMLStep = self.HTMLStep + r"""
        </body>
        <script src="https://cdn.jsdelivr.net/jquery/1.11.3/jquery.min.js"></script>
        <script src="https://cdn.jsdelivr.net/mousewheel/3.1.13/jquery.mousewheel.min.js"></script>
        <script src="https://cdn.jsdelivr.net/fancybox/2.1.5/jquery.fancybox.pack.js"></script>
        <script src="https://cdn.jsdelivr.net/bootstrap/3.3.6/js/bootstrap.min.js"></script>
        <script src="https://cdn.jsdelivr.net/vue/1.0.24/vue.min.js"></script>
        """

        report.insert(self.HTMLStep)

    def set_step(self,testcaseName, step, action, status, value, image):

        if status=="Success":
            bg_color = "success"
        else:
            bg_color = "danger"

        self.actionvalue = ""
        if value[0] != "":
            self.actionvalue = value[0]

        if image[0]!=None:
            self.actionvalue = self.step_IMG(image[0])


        self.HTMLStep = self.HTMLStep + r"""
	<div class="panel panel-""" + bg_color + """">
      <div class="panel-heading"><h4>"""+ testcaseName +" Step "+ str(step + 1) + " " + action[0] + " : </br></br>" +self.actionvalue + """</h4></div>
      <div class="panel-body">
        <div class="col-md-6">
          <ul class="device-info">
            <li><h4>Before</h4></li>
            <li>"""+ self.beforeImg_base64 + """</li>
          </ul>
        </div>
        <div class="col-md-6">
          <ul class="device-info">
            <li><h4>After</h4></li>
            <li>"""+ self.afterImg_base64 + """</li>
          </ul>
        </div>
      </div>
    </div>
"""