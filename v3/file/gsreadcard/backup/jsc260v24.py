# -*- coding:utf-8 -*-
import sys,os,threading,platform,time
path=sys.path[0]
sys.path.append(path+"/../../..")
from lib import *
from lib.iot.gsreadcard import ReadCard
try:   from Queue import Queue
except:from queue import Queue
class gsReadCard(ReadCard):
    def __init__(self,serialname):
        ReadCard.__init__(self,serialname,"jsc260v24")
        self.m1card_start=9
        self.m1card_end=17
        self.cpucard_start=11
        self.cpucard_end=19
        self.task=self.readcard
        self.__ispsam=False
    def ispsam(self,value=None):
        # print self.dev.testflag
        if value==None:return self.__ispsam
        elif self.dev.testflag[1]==True:self.__ispsam=value
    def readcard(self):
        card,status="",False
        # print "run readcard"
        if self.dev.isOpen()==True:
            data=self.dev.sendcmd(self.dev.cmd).replace(self.dev.cmd,"")
            if data=="" or data==self.dev.notfind:
                # 如果没有找到卡，尝试查找m1卡
                # 发送查找m1卡命令
                data=self.dev.sendcmd(self.dev.findm1card).replace(self.dev.findm1card,"")
                # 如果找到卡，则选择该卡，发送防冲撞指令
                # print self.findm1card,data,self.findcard,self.findcard==data
                if data==self.dev.findcard:
                    data=self.dev.sendcmd(self.dev.readm1card).replace(self.dev.readm1card,"")
                    card=data[self.m1card_start:self.m1card_end]
                else:card=""
            # 如果查到卡，从返回的数据中获得卡数据
            elif len(data)==self.dev.cpucardlength:card=data[self.cpucard_start:self.cpucard_end]
            if card!="":
                card=card[6:8]+card[4:6]+card[2:4]+card[0:2]
                if self.ispsam()==True:card=self.dev.getcrypdata(card)
                
        return card
    
def readcard_data(data):
    card,status=data
    printf("read card(hex):{},card(int):{},status:{}".format(card,int(card,16),status))
if __name__ == "__main__":
    readcard=gsReadCard("/dev/ttyUSB0")
    readcard.ReadData=readcard_data
    readcard.ispsam(True)
    readcard.Open()

        