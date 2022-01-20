# -*- coding: utf-8 -*-
from gsiot.v3 import *
class dbConn:
    def __init__(self,**argv):pass
class dbServer:
    def __init__(self,**argv):
        self.dbconn=dbConn(**argv)
        self.db=[]
        self.ip=argv["ip"]
    def Connection(self):pass
    def DisConnect(self):pass
    def reLoad(self):pass
class dbDatabases:
    def __init__(self,**argv):
        self.from=argv["dbserver"]
        self.module="dbDatabase"
        self.name=argv["dbname"]
class dbTable:
    def __init__(self,**argv):
        self.from=argv["dbase"]
        self.isonly=False
        self.name=argv["dbtable"] if "dbtable" in argv else argv["dbview"] if "dbview" in argv else None
        self.module="dbTable"
        self.fullname="{}.{}".format(argv["dbname"],self.name)
class dbView(dbTable):
    def __init__(self,**argv):
        dbTable.__init__(self,**argv)
        self.isonly=True
        self.module="dbView"