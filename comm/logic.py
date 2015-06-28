import os, sys
import logging
import MySQLdb
def verify(name, pwd):
        return True


def deamon():
    pid = os.fork()
    if pid > 0:
        sys.exit(0)
    #os.chdir("/")
    os.setsid()
    os.umask(0)
    pid = os.fork()
    if pid > 0:
        sys.exit(0)
    sys.stdout.flush()
    sys.stderr.flush()
    si = file("/dev/null", 'r')
    so = file("/dev/null", 'a+')
    se = file("/dev/null", 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

class mysql():
    def __init__(self, vhost='localhost', vuser='root', vpasswd='root', vdb='blog', vport=3306):
        self.host, self.user, self.passwd,self.db, self.port = vhost, vuser, vpasswd,vdb, vport
        self.flag = False
    def init(self):
        self.conn=MySQLdb.connect(self.host,self.user,self.passwd,self.db,self.port)
        self.cur=self.conn.cursor()
        self.flag = True
    def query(self, sql):
        if( not self.flag):self.init()
        logging.info("sql: %s" % sql)
        try:
            num = self.cur.execute(sql);
        except:
            self.init()
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
        return blog.db.query("insert into articles (author, title, context) values ('%s', '%s', '%s');" % (author, title, context))
    def update_blog(self,old_title, old_context, new_title, new_context, author):
        return blog.db.query("update articles set ( title, context) values ('%s', '%s') where title='%s' and context='%s' and author='%s' ;" % (new_title, new_context, old_title,old_context,author))

    def del_blog(self, author, title):
        return blog.db.query("delete from articles where author='%s' and title='%s';" % (author, title))

    def get_all_titles(self, author):
        return blog.db.query("select title from articles where author='%s';" % author)
        
    def get_context_by_title(self, author, title):
        return blog.db.query("select context, createtime,author from articles where author='%s' and title = '%s'; " % (author,title))

    def get_all_articles(self, author):
        return blog.db.query("select title, context from articles where author='%s' ;" % author)

    def query_user(self,name):
        num, ret = blog.db.query("select user from user where user ='%s';" % name)
        if num == 1 : return True;
        return False

    def RegisterUser(self, name, passwd):
        return blog.db.query("insert into user ( user, passwd) values ('%s', '%s');" % (name, passwd))
        
        
    def VerifyUser(self, user, passwd):
        num ,ret = blog.db.query("select passwd from user where user='%s'; " % user)
        if(num == 0): return False
        logging.info("passwd from web:%s, passw from db:%s" % (passwd,str(ret[0][0])))
        if ret[0][0] == passwd: return True 
        return False
        
