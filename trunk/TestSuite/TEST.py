'''
Created on Nov 18, 2013

@author: pli
'''
from ChorusCore.TestSuiteManagement import MyTestCase
# from ChorusCore import TestScope

class TEST(MyTestCase):
    
    @classmethod
    def setUpClass(cls):   
        super(TEST,cls).setUpClass()
        
    def setUp(self):  
        MyTestCase.setUp(self)   
        
    def tearDown(self):       
        MyTestCase.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        super(TEST,cls).tearDownClass()
        
#     @TestScope.setscope(TestScope.Scope.All)
    def testC01(self):
        
#         self.assertEqualOnFly("compare2", data1, data2)
#         self.assertEqual("compare1", data1)
        
    def testC02(self):
        
#         self.assertEqualOnFly("compare2", data1, data2)
#         self.assertEqual("compare1", data1)
