'''
Created on Jun 22, 2013

@author: Dell
'''
import os.path
import tornado.ioloop
import tornado.web
import Util
from webclassifier import OryXdb
from webclassifier.UrlDocuments import URLDocument
from webclassifier import ClassfierFacade

import tornado.options
from tornado.options import define, options

define("port", default=5000, help="run on the given port", type=int)

urlCollection = OryXdb.UrlCollectionService()
classificationCollection = OryXdb.ClassificationCollectionService()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        l = self.get_arguments(Util.arg_type)
        href = l[0] if len(l)>0 else ""
        typeList = classificationCollection.getTagList(l)
        self.render(Util.template_name,items=typeList,bc=href,searchURL="",urldoc=None,model=None)
        
    def post(self):
        sURL = self.get_arguments("search")[0]
        self.render(Util.template_name,items=None,bc=None,searchURL=sURL,urldoc=urlCollection.getClassificationForURl(sURL),model = None)

class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        unamet = self.get_arguments("uname")[0]
        passwdt = self.get_arguments("pass")[0]
        self.render(Util.logintemplate_name,uname=unamet,passwd=passwdt) 
        
    def get(self):
        self.render(Util.logintemplate_name,uname="",passwd="")        
        
class APIHandler(tornado.web.RequestHandler):      
    def get(self):
        url = self.get_arguments("url")
        if len(url) is 0:
            self.write("Invalid key [url]")
        else:
            facade = ClassfierFacade.ClassifierFacade();
            self.set_header("Content-Type", "application/xml")
            self.render(Util.apitemplate_name,doc= facade.getURLDOCForURl(url[0])) #urlCollection.getClassificationForURl(url[0]))
            
class ListHandler(tornado.web.RequestHandler):      
    def get(self):
        type = self.get_arguments("type")
        if len(type) is 0:
            self.write("Invalid key [type]")
        tag = self.get_arguments("tag")
        if len(tag) is 0:
            self.write("Invalid key [tag]")
        else:
            facade = ClassfierFacade.ClassifierFacade();
            self.set_header("Content-Type", "application/xml")
            self.render(Util.listtemplate_name,urllist= urlCollection.getUrlListFromCol(type[0], tag[0], urlCollection.frontendcollection))
  

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", LoginHandler),
    (r"/api", APIHandler),
    (r"/list", ListHandler),
    (r'/detaillist/(.*)', tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), "template/urldetails")}),
    ],
        template_path=os.path.join(os.path.dirname(__file__), "template"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
    )

if __name__ == "__main__":
    application.listen(os.environ.get("PORT", 5000))
    print "server listening @ port "+str(options.port)
    tornado.ioloop.IOLoop.instance().start()
    
    
    
    
    
    
    