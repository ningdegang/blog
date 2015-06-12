import os.path
import random
import logging

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

from comm import logic

define("port", default=8080, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("sessionid")

class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('index.htm', user=self.current_user)

class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")
    def post(self):
        if logic.verify(self.get_argument("username"), self.get_argument("passwd")):
            self.set_secure_cookie("sessionid", self.get_argument("username"))
            self.redirect("/")
        else:
            self.write("login failed")
            
    

class LogoutHandler(BaseHandler):
    def get(self):
        #if (self.get_argument("logout", None)):
        self.clear_cookie("sessionid")
        self.redirect("/")


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
    tornado.options.options.log_file_prefix = os.path.join(os.path.dirname(__file__), "log")+ "/access.log"
    tornado.options.parse_command_line()
    handlers = [
        (r'/', IndexHandler), 
        (r'/login', LoginHandler),
        (r'/logout', LogoutHandler),
        (r'/poem', MungedPageHandler),
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
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
