from tests import *
import unittest
import xmlrunner
import sys
import os

if __name__ == "__main__":
    with open('testReport.xml', 'wb') as report:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=report),
            failfast=False, buffer=False, catchbreak=False)
