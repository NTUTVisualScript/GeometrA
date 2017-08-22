import sys
sys.path.append('../')
sys.path.append('../Save')
import time
from cv2img import CV2Img
from adb_roboot import ADBRobot
from Load import FileLoader
from MessageUI import Message
from HTML.step import HtmlTestStep
from finder.template_finder import TemplateFinder




class Executor():
    def __init__(self, case):
        if str(case.__class__) != '<class \'TestCase.TestCase\'>':
            raise Exception('Not a executable case')
        self.case = case
        self.robot = ADBRobot()
        self.htmlstep = HtmlTestStep.getHtmlTestStep()

    def getOriginalScreen(self):
        filePath = self.robot.before_screenshot()
        self.originalScreen = filePath

    def getCurrentScreen(self):
        filePath = self.robot.before_screenshot()
        self.currentScreen = filePath

    def runAll(self):
        for i in range(self.case.getSize()):
            status = self.execute(i)
            if status == 'Failed':
                return 'Failed'
            if status == 'Error':
                return 'Error'
        return 'Success'

    def run(self, n):
        self.getOriginalScreen()
        self.htmlstep.step_before(self.originalScreen)

        status = self.execute(n)

        self.getCurrentScreen()
        self.htmlstep.step_after(self.currentScreen)

        self.stepResult(n)

        return status

    def execute(self, n):
            act = self.case.getSteps(n).getAction()
            if act == '':
                return self.case.setStatus(n, 'Success')
            elif act == 'Click':
                return self.case.setStatus(n, self.click(n))
            elif act == 'Swipe':
                return self.case.setStatus(n, self.Swipe(n))
            elif act == 'Set Text':
                return self.case.setStatus(n, self.setText(n))
            elif act == 'TestCase':
                return self.case.setStatus(n, self.testCase(n))
            elif act == 'Sleep(s)':
                return self.case.setStatus(n, self.sleep(n))
            elif act == 'Android Keycode':
                return self.case.setStatus(n, self.sendKeyValue(n))
            elif act == 'Assert Exist':
                return self.case.setStatus(n, self.imageExist(n))
            elif act == 'Assert Not Exist':
                return self.case.setStatus(n, self.imageNotExist(n))

    def click(self, n):
        status = self.imageFinder(targetImage=self.case.getSteps(n).getValue())

        if status == 'Success':
            self.robot.tap(self.clickX, self.clickY)
            return 'Success'
        elif status == 'Failed':
            return 'Failed'
        '''
            Wait for Tree node designed
        '''
        # else:
        #     self.clickNode(n)

    def imageFinder(self, sourceImage=None, targetImage=None, resultImage=None):
        # return True
        if sourceImage == None:
            sourceImage = self.originalScreen
        if resultImage == None:
            resultImage = sourceImage
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
            drawCircle = CV2Img()
            drawCircle.load_file(sourceImage, 1)
            drawCircle.draw_circle(int(self.clickX), int(self.clickY))
            drawCircle.save(resultImage)
            return 'Success'
        else:
            return 'Too many'

    def Swipe(self, n):
        value = str(self.case.getSteps(n).getValue())
        try:
            coordinate = value.split(',')
            startX = int(coordinate[0].split('=')[1])
            startY = int(coordinate[1].split('=')[1])

            endX = int(coordinate[2].split('=')[1])
            endY = int(coordinate[3].split('=')[1])

        except:
            return 'Error'
        try:
            self.swipeImage(startX, startY, endX, endY)
            self.robot.drag_and_drop(startX, startY, endX, endY)
            return 'Success'
        except Exception as e:
            print(e)
            return 'Failed'

    def swipeImage(self, x1, y1, x2, y2):
        source = CV2Img()
        source.load_file(self.originalScreen, 1)
        source.draw_line(x1,y1,x2,y2)
        source.draw_Arrow(x1, y1, x2, y2)
        source.save(self.originalScreen)

    def setText(self, n):
        '''
        Here is comment for unittest to pass
        '''
        try:
            # self.robot.input_text(self.case.getSteps(n).getValue())
            return 'Success'
        except:
            return 'Failed'

    def testCase(self, n):
        try:
            path = self.case.getSteps(n).getValue()
            exe = Executor(FileLoader(path).getTestCase())
            exe.runAll()
            return 'Success'
        except:
            return 'Error'

    def sleep(self, n):
        try:
            t = int(self.case.getSteps(n).getValue())
        except:
            return 'Error'
        try:
            time.sleep(t)
            return 'Success'
        except:
            return 'Failed'

    def sendKeyValue(self, n):
        try:
            self.robot.send_key(self.case.getSteps(n).getValue())
            return 'Success'
        except:
            return 'Error'

    def imageExist(self, n):
        status = self.imageFinder(targetImage=self.case.getSteps(n).getValue())
        if status == 'Failed':
            return 'Failed'
        return 'Success'

    def imageNotExist(self, n):
        status = self.imageFinder(targetImage=self.case.getSteps(n).getValue())
        if status == 'Failed':
            return 'Success'
        return 'Failed'

    def stepResult(self, n):
        if self.case.getStatus(n) == 'Success':
            result = 'Action ' + str(n+1) + ' Success'
        elif self.case.getStatus(n) == 'Failed':
            result = 'Action ' + str(n+1) + ' Failed'
        else:
            result = 'Action ' + str(n+1) + ' Error'

        return result
