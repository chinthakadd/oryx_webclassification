'''
Created on Aug 13, 2013

@author: acer
'''

#===============================================================================
# Testing the service functionalities
#===============================================================================

from OryXdb import UrlCollectionService

if __name__ == '__main__':
    service =UrlCollectionService()
    
    print service.getUrlListFromCol("Blogs", "Business", service.frontendcollection)
                                            
    