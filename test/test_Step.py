import unittest
import sys
sys.path.append('../src/TestCase/')
from TestStep import Step

class StepTestSuite(unittest.TestCase):
    def testConstructer(self):
        step = Step()
        self.assertEqual('', step.getAction())
        self.assertEqual('', step.getValue())

    def testSetAction(self):
        step = Step()
        step.setAction('Click')
        self.assertEqual('Click', step.getAction())
    def testSetActionExcept(self):
        step = Step()
        self.assertRaisesRegex(Exception, 'Not an action', step.setAction, 'clik')

    def testSetValue(self):
        step = Step()
        step.setValue('KEYCODE_HOME')
        self.assertEqual('KEYCODE_HOME', step.getValue())

    def testSetStatus(self):
        step = Step()
        self.assertEqual('Success', step.setStatus('Success'))
        self.assertEqual('Failed', step.setStatus('Failed'))
        self.assertEqual('Error', step.setStatus('Error'))
    def testSetStatusExcept(self):
        step = Step()
        self.assertRaisesRegex(Exception, 'setStatus Function Invalid Used Error', step.setStatus, 'Hello World')

    def testGetStatus(self):
        step = Step()
        step.setStatus('Success')
        self.assertEqual('Success', step.getStatus())
    def testGetStatusExcept(self):
        step = Step()
        self.assertRaisesRegex(Exception, 'Step Not Executed', step.getStatus)

    def testSetSequence(self):
        step = Step()
        self.assertEqual(0, step.setSequence(0))

    def testGetSequence(self):
        step = Step()
        step.setSequence(0)
        self.assertEqual(0, step.getSequence())
