#!/usr/bin/python
# -*- coding:utf-8 -*-
from gsiot.v3 import *
from gsiot.v3.file.jsonfile import gsJsonFile

class dbFile(gsJsonFile):
    def __init__(self,filename):
        gsJsonFile.__init__(self,filename)
        self.fields=[]
        self.flag=False
        self.Readfile()
    def Savefile(self):
        try:data=self.data.toJsonString(self.flag)
        except:data=""
        if data!="":
            self.Open("w")
            self.Write(data)
            self.Close()
    def Readfile(self):
        if os.path.isfile(self.filename)==True:
            self.Open("r")
            data=self.Read()
            if data!="":
                self.Clear()
                try:self.data.update(eval(data))
                except:self.data.readdict(json.loads(data))
            else:self.data=edict()
            self.Close()
        else:
            self.Savefile()
        return self.data
class dbRecord(gsJsonFile):pass