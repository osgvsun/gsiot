#!/usr/bin/python
# -*- coding:utf-8 -*-
from gsiot.v3 import *
from gsiot.v3.file import gsFile
# 原型：操作所有GPIO设备文件
class gsGPIOFile(gsFile):
    def __init__(self, PIN, Name=None, GPIO=None):
        gsFile.__init__(self,PIN)
        self.pin = PIN
        self.Name = Name
        self.gpio = GPIO
        self.LogData = None
        self.status = 0
        self.LogData=None
        self.ReadData=None
        self.index=None
        self.modulename="gsGPIO"
    def StartEvent(self):
        try:
            if self.OpenModel() == "r":self.gpio.add_event_detect(self.pin, self.gpio.FALLING, callback= self.readdata,bouncetime=200)
        except RuntimeError,e:
            self.logprint(str(e))
    def StopEvent(self):
        if self.OpenModel() == "r":self.gpio.remove_event_detect(self.pin)
    def Open(self, value='w'):
        try:
            if not self.gpio:
                import RPi.GPIO as GPIO
                self.gpio = GPIO
            self.gpio.setwarnings(False)
            self.gpio.setmode(self.gpio.BOARD)
            if value == "w":self.gpio.setup(self.pin, self.gpio.OUT)
            elif value == "r":self.gpio.setup(self.pin, self.gpio.IN)
            self.os = "raspberry pi"
        except Exception as e:
            self.gpio = None
            self.os = "not raspberry pi"
        self.OpenModel(value)
        self.isOpen(True)
    def Close(self):
        self.isOpen(False)
        self.gpio = None
    def On(self):self.write(1)
    def Off(self):self.write(0)
    def Write(self, data):
        if self.OpenModel() == "w":
            self.status = data
            printdata = "The %s(PIN %s) "
            if data == 1:printdata += "is HIGH"
            elif data == 0:printdata += "is LOW"

            self.logprint(printdata % (self.Name, str(self.pin)))
            if self.isOpen() and self.gpio != None: self.gpio.output(self.pin, self.status)
    def Read(self):
        if self.isOpen() == False:
            if self.status == 0:self.logprint("The %s(PIN %s) is LOW" % (self.Name, str(self.pin)))
            elif self.status == 1:self.logprint("The %s(PIN %s) is HIGH" % (self.Name, str(self.pin)))
        else:
            if self.gpio != None and self.OpenModel() == "r": self.status = self.gpio.input(self.pin)
        return self.status

# 单线通信服务
class gsOneLine(gsGPIOFile,gsService):pass
