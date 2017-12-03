import unittest

import os, shutil
import sys
sys.path.append('../../src')

import subprocess

from File.TestSuite import TestSuite

class TestSuiteTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        shutil.rmtree('./Project1', True)

    def setUp(self):
        self.path = os.getcwd() + '/Project1/Suite1'
        shutil.copytree('./Project/Suite1', './Project1/Suite1')

    def tearDown(self):
        shutil.rmtree('./Project1', True)

    def testConstructor(self):
        cases = ['case1', 'case2']
        suite = TestSuite(cases, self.path)
        self.assertEqual("<class 'File.TestSuite.TestSuite'>", str(suite.__class__))
        self.assertEqual('case1', suite.cases[0])
        self.assertEqual('case2', suite.cases[1])

    def testConstructorNotExist(self):
        cases = ['case1', 'case']
        suite = TestSuite(cases, self.path)
        self.assertEqual("<class 'File.TestSuite.TestSuite'>", str(suite.__class__))
        self.assertEqual('case1', suite.cases[0])
        self.assertEqual(1, len(suite.cases))

    def testInsertList(self):
        cases1 = ['case1', 'case2']
        suite = TestSuite(cases1, self.path)
        cases2 = ['case3', 'case4']
        suite.insert(cases2)
        self.assertEqual(4, len(suite.cases))
        self.assertEqual('case3', suite.cases[2])
        self.assertEqual('case4', suite.cases[3])
    def testInsertListEmptyExcept(self):
        cases1 = ['case1', 'case2']
        suite = TestSuite(cases1, self.path)
        cases2 = ['', 'case3']
        self.assertRaisesRegex(Exception, 'Empty case name in the list!', suite.insert, cases2)
    def testInsertLIstExistExcept(self):
        cases1 = ['case1', 'case2']
        suite = TestSuite(cases1, self.path)
        cases2 = ['case3', 'case1']
        self.assertRaisesRegex(Exception, 'Case exist!', suite.insert, cases2)

    def testInsert(self):
        cases1 = ['case1', 'case2']
        suite = TestSuite(cases1, self.path)
        case = 'case3'
        suite.insert(case)
        self.assertEqual(3, len(suite.cases))
        self.assertEqual('case3', suite.cases[2])
    def testInsertEmptyExcept(self):
        cases1 = ['case1', 'case2']
        suite = TestSuite(cases1, self.path)
        case = ''
        self.assertRaisesRegex(Exception, 'Empty case name!', suite.insert, case)
    def testInsertExistExcept(self):
        cases1 = ['case1', 'case2']
        suite = TestSuite(cases1, self.path)
        case = 'case1'
        self.assertRaisesRegex(Exception, 'Case exist!', suite.insert, case)

    def testInsertExcept(self):
        cases1 = ['case1', 'case2']
        suite = TestSuite(cases1, self.path)
        self.assertRaisesRegex(Exception, 'Invalid case name', suite.insert, 1)

    def testDelete(self):
        cases1 = ['case1', 'case2']
        suite = TestSuite(cases1, self.path)
        case = 'case1'
        suite.delete(case)
        self.assertEqual(1, len(suite.cases))
        self.assertEqual('case2', suite.cases[0])
        self.assertFalse(os.path.isdir('./Project1/Suite1/case1'))
    def testDeleteExcept(self):
        cases1 = ['case1', 'case2']
        suite = TestSuite(cases1, self.path)
        case = 'case3'
        self.assertRaises(ValueError, suite.delete, case)

    def testRename(self):
        cases1 = ['case1', 'case2']
        suite = TestSuite(cases1, self.path)
        origin = 'case1'
        new = 'case3'
        suite.rename(origin, new)
        self.assertEqual(0, suite.cases.count(origin))
        self.assertEqual(2, len(suite.cases))
        self.assertEqual('case3', suite.cases[0])
        self.assertTrue(os.path.isdir('./Project1/Suite1/case3'))
        self.assertFalse(os.path.isdir('./Project1/Suite1/case1'))
    def testRenameExcept(self):
        cases = ['case1', 'case2']
        suite = TestSuite(cases, self.path)
        origin = 'case3'
        new = 'case4'
        self.assertRaises(ValueError, suite.rename, origin, new)
        self.assertTrue(os.path.isdir('./Project1/Suite1/case1'))
        self.assertTrue(os.path.isdir('./Project1/Suite1/case2'))
    def testRenameExistExcept(self):
        cases = ['case1', 'case2']
        suite = TestSuite(cases, self.path)
        origin = 'case1'
        new = 'case2'
        self.assertRaisesRegex(Exception, 'Case already exists', suite.rename, origin, new)
        self.assertListEqual(cases, suite.cases)


    def testGetTreeJSON(self):
        cases = ['case1', 'case2']
        result = [
            {"text": 'case1'},
            {"text": 'case2'}
        ]
        suite = TestSuite(cases, self.path)
        self.assertEqual(result, suite.getTreeJSON())
