# -*- coding:utf-8 -*-
from gsiot.v3 import *
# from lib.iot.gsserial
# 模块处理电子开关,目前电子开关有两种形式,
# 第一是GPIO输出高低电平的方式完成
# 第二是通过串口操作完成,主要是电表和继电开关
# 当前对象处理的是一组电子开关,单个gpio开关直接由gsGPIO对象完成
class ReadCard(gsobject):
    def __init__(self,modulename=None):
        gsobject.__init__(self)
        # 操作对象和相关信息
        self.data=edict()
        self.serialmodulename=modulename
        self.serialname=""
        self.LastCard=""
        if modulename:self.initdev()
    def __exit__(self,exc_type,exc_value,exc_trackback):
        printf("close readcard")
    def initdev(self,modname=None):
        if not modname:modname=self.serialmodulename
        module=__import__("lib.file.gsserial.{}".format(modname),fromlist=['xxx'])
        # setattr(self.module,module_name, getattr(module,self.cfg.module[module_name])(self))
        self.dev=getattr(module,"gsDevSerial")()
        if self.dev.moduletype=="readcard":
            self.isOpen=self.dev.isOpen
            self.ReadCard=self.dev.ReadCard
            self.Close=self.dev.Close
        else:self.dev=None
        return self.dev
    def Open(self,*argv):
        for port in System.Serials.list:
            if self.serialmodulename and System.Serials[port]==self.serialmodulename:
                if isLinux:port="/dev/"+port
                self.serialname=port
                self.dev.Open(port)
                break
            elif not self.serialmodulename and System.Serials[port] and self.initdev(System.Serials[port]):
                if isLinux:port="/dev/"+port
                self.serialname=port
                self.dev.Open(port)
                break
        if self.isOpen():self.logprint("模块{}已经打开串口{}:{}".format(self.dev.modulename,self.dev.serialname,self.isOpen()))
        else:self.errormsg({"code":500,"msg":"查找不到{}模块对应的串口".format(self.serialmodulename)})

if __name__ == "__main__":
    System.CheckSerials()
    s=ReadCard("tx800t")
    s.Open()
    while True:
        card=s.ReadCard()
        if card!="":printf(card)
    s.Close()