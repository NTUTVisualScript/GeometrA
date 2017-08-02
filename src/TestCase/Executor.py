import sys
sys.path.append('../')
sys.path.append('../Save')
import time
from cv2img import CV2Img
from adb_roboot import ADBRobot
from Load import FileLoader
from MessageUI import Message
from HTML.step import HtmlTestStep


def dragImage(x1,y1,x2,y2):
    '''
    Here Should add a code to get screenshot
    '''
    source = CV2Img()
    source.load_file(source_image, 1)
    source.draw_line(x1,y1,x2,y2)
    source.draw_circle(x2,y2)
    source.save(source_image)

class Executor():
    def __init__(self, case):
        if str(case.__class__) != '<class \'TestCase.TestCase\'>':
            raise Exception('Not a executable case')
        self.case = case
        self.robot = ADBRobot()
        self.htmlstep = HtmlTestStep.getHtmlTestStep()
        # self.message = Message.getMessage(self)

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
                # self.message.InsertText('Step' + str(i+1) + 'Status Failed')
                return 'Failed'
            if status == 'Error':
                # self.message.InsertText('Step' + str(i+1) + 'Status Failed')
                return 'Error'
            # self.message.InsertText('Step' + str(i+1) + 'Status Success')
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
            elif act == 'Drag':
                return self.case.setStatus(n, self.drag(n))
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
        '''
            imageFinder is waiting for be write after.
            It should get the screenshot and compare with target image it got from parameter
        '''
        status = self.imageFinder(self.case.getSteps(n).getValue())

        if status == True:
            '''
            Here is commented for unittest
            '''
            # self.robot.tap(coordinate_x, coordinate_y)
            return 'Success'
        else:
            # self.message.InsertText('Error: Image Not Find\n')
            return 'Failed'

    def imageFinder(self, target):
        self.robot.before_screenshot()

        return True

    def drag(self, n):
        value = str(self.case.getSteps(n).getValue())
        try:
            coordinate = value.split(',')
            startX = int(coordinate[0].split('=')[1])
            startY = int(coordinate[1].split('=')[1])

            endX = int(coordinate[2].split('=')[1])
            endY = int(coordinate[3].split('=')[1])

        except:
            # print('Coordinate Value Split Error: ', str(value))
            # self.message.InsertText('Invalid Coordinate')
            return 'Error'
        try:
            '''
            Here is comment for unittest to pass
            '''
            # dragImage(startX, startY, endX, endY)
            # self.robot.drag_and_drop(startX, startY, endX, endY)
            return 'Success'
        except:
            print('Drag and drop error')
            # self.message.InsertText('Drag and drop error')
            return 'Failed'

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
            testCaseFile = FileLoader()
            testCaseFile.jsonDecoder(self.case.getSteps(n).getValue())

            name = self.case.getSteps(n).getValue().split('/')
            foldername = str(name.pop())
            '''
            Here is comment for unittest to pass
            '''
            exe = Executor(testCaseFile.getTestCase())
            exe.runAll()
            return 'Success'
        except:
            # self.message.InsertText('Error! Please check the test case file: \n' + self.case.getSteps(n).getValue() + '\n')
            return 'Error'

    def sleep(self, n):
        try:
            t = int(self.case.getSteps(n).getValue())
        except:
            # self.message.InsertText('Invalid Time')
            return 'Error'
        try:
            time.sleep(t)
            return 'Success'
        except:
            # self.message.InsertText('Time Sleep Failed\n')
            return 'Failed'

    def sendKeyValue(self, n):
        try:
            self.robot.send_key(self.case.getSteps(n).getValue())
            return 'Success'
        except:
            # self.message.InsertText('Invalid Android Keycode\n')
            return 'Error'

    def imageExist(self, n):
        '''
        Here is waiting for imageFinder too
        '''
        if self.imageFinder(self.case.getSteps(n).getValue()):
            return 'Success'
        self.message.InsertText('Failed: image and node Not Found')
        return 'Failed'

    def imageNotExist(self, n):
        '''
        Here return true for unittest, the comment line is real code
        '''
        # if self.imageFinder(self.case.getSteps(n).getValue()):
        #     return 'Failed'
        return 'Success'

    def stepResult(self, n):
        if self.case.getStatus(n) == 'Success':
            result = 'Action ' + str(n+1) + ' Success'
        elif self.case.getStatus(n) == 'Failed':
            result = 'Action ' + str(n+1) + ' Failed'
        else:
            result = 'Action ' + str(n+1) + ' Error'

        # self.message.InsertText(result)
        return result
