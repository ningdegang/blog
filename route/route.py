#!/usr/bin/env python

from views.views import *



handlers = [
        (r'/', IndexHandler), 
        (r'/login', LoginHandler),
        (r'/logout', LogoutHandler),
        (r'/list', ListHandler),
        (r'/regist', RegisterHandler),
        (r'/create', CreateBlogHandler),
        (r'/del', DelBlogHandler),
        (r'/update', ModifyBlogHandler),]
