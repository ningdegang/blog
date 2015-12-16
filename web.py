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
from config import config
from model import models

define("port", default=80, help="run on the given port", type=int)

def main():
    app = tornado.web.Application(
        handlers = route.handlers,
        **config.settings)
    #logic.deamon()
    #tornado.options.options.log_file_prefix = os.path.join(os.path.dirname(__file__), "log")+ "/access.log"
    tornado.options.parse_command_line()

    try:  
        models.init_db()
        http_server = tornado.httpserver.HTTPServer(app)
        if config.settings.get("debug"):
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
