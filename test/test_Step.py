import unittest
import sys
sys.path.append('../src/TestCase/')
from TestStep import Step

class StepTestSuite(unittest.TestCase):
    def testConstructer(self):
        step = Step('Sleep(s)', '1')
        self.assertEqual('Sleep(s)', step.getAction())
        self.assertEqual('1', step.getValue())

    def testSetAction(self):
        step = Step(act='Sleep(s)', val='1')
        step.setAction('Click')
        self.assertEqual('Click', step.getAction())
    def testSetActionExcept(self):
        step = Step(act='Sleep(s)', val='1')
        self.assertRaisesRegex(Exception, 'Not an action', step.setAction, 'clik')

    def testSetValue(self):
        step = Step('Android Keycode', 'KEYCODE_BACK')
        step.setValue('KEYCODE_HOME')
        self.assertEqual('KEYCODE_HOME', step.getValue())

    def testSetStatus(self):
        step = Step('Sleep(s)', '1')
        self.assertEqual('Success', step.setStatus('Success'))
        self.assertEqual('Failed', step.setStatus('Failed'))
        self.assertEqual('Error', step.setStatus('Error'))
    def testSetStatusExcept(self):
        step = Step('Sleep(s)', '1')
        self.assertRaisesRegex(Exception, 'setStatus Function Invalid Used Error', step.setStatus, 'Hello World')

    def testGetStatus(self):
        step = Step('Sleep(s)', '1')
        step.setStatus('Success')
        self.assertEqual('Success', step.getStatus())
    def testGetStatusExcept(self):
        step = Step('Sleep(s)', '1')
        self.assertRaisesRegex(Exception, 'Step Not Executed', step.getStatus)

    def testSetStep(self):
        step = Step('Sleep(s)', '1')
        step.setStep('Android Keycode', 'KEYCODE_HOME')
        self.assertEqual('Android Keycode', step.getAction())
        self.assertEqual('KEYCODE_HOME', step.getValue())
