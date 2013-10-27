import urllib2
from bs4 import BeautifulSoup
import urlparse
from external import getimageinfo
from urllib2 import HTTPError
import logging

def countImages(page_images, THRESHOLD):
    
    
    count = 0
    for uri in page_images:
        try:
            imgdata = urllib2.urlopen(uri)
        except Exception, e:
            print(">>>>>>>>"+ str(uri) +"<<<<<<<<")
            print(e)
            continue
        image_type,width,height = getimageinfo.getImageInfo(imgdata)        
        if(width>THRESHOLD or height>THRESHOLD):
            count += 1
    return count

def countImagesFromSite(siteurl, THRESHOLD):
    try:
        response = urllib2.urlopen(verifyUrl(siteurl))
    except:
        return 0        
    msg = response.read()
    soup = BeautifulSoup(msg)
                
    page_images = [image["src"] for image in soup.findAll("img")]
#     print(page_images)
    for x in range(0, len(page_images)):
        page_images[x] = urlparse.urljoin(siteurl, page_images[x])
    
    return countImages(page_images, THRESHOLD)

def verifyUrl(weblink):
    if not weblink.startswith('http://'):
        weblink = 'http://' + weblink 
    return weblink