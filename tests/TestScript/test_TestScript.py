import unittest
import os

from VisualScript.src.TestScript import TestScript
from VisualScript.src.TestScript.TestCase import TestCase

class TestScriptTestSuite(unittest.TestCase):
    def testAddCase(self):
        case1 = TestCase()
        case1.insert(act='Sleep(s)', val='0')
        name1 = "Case1"
        case2 = TestCase()
        name2 = "Case2"
        case2.insert(act='Set Text', val='Hello')
        script = TestScript()

        script.add(name1, case1)
        script.add(name2, case2)
        self.assertEqual(2, script.size())
        self.assertEqual('Sleep(s)', script.getCase(name1).getAction(0))
        self.assertEqual('Set Text', script.getCase(name2).getAction(0))

    def testModified(self):
        case1 = TestCase()
        case1.insert(act='Sleep(s)', val='0')
        name1 = "Case1"
        script = TestScript()
        script.add(name1, case1)

        changedData = {
            0: {
                'act': 'Sleep(s)',
                'val': '1'
            },
            1: {
                'act': 'Set Text',
                'val': 'Hello',
            },
        }
        script.modified(name1, changedData)

    def testLoad(self):
        path = './TestScript/Project/Suite/Case'
        script = TestScript()
        script.load(path)
        self.assertEqual('Sleep(s)', script.getCase(path).getAction(0))

    def testRunAll(self):
        path = './TestScript/Project/Suite/Case'
        script = TestScript()
        script.load(path)
        self.assertEqual('success',script.runAll())
