# -*- coding:utf-8 -*-
from gsiot.v3 import *

class gsGPIO(gsIO):
    def __init__(self,pin,Name=None,GPIO=None):
        gsIO.__init__(self,pin)
        self.pin = pin
        self.Name = Name
        self.gpio = GPIO
        self.LogData = None
        self.status = 0
        self.LogData=None
        self.ReadData=None
        self.index=None
        self.modulename="gsGPIO"
        self.setmode="BOARD"
    def StartEvent(self):
        try:
            if self.OpenModel() == "r":self.gpio.add_event_detect(self.pin, self.gpio.FALLING, callback= self.readdata,bouncetime=200)
        except RuntimeError as e:
            self.logprint(str(e))
    def StopEvent(self):
        if self.OpenModel() == "r":self.gpio.remove_event_detect(self.pin)
    def Open(self, value='w'):
        try:
            if not self.gpio:
                import RPi.GPIO as GPIO
                self.gpio = GPIO
            self.gpio.setwarnings(False)
            if   self.setmode=="BCM":self.gpio.setmode(self.gpio.BCM)
            elif self.setmode=="BOARD":self.gpio.setmode(self.gpio.BOARD)
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
    def On(self):self.__write(1)
    def Off(self):self.__write(0)
    def OnOff(self,sleepValue=0.2):
        self.On()
        time.sleep(sleepValue)
        self.Off()
    def __write(self, data):
        if self.OpenModel() == "w":
            self.status = data
            printdata = "The %s(%s %s) "
            if data == 1:printdata += "is HIGH"
            elif data == 0:printdata += "is LOW"

            self.logprint(printdata % (self.Name,self.setmode, str(self.pin)))
            if self.isOpen() and self.gpio != None: self.gpio.output(self.pin, self.status)
    def Read(self):
        if self.isOpen() == False:
            if self.status == 0:self.logprint("The %s(%s %s) is LOW" % (self.Name,self.setmode, str(self.pin)))
            elif self.status == 1:self.logprint("The %s(%s %s) is HIGH" % (self.Name,self.setmode, str(self.pin)))
        elif self.gpio != None and self.OpenModel() == "r": self.status = self.gpio.input(self.pin)
        return self.status

if __name__ == "__main__":
    gp=gsGPIO(12,"buzz")
    gp.setmode="BCM"
    gp.showlog(True)
    gp.Open()
    gp.OnOff()
    gp.Close()