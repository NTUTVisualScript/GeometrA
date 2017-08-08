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

    # def testInsert_1(self):
    #     case = TestCase()
    #     case.insert()
    #     self.assertEqual(1, case.getSize())
    def testInsert(self):
        case = TestCase()
        step1 = Step()
        step1.setSequence(0)
        step2 = Step()
        step2.setSequence(2)
        step3 = Step()
        step3.setSequence(4)
        case.insert(step3)
        case.insert(step2)
        case.insert(step1)
        self.assertEqual(0, case.getSteps(0).getSequence())
        self.assertEqual(2, case.getSteps(1).getSequence())
        self.assertEqual(4, case.getSteps(2).getSequence())
    # def testInsertException(self):
    #     case = TestCase(2)
    #     self.assertRaisesRegex(Exception, 'Input Out Of Range', case.insert, 3)

    def testDelete(self):
        case = TestCase(5)
        case.setValue(2, 'KEYCODE_HOME')
        case.setValue(3, '1')
        case.delete(2)
        self.assertEqual(4, case.getSize())
        self.assertEqual('1', case.getSteps(2).getValue())

    def testSetStatus(self):
        case = TestCase(5)
        self.assertEqual('Success', case.setStatus(2, 'Success'))

    def testGetStatus(self):
        case = TestCase(5)
        case.setStatus(2, 'Success')
        self.assertEqual('Success', case.getStatus(2))
