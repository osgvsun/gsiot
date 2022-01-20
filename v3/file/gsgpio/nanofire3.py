# -*- coding:utf-8 -*-
from gsiot.v3 import *
from gsiot.v3.file.gsgpio import gsGPIO
class GPIOCtrl(gsGPIO):
    def __init__(self,pin,Name=None,GPIO=None):
        gsGPIO.__init__(self,pin,Name,GPIO)
        self.pins=[]
        for i in range(0,41):self.pins.append(-1)
        self.pins[7]=104 # GPIOD8/PPM
        self.pins[8]=117 # UART3_TXD/GPIOD21
        self.pins[10]=113 # UART3_RXD/GPIOD17
        self.pins[11]=61 # UART4_TX/GPIOB29
        self.pins[12]=97 # GPIOD1/PWM0
        self.pins[13]=62 # GPIOB30
        self.pins[15]=63 # GPIOB31
        self.pins[16]=78 # GPIOC14/PWM2
        self.pins[18]=59 # GPIOB27
        self.pins[19]=95 # SPI0_MOSI/GPIOC31
        self.pins[21]=96 # SPI0_MISO/GPIOD0
        self.pins[22]=60 # UART4_RX/GPIOB28
        self.pins[23]=93 # SPI0_CLK/GPIOC29
        self.pins[24]=94 # SPI0_CS/GPIOC30
        self.pins[26]=58 # GPIOB26
        self.pins[29]=72 # GPIOC8
        self.pins[31]=71 # GPIOC7
        self.pins[32]=92 # GPIOC28
        self.pins[33]=77 # GPIOC13/PWM1
        self.pins[35]=75 # SPI2_MISO/GPIOC11
        self.pins[36]=74 # SPI2_CS/GPIOC10
        self.pins[37]=163 # AliveGPIO3
        self.pins[38]=76 # SPI2_MOSI/GPIOC12
        self.pins[40]=73 # SPI2_CLK/GPIOC9
        self.pin=self.pins[pin]
        self.pin_path=""
        self.gpios_path="/sys/class/gpio"
        self.modulename="gsgpio.nanofire3.GPIOCtrl"
        self.__direction=""
    def Open(self):
        if self.pin==-1:self.isOpen(False)
        else:
            os.system("echo {} > {}/export".format(self.pin,self.gpios_path))
            self.pin_path="{}/gpio{}".format(self.gpios_path,self.pin)
            self.isOpen(True)
    def Close(self):
        if self.isOpen()==True:
            os.system("echo {} > {}/unexport".format(self.pin,self.gpios_path))
            self.pin_path=""
            self.__direction=""
            self.isOpen(False)
    def direction(self,value=None):
        if value==None:return self.__direction
        elif self.isOpen()==True and self.__direction!=value:
            os.system("echo {} >{}/direction".format(value,self.pin_path))
            self.__direction=value
    def On(self):
        if self.isOpen()==True:
            self.direction("out")
            os.system("echo 1 >{}/value".format(self.pin_path))
            self.status=1
    def Off(self):
        if self.isOpen()==True:
            self.direction("out")
            os.system("echo 0 >{}/value".format(self.pin_path))
            self.status=0
    def OnOff(self,sleepValue=1):
        self.On()
        printf(self.Read())
        time.sleep(sleepValue)
        self.Off()
        printf(self.Read())
    def StartEvent(self):pass
    def StopEvent(self):pass
    def Read(self):
        if self.isOpen()==True:
            if self.__direction=="in":return os.popen("cat {}/value".format(self.pin_path))
            elif self.__direction=="out":return self.status
    
if __name__ == "__main__":
    gp=GPIOCtrl(32)
    gp.Open()
    gp.OnOff(3)
    gp.Close()