'''
Created on Jun 13, 2013

@author: acer
'''


import pymongo
import urlparse
from collections import deque
import json
from UrlDocuments import URLDocument
#from MLTest import Predict

DB_URL = "192.248.15.233"
DB_PORT = 27017

#blogPredictor = Predict.Predict()

class UrlCollectionService():

    client = None
    #url collection is the main repository and frontend collection is for the ui categories.
    urlcollection = None
    frontendcollection = None
    
    def __init__(self):
        self.client = pymongo.MongoClient(DB_URL, DB_PORT)
        self.urlcollection = self.client.OryX.UrlCollection
        self.frontendcollection = self.client.OryX.FrontendCollection
        
    def getUrlCollection(self):
        return self.urlcollection
    
    def getFronendCollection(self):
        return self.frontendcollection
    
    def insertURLFromJson(self,jsonlist):
        for item in jsonlist:
            print item
            try:
                self.urlcollection.save(json.loads(item))
            except Exception,e:
                print e
        return True
    

    def insertURLDocument(self,urldoc):
        if(self.getUrlType(urldoc.url) is False):
            item={"url":urldoc.url,"classification":urldoc.classification, "maintag" : urldoc.maintag, "tags": urldoc.tags}
            self.urlcollection.save(item)
        else:
            print urldoc.url+" :Possible duplicate insert"
            
        
    def insertURLToCollection(self,urldoc, collection):
        if(self.getUrlType(urldoc.url) is False):
            item={"url":urldoc.url,"classification":urldoc.classification, "maintag" : urldoc.maintag, "tags": urldoc.tags}
            collection.save(item)
        else:
            print urldoc.url+" :Possible duplicate insert"
        
    def getUrlList(self,classification):
        urllist=list(self.urlcollection.find({"classification" : classification}))
        return urllist
    
    def getUrlListFromCol(self,classification, maintag, collection):
        urlss=deque()
        for item in collection.find({"classification" : classification, "maintag":maintag}):
            urlss.append(item["url"])
        return urlss
    
    def getUrlDocListFromCol(self,classification, maintag, collection):
        urllist=list(collection.find({"classification" : classification, "maintag":maintag}))
        
#         urldocList= deque()
#         for item in urllist:
#             urldoc= URLDocument(item["url"],item["classification"], item["maintag"], item["tags"])
#             urldocList.append(urldoc)
  
        return urllist
    
    def getUrlListByTag(self,classification,tag):
        urllist=self.urlcollection.find({"classification" : classification,"maintag":tag})
        return urllist
    
    def getUrlType(self,url):
        item=self.urlcollection.find_one({"url" : url})
        if item is None:
            return False
        return item["classification"]
    
    def getUrlTypeFromCol(self,url, collection):
        item=collection.find_one({"url" : url})
        return item["classification"]
    
    def getUrlDocument(self,url):
        item=self.urlcollection.find_one({"url" : url})
        if item is None:
            return None
        urldoc=URLDocument(item["url"],item["classification"],item["maintag"],item["tags"])
        urldoc.isFound = 1
        return urldoc    
    
    def getClassificationForURl(self,url):
        
        if not url:
            return None
        
        hostService = HostCollectionService()
        
        item = self.getUrlDocument(url)
        if item:
            return item
        else:
            classification=hostService.GetUrlClassifcation(url)
            
        if(classification is False):
            urldoc= URLDocument(url,"Could not find any classification","None","")
        else:
            urldoc= URLDocument(url,classification,"","")
            urldoc.isFound = 1
        
        return urldoc
    
    def getClassificationFromModel(self,url):
        if not url:
            return None
        #return blogPredictor.predictBlog(url)

    
import urlparse

class HostCollectionService():

    client = None
    hostcollection = None
    
    def __init__(self):
        self.client = pymongo.MongoClient(DB_URL, DB_PORT)
        self.hostcollection = self.client.OryX.HostCollection
        
    def InsertHostCollection(self,host):
        item={"domain":host.domain,"classification":host.classification, "name": host.name}
        self.hostcollection.save(item)
        
    def GetUrlClassifcation(self,url):
        url = urlparse.urlparse(url)

        urlparts = url.hostname.split('.')    

        if(urlparts != None):
            for item in urlparts:
                if(item == "www"): continue
                item=self.hostcollection.find_one({"domain": item})
                if(item!=None):
                    return item["classification"]
        
        return False

    def GetHost(self,url):
        url = urlparse.urlparse(url)
        subdomain = url.hostname.split('.')[1]
        hostObj= None
        if(subdomain != None):
            item=self.hostcollection.find_one({"domain": subdomain})["classification"]
            hostObj=Host(item["classification"], subdomain)
            hostObj.setName(item["name"])
            return hostObj
            
        return False
    
    
class ClassificationCollectionService():

    client = None
    classificationcollection = None
    urlColl = None
    
    def __init__(self):
        self.client = pymongo.MongoClient(DB_URL, DB_PORT)
        self.classificationcollection = self.client.OryX.UrlTypes
        self.urlColl = UrlCollectionService()

    def insertNew(self,name,tags):
        item={"classification":name, "tags" : tags}
        self.classificationcollection.save(item)
        
    def getClassTypes(self):
        types=deque()
        for item in self.classificationcollection.find():
            types.append(item["classification"])
        return types
    
    def getTags(self,classy):
        tags=deque()
        item = self.classificationcollection.find({"classification":classy})
        if item.count() == 0:
            return tags
        for i in item[0]["tags"]:
            tags.append(i)
        return tags
    
    def getURLs(self,args):
        urlss=deque()
        for item in self.urlColl.getUrlDocListFromCol(args[0], args[1],self.urlColl.frontendcollection):
            urlss.append(item["url"])
        return urlss;
    
    def getTagList(self,arglist):
        
        if len(arglist) <= 0:
            return self.getClassTypes()
        elif len(arglist) == 1:
            listt = arglist[0].split(",")
            if len(listt) == 1:
                return self.getTags(listt[0])
            elif len(listt) == 2:
                return self.getURLs(listt)

        return None

        
class Host():
    name = None
    domain = None
    classification = None
    
    def __init__(self, domain,classification, name=None):
        
        self.classification=classification
        self.domain=domain
        self.name=name
        
    def setName(self,name):
        self.name=name
        
class Category():
    name = None
    categories = None
        

    def __init__(self, domain,classification, name=None):
        self.classification=classification
        self.domain=domain
        self.name=name
