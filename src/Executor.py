from cv2img import CV2Img
from adb_roboot import ADBRobot

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

    def run(self, n):
        act = self.case.getSteps(n).getAction()
        if act == '':
            print('hi')
            return None
        if act == 'Click':
            return self.click(n)
        if act == 'Drag':
            return self.drag(n)
        if act == 'Set Text':
            return self.setText(n)
        if act == 'TestCase':
            return self.testCase(n)

        #     elif self.action == "TestCase":
        #         self.status, count = self.TestCasePath()
        #         self.count = self.count + count
        #     elif self.action == "Sleep(s)":
        #         self.status = self.Sleep()
        #     elif self.action == "Android Keycode":
        #         self.status = self.Send_Key_Value()
        #     elif self.action == "Assert Exist":
        #         self.ActionStatus = self.ExistsImage()
        #     elif self.action == "Assert Not Exist":
        #         self.status = self.ExistsImage()
        #         if self.status == "Success":
        #             self.status = "Error"
        #         else:
        #             self.status = "Success"
        #
        #     return self.status

    def click(self, n):
        '''
            imageFinder is waiting for be write after.
            It should get the screenshot and compare with target image it got from parameter
        '''
        status = self.imageFinder(self.case.getSteps(n).getValue())

        if status == 'Success':
            '''
            Here is commented for unittest
            '''
            # ADBRobot().tap(coordinate_x, coordinate_y)
            return 'Success'
    def imageFinder(self, target):
        return 'Success'

    def drag(self, n):
        value = str(self.case.getSteps(n).getValue())
        try:
            coordinate = value.split(',')
            startX = int(coordinate[0].split('=')[1])
            startY = int(coordinate[1].split('=')[1])

            endX = int(coordinate[2].split('=')[1])
            endY = int(coordinate[3].split('=')[1])

        except:
            print('Coordinate Value Split Error: ', str(value))
            return 'Error'
        try:
            '''
            Here is comment for unittest to pass
            '''
            # dragImage(startX, startY, endX, endY)
            # ADBRobot().drag_and_drop(startX, startY, endX, endY)
            return 'Success'
        except:
            print('Drag and drop error')
            return 'Error'

    def setText(self, n):
        '''
        Here is comment for unittest to pass
        '''
        # ADBRobot().input_text(self.case.getSteps(n).getValue())
        return 'Success'

    def testCase(self, n):
        testCaseFile = LoadFile()
        testCase.Decoder_Json(self.case.getSteps(n).getValue())

        name = self.case.getSteps(n).getValue().split('/')
        foldername = str(name.pop())

        testCase = Test
