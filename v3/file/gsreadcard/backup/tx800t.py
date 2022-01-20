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
        ReadCard.__init__(self,serialname,"tx800t")
        self.card_start=16
        self.card_end=24
        self.cardlength=28
        self.task=self.readcard  
    def readcard(self):
        card=""
        # if self.dev.isOpen()==True:
        if self.icCardtype()=="m1 ic card":
            data=self.dev.sendcmd(self.dev.cmd)#.replace(self.dev.cmd,"")
            if data=="" or data==self.dev.notfind:pass
            else:card=data[self.card_start:self.card_end]
        else:
            data=self.dev.sendcmd(self.dev.findcpu)#.replace(self.dev.findcpu,"")
            data=self.dev.sendcmd(self.dev.readcpu)#.replace(self.dev.readcpu,"")
            if data!="":
                cardtype=data[6:10]
                # 银行卡
                if   cardtype=="0f0e" and data[40:52]=='03':card=data[-8:-6]+data[-10:-8]+data[-12:-10]+data[-14:-12]+data[-16:-14]
                # 校园卡
                elif cardtype=="1110" and data[44:46]=='03':card=data[-8:-6]+data[-10:-8]+data[-12:-10]+data[-14:-12]
                # 公交卡
                elif cardtype=="1312" and data[48:50]=='03':card=data[-8:-6]+data[-10:-8]+data[-12:-10]+data[-14:-12]
        if card!="":card=card[6:8]+card[4:6]+card[2:4]+card[0:2]
        if card=="03fe0001" or len(card)!=8:card=""
        return card
    
def readcard_data(data):
    card,status=data
    printf("read card(hex):{},card(int):{},status:{}".format(card,int(card,16),status))
if __name__ == "__main__":
    readcard=None
    for serialname in os.popen('ls /dev/ttyUSB*').read().split("\n"):
        if serialname!="":
            readcard=gsReadCard(serialname)
            if readcard.dev!=None:break
    if readcard!=None:
        readcard.ReadData=readcard_data
        # 1-m1卡，2-cpu卡
        readcard.icCardtype(1)
        readcard.Open()
    else:printf("找不到读卡模块")
        