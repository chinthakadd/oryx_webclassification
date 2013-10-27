'''
Created on Aug 13, 2013

@author: acer
'''

import pymongo

class TransformedCollectionService():

    client = None
    transformedcollection = None
    
    def __init__(self):
        self.client = pymongo.MongoClient("192.248.8.246:27017", 27017)
        self.transformedcollection = self.client.OryX.TransformedUrlCollection
        
        
    


    
    