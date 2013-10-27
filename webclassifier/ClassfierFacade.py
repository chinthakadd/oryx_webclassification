'''
Created on Jul 23, 2013

@author: acer
'''

from webclassifier.OryXdb import HostCollectionService,UrlCollectionService
from TypeCollectionService import TypeCollectionService
from UrlDocuments import URLDocument

class ClassifierFacade(object):
    '''
    separate concerns between the frontend requests and data layer
    '''

    host_dbservice = None
    type_dbservice = None
    url_dbservice = None
    
    def __init__(self):
        self.host_dbservice = HostCollectionService()
        self.type_dbservice = TypeCollectionService()
        self.url_dbservice = UrlCollectionService()
    
    
    def getClassification(self,url):
        
        return self.host_dbservice.GetUrlClassifcation(url)
        
        
    def getClassificationForURl(self,url):
        
        classification=self.host_dbservice.GetUrlClassifcation(url)
        
        urldoc=False
        
        if(classification is False):
            classification=self.url_dbservice.getUrlDocument(url).classification
    
#------------------------------------------------------------------------------ 
#Connect the orange DB here
#------------------------------------------------------------------------------ 
        
        return classification
        
    def getURLDOCForURl(self,url):
        
        if not url:
            return None
        
        item = self.url_dbservice.getUrlDocument(url)
        if item:
            
            return item
        else:
            classification=self.host_dbservice.GetUrlClassifcation(url)
        if(classification is False):
            urldoc= URLDocument(url,"Could not find any classification","None","")
        else:
            urldoc= URLDocument(url,classification,"","")
            urldoc.isFound = 1
        
        return urldoc
     
        
        
    
    
        