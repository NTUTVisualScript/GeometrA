from adbRobot import ADBRobot
import base64
import io
from cv2img import CV2Img
from finder.template_finder import TemplateFinder

class Step:
    def __init__(self):
        self.HTMLStep = "<h3>Test Step</h3>"
        self.afterImg = ""
        self.beforeImg = ""
        self.actionvalue = ""

    def stepBefore(self, step):
        self.reportImage(step)
        dataURI = base64.b64encode(open(self.beforeScreenshot, 'rb').read()).decode('utf-8').replace('\n', '')
        self.beforeImg = """<img data-src="holder.js/140x140" class="img-responsive" src="data:image/png;base64,%s"  data-holder-rendered="true" style="width: 500px;">""" % dataURI

    def reportImage(self, step):
        act = step.getAction()
        self.beforeScreenshot = ADBRobot().before_screenshot()
        if (act == 'Click') or (act == 'Assert Exist') or (act == 'Assert Not Exist'):
            self.findImage(step)
        elif act == 'Swipe':
            self.swipeImage(step.getValue())

    def findImage(self, step):
        if self.imageFinder(self.beforeScreenshot, step.getValue()) != 'Success': return
        drawCircle = CV2Img()
        drawCircle.load_file(self.beforeScreenshot, 1)
        drawCircle.draw_circle(int(self.clickX), int(self.clickY))
        drawCircle.save(self.beforeScreenshot)

    def swipeImage(self, val):
        coor = val.split(',')
        x1 = int(float(coor[0].split('=')[1]))
        y1 = int(float(coor[1].split('=')[1]))
        x2 = int(float(coor[2].split('=')[1]))
        y2 = int(float(coor[3].split('=')[1]))

        source = CV2Img()
        source.load_file(self.beforeScreenshot, 1)
        source.draw_line(x1,y1,x2,y2)
        source.draw_Arrow(x1, y1, x2, y2)
        source.save(self.beforeScreenshot)

    def imageFinder(self, sourceImage, targetImage):
        source = CV2Img()
        source.load_file(sourceImage, 0)
        target = CV2Img()
        target.load_PILimage(targetImage)
        finder = TemplateFinder(source)
        results = finder.find_all(target, 0.9)
        if len(results) < 1:
            return 'Failed'
        elif len(results) == 1:
            self.clickX, self.clickY = source.coordinate(results[0])
            return 'Success'
        else:
            return 'Too many'

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

    def clearStep(self):
        self.HTMLStep = "<h3>Test Step</h3>"

    def reportStep(self):
        stepResult = self.HTMLStep + r"""
        </body>
        <script src="https://cdn.jsdelivr.net/jquery/1.11.3/jquery.min.js"></script>
        <script src="https://cdn.jsdelivr.net/mousewheel/3.1.13/jquery.mousewheel.min.js"></script>
        <script src="https://cdn.jsdelivr.net/fancybox/2.1.5/jquery.fancybox.pack.js"></script>
        <script src="https://cdn.jsdelivr.net/bootstrap/3.3.6/js/bootstrap.min.js"></script>
        <script src="https://cdn.jsdelivr.net/vue/1.0.24/vue.min.js"></script>
        """
        self.clearStep()
        return stepResult

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

        act = step.getAction()
        self.HTMLStep = self.HTMLStep + r"""
	<div class="panel panel-""" + bg_color + """">
      <div class="panel-heading"><h4>""" + " Step "+ str(n + 1) + " " + step.getAction() + " : </br></br>" +self.actionvalue + """</h4></div>
"""
        if act != 'Sleep(s)':
            self.HTMLStep = self.HTMLStep + r"""
      <div class="panel-body">
        <div class="col-md-6">
          <ul class="device-info">
            <li><h4>Before</h4></li>
            <li>"""+ self.beforeImg + """</li>
          </ul>
        </div>
"""
            if (act != 'Assert Exist') & (act != 'Assert Not Exist'):
                self.HTMLStep = self.HTMLStep + r"""
        <div class="col-md-6">
          <ul class="device-info">
            <li><h4>After</h4></li>
            <li>"""+ self.afterImg + """</li>
          </ul>
        </div>
"""
            self.HTMLStep = self.HTMLStep + r"""
      </div>
"""
        self.HTMLStep = self.HTMLStep + r"""
    </div>
"""
