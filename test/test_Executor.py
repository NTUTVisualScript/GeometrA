import unittest
from PIL import Image, ImageTk

import sys
sys.path.append('../src/TestCase')
sys.path.append('../src')
sys.path.append('../src/Save')
from Executor import Executor
from TestStep import Step
from TestCase import TestCase

class ExecutorTestSuite(unittest.TestCase):
    def testConstructer(self):
        case = TestCase()
        exe = Executor(case)
        self.assertEqual('<class \'TestCase.TestCase\'>', str(exe.case.__class__))

    def testConstructerExcept(self):
        step = Step('Set Text', 'Hello World')
        self.assertRaisesRegex(Exception, 'Not a executable case', Executor, step)

    def testExecuteClick(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='Android Keycode', val='KEYCODE_HOME')
        case.insert(act='Click', val=Image.open('./TestCase/Test/image/exist.png'))
        exe.execute(0)
        self.assertEqual('Success', exe.execute(1))
        exe.execute(0)

    def testExecuteSwipe(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='Swipe', val='start x=400, y=300, end x=200, y=300')
        self.assertEqual('Success', exe.execute(0))
        case.insert(act='Android Keycode', val='KEYCODE_HOME')
        exe.execute(1)
    def testExecuteSwipeError(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='Swipe', val='x=, y=3, x=4, y=3')
        self.assertEqual('Error', exe.execute(0))

    def testExecuteSetText(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='TestCase', val='./TestCase/SetText/SetTextSetUp')
        case.insert(act='Set Text', val='Hello World')
        case.insert(act='TestCase', val='./TestCase/SetText/SetTextTearDown')
        exe.execute(0)
        self.assertEqual('Success', exe.execute(1))
        target = Image.open('./TestCase/SetText/source.png')
        self.assertEqual('Success', exe.imageFinder(targetImage=target))
        exe.execute(2)

    def testExecuteTestCase(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='TestCase', val='./TestCase/Test')
        self.assertEqual('Success', exe.execute(0))
    def testExecuteTestCaseExcept(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='TestCase', val='D:/')
        self.assertEqual('Error', exe.execute(0))

    def testExecuteSleep(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='Sleep(s)', val='0')
        self.assertEqual('Success', exe.execute(0))
    def testExecuteSleepExcept(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='Sleep(s)', val='Hello World')
        self.assertEqual('Error', exe.execute(0))

    def testExecuteAndroidKeycode(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='Android Keycode', val='KEYCODE_HOME')
        self.assertEqual('Success', exe.execute(0))
    '''
    It seems like there is no checking for key code in ADBRobot
    '''
    # def testExecuteAndroidKeycodeExcept(self):
    #     case = TestCase(5)
    #     case.setAction(2, 'Android Keycode')
    #     case.setValue(2, 'Hello World')
    #     exe = Executor(case)
    #     self.assertEqual('Error', exe.execute(2))

    def testExecuteAssertExist(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='Assert Exist', val=Image.open('./TestCase/Test/image/exist.png'))
        self.assertEqual('Success', exe.execute(0))

    def testExecuteAssertNotExist(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='Assert Not Exist', val=Image.open('./TestCase/Test/image/notexist.png'))
        self.assertEqual('Success', exe.execute(0))

    def testRun(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='Sleep(s)', val='0')
        self.assertEqual('Success', exe.run(0))

    def testStepResult(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='Sleep(s)', val='0')
        case.insert(act='Click', val='./TestCase/Test/image/exist.png')
        case.insert(act='Android Keycode', val='KEYCODE_HOME')
        case.setStatus(0, 'Success')
        case.setStatus(1, 'Failed')
        case.setStatus(2, 'Error')
        self.assertEqual('Action 1 Success', exe.stepResult(0))
        self.assertEqual('Action 2 Failed', exe.stepResult(1))
        self.assertEqual('Action 3 Error', exe.stepResult(2))

    def testRunAll(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='Android Keycode', val='KEYCODE_HOME')
        case.insert(act='Click', val=Image.open('./TestCase/Test/image/exist.png'))
        # case.insert(act='Swipe', val='start x=800, y=1000, end x=300, y=1000')
        case.insert(act='Android Keycode', val='KEYCODE_HOME')
        self.assertEqual('Success', exe.runAll())
    def testRunAllError(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='Android Keycode', val='KEYCODE_HOME')
        case.insert(act='Sleep(s)', val='Hello World')
        self.assertEqual('Error', exe.runAll())

    def testImageFinder(self):
        source = ('./TestCase/Test/image/source.png')
        successTarget = Image.open('./TestCase/Test/image/success.png')
        failedTarget = Image.open('./TestCase/Test/image/failed.png')
        tooManyTarget = Image.open('./TestCase/Test/image/toomany.png')

        exe = Executor(TestCase())
        self.assertEqual('Success', exe.imageFinder(source, successTarget))
        self.assertEqual('Failed', exe.imageFinder(source, failedTarget))
        self.assertEqual('Too many', exe.imageFinder(source, tooManyTarget))
