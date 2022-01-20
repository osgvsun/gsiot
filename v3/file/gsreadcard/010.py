# -*- coding:utf-8 -*-
import sys,os,threading,platform,time
path=sys.path[0]
sys.path.append(path+"/../../..")
from lib import *
try:   from Queue import Queue
except:from queue import Queue
from copy import copy
class ReadCard(gsobject):
    def __init__(self,modulename=None,serialname=None):
        gsobject.__init__(self)
        self.serialname=serialname
        self.modulename=modulename
        self.dev=self.__initdev() if modulename!=None else None
        self.task=None
        self.timesleep=0.1
        self.lastcard=""
        self.__m1card=True
        self.__cpucard=False
    def icCardtype(self,value=None):
        if value==None:
            if self.__m1card:return "m1 ic card"
            elif self.__cpucard:return "cpu ic card"
        else:
            self.__m1card=False
            self.__cpucard=False
            if   value==1:self.__m1card=True
            elif value==2:self.__cpucard=True
    # 线程是随着打开和关闭方法动作的，所以在打开函数里建立线程，启动线程
    # 在关闭函数里，仅仅标记线程结束，当线程退出循环后，直接关闭相关dev
    # 所以，线程不能写的太罗嗦，需尽量简单，快速解决问题
    def Open(self):
        if self.dev==None:
            exec("from lib.iot.gsserial.{} import gsDevSerial".format(self.modulename))
            self.dev=self.__initdev()
        while self.dev.isOpen()==False:
            self.dev.Open(self.serialname)
            time.sleep(0.2)
        self.__t=threading.Thread(target=self.__task)
        if __name__!="lib.iot.gsreadcard":self.__t.setDaemon(True)
        self.__t.start()
    def Close(self):
        if self.dev!=None :self.dev.isOpen(False) 
    def __initdev(self):
        exec("from lib.iot.gsserial.{} import gsDevSerial".format(self.modulename))
        return eval("gsDevSerial()")
    def CheckHardware(self,port=None):
        ret=None
        if self.modulename!=None:
            self.dev=self.__initdev()
            if self.dev.moduletype=="readcard":
                ret=self.dev.CheckHardware()
                self.dev.Close()
            self.dev=None
        return ret
    def getgsSerialModule(self):
        files=[]
        for filename in os.listdir(path+"/../gsserial"):
            if filename!="backup":
                device=filename.split(".")[0]
                if device!="test" and device[:2]!="__" and not(device in files):
                    files.append(device)
        return files
    def __read(self,card,status):
        if self.ReadData!=None:self.ReadData(card,status)
    def __task(self):
        while self.dev.isOpen()==True:
            # print datetime.now(),"gsreadcard.task",self.dev.serialname,self.modulename
            card=self.dev.task_readcard(self.icCardtype())
            # print "gsreadcard:",card
            status=None
            if card==None:self.lastcard=""
            elif card=="":
                # 上次读取到卡，说明当前卡已离开
                if   self.lastcard!=card:
                    card=copy(self.lastcard)
                    status=True
                    self.lastcard=""
            #说明读到卡
            elif card!=self.lastcard:
                status=False
                self.lastcard=card
                # print card,status,self.dev.serialname,self.dev.modulename
            if status!=None:self.__read(card,status)
            time.sleep(self.timesleep)