#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
config ={
    "sqlalchemy":
    { 
        "url":"mysql+pymysql://root:root@localhost/blog?charset=utf8",
        "pool_size":10,
        "max_overflow": 20,
        "pool_recycle":600,
        "echo":0,
    }
}


settings = {
    "template_path": os.path.join(os.path.dirname(__file__), "../templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "../static"),
    "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
    "xsrf_cookies": True,
    "login_url": "/login",
    "debug": True,
    }
