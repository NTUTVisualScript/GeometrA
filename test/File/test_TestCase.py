import unittest
import os
import sys
sys.path.append('../../src')

from File.TestCase import TestCase

class TestCaseTestSuite(unittest.TestCase):
    def testConstructer(self):
        name = 'test'
        case = TestCase(name)
        self.assertEqual("<class 'File.TestCase.TestCase'>", str(case.__class__))
        self.assertEqual('test', case.name)
