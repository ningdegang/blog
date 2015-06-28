import os.path
import random
import logging

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

from comm import logic
from comm.logic import blog

define("port", default=80, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("sessionid")

class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        #self.render('index.html')
        b = blog() 
        num, ret = b.get_all_articles(self.get_current_user())
        t, c = list(), list()
        if num > 0 :
            t = [x[0] for x in ret]
            c = [x[1] for x in ret]
            logging.info("titles: %s" % str(t))
            self.render('index.htm', titles=t, contexts=c)
        else:
            self.write("<a href='/create'>you have no articles, try write new one!!! </a>")

class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")
    def post(self):
        b = blog()  
        if b.VerifyUser(self.get_argument("username"), self.get_argument("passwd")):
            self.set_secure_cookie("sessionid", self.get_argument("username"))
            self.redirect("/")
        else:
            self.write("login failed")
            
    

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("sessionid")
        self.redirect("/")

class ListHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        title = self.get_argument("title")
        b = blog()
        num, ret = b.get_context_by_title(self.get_current_user(),title)
        if num == 0 : return self.redirect("/")
        context, ct ,author = ret[0][0], str(ret[0][1]), ret[0][2] 
        context = context.replace("\r\n", "<br>")
        tt = list()
        num ,ret = b.get_all_articles(self.get_current_user())
        if( num >0):
            tt = [t[0] for t in ret]
        self.render("list.html",titles=tt,  t=title, c = context, createtime = ct, au = author)

class RegisterHandler(BaseHandler):
    def get(self):
        self.render("register.html")
    def post(self):
        name = self.get_argument("username")
        passwd  = self.get_argument("passwd")
        b = blog()
        if( b.query_user("name") ) : return self.write("user exists")
        num, ret = b.RegisterUser(name, passwd)
        if num == 1 : return self.redirect("/login")
class CreateBlogHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("create.html")
    @tornado.web.authenticated
    def post(self):
        b = blog()
        author = self.get_current_user()
        title = self.get_argument("title")
        context =  self.get_argument("context").replace("\r\n", "<br>")
        num,ret= b.save_blog(author, title, context)
        if num == 1: return self.redirect("/")
        self.write("create blog failed") 
class DelBlogHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        b = blog()
        title = self.get_argument("title")
        b.del_blog(self.get_current_user(), title)
        self.redirect("/")
class ModifyBlogHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        b = blog()
        old_title = self.get_argument("old_title")
        new_title = self.get_argument("new_title")
        new_context = self.get_argument("new_context")
        b.update_blog(self.get_current_user(), old_title, new_title, new_context)
        self.redirect("/list?title='%s'" % new_title)
        
        

if __name__ == '__main__':
    handlers = [
        (r'/', IndexHandler), 
        (r'/login', LoginHandler),
        (r'/logout', LogoutHandler),
        (r'/list', ListHandler),
        (r'/regist', RegisterHandler),
        (r'/create', CreateBlogHandler),
        (r'/del', DelBlogHandler),
        (r'/update', ModifyBlogHandler),
    ]
    settings = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
    "xsrf_cookies": True,
    "login_url": "/login"
    }
    app = tornado.web.Application(
        handlers = handlers,
        debug=True,
        **settings)
    #logic.deamon()
    #tornado.options.options.log_file_prefix = os.path.join(os.path.dirname(__file__), "log")+ "/access.log"
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
