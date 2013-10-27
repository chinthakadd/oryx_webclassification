import re
import urllib2
import urlparse
from bs4 import BeautifulSoup, Comment
from urllib2 import URLError
import BlogAnalyser
import ImageAnalyzer

class FeatureFetch:
    IMAGE_THRESHOLD = 92
    BLOG = 'blog'
    LINK_REGEX = '<a\s*href=[\'|"](.*?)[\'"].*?>'
    
    def crawl(self, url):

        stats = {'paraCount':0,'smallParaCount':0,'wordCount':0,'imgCount':0,'largeImgCount':0,'internalLinks':0,'externalLinks':0,'hasMetaDis':False,'hasMetaKeywords':False,'hasBlogWordInMetaData':False,'hasCommentBox':False,'hasPostsArchive':False,'hasBlogWordInURL':False,'hasFeed':False}
        #with open('output/data/feature_set.xml', 'a') as featurefile:
            
                
        try:
                    response = urllib2.urlopen(url)
                    siteurl = response.geturl()
                                       
                    soup = BeautifulSoup(response.read())                    
                    
                    '''Remove Comments'''
                    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
                    [comment.extract() for comment in comments]
                    
                    '''Extract img tags'''
                    images = soup.findAll('img')
    #                 page_images = [image["src"] for image in images]
    #                 [img.extract() for img in images]
                    
                    '''Remove scripts,img,iframe and style tags'''
                    [s.extract() for s in soup(['script', 'img', 'iframe', 'style'])]
                    '''Extract <head>'''
                    head = soup.find('head')
                    head.extract()            
        #             print(head)
                    
                    '''Check "blog" in URL'''
                    stats['hasBlogWordInURL'] = self.checkURL(siteurl)
                    
                    '''Check for feed (rss, atom) links'''
                    stats['hasFeed'] = self.checkFeed(head)
                    
                    '''Check Metadata'''
                    stats['hasMetaDis'], stats['hasMetaKeywords'], stats['hasBlogWordInMetaData'] = self.checkMetaData(head)
                    
                    '''Count internal and external links'''
                    stats['internalLinks'], stats['externalLinks'] =self.countLinks(soup, siteurl)
                    
                    '''Check for comment section'''
                    stats['hasCommentBox'] = self.CheckCommentsSection(soup)
                    
                    '''Check for posts archive'''
                    stats['hasPostsArchive'] = BlogAnalyser.checkForArchiveList(soup)
                    
                    '''Count Words and Paragraphs'''
                    stats['paraCount'], stats['smallParaCount'], stats['wordCount'] = BlogAnalyser.countParaAndWord(soup)
                    
                    '''Count Images'''
    #                 stats['imgCount'], stats['largeImgCount'] = self.countImages(siteurl, page_images)
                    stats['imgCount'], stats['largeImgCount'] = self.countImages(siteurl, images)
                    
                    print(">>> fetched <<<")
                    
                    
              
        except Exception, err:
                    print(err)
                   
                
        return stats
                
                
        
    def checkMetaData(self, head):
        hasMetaDis = hasMetaKeywords = hasBlogWordInMetaData = False    
        description = head.find("meta", attrs={'name':re.compile("^description$", re.I)})
        keywords = head.find("meta", attrs={'name':re.compile("^keywords$", re.I)})
        if(description is not None):
            hasMetaDis = True
            hasBlogWordInMetaData = self.BLOG in description['content'].lower()
#             print(description)
#             print(hasBlogWordInMetaData)
        if(keywords is not None):
            hasMetaKeywords = True
            hasBlogWordInMetaData = hasBlogWordInMetaData or self.BLOG in keywords['content'].lower()
#             print(keywords)
#             print(hasBlogWordInMetaData)
        return hasMetaDis, hasMetaKeywords, hasBlogWordInMetaData            
       
#     def countImages(self, siteurl, page_images):
#         for x in range(0, len(page_images)):
#             page_images[x] = urlparse.urljoin(siteurl, page_images[x])
#         imgCount = len(page_images)
#         largeImgCount = ImageAnalyzer.countImages(page_images, self.IMAGE_THRESHOLD)
# #         print("Images: " +str(imgCount) + "Large Images: " + str(largeImgCount))
#         return imgCount, largeImgCount
    
    def countImages(self, siteurl, images):
#         print(images)
        imgCount = largeImgCount = 0
        page_images = list()
        for img in images:
            w = int(re.match(r'\d+', img.attrs['width']).group() if 'width' in img.attrs else -1)
            h = int(re.match(r'\d+', img.attrs['height']).group() if 'height' in img.attrs else -1)
#             print(str(w) )
            if(w > self.IMAGE_THRESHOLD or h > self.IMAGE_THRESHOLD):
                largeImgCount += 1
            elif(w < 0 or h < 0):
                page_images.append(urlparse.urljoin(siteurl, img['src']))
                
#         for x in range(0, len(page_images)):
#             page_images[x] = urlparse.urljoin(siteurl, page_images[x])
        imgCount = len(images)
        largeImgCount += ImageAnalyzer.countImages(page_images, self.IMAGE_THRESHOLD)
#         print("Images: " +str(imgCount) + "Large Images: " + str(largeImgCount))
        return imgCount, largeImgCount
    
    def checkURL(self, siteurl):
        return self.BLOG in siteurl
    
    def checkTitle(self, soup):
        tit = soup.find('title')
        if(tit is not None):
            return self.BLOG in tit.string.lower()
        return False
    
    def CheckCommentsSection(self, soup):
        elem = soup.findAll(attrs={"id" : "comment*"}) + soup.findAll(attrs={"class" : re.compile('comment*')})
        return True if(len(elem) > 0) else False
    
    def checkFeed(self, head):
        for feed in head.findAll("link"):
            if feed.has_key('type') and (feed["type"] == "application/rss+xml" or feed["type"] == "application/atom+xml") and feed.has_key('href') and not "/comments/" in feed['href']:
                return True
        return False
    
    def countLinks(self, soup, siteurl):
        intLinks = extLinks = 0
        basedomain = urlparse.urlparse(siteurl)[1]
        for link in soup.findAll('a'):
            if(link.has_attr('href')):
#                 print(link['href'])
                fulllink = urlparse.urljoin(siteurl, link['href'])
                linkdomain = urlparse.urlparse(fulllink)[1]
                if(basedomain == linkdomain):
                    intLinks += 1
                else:
                    extLinks += 1
        return intLinks, extLinks