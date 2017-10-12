from adbRobot import ADBRobot
import io

class Step:
    def __init__(self):
        self.HTMLStep = "<h3>Test Step</h3>"
        self.afterImg = ""
        self.beforeImg = ""
        self.actionvalue = ""

    def stepBefore(self):
        imagePath = ADBRobot().before_screenshot()
        dataURI = base64.b64encode(open(imagePath, 'rb').read()).decode('utf-8').replace('\n', '')
        self.beforeImg = """<img data-src="holder.js/140x140" class="img-responsive" src="data:image/png;base64,%s"  data-holder-rendered="true" style="width: 500px;">""" % dataURI

    def stepAfter(self):
        imagePath = ADBRobot().after_screenshot()
        dataURI = base64.b64encode(open(imagePath, 'rb').read()).decode('utf-8').replace('\n', '')
        self.afterImg = """<img data-src="holder.js/140x140" class="img-responsive" src="data:image/png;base64,%s"  data-holder-rendered="true" style="width: 500px;">""" % dataURI

    def stepIMG(self, image):
        pngImgBuffer = io.BytesIO()
        image.save(pngImgBuffer, format="PNG")
        base64_encoded_result = base64.b64encode(pngImgBuffer.getvalue())
        imgStr = base64_encoded_result.decode('utf-8')
        return """<img data-src="holder.js/140x140" class="img-responsive" src="data:image/png;base64,%s"  data-holder-rendered="true" style="height: 100px;">""" % imgStr

    def clearstep(self):
        self.HTMLStep = "<h3>Test Step</h3>"

    def reportStep(self):
        self.HTMLStep = self.HTMLStep + r"""
        </body>
        <script src="https://cdn.jsdelivr.net/jquery/1.11.3/jquery.min.js"></script>
        <script src="https://cdn.jsdelivr.net/mousewheel/3.1.13/jquery.mousewheel.min.js"></script>
        <script src="https://cdn.jsdelivr.net/fancybox/2.1.5/jquery.fancybox.pack.js"></script>
        <script src="https://cdn.jsdelivr.net/bootstrap/3.3.6/js/bootstrap.min.js"></script>
        <script src="https://cdn.jsdelivr.net/vue/1.0.24/vue.min.js"></script>
        """
        return self.HTMLStep

    def setStep(self, step, n):

        if step.getStatus()=="Success":
            bg_color = "success"
        else:
            bg_color = "danger"

        self.actionvalue = ""
        if str(step.getValue().__class__) == "<class 'str'>":
            self.actionvalue = step.getValue()
        else:
            self.actionvalue = self.stepIMG(step.getValue())


        self.HTMLStep = self.HTMLStep + r"""
	<div class="panel panel-""" + bg_color + """">
      <div class="panel-heading"><h4>""" + " Step "+ str(n + 1) + " " + step.getAction() + " : </br></br>" +self.actionvalue + """</h4></div>
      <div class="panel-body">
        <div class="col-md-6">
          <ul class="device-info">
            <li><h4>Before</h4></li>
            <li>"""+ self.beforeImg + """</li>
          </ul>
        </div>
        <div class="col-md-6">
          <ul class="device-info">
            <li><h4>After</h4></li>
            <li>"""+ self.afterImg + """</li>
          </ul>
        </div>
      </div>
    </div>
"""
