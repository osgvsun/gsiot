# -*- coding:utf-8 -*-
from gsiot.v3 import *
from gsiot.v3.file.gsgpio import gsGPIO
def runas(cmd):printf(cmd,os.system(cmd))
class GPIOCtrl(gsGPIO):
    def __init__(self,pin,Name=None,GPIO=None):
        gsGPIO.__init__(self,pin,Name,GPIO)

    
if __name__ == "__main__":
    gp=GPIOCtrl(32,"buzz")
    gp.Open()
    gp.OnOff()
    gp.Close()
