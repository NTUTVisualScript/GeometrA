import unittest

import os
import sys
sys.path.append('../../src')

from File.TestSuite import TestSuite

class TestSuiteTestSuite(unittest.TestCase):
    def testConstructor(self):
        cases = ['test1', 'test2']
        suite = TestSuite(cases)
        self.assertEqual("<class 'File.TestSuite.TestSuite'>", str(suite.__class__))
        self.assertEqual('test1', suite.cases[0])
        self.assertEqual('test2', suite.cases[1])

    def testInsertList(self):
        cases1 = ['test1', 'test2']
        suite = TestSuite(cases1)
        cases2 = ['test3', 'test4']
        suite.insert(cases2)
        self.assertEqual(4, len(suite.cases))
        self.assertEqual('test3', suite.cases[2])
        self.assertEqual('test4', suite.cases[3])
    def testInsertListEmptyExcept(self):
        cases1 = ['test1', 'test2']
        suite = TestSuite(cases1)
        cases2 = ['', 'test3']
        self.assertRaisesRegex(Exception, 'Empty case name in the list!', suite.insert, cases2)
    def testInsertLIstExistExcept(self):
        cases1 = ['test1', 'test2']
        suite = TestSuite(cases1)
        cases2 = ['test3', 'test1']
        self.assertRaisesRegex(Exception, 'Case exist!', suite.insert, cases2)

    def testInsert(self):
        cases1 = ['test1', 'test2']
        suite = TestSuite(cases1)
        case = 'test3'
        suite.insert(case)
        self.assertEqual(3, len(suite.cases))
        self.assertEqual('test3', suite.cases[2])
    def testInsertEmptyExcept(self):
        cases1 = ['test1', 'test2']
        suite = TestSuite(cases1)
        case = ''
        self.assertRaisesRegex(Exception, 'Empty case name!', suite.insert, case)
    def testInsertExistExcept(self):
        cases1 = ['test1', 'test2']
        suite = TestSuite(cases1)
        case = 'test1'
        self.assertRaisesRegex(Exception, 'Case exist!', suite.insert, case)

    def testInsertExcept(self):
        cases1 = ['test1', 'test2']
        suite = TestSuite(cases1)
        self.assertRaisesRegex(Exception, 'Invalid case name', suite.insert, 1)

    def testDelete(self):
        cases1 = ['test1', 'test2']
        suite = TestSuite(cases1)
        case = 'test1'
        suite.delete(case)
        self.assertEqual(1, len(suite.cases))
        self.assertEqual('test2', suite.cases[0])
    def testDeleteExcept(self):
        cases1 = ['test1', 'test2']
        suite = TestSuite(cases1)
        case = 'test3'
        self.assertRaises(ValueError, suite.delete, case)

    def testRename(self):
        cases1 = ['test1', 'test2']
        suite = TestSuite(cases1)
        origin = 'test1'
        new = 'test3'
        suite.rename(origin, new)
        self.assertEqual(0, suite.cases.count(origin))
        self.assertEqual(2, len(suite.cases))
        self.assertEqual('test3', suite.cases[0])
    def testRenameExcept(self):
        cases1 = ['test1', 'test2']
        suite = TestSuite(cases1)
        origin = 'test3'
        new = 'test4'
        self.assertRaises(ValueError, suite.rename, origin, new)
