import unittest
import sys
sys.path.append('../src/TestCase')
from TestCase import TestCase
from TestStep import Step

class TestCaseTestSuite(unittest.TestCase):
    def testConstructer(self):
        case = TestCase(5)
        self.assertEqual(5, case.getSize())
        for i in range(0, case.getSize()):
            self.assertEqual('<class \'TestStep.Step\'>', str(case.getSteps(i).__class__))

    def testSetAction(self):
        case = TestCase(5)
        case.setAction(2, 'Click')
        self.assertEqual('Click', case.getSteps(2).getAction())

    def testSetValue(self):
        case = TestCase(5)
        case.setValue(2, 'KEYCODE_HOME')
        self.assertEqual('KEYCODE_HOME', case.getSteps(2).getValue())

    def testInsert(self):
        case = TestCase()
        step1 = Step()
        step1.setAction('Click')
        step2 = Step()
        step2.setAction('Sleep(s)')
        step3 = Step()
        step3.setAction('')
        case.insert(2, step3)
        case.insert(1, step2)
        case.insert(0, step1)
        self.assertEqual('Click', case.getSteps(0).getAction())
        self.assertEqual('Sleep(s)', case.getSteps(1).getAction())
        self.assertEqual('', case.getSteps(2).getAction())

    def testDelete(self):
        case = TestCase(5)
        case.delete(2)
        self.assertEqual(4, case.getSize())
        self.assertRaises(Exception, case.getSteps, 2)

    def testSetStatus(self):
        case = TestCase(5)
        self.assertEqual('Success', case.setStatus(2, 'Success'))

    def testGetStatus(self):
        case = TestCase(5)
        case.setStatus(2, 'Success')
        self.assertEqual('Success', case.getStatus(2))
