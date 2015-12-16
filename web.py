#!/usr/bin/env python
# char-set: utf-8
import os,sys
import random
import logging
import json

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

from comm import logic
from comm.logic import blog
from route import route

define("port", default=80, help="run on the given port", type=int)

def main():
    settings = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
    "xsrf_cookies": True,
    "login_url": "/login",
    "debug": False,
    }
    app = tornado.web.Application(
        handlers = route.handlers,
        **settings)
    #logic.deamon()
    #tornado.options.options.log_file_prefix = os.path.join(os.path.dirname(__file__), "log")+ "/access.log"
    tornado.options.parse_command_line()

    try:  
        http_server = tornado.httpserver.HTTPServer(app)
        if settings.get("debug"):
            http_server.listen(options.port)
        else:
            http_server.bind(options.port)
            http_server.start(num_processes=0) 
        tornado.ioloop.IOLoop.instance().start()
    except  KeyboardInterrupt as e:
        print "Exit By User From KeyboardInterrupt"
        sys.exit(-1)
    except Exception as e:
        print e
        sys.exit(-1)
    except AttributeError as e:
        sys.exit(-1)

if __name__ == '__main__':
    main()
