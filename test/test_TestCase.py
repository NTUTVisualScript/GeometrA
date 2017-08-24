import unittest
import sys
sys.path.append('../src/TestCase')
from TestCase import TestCase
from TestStep import Step

class TestCaseTestSuite(unittest.TestCase):
    def testConstructer(self):
        case = TestCase()
        self.assertEqual(0, case.getSize())

    def testInsert(self):
        case = TestCase()
        case.insert(act='Click', val='./TestCase/Test/image/exist.png')
        case.insert(act='Sleep(s)', val='1')
        case.insert(n=0, act='Android Keycode', val='KEYCODE_HOME')
        case.insert(step=Step('Set Text', 'Hello World'))
        # self.assertEqual(4, case.getSize())
        self.assertEqual('Android Keycode', case.getSteps(0).getAction())
        self.assertEqual('Click', case.getSteps(1).getAction())
        self.assertEqual('Sleep(s)', case.getSteps(2).getAction())
        self.assertEqual('Set Text', case.getSteps(3).getAction())

    def testRefrash(self):
        case = TestCase()
        case.insert(act='Click', val='./TestCase/Test/image/exist.png')
        case.insert(act='Sleep(s)', val='1')
        case.insert(n=0, act='Android Keycode', val='KEYCODE_HOME')
        case.insert(n=5, step=Step('Set Text', 'Hello World'))
        case.refrash()
        self.assertEqual(4, case.getSize())
        self.assertEqual('Android Keycode', case.getSteps(0).getAction())
        self.assertEqual('Click', case.getSteps(1).getAction())
        self.assertEqual('Sleep(s)', case.getSteps(2).getAction())
        self.assertEqual('Set Text', case.getSteps(3).getAction())

    def testSetAction(self):
        case = TestCase()
        case.insert(act='Click', val='./TestCase/Test/iamge/exist.png')
        case.setAction(0, 'Sleep(s)')
        self.assertEqual('Sleep(s)', case.getSteps(0).getAction())

    def testSetValue(self):
        case = TestCase()
        case.insert(act='Android Keycode', val='KEYCODE_BACK')
        case.setValue(0, 'KEYCODE_HOME')
        self.assertEqual('KEYCODE_HOME', case.getSteps(0).getValue())

    def testSetStep(self):
        case = TestCase()
        case.insert(act='Sleep(s)', val='1')
        case.setStep(0, 'Set Text', 'Hello World')
        self.assertEqual('Set Text', case.getSteps(0).getAction())
        self.assertEqual('Hello World', case.getSteps(0).getValue())

    def testDelete(self):
        case = TestCase()
        case.insert(act='Android Keycode', val='KEYCODE_HOME')
        case.insert(act='Click', val='./TestCase/Test/image/exist.png')
        case.insert(act='Sleep(s)', val='1')
        case.delete(1)
        self.assertEqual(2, case.getSize())
        self.assertRaises(Exception, case.getSteps, 1)

    def testSetStatus(self):
        case = TestCase()
        case.insert(act='Click', val='./TestCase/Test/image/exist.png')
        self.assertEqual('Success', case.setStatus(0, 'Success'))

    def testGetStatus(self):
        case = TestCase()
        case.insert(act='Click', val='./TestCase/Test/image/exist.png')
        case.setStatus(0, 'Success')
        self.assertEqual('Success', case.getStatus(0))