'''
Created on Jan 20, 2014

@author: Anduril
'''

import unittest,sys
import ChorusGlobals,Utils
from TestSuiteManagement import TestSuiteManagement

class RunTest:
    def __init__(self):
        self.currunname=Utils.get_timestamp()
        self.init_testsuite()
        
    def init_testsuite(self):
        self.tsm = TestSuiteManagement()
#         self.allsuites, self.scope_info =self.tsm.GetTestSuites()