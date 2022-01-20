# -*- coding:utf-8 -*-
from gsiot.v3 import *
# from lib.iot.gsserial
# 模块处理电子开关,目前电子开关有两种形式,
# 第一是GPIO输出高低电平的方式完成
# 第二是通过串口操作完成,主要是电表和继电开关
# 当前对象处理的是一组电子开关,单个gpio开关直接由gsGPIO对象完成
class gsOnOff(gsobject):
    def __init__(self,modulename=None):
        gsobject.__init__(self)
        # 操作对象和相关信息
        self.data=edict()
        self.serialmodulename=modulename
        self.serialname=""
        self.LastCard=""
        self.isReadElecData=False
        if modulename:self.initdev()
    def __exit__(self,exc_type,exc_value,exc_trackback):
        printf("close readcard")
    def initdev(self,modname=None):
        if not modname:modname=self.serialmodulename
        module=__import__("lib.file.gsserial.{}".format(modname),fromlist=['xxx'])
        self.dev=getattr(module,"gsDevSerial")()
        if self.dev.moduletype=="power":
            self.isOpen=self.dev.isOpen
            self.isReadElecData=self.dev.isReadElecData
            self.On=self.dev.On
            self.Off=self.dev.Off
            self.ReadStatus=self.dev.ReadStatus
            self.ReadData=None if "ReadPower" not in dir(self.dev) else self.dev.ReadPower
            self.Close=self.dev.Close
        else:self.dev=None
        return self.dev
    # OnOff方法适合瞬间开关，
    # 例如出门按钮，一开一关，门就打开了，
    # 如果是电源，则需要长时间打开，才能供电，关闭就没电了
    def OnOff(self,index):
        ret=self.On(index)
        time.sleep(2)
        ret=ret and self.Off(index)
        return ret
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
    # s=gsOnOff("zy408")
    s=gsOnOff("dds253")
    s.Open()
    printf(s.serialname,s.isOpen())
    # for i in range(1,s.dev.indexs+1):
    #     if s.ReadStatus(i)==True:print "port close {} isOpen:{}".format(i,s.Off(i))
    #     else:print "port open {} isOpen:{}".format(i,s.On(i))
    while True:printf(s.ReadData())
    s.Close()
