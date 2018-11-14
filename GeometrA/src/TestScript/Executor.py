import time
from GeometrA.src.finder.cv2img import CV2Img
from GeometrA.src.ADB.adbRobot import ADBRobot
from GeometrA.src.Controller.FileLoader import FileLoader
from GeometrA.src.finder.template_finder import TemplateFinder

class Executor():
    def __init__(self, case):
        if str(case.__class__) != '<class \'GeometrA.src.TestScript.TestCase.TestCase\'>':
            raise Exception('Not a executable case')
        self.case = case
        self.robot = ADBRobot()
        self.originalScreen = None

    def getOriginalScreen(self):
        filePath = self.robot.before_screenshot()
        self.originalScreen = filePath

    def getCurrentScreen(self):
        filePath = self.robot.before_screenshot()
        self.currentScreen = filePath

    def runAll(self):
        i = 0
        while i < self.case.getSize():
            print('Step ' + str(i))
            status = self.execute(i)
            if self.case.getSteps(i).getAction() == 'Loop Begin':
                i = self.loopEnd(i)
            if status == 'Failed':
                return 'Failed'
            if status == 'Error':
                return 'Error'
            i = i+1
        return 'Success'

    def execute(self, n):
            act = self.case.getSteps(n).getAction()
            if (act == '') or act == 'Loop End':
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
            elif act == 'Loop Begin':
                return self.case.setStatus(n, self.loop(n))
            elif act == 'Open App':
                return self.case.setStatus(n, self.openApp(n))
            elif act == 'Close App':
                return self.case.setStatus(n, self.closeApp(n))

    def click(self, n):
        status = self.imageFinder(step=self.case.getSteps(n))
        print(status)
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

    def imageFinder(self, step, sourceImage=None):
        # return True
        if sourceImage is None:
            sourceImage = self.robot.before_screenshot()
        targetImage = step.getValue()
        if str(sourceImage.__class__) == "<class 'cv2img.CV2Img'>":
            source = sourceImage
        else:
            source = CV2Img()
            source.load_file(sourceImage, 0)
        target = CV2Img()
        target.load_PILimage(targetImage)
        finder = TemplateFinder(source)
        results = finder.find_all(target, 0.9)
        # if len(results) < 1:
        #     return 'Failed'
        if len(results) == 1:
            self.clickX, self.clickY = source.coordinate(results[0])
            return 'Success'
        else:
            return self.nodeFinder(step)

    def nodeFinder(self, step):
        from GeometrA.src.Controller.TreeController import Tree
        node = step.getNode()
        if node is None:
            return 'Failed'
        result = Tree.getTree().findNode(node)

        if result == 'Failed': return result

        self.clickX, self.clickY = result
        return 'Success'
        # return self.imageFinder(step, nodeSource)

    def Swipe(self, n):
        value = str(self.case.getSteps(n).getValue())
        try:
            coordinate = value.split(',')
            self.startX = float(coordinate[0].split('=')[1])
            self.startY = float(coordinate[1].split('=')[1])

            self.endX = float(coordinate[2].split('=')[1])
            self.endY = float(coordinate[3].split('=')[1])
            print(self.startX)
            print(self.startY)
            print(self.endX)
            print(self.endY)

            self.robot.drag_and_drop(self.startX, self.startY, self.endX, self.endY)
            return 'Success'
        except Exception as e:
                print(e)
                return 'Error'

    def setText(self, n):
        self.robot.input_text(self.case.getSteps(n).getValue())
        return 'Success'

    def testCase(self, n):
        try:
            path = self.case.getSteps(n).getValue()
            print(path)
            case = FileLoader.getFileLoader()
            case.loadFile(path)
            return Executor(case.getTestCase()).runAll()
        except Exception as e:
            print(e)
            return 'Error'

    def sleep(self, n):
        t = int(self.case.getSteps(n).getValue())
        print('Sleep ' + str(t) + 's')
        time.sleep(t)
        return 'Success'

    def sendKeyValue(self, n):
        self.robot.send_key(self.case.getSteps(n).getValue())
        return 'Success'

    def imageExist(self, n):
        status = self.imageFinder(step=self.case.getSteps(n))
        if status == 'Failed':
            return 'Failed'
        return 'Success'

    def imageNotExist(self, n):
        status = self.imageFinder(step=self.case.getSteps(n))
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

    def loop(self, n):
        times = int(self.case.getSteps(n).getValue())
        for i in range(times):
            print('Loop ' + str(i))
            j = n + 1
            try:
                while True:
                    act = self.case.getSteps(j).getAction()
                    if act == 'Loop End':
                        break
                    status = self.execute(j)
                    if act == 'Loop Begin':
                        j = self.loopEnd(j)
                    if (status == 'Failed') or (status == 'Error'):
                        return status
                    j = j+1
            except:
                print('Loop Without End')
                return 'Error'
        return 'Success'

    def loopEnd(self, n):
        i = n+1
        while True:
            act = self.case.getSteps(i).getAction()
            if act == 'Loop End':
                break
            if act == 'Loop Begin':
                i = self.loopEnd(i)
            i = i+1
        return i

    def openApp(self, n):
        appName = self.case.getSteps(n).getValue()
        return self.robot.open_app(appName)

    def closeApp(self, n):
        appName = self.case.getSteps(n).getValue()
        return self.robot.close_app(appName)
