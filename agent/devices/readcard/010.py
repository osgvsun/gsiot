#!/usr/bin/python
# -*- coding:utf-8 -*-
import os,sys,time,threading
from datetime import datetime
from multiprocessing import Process
path=sys.path[0]
sys.path.append(path+"/../../..")
from lib import *
from lib.net import Net
from app.devices import App
from lib.app.devices import DeviceUnit
# from lib.app.devices.mythread import gsThread
from lib.iot.gsreadcard import ReadCard
from lib.file.log import logFile
@Singleton
class readcardUnit(DeviceUnit):
    cmd=command_interpreter()
    def __init__(self,app,*argv):
        DeviceUnit.__init__(self,"/etc/conf/readcard.json",app,*argv)
        self.log=logFile(self.app.rootpath+"/etc/log/readcard")
        self.addr="readcard"
        self.serialname=""
        self.gpbuzz=None
        self.checkflag=True
        self.dev=ReadCard(self.cfg.device.modulename)     
    @cmd.command("readcard.open")
    def openreadcard(self):
        this=self.app.module.readcard
        this.dev.serialname=this.serialname
        this.dev.ReadData=this.read_card
        this.dev.Open()
    @cmd.command("readcard.close")
    def closereadcard(self):
        this=self.app.module.readcard
        this.dev.Close()
    @cmd.command("readcard.wg34")
    def getCardfromWG34(self,card):return str(int(card,16))
    def read_card(self,card,status):
        card=self.app("readcard.{}".format(self.cfg.readconfig.cardtype),card)
        # 测试用代码，发布时需要注释掉
        if str(card)=="669417875":card=""
        elif str(card)=="3100465280":card="164887559" 
        # self.app.printf("card!=\"\"",card!="") 
        if card!="" and status==False:
            self.app.logservice("info","卡号[{}]已{}识别区".format(card,"进入" if status==False else "离开"))
            self.app.getGPIO_Buzz()
            user=self.app("auth.readcard",card=card)
            record=None
            # 没有此人
            if user==None:
                self.app.logservice("info","当前卡号:{}没有对应用户".format(card))
                self.app("event",eventType="readcard",user="",card=card)
            else:
                username,cname,card=user
                self.app.logservice("info","识别到用户,工号:{},姓名:{},卡号:{}".format(username,cname,card))
                # 广播到其他模块处理信息
                self.app("event",eventType="readcard",user=username,cname=cname)
    def Open(self,**keyargv):
        port=self.dev.CheckHardware()
        if len(port)!=0:
            self.serialname=port[0]
            self.app.logservice("info","{} is {}[ok]".format(self.serialname,self.cfg.device.modulename))
            self.app("readcard.open")
        else:
            self.app.logservice("error","未识别到读卡模块：{},请人工干预".format(self.cfg.device.modulename))
            while True:time.sleep(1) 
    @cmd.command("event")
    def readcard_event(self,*argv,**keyargv):pass       


if __name__ == "__main__":
    appmodule=App(path+"/../..")
    serv=readcardUnit(appmodule)
    print serv.cfg.device.modulename
    print serv.cfg.device.serialname
    serv.Open()
    print appmodule.cmd.cmds