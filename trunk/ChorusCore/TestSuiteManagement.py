'''
Created on Jan 25, 2014

@author: Anduril
'''
import Utils
import unittest
import inspect, sys
import time, copy
import ChorusGlobals
import os
import importlib

class TestSuiteManagement:
    '''
    Entry in charge of test suite management: get test suite, run test suite  
    '''
#     testsuites={}
    baselinepath = None
    TESTSUITE_FOLDER = "TestSuite"
    scopes = ["all"]
    
    def __init__(self):
        self.logger = ChorusGlobals.get_logger()
        self.suiteinfo = ChorusGlobals.get_suiteinfo()
        self.set_baselinepath()
        self.suite_dict = self.get_test_mapping()
        self.filter_test_mapping()
        self.set_scope()
        self.get_testsuites()
#         self.testsuites = {"Suite":self.suite_dict,"Baseline":self.baselinepath}
    
    def get_testsuites(self, sortflag=True):
        alltestsuites=unittest.TestSuite()
        scope_cfg_info = {}
        suite_resource_info = {}
        
        suite_list = sorted(self.suite_dict.keys()) if sortflag else self.suite_dict.keys()
        for suitename in suite_list:
            case_list = sorted(self.suite_dict[suitename])
            suite_module = importlib.import_module("%s.%s" % (self.TESTSUITE_FOLDER, suitename))
        
        
    def set_scope(self):
        if self.suiteinfo.has_key("scope") and self.suiteinfo["scope"]:
            self.scopes=[]
            for item in self.suiteinfo["scope"].split(','):
                self.scopes.append(item.strip().lower())
    
    def filter_test_mapping(self):
        self.filter_include_testsuites()
        self.filter_exclude_testsuites()
        self.filter_include_testcases()
        self.filter_exclude_testcases()
        for insuite in self.suite_dict:
            if len(self.suite_dict[insuite])>0:
                self.logger.info("include testsuite %s cases: %s" % (insuite, ",".join(self.suite_dict[insuite])))
   
    def set_baselinepath(self):
        if self.suiteinfo.has_key("baseline"):
            self.baselinepath = self.suiteinfo["baseline"]
    
    def get_test_mapping(self):
        suites_path = Utils.get_filestr([self.TESTSUITE_FOLDER], "")
        suites_filelist = os.listdir(suites_path)
        suites_dict={}
        for suite_file in suites_filelist:
            if suite_file.endswith(".py"):
                suite_name = suite_file[0:suite_file.rfind('.')]
                case_dict = Utils.class_browser("%s.%s" % (self.TESTSUITE_FOLDER,suite_name))
                if case_dict:
                    case_list = []
                    for case in case_dict[suite_name].methods:
                        if case[0:4] == 'test':
                            case_list.append(case)
                    suites_dict[suite_name]=case_list
        return suites_dict

    def filter_include_testsuites(self):
        include_testsuites = []
        if self.suiteinfo.has_key("include_testsuite"):
            include_testsuites = self.suiteinfo["include_testsuite"].split(",")
        if len(include_testsuites)>0:
            origin_suite_dict=Utils.create_entity(self.suite_dict)
            self.suite_dict.clear()
            nomatchsuite = []
            for insuite in include_testsuites:
                if origin_suite_dict.has_key(insuite):
                    self.suite_dict[insuite]=origin_suite_dict[insuite]            
                else:
                    nomatchsuite.append(insuite)
            self.logger.info("include test suites: %s" % ",".join(self.suite_dict.keys()))
            if len(nomatchsuite)!=0:
                self.logger.debug("following include suites: %s are not matched with any suite" % ",".join(nomatchsuite))
        else:
            self.logger.debug("All test suites to be included in configuration")
    
    def filter_exclude_testsuites(self):
        exclude_testsuites = []
        if self.suiteinfo.has_key("exclude_testsuite"):
            exclude_testsuites = self.suiteinfo["exclude_testsuite"].split(",")
        if len(exclude_testsuites)>0:
            nomatchsuite = []
            matchsuite = []
            for exsuite in exclude_testsuites:
                if exsuite in self.suite_dict.keys():
                    del self.suite_dict[exsuite]
                    matchsuite.append(exsuite)
                else:
                    nomatchsuite.append(exsuite)
            if len(matchsuite)>0:
                self.logger.debug("skip test suites: %s" % ",".join(matchsuite))
            if len(nomatchsuite)!=0:
                self.logger.debug("exlude suite: %s not find " % ",".join(nomatchsuite))
    
    def filter_include_testcases(self):
        include_testcases = []
        if self.suiteinfo.has_key("include_testcase"):
            include_testcases = self.suiteinfo["include_testcase"].split(",")
        if len(include_testcases)>0:
            origin_suite_dict=Utils.create_entity(self.suite_dict)
            for insuite in self.suite_dict:
                self.suite_dict[insuite]=[]
            nomatchcase = Utils.create_entity(include_testcases)
            for insuite in origin_suite_dict:
                for incase in origin_suite_dict[insuite]:
                    if incase in include_testcases:
                        self.suite_dict[insuite].append(incase)
                        if incase in nomatchcase:
                            nomatchcase.remove(incase)
            if len(nomatchcase)!=0:
                self.logger.debug("following include cases: %s are not matched with any case" % ",".join(nomatchcase))
    
    def filter_exclude_testcases(self):
        exclude_testcases = []
        if self.suiteinfo.has_key("exclude_testcase"):
            exclude_testcases = self.suiteinfo["exclude_testcase"].split(",")
        if len(exclude_testcases)>0:
            nomatchcase = Utils.create_entity(exclude_testcases)
            for excase in exclude_testcases:
                for insuite in self.suite_dict:
                    if excase in self.suite_dict[insuite]:
                        self.suite_dict[insuite].remove(excase)
                        if excase in nomatchcase:
                            nomatchcase.remove(excase)   
            if len(nomatchcase)!=0:
                self.logger.debug("following exclude cases: %s are not matched with any case" % ",".join(nomatchcase))
    
    
class MyTestCase(unittest.TestCase):
    '''
    Inherit from python's unittest.TestCase
    override the setUp, setUpClass, tearDown, tearDownClass methold    
    '''
    def __init__(self, methodName):
        unittest.TestCase.__init__(self, methodName)     
        if hasattr(getattr(self, methodName), '_scopes'):          
            self.scopes = getattr(self, methodName)._scopes
        else:
            self.scopes = ["all"]
        self.executed_cases = []
        
    def setUp(self):
        '''
        setUp is executed every time before run a test case
        you can do some initial work here
        '''
        self.startTime = time.time()
        unittest.TestCase.setUp(self)
        
    @classmethod
    def setUpClass(cls):        
        '''
        setUpClass is executed every time before run a test suite
        '''
        super(MyTestCase,cls).setUpClass()
        
    def tearDown(self):
        '''
        tear down is executed after each case has finished, 
        you can do some clean work here, including
        1.check if crash happens, 
        2.analyze failed/passed actions, 
        3.store the case level test result 
        '''
        unittest.TestCase.tearDown(self)
#         rm = ReportManagement()
        self.endTime = time.time()
    
    @classmethod
    def tearDownClass(cls): 
        '''
        tearDownClass is executed after each suite has finished, 
        you can do some clean work here, including
        1.generate baseline, 
        '''      
        super(MyTestCase,cls).tearDownClass()