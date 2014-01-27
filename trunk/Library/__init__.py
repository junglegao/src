'''
Created on Nov 8, 2013

@author: pli
'''
from ChorusCore.APIManagement import HTTP_API
from ChorusCore import Utils
import APIUtils

class Connector_API(HTTP_API):
    opendic={}
    def __init__(self,template,ignored_keys = None, header_keys = None):
        '''initialize API class'''
        HTTP_API.__init__(self, template,ignored_keys, header_keys)
        
#        '''pki enable, then enter pki=True'''
#        if Utils.GetConfig("CONNECTOR_VARS","pki_enable")=="True":
#            self.PreparePKI()
#            self.request.add_certificate( self.key_file, self.cert_file, None)
#        if Utils.GetConfig("CONNECTOR_VARS","proxy")=="True":
#            self.AddProxy()
        
        
    def PreparePKI(self):
        '''prepare PKI key and cert file'''
        self.key_file="filepath" #Utils.Getconfig("..","..")
        self.cert_file="filepath" #Utils.Getconfig("..","..")
        
    def CleanParameter(self):
        '''drop those parameter which value is Null from URL'''
        parameters=self.request.parameters
        for (key,value) in parameters.items():
            if value==None:
                del self.request.parameters[key]
        
    def Call_URL(self,checkstatus=True):
        '''Call current request url, and save its response to self.response, 
            if checkstatus, then it will raise exception when it doesn't lead to 200 OK
            if redirects, then the new url will be saved in redirect_url'''
        self.response=self.request.send()
        if checkstatus and self.response.response.status!="200 OK":
            print self.request.ShowURL(self.response.response.status)
            raise Exception("Server has errors")
        elif self.response.response.status=="404 Not Found":
            self.response.result["data"]={
                                            "error":"404 Common Error for invalid case",
                                            "error_generated":"From framework build-in Call URL Method"
                                          }
    
    def GetRedirectURL(self):
        '''return redirect_url, if non-redirect, then only return part of it, if redirect, then return full of it'''
        if self.response.response.headers["status"] in ["301","302","303"]:
            self.redirect_url=self.response.response.headers["location"]
            self.response.result["headers"]["location"]=self.response.response.headers["location"]
            
        elif self.response.response.headers["status"] in ["200"]:
            self.redirect_url=self.response.response.headers["content-location"]
            self.response.result["headers"]["content-location"]=APIUtils.ReplaceDomainURL(self.response.response.headers["content-location"])
        else:
            raise Exception("Cannot get redirect_url")
    
    def TransferNonjsonHTTP(self,data):
        '''change all < and >, make the response can be recognized from HTML report'''
        data=data.replace("<","&lt")
        data=data.replace(">","&gt")
        return data
    
    def Set_redirect_uri(self,redirect_uri,response_type):
        '''Set redirect parameter'''
        self.request.parameters["redirect_uri"]=redirect_uri
        self.request.parameters["response_type"]=response_type
        
    def Set_redirect_option(self,follow=True):
        '''set if request call redirect url'''
        self.request.follow_redirects=follow
        
    def Set_access_token(self,access_token):
        '''set access_token'''
        self.request.parameters["access_token"]=access_token
        
    def Set_client_id(self,client_id):
        '''set client_id'''
        self.request.parameters["client_id"]=client_id
        
    def AddProxy(self):
        '''add proxy from config file'''
        proxy=Utils.GetConfig("PROXY")
        if proxy:
            self.request.enable_proxy(proxy["host"],proxy["port"],proxy["type"])
        else:
            raise Exception("No proxy found")
    