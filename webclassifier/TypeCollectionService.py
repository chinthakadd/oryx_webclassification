'''
Created on Jul 23, 2013

@author: acer
'''

import pymongo
class TypeCollectionService():

    client = None
    hostcollection = None
    
    def __init__(self):
        self.client = pymongo.MongoClient("192.248.8.246:27017", 27017)
        self.hostcollection = self.client.OryX.HostCollection
        
        
    def InsertHostCollection(self,category):
        item={"type":category.name}
        self.hostcollection.save(item)    