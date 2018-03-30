import unittest
import GeometrA

from GeometrA.src.TestScript.TestStep import Step

class StepTestSuite(unittest.TestCase):
    def setUp(self):
        GeometrA.app.testing = True
        self.app = GeometrA.app.test_client()

    def testConstructer(self):
        step = Step('Sleep(s)', '1')
        self.assertEqual('Sleep(s)', step.getAction())
        self.assertEqual('1', step.getValue())
    def testValueImageException(self):
        self.assertRaisesRegex(Exception, 'Value Should be PIL image', Step, 'Click', './TestCase/Test/image/exist.png')
        self.assertRaisesRegex(Exception, 'Value Should be PIL image', Step, 'Assert Exist', './TestCase/Test/image/exist.png')
        self.assertRaisesRegex(Exception, 'Value Should be PIL image', Step, 'Assert Not Exist', './TestCase/Test/image/notexist.png')
    def testValueDigitException(self):
        self.assertRaisesRegex(Exception, 'Value Should be digit', Step, 'Sleep(s)', 'Hello World')
        self.assertRaisesRegex(Exception, 'Value Should be digit', Step, 'Loop Begin', 'Hello World')
    def testKeycodeException(self):
        self.assertRaisesRegex(Exception, 'Value is not Android Keycode', Step, 'Android Keycode', 'Hello World')
        self.assertRaisesRegex(Exception, 'Value is not Android Keycode', Step, 'Android Keycode', 'Hello World')

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

    def testCopy(self):
        step1 = Step('Sleep(s)', '1')
        step2 = step1.copy()
        step1.setValue('2')
        self.assertEqual('Sleep(s)', step2.getAction())
        self.assertEqual('1', step2.getValue())
