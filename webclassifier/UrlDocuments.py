'''
Created on Aug 13, 2013

@author: acer

These are the entities which contain and represent the URL information
'''


#===============================================================================
# URLDocument
# This is the main document type
#===============================================================================
class URLDocument():
    url = None
    isFound = 0
    classification = None
    maintag = None
    tags = None
    
    def __init__(self,url,classitype,maintagitem,tagsArray):
        self.url=url
        self.classification=classitype
        self.maintag=maintagitem
        self.tags=tagsArray
        
        
        
#===============================================================================
# TransformedURL
# The transformed URL is stored once the transformation is completed
#===============================================================================
class TransformedURL(URLDocument):
    result =None
    
    def __init__(self,url,classitype,maintagitem,tagsArray, result):
        self.url=url
        self.classification=classitype
        self.maintag=maintagitem
        self.tags=tagsArray
        self.result=result
        
        
    