# -*- coding:utf-8 -*-
from gsiot.v3 import *
from gsiot.v3.file.gsserial import *
class gsDevSerial(gsSerial):
    def __init__(self):
        gsSerial.__init__(self)
        self.istest=True
        # self.ReadData=self.__readdata
        self.modulename="gsSerial.tx800t"
        self.moduletype="readcard"
        self.timeout=0.1
        self.show_log_data=False
        self.readlength=16
        # 操作代码
        self.cmd = '2000100100ee03'
        self.notfind = "20000100fe03"
        self.findcpu='20002D00D203'
        self.readcpu="200022010103"
        self.model_data = "bin" 
        self.head=b"20"
        self.card_start=16
        self.card_end=24
        self.cardlength=28
        self.icCardtype="m1iccard"
    def Test(self,Port):
        ret=False
        self.Open(Port)
        if self.isOpen():
            data=self.SendCMD(self.cmd)
            if data.find(self.cmd)!=-1:ret=False
            elif data.find(self.notfind)!=-1 or (data.find(self.head)!=-1 and data.find(self.cmd)==-1):ret=True
            self.Close()
            return ret
        else:return False
    def read_data(self,value):pass
    def ReadCard(self):
        card=""
        # print self.modulename,self.serialname,self.isOpen(),self.dev.isOpen()
        # print gsSerial.isOpen(self)
        if self.isOpen():
            if self.icCardtype=="m1iccard":
                data=self.SendCMD(self.cmd)#.replace(self.dev.cmd,"")
                if data=="" or data==self.notfind:pass
                else:card=data[self.card_start:self.card_end]
            else:
                data=self.SendCMD(self.findcpu)#.replace(self.dev.findcpu,"")
                data=self.SendCMD(self.readcpu)#.replace(self.dev.readcpu,"")
                if data!="":
                    cardtype=data[6:10]
                    # 银行卡
                    if   cardtype=="0f0e" and data[40:52]=='03':card=data[-8:-6]+data[-10:-8]+data[-12:-10]+data[-14:-12]+data[-16:-14]
                    # 校园卡
                    elif cardtype=="1110" and data[44:46]=='03':card=data[-8:-6]+data[-10:-8]+data[-12:-10]+data[-14:-12]
                    # 公交卡
                    elif cardtype=="1312" and data[48:50]=='03':card=data[-8:-6]+data[-10:-8]+data[-12:-10]+data[-14:-12]
            if card!="":card=card[6:8]+card[4:6]+card[2:4]+card[0:2]
        return card
    def SendCMD(self,cmd=None):
        if self.isOpen()==True:
            if cmd!=None:
                # print "send:",self.serialname,self.isOpen(),str(cmd)
                self.Write(cmd)
            data=self.Read()            
            # print "recv:",data
            if data!=self.cmd_error:return data
            else:return ""
        else:return ""
if __name__ == "__main__":
    o=gsDevSerial()
    for port in System.Serials:
        printf(port,o.Test(port))
    # print "\r",