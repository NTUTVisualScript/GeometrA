import unittest
import sys
sys.path.append('../src')
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

    def testRunNone(self):
        case = TestCase(5)
        exe = Executor(case)
        self.assertEqual(None, exe.run(2))

    def testRunClick(self):
        case = TestCase(5)
        case.setAction(2, 'Click')
        case.setValue(2, 'Image')
        exe = Executor(case)
        self.assertEqual('Success', exe.run(2))

    def testRunDrag(self):
        case = TestCase(5)
        case.setAction(2, 'Drag')
        case.setValue(2, 'x=2, y=3, x=4, y=3')
        exe = Executor(case)
        self.assertEqual('Success', exe.run(2))

    def testRunSetText(self):
        case = TestCase(5)
        case.setAction(2, 'Set Text')
        case.setValue(2, 'Hello World')
        exe = Executor(case)
        self.assertEqual('Success', exe.run(2))

    def testRunTestCase(self):
        case = TestCase(5)
        case.setAction(2, 'TestCase')
        case.setValue(2, 'C:/test')
        exe = Executor(case)
        self.assertEqual('Success', exe.run(2))
        
