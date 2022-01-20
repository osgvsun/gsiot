#!/usr/bin/python
# -*- coding:utf-8 -*-
import os,sys,time,json,io
from datetime import datetime
if __name__=="__main__":
    path=sys.path[0]
    sys.path.append(path+"/../../..")
from lib import *
from lib.file.gsreadcard import ReadCard
from app.devices import App
from lib.app.devices import DeviceUnit
@Singleton
class readcardUnit(DeviceUnit):
    cmd=command_interpreter()
    def __init__(self,app,*argv):
        DeviceUnit.__init__(self,"/app/etc/readcard.json",app,"/etc/conf/readcard.json",*argv)
        self.addr="readcard"
        self.dev=ReadCard(self.cfg.device.modulename)
        # self.dev.ErrorMsg=self.error_log
        self.dev.LogData=self.logservice
        self.isOpen=self.dev.isOpen
        self.dev_task=self.work_job
    def logservice(self,*data):
        # data=data.replace("\n","").split()[-1]
        self.app.logservice("info",*data)
        # self.log.info(data)
    # def error_log(self,data):self.app.logservice("error",data["msg"])
    def Open(self,*argv):DeviceUnit.Open(self,*argv)
    def work_job(self):
        if self.isOpen():
            card=self.dev.ReadCard()
            if card=="" and self.dev.LastCard!="":
                self.app("readcard_read",self.dev.LastCard,True)
                self.dev.LastCard=""
            elif card!=self.dev.LastCard and card!="":
                self.app("readcard_read",card,False)
                self.dev.LastCard=card
    @cmd.command("readcard_read")
    def readcard(self,card,status=False):
        this=self.app.module.readcard
        card=self.app(this.cfg.device.cardtype,card)
        # 测试用代码，发布时需要注释掉
        if str(card)=="3100465280":card="164887559" 
        elif str(card)=="3081525277":card="164887559" 
        # elif str(card)=="66977793":return
        self.app.logservice("info","卡号[{}]已{}识别区".format(card,"进入" if status==False else "离开"))
        this.log.info("{}:{}".format(card,status))
        if status==False or this.cfg.device.readcard_credit_card_mod.value==1:
            ret=self.app("auth.from_card",card=card,status=status)
            if ret:return ret
            else:
                self.app.logservice("info","未加载认证模块")
                self.app("gpio.operation",**{"pinname":"buzz"})
                self.app("event",type="alert",msg="卡号：{}\n未加载认证模块".format(card))
    @cmd.command("wg34")
    def getCardfromWG34(self,card):return str(int(card,16))
    @cmd.command("event")
    def readcard_event(self,*argv,**keyargv):
        data=edict(keyargv)
        # 模拟power
        if data.type=="readcard_read":
            # 检查是否曾刷过卡
            # 检查到则处理并返回True，否则返回False
            return False