#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random
import string
from datetime import datetime, timedelta
from contextlib import contextmanager
from sqlalchemy import create_engine, Table, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy import String, Integer, DateTime, TIMESTAMP, BigInteger, Float

import sys 
sys.path.append("..")
from config.config import config

class Query(object):
    def __get__(self, obj, objtype):
        if Session : return Session().query(objtype)
        return None

class Base(object):
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    query = Query()

Base = declarative_base(cls=Base)
Session = None

class User(Base):
    __tablename__ = 'user'
    username = Column(String(50), unique=True, nullable=False)
    password = Column('password', String(255), nullable=False)

def init_db():
    engine = create_engine(
        config['sqlalchemy']['url'],
        encoding='utf-8',
        pool_size =config['sqlalchemy']['pool_size'],
        max_overflow = config['sqlalchemy']['max_overflow'],
        pool_recycle = config['sqlalchemy']['pool_recycle'],
        echo = config['sqlalchemy']['echo']
    )
    global Base, Session
    Base.metadata.bind = engine
    Session = sessionmaker(bind=engine)
    return engine


from mongoengine import connect, Document, IntField, StringField, DateTimeField

connect("blog", host="localhost", port=27017)

class Blog(Document):
    create_time = DateTimeField()
    modify_time = DateTimeField()
    content = StringField()

@contextmanager
def make_session():
    global Session
    if Session: session =Session(); yield session
    else:
        engine = init_db()
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session
    session.commit()
    


def test():
    engine = init_db()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    degang = User()
    degang.username = "degang"
    degang.password = "test"
    with make_session() as session:
        session.add(degang)
    qu = User.query
    print qu, type(qu), dir(qu)
    users = User.query.filter_by(username="degang")
    b = Blog()
    b.content= "asdfaf"
    b.save()
    bb = Blog.objects()
    for b in bb :
        print b.content

if __name__ == "__main__":
    test()
