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

    def testSetAction(self):
        step = Step()
        self.assertRaisesRegex(Exception, 'Not an action', step.setAction, 'clik')

    def testSetValue(self):
        step = Step()
        step.setValue('KEYCODE_HOME')
        self.assertEqual('KEYCODE_HOME', step.getValue())
