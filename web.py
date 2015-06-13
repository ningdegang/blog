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
        b = blog() 
        num, ret = b.get_all_articles()
        t, c = list(), list()
        if num > 0 :
            logging.error("ret : %s" % str(ret))
            for i in range(len(ret)):
                t.append(ret[i][2])
                c.append(ret[i][3])
            self.render('index.htm', titles=t, contexts=c)

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
    def get(self):
        title = self.get_argument("title")
        b = blog()
        num, ret = b.get_context_by_title(title)
        if num == 0 : return self.render("list.html", t="no suck articles", c = "There is something wrong with it")
        context = ret[0][0]
        self.render("list.html", t=title, c = context)

class RegisterHandler(BaseHandler):
    def get(self):
        self.render("register.html")
    def post(self):
        name = self.get_argument("username")
        passwd  = self.get_argument("passwd")
        b = blog()
        if( b.query_user("name") ) : return self.write("user exists")
        num, ret = b.RegisterUser(name, passwd)
        if num == 1 : return self.write("register sucess")
        self.write("register failed")
class CreateBlog(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("createblog.html")
    @tornado.web.authenticated
    def post(self):
        b = blog()
        author = self.get_current_user()
        title = self.get_argument("title")
        context =  self.get_argument("context")
        num , ret = b.save_blog(author, title, context)
        if num == 1: return self.write("create blog sucess")
        self.write("create blog failed") 

class MungedPageHandler(BaseHandler):
    def map_by_first_letter(self, text):
        mapped = dict()
        for line in text.split('\r\n'):
            for word in [x for x in line.split(' ') if len(x) > 0]:
                if word[0] not in mapped: mapped[word[0]] = []
                mapped[word[0]].append(word)
        return mapped

    def post(self):
        source_text = self.get_argument('source')
        text_to_change = self.get_argument('change')
        source_map = self.map_by_first_letter(source_text)
        change_lines = text_to_change.split('\r\n')
        self.render('munged.html', source_map=source_map, change_lines=change_lines, choice=random.choice)
if __name__ == '__main__':
    handlers = [
        (r'/', IndexHandler), 
        (r'/login', LoginHandler),
        (r'/logout', LogoutHandler),
        (r'/poem', MungedPageHandler),
        (r'/list', ListHandler),
        (r'/regist', RegisterHandler),
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
