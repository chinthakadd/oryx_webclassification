import Orange, cPickle
from FeatureFetch import FeatureFetch
import math

class Predict:
    
    def predictBlog(self,urlpassed):
        url = urlpassed
        b = FeatureFetch()
        features = b.crawl(url)
        print features
        
        siteinfoo = [features['hasPostsArchive'], features['paraCount'], features['externalLinks'], features['smallParaCount'], features['internalLinks'], features['hasMetaDis'], features['hasMetaKeywords'], features['hasFeed'], features['imgCount'], features['wordCount'], features['hasBlogWordInMetaData'], features['largeImgCount'], features['hasBlogWordInURL'] ]
        hasPostsArchive = features['hasPostsArchive']
        paraCount = features['paraCount']
        hasCommentBox = features['paraCount']
        externalLinks = features['hasCommentBox']
        smallParaCount = features['smallParaCount']
        internalLink = features['internalLinks']
        hasMetaDis = features['hasMetaDis'] 
        hasMetaKeywords = features['hasMetaKeywords']
        hasFeed = features['hasFeed']   
        imgCount = features['imgCount'] 
        wordCount = features['wordCount']
        hasBlogWordInMetaData = features['hasBlogWordInMetaData']
        largeImgCount = features['largeImgCount']
        hasBlogWordInURL = features['hasBlogWordInURL']

#print siteinfoo
        classifier = cPickle.load(open('MLTest/oryx1.pck'))

        print 'predictions:'


        oryx = Orange.data.Table("MLTest/dataset.csv")
#print oryx.domain.features
#print "Attributes:", ", ".join(x for x in oryx.domain.features)
        domain = oryx.domain
        inst = Orange.data.Instance(domain,[features['hasPostsArchive'], features['paraCount'], features['hasCommentBox'], features['externalLinks'], features['smallParaCount'], features['internalLinks'], features['hasMetaDis'], features['hasMetaKeywords'], features['hasFeed'], features['imgCount'], features['wordCount'], features['hasBlogWordInMetaData'], features['largeImgCount'], features['hasBlogWordInURL'], None ])

#inst = Orange.data.Instance(domain, ['False', 3, 'False', 23, 64, 119, 'False', 'False', 'True', 32, 1175, 'False', 14, 'False', 'NonBlogs'])
        print "Start: "+ urlpassed
        prediction = classifier(inst,result_type=2)
        print "Type: " + prediction[0].value
        typee = prediction[0].value
        pro = prediction[1][0]
        if(typee == "NonBlogs") :
            pro = prediction[1][1]
        print "Probability: " 
        print prediction[1][0]
        print "End"
        
        r = Results(urlpassed, typee,pro)
        return r


class Results():
    
    type =""
    prob = ""
    url = ""
    
    def __init__(self,url, typee,pr):
        
        prrr = str(pr*100)+" %"
        self.prob = prrr
        self.type = typee
        self.url = url
