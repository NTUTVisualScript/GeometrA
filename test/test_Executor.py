import unittest
import sys
sys.path.append('../src/TestCase')
sys.path.append('../src')
sys.path.append('../src/Save')
from Executor import Executor
from TestStep import Step
from TestCase import TestCase

class ExecutorTestSuite(unittest.TestCase):
    def testConstructer(self):
        case = TestCase(5)
        exe = Executor(case)
        self.assertEqual('<class \'TestCase.TestCase\'>', str(exe.case.__class__))

    def testConstructerExcept(self):
        step = Step()
        self.assertRaisesRegex(Exception, 'Not a executable case', Executor, step)

    def testExecuteNone(self):
        case = TestCase(5)
        exe = Executor(case)
        self.assertEqual('Success', exe.execute(2))

    def testExecuteClick(self):
        case = TestCase(5)
        case.setAction(2, 'Click')
        case.setValue(2, 'Image')
        exe = Executor(case)
        self.assertEqual('Success', exe.execute(2))

    def testExecuteDrag(self):
        case = TestCase(5)
        case.setAction(2, 'Drag')
        case.setValue(2, 'x=2, y=3, x=4, y=3')
        exe = Executor(case)
        self.assertEqual('Success', exe.execute(2))
    def testExecuteDragExcept(self):
        case = TestCase(5)
        case.setAction(2, 'Drag')
        case.setValue(2, 'x=, y=3, x=4, y=3')
        exe = Executor(case)
        self.assertEqual('Error', exe.execute(2))

    def testExecuteSetText(self):
        case = TestCase(5)
        case.setAction(2, 'Set Text')
        case.setValue(2, 'Hello World')
        exe = Executor(case)
        self.assertEqual('Success', exe.execute(2))

    def testExecuteTestCase(self):
        case = TestCase(5)
        case.setAction(2, 'TestCase')
        case.setValue(2, 'C:/test')     # We need to put a sample TestCase in the path
        exe = Executor(case)
        self.assertEqual('Success', exe.execute(2))
    def testExecuteTestCaseExcept(self):
        case = TestCase(5)
        case.setAction(2, 'TestCase')
        case.setValue(2, 'D:/test')
        exe = Executor(case)
        self.assertEqual('Error', exe.execute(2))

    def testExecuteSleep(self):
        case = TestCase(5)
        case.setAction(2, 'Sleep(s)')
        case.setValue(2, '0')
        exe = Executor(case)
        self.assertEqual('Success', exe.execute(2))
    def testExecuteSleepExcept(self):
        case = TestCase(5)
        case.setAction(2, 'Sleep(s)')
        case.setValue(2, 'Hello World')
        exe = Executor(case)
        self.assertEqual('Error', exe.execute(2))

    def testExecuteAndroidKeycode(self):
        case = TestCase(5)
        case.setAction(2, 'Android Keycode')
        case.setValue(2, 'KEYCODE_HOME')
        exe = Executor(case)
        self.assertEqual('Success', exe.execute(2))
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
        case = TestCase(5)
        case.setAction(2, 'Assert Exist')
        case.setValue(2, 'Image')
        exe = Executor(case)
        self.assertEqual('Success', exe.execute(2))

    def testExecuteAssertNotExist(self):
        case = TestCase(5)
        case.setAction(2, 'Assert Not Exist')
        case.setValue(2, 'Disappeared image')
        exe = Executor(case)
        self.assertEqual('Success', exe.execute(2))

    def testRun(self):
        case = TestCase(5)
        case.setAction(2, 'Sleep(s)')
        case.setValue(2, '0')
        exe = Executor(case)
        self.assertEqual(True, exe.run(2))

    def testStepResult(self):
        case = TestCase(5)
        case.setStatus(0, True)
        case.setStatus(1, False)
        exe = Executor(case)
        self.assertEqual('Action 1 Success', exe.stepResult(0))
        self.assertEqual('Action 2 Failed', exe.stepResult(1))

    def testRunAll(self):
        case = TestCase(5)
        case.setAction(1, 'Android Keycode')
        case.setValue(1, 'KEYCODE_HOME')
        case.setAction(2, 'Sleep(s)')
        case.setValue(2, '0')
        case.setAction(4, 'TestCase')
        case.setValue(4, 'C:/test')
        exe = Executor(case)
        self.assertEqual(True, exe.runAll())
    def testRunAll(self):
        case = TestCase(5)
        case.setAction(0, 'Android Keycode')
        case.setValue(0, 'KEYCODE_HOME')
        case.setAction(1, 'Sleep(s)')
        case.setValue(1, 'Hello World')
        case.setAction(2, 'Sleep(s)')
        case.setValue(2, '3')
        exe = Executor(case)
        self.assertEqual(False, exe.runAll())
