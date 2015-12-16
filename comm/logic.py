import os, sys
import logging
import MySQLdb

def verify(name, pwd):
        return True

class mysql():
    def __init__(self, vhost='localhost', vuser='root', vpasswd='root', vdb='blog', vport=3306):
        self.host, self.user, self.passwd,self.db, self.port = vhost, vuser, vpasswd,vdb, vport
        self.flag = False
    def __del__(self):
        if hasattr(self, "cur") : self.cur.close()
        if hasattr(self, "conn"): self.conn.commit();self.conn.close()
    def init(self):
        self.conn=MySQLdb.connect(self.host,self.user,self.passwd,self.db,self.port)
        self.cur=self.conn.cursor()
        self.flag = True
    def escape(self, *var):
        return (MySQLdb.escape_string(v) for v in var)
    def query(self, sql):
        if( not self.flag):self.init()
        logging.info("sql: %s" % sql)
        try:
            num = self.cur.execute(sql);
        except Exception, r:
            self.init()
            logging.error("exec %s  failed, reason:%s" % (sql, str(r)))
            return 0, None
        self.conn.commit()
        logging.debug("total db action: %d rows" % num)
        if num == 0: return num, None
        results = self.cur.fetchall()
        logging.debug("fetch all return: %s" % str(results))
        return num,results
        

class blog:
    db = mysql() 
    def save_blog(self, author, title, context):
        author, title, context = blog.db.escape(author, title, context)
        return blog.db.query("insert into articles (author, title, context) values ('%s', '%s', '%s');" % (author, title, context))
    def update_blog(self,old_title, old_context, new_title, new_context, author):
        old_title, old_context, new_title, new_context, author = blog.db.escape(old_title, old_context, new_title, new_context, author)
        return blog.db.query("update articles set ( title, context) values ('%s', '%s') where title='%s' and context='%s' and author='%s' ;" % (new_title, new_context, old_title,old_context,author))

    def del_blog(self, author, title):
        author, title = blog.db.escape(author, title)
        return blog.db.query("delete from articles where author='%s' and title='%s';" % (author, title))

    def get_all_titles(self, author):
        author, = blog.db.escape(author)
        return blog.db.query("select title from articles where author='%s';" % author)
        
    def get_context_by_title(self, author, title):
        author, title = blog.db.escape(author, title)
        return blog.db.query("select context, createtime,author from articles where author='%s' and title = '%s'; " % (author,title))

    def get_all_articles(self, author):
        author, = blog.db.escape(author)
        return blog.db.query("select title, context from articles where author='%s' ;" % author)

    def query_user(self,name):
        name, = blog.db.escape(name)
        num, ret = blog.db.query("select user from user where user ='%s';" % name)
        if num == 1 : return True;
        return False

    def RegisterUser(self, name, passwd):
        name, passwd = blog.db.escape(name, passwd)
        return blog.db.query("insert into user ( user, passwd) values ('%s', '%s');" % (name, passwd))
        
        
    def VerifyUser(self, user, passwd):
        user, passwd = blog.db.escape(user, passwd)
        num ,ret = blog.db.query("select passwd from user where user='%s'; " % user)
        if(num == 0): return {"ret":-1, "msg":"Invalid User"}
        logging.info("passwd from web:%s, passw from db:%s" % (passwd,str(ret[0][0])))
        if str(ret[0][0]) == passwd: return {"ret":0, "msg":"OK"}
        return {"ret":-1, "msg":"Invalid passwd"}
        
