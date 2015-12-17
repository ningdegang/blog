#!/usr/bin/env python


import tornado.web
from model  import models
import json

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("sessionid")

class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        #self.render('boot.html')
        data = {"titles":list(), "contexts":list()}
        bb = models.Blog.objects(user= self.get_current_user())
        if bb.count() > 0:
            for b in bb :
                data["titles"].append(b.title)
                data["contexts"].append(b.content)
            self.render('index.htm', **data)
        else:
            self.write("<a href='/create'>you have no articles, try write new one!!! </a>")

class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.htm")
    def post(self):
        username, passwd = self.get_argument("username"), self.get_argument("passwd")
        user = models.User.query.filter_by(username= username).first()
        ret = dict()
        if user and user.username == username and user.password == passwd:
            self.set_secure_cookie("sessionid", self.get_argument("username"))
            ret["ret"] = 0
        else:
            ret["ret"] = -1
        self.write(json.dumps(ret))
            
            
    

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("sessionid")
        self.redirect("/")

class ListHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        title = self.get_argument("title")
        b = models.Blog.objects(user=self.get_current_user(), title = title).first()
        if not b: return self.redirect("/")
        self.write(b.content)

class RegisterHandler(BaseHandler):
    def get(self):
        act = self.get_argument("act", "NULL")
        if act == "NULL":
            self.render("register.html")
        else:
            name = self.get_argument("name", "NULL")
            b = models.User.query.filter_by(username= name)
            if b : return self.write("exists")
            self.write("not exist")
    def post(self):
        b = models.User()
        b.username = self.get_argument("username")
        b.password  = self.get_argument("passwd")
        with models.make_session() as session:
            session.add(b)
        self.write("success")
        #self.redirect("/login")
class CreateBlogHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("create.html")
    @tornado.web.authenticated
    def post(self):
        title = self.get_argument("title")
        context =  self.get_argument("context")
        #self.write("title: " + title+"<br>")
        #self.write("context: " + context+"<br>")
        #return 
        author = self.get_current_user()
        b = models.Blog()
        b.content = context
        b.title = title
        b.user = author
        b.save()
        return self.redirect("/")
class DelBlogHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        title = self.get_argument("title")
        b = models.Blog.objects(user = self.get_current_user(), title = title).first()
        if b : b.remove() 
        self.redirect("/")
class ModifyBlogHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        old_title = self.get_argument("old_title")
        new_title = self.get_argument("new_title")
        new_context = self.get_argument("new_context")
        b = models.Blog.objects(user = self.get_current_user(), title = old_title).first()
        b.title = new_title
        b.content = new_content
        b.update()
        self.redirect("/list?title='%s'" % new_title)
