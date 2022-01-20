# -*- coding:utf-8 -*-
import sys,os,threading,platform,time
if __name__=="__main__":
    path=sys.path[0]
    sys.path.append(path+"/../../..")
from lib import *
from lib.iot.power import gsOnOff
# 模块处理电子开关,目前电子开关有两种形式,
# 第一是GPIO输出高低电平的方式完成
# 第二是通过串口操作完成,主要是电表和继电开关
# 当前对象处理的是一组电子开关,单个gpio开关直接由gsGPIO对象完成
class Power(gsOnOff):
    def On(self,index):pass
    def Off(self,index):pass
    def AddDev(self,index):pass
    def RemoveDev(self,index):pass
    def ReadStatus(self,index):pass
    def OnOff(self,index):pass
    # 针对GPIO针脚,以下两个方法无用
    # def Open(self):pass
    # def Close(self):pass


