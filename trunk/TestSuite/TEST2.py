'''
Created on Nov 18, 2013

@author: pli
'''
from ChorusCore.TestSuiteManagement import MyTestCase
# from ChorusCore import TestScope

class TEST2(MyTestCase):
    
    @classmethod
    def setUpClass(cls):   
        super(TEST2,cls).setUpClass()
        
    def setUp(self):  
        MyTestCase.setUp(self)   
        
    def tearDown(self):       
        MyTestCase.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        super(TEST2,cls).tearDownClass()
        
#     @TestScope.setscope(TestScope.Scope.All)
    def testC03(self):
        
    def testC04(self):
        
