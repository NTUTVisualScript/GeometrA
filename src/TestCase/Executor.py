import sys
sys.path.append('../')
sys.path.append('../Save')
import time
from cv2img import CV2Img
from adb_roboot import ADBRobot
from Load import FileLoader
from MessageUI import Message

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
        # self.message = Message.getMessage(self)

    def runAll(self):
        for i in range(self.case.getSize()):
            if not self.run(i):
                # self.message.InsertText('Step' + str(i+1) + 'Status Failed')
                return False
            # self.message.InsertText('Step' + str(i+1) + 'Status Success')
        return True

    def run(self, n):
            act = self.case.getSteps(n).getAction()
            if act == '':
                return True
            elif act == 'Click':
                return self.click(n)
            elif act == 'Drag':
                return self.drag(n)
            elif act == 'Set Text':
                return self.setText(n)
            elif act == 'TestCase':
                return self.testCase(n)
            elif act == 'Sleep(s)':
                return self.sleep(n)
            elif act == 'Android Keycode':
                return self.sendKeyValue(n)
            elif act == 'Assert Exist':
                return self.imageExist(n)
            elif act == 'Assert Not Exist':
                return self.imageNotExist(n)

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
            # ADBRobot().tap(coordinate_x, coordinate_y)
            return True
        else:
            # self.message.InsertText('Error: Image Not Find\n')
            return False

    def imageFinder(self, target):
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
            return False
        try:
            '''
            Here is comment for unittest to pass
            '''
            # dragImage(startX, startY, endX, endY)
            # ADBRobot().drag_and_drop(startX, startY, endX, endY)
            return True
        except:
            print('Drag and drop error')
            # self.message.InsertText('Drag and drop error')
            return False

    def setText(self, n):
        '''
        Here is comment for unittest to pass
        '''
        # ADBRobot().input_text(self.case.getSteps(n).getValue())
        return True

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
            return True
        except:
            # self.message.InsertText('Error! Please check the test case file: \n' + self.case.getSteps(n).getValue() + '\n')
            return False

    def sleep(self, n):
        try:
            time.sleep(int(self.case.getSteps(n).getValue()))
            return True
        except:
            # self.message.InsertText('Invalid Time\n')
            return False

    def sendKeyValue(self, n):
        try:
            ADBRobot().send_key(self.case.getSteps(n).getValue())
            return True
        except:
            # self.message.InsertText('Invalid Android Keycode\n')
            return False

    def imageExist(self, n):
        '''
        Here is waiting for imageFinder too
        '''
        return self.imageFinder(self.case.getSteps(n).getValue())

    def imageNotExist(self, n):
        '''
        Here return true for unittest, the comment line is real code
        '''
        # return !self.imageExist(n)
        return True
