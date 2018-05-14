import unittest

from GeometrA.src.Node import Node
from pprint import pprint

class NodeTestSuite(unittest.TestCase):
    def testXML(self):
        n = Node()
        xml = n.export()
        n.treeInfo(xml)
        pprint(n.nodes)
        # self.assertEqual('', xml)
