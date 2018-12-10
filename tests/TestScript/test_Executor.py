import unittest
import GeometrA

from PIL import Image, ImageTk

from GeometrA.src.TestScript.Executor import Executor
from GeometrA.src.TestScript.TestStep import Step
from GeometrA.src.TestScript.TestCase import TestCase

class ExecutorTestSuite(unittest.TestCase):
    def setUp(self):
        GeometrA.app.testing = True
        self.app = GeometrA.app.test_client()

    def testConstructer(self):
        case = TestCase()
        exe = Executor(case)
        self.assertEqual('<class \'GeometrA.src.TestScript.TestCase.TestCase\'>', str(exe.case.__class__))
    def testConstructerExcept(self):
        step = Step('Set Text', 'Hello World')
        self.assertRaisesRegex(Exception, 'Not a executable case', Executor, step)



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

    def testExecuteSleep(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='Sleep(s)', val='0')
        self.assertEqual('Success', exe.execute(0))

    def testExecuteAndroidKeycode(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='Android Keycode', val='KEYCODE_HOME')
        self.assertEqual('Success', exe.execute(0))

    def testStepResult(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='Sleep(s)', val='0')
        case.insert(act='Click', val=Image.open('./tests/TestCase/Test/image/notexist.png'))
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
        case.insert(act='Click', val=Image.open('./tests/TestCase/Test/image/exist.png'))
        case.insert(act='Swipe', val='start x=800, y=1000, end x=300, y=1000')
        case.insert(act='Android Keycode', val='KEYCODE_HOME')
        self.assertEqual('Success', exe.runAll())
    def testRunAllError(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='Android Keycode', val='KEYCODE_HOME')
        case.insert(act='Swipe', val='x=, y=1000, x=300, y=1000')
        self.assertEqual('Error', exe.runAll())
    def testRunAllFailed(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='Click', val=Image.open('./tests/TestCase/Test/image/notexist.png'))
        self.assertEqual('Failed', exe.runAll())

    def testImageFinder(self):
        source = ('./tests/TestCase/Test/image/source.png')
        successTarget = Image.open('./tests/TestCase/Test/image/success.png')
        failedTarget = Image.open('./tests/TestCase/Test/image/failed.png')
        # tooManyTarget = Image.open('./TestCase/Test/image/toomany.png')

        step1 = Step(act='Click', val=successTarget)
        step2 = Step(act='Click', val=failedTarget)
        # step3 = Step(act='Click', val=tooManyTarget)

        exe = Executor(TestCase())
        self.assertEqual('Success', exe.imageFinder(sourceImage=source, step=step1))
        self.assertEqual('Failed', exe.imageFinder(sourceImage=source, step=step2))
        # self.assertEqual('Too many', exe.imageFinder(sourceImage=source, step=step3))

    def testExecuteLoop(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='Android Keycode', val='KEYCODE_HOME')
        case.insert(act='Loop Begin', val='3')
        case.insert(act='Swipe', val='start x=800, y=1000, end x=500, y=1000')
        case.insert(act='Swipe', val='start x=500, y=1000, end x=800, y=1000')
        case.insert(act='Loop End', val=None)
        self.assertEqual('Success', exe.runAll())
    def testExecuteLoopWithoutEnd(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='Android Keycode', val='KEYCODE_HOME')
        case.insert(act='Loop Begin', val='3')
        case.insert(act='Swipe', val='start x=800, y=1000, end x=500, y=1000')
        case.insert(act='Swipe', val='start x=500, y=1000, end x=800, y=1000')
        exe.execute(0)
        self.assertEqual('Error', exe.execute(1))
    def testExecuteNestLoopWithoutEnd(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='Loop Begin', val='2')
        case.insert(act='Sleep(s)', val='0')
        case.insert(act='Loop Begin', val='2')
        case.insert(act='Swipe', val='start x=500, y=1000, end x=300, y=1000')
        case.insert(act='Android Keycode', val = 'KEYCODE_HOME')
        case.insert(act='Loop End', val=None)
        self.assertEqual('Error', exe.execute(0))
    def testExecuteLoopFailed(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='Android Keycode', val='KEYCODE_HOME')
        case.insert(act='Loop Begin', val='3')
        case.insert(act='Click', val=Image.open('./tests/TestCase/Test/image/notexist.png'))
        case.insert(act='Loop End', val=None)
        exe.execute(0)
        self.assertEqual('Failed', exe.execute(1))
    def testExecuteLoopError(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='Android Keycode', val='KEYCODE_HOME')
        case.insert(act='Loop Begin', val='3')
        case.insert(act='Swipe', val='x=, y=1000, x=500, y=1000')
        case.insert(act='Loop End', val=None)
        exe.execute(0)
        self.assertEqual('Error', exe.execute(1))

    def testLoopEnd(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='Loop Begin', val='1')
        case.insert(act='Loop Begin', val='2')
        case.insert(act='Loop Begin', val='3')
        case.insert(act='Loop End', val=None)
        case.insert(act='Loop End', val=None)
        case.insert(act='Loop End', val=None)
        self.assertEqual(5, exe.loopEnd(0))
        self.assertEqual(4, exe.loopEnd(1))
        self.assertEqual(3, exe.loopEnd(2))
