# -*- coding: utf-8 -*-
from gsiot.v3 import *
class dbServer():
    #构造器函数
    def __init__(self,modulename,host,user,passwd):
        #确定使用何种数据库引擎
        self.host=host
        self.user=user
        self.passwd=passwd
        exec("from lib.db.conn.%sconn import conn"%modulename)
        self.conn=eval("conn(host,user,passwd)")
        self.db=edict()
    def open(self,*dbnames):
        self.conn.open()
        if len(dbnames)==0:self.db=self.conn.getstructure()
        else:
            for dbname in dbnames :
                self.db.readdict(eval(self.conn.getstructure(dbname).toJsonString()))
    def use(self,dbname):
        if dbname in self.db.list:
            db=edict()
            db.readdict(self.db[dbname].copy())
            self.db[dbname]=dbDatabases(self.conn,dbname,db)
            return self.db[dbname]
        else:return None
    def close(self):
        self.conn.close()

if __name__ == "__main__":
    oserv=dbServer("mysql","127.0.0.1","root","gengshang")
    oserv.open("iot","datashare")
    # printf(oserv.db.toJsonString())
    a=oserv.use("datashare")
    printf(a.tables.toJsonString(),type(a.tables))
    oserv.close()
