'''
Created on Jun 23, 2013

@author: Dell
'''

import pymongo
import urlparse

    
client = pymongo.MongoClient("192.248.15.233", 27017)
db = client.OryX


class URLDoc():
    url = ""
    type = ""
    keywords = ""
    
    def __init__(self, uurl,ttype,kkey):
        self.url = uurl
        self.type = ttype
        self.keywords = kkey
        

def getTypeFromDB(urlS):
    
    if not urlS:
        return None
    url = urlparse.urlparse(urlS)
    if(url.hostname is None):
        return None
    ss = url.hostname.split('.')
    subdomain = ss[1]
    ud = URLDoc(urlS,"Could not find any classification","None") 
    for item in db.blogs.find():
        if(subdomain.lower() == item["host"].lower()):
            ud.type = item["type"]
            return ud
    return ud
   

