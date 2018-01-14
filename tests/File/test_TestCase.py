import unittest
import os

from VisualScript.src.File.TestCase import TestCase

class TestCaseTestSuite(unittest.TestCase):
    def testConstructer(self):
        name = 'test'
        case = TestCase(name)
        self.assertEqual("<class 'VisualScript.src.File.TestCase.TestCase'>", str(case.__class__))
        self.assertEqual('test', case.name)
