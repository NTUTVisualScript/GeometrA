import unittest
import sys
sys.path.append('../src/TestCase')
from TestCase import TestCase

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
        case = TestCase(5)
        case.setValue(2, 'KEYCODE_HOME')
        case.insert(2)
        self.assertEqual(6, case.getSize())
        self.assertEqual('KEYCODE_HOME', case.getSteps(3).getValue())

    def testSetStatus(self):
        case = TestCase(5)
        self.assertEqual('Success', case.setStatus(2, 'Success'))

    def testGetStatus(self):
        case = TestCase(5)
        case.setStatus(2, 'Success')
        self.assertEqual('Success', case.getStatus(2))
