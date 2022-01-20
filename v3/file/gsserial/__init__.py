# -*- coding:utf-8 -*-
import serial
from gsiot.v3 import *
try:import fcntl
except:import lib.file.fcntlock as fcntl

# 串口原型
class gsSerial(gsobject):
    PARITY_NONE = serial.PARITY_NONE
    PARITY_EVEN = serial.PARITY_EVEN
    PARITY_ODD = serial.PARITY_ODD
    PARITY_MARK = serial.PARITY_MARK
    PARITY_SPAC = serial.PARITY_SPACE
    EIGHTBITS = serial.EIGHTBITS
    FIVEBITS = serial.FIVEBITS
    SIXBITS = serial.SIXBITS
    SEVENBITS = serial.SEVENBITS
    STOPBITS_ONE = serial.STOPBITS_ONE
    STOPBITS_ONE_POINT_FIVE = serial.STOPBITS_ONE_POINT_FIVE
    STOPBITS_TWO = serial.STOPBITS_TWO
    def __init__(self):
        gsobject.__init__(self)
        self.serialname=""
        self.baudrate = 9600
        self.parity = self.PARITY_NONE
        self.bytesize = 8
        self.stopbits = 1
        self.timeout = 1
        self.moduletype=""
        # 串口封装对象的配置
        self.model_data = "bin"
        self.index=None
        self.modulename="gsSerial"
        self.readlength=64
        self.ReadData=self.__readdata
        self.show_log_data=False
        self.showlog(self.show_log_data)
        self.ErrorMsg=None 
        self.istest=False
        self.dev=None
        self.Ports=[]
        self.cmd=""
        self.cmd_error=""
    def read_data(self,data):pass
    def __readdata(self,data):pass
    def Open(self, value=None):
        self.showlog(self.show_log_data)
        self.DataModel(self.model_data)
        if value!=None:self.serialname=value
        # try:
        if isWindows:self.dev = serial.Serial(
            port=self.serialname,
            baudrate=self.baudrate,
            parity=self.parity,
            bytesize=self.bytesize,
            stopbits=self.stopbits)
        elif isLinux:self.dev = serial.Serial(
            port=self.serialname,
            baudrate=self.baudrate,
            parity=self.parity,
            bytesize=self.bytesize,
            stopbits=self.stopbits,timeout=self.timeout)
        self.logprint("{} Open serial port:{} [ok]".format(self.modulename,self.serialname))
        self.isOpen(True)
        # except Exception as e:
        #     self.isOpen(False)
        #     self.logprint("{} Open serial port:{} [fail]".format(self.modulename,self.serialname))
        #     self.logprint("error:{}".format(e))
    def Close(self):
        # if len(self.getPorts())>1:self.unLock()
        if self.dev!=None and self.dev.isOpen()==False:self.dev.close()
        self.logprint("{} Close serial port:{} [ok]".format(self.modulename,self.serialname))
        self.isOpen(False)
    def unLock(self):fcntl.flock(self.dev.fileno(),fcntl.LOCK_UN)
    def Read(self):
        data = ""
        if self.isOpen()==True:
            runing = True
            data = b""
            r = b""
            if self.readlength!=0:n=self.readlength
            else:n=self.dev.inWaiting()          
            try:
                if n==0:
                    while runing:
                        r = bytes(self.dev.read(1))
                        if r == b'':runing = False
                        else:data =data+  r
                else:data = self.dev.read(n)
            except:pass
            if self.DataModel() == 'bin': data = binascii.b2a_hex(data)
        if data!="":
            if self.DataModel()=='ascii':
                if type(data)==type(""):data=data.replace("\r","0d").replace("\n","0a")
                elif type(data)==type(b""):data=str(data).replace("\\r","0d").replace("\\n","0a").replace("b'","")[:-1]
            if self.showlog()==True:self.logprint("recv:%s" % data)
            self.readdata(data)
        return data
    def Write(self, data):
        if data!="" and self.isOpen():            
            try:
                if self.DataModel() == 'bin':self.dev.write(binascii.a2b_hex(data))
                elif self.DataModel() == 'ascii':self.dev.write(data)
            except Exception as e:
                self.logprint(repr(e))
                self.Close()
                self.Open()
    def SendCMD(self,cmd=None):
        if self.isOpen()==True:
            if cmd!=None:self.Write(cmd)
            self.logprint( "send:",self.serialname,cmd)
            data=self.Read()
            self.logprint("recv:",data)
            if data!=self.cmd_error:return data
            else:return ""
        else:return ""
    def Test(self,Port=None):pass
    def getPorts(self):
        if len(self.Ports)==0:
            sysserials=list(serial.tools.list_ports.comports())
            value=[]
            for port in sysserials:
                if " ".join(platform.uname()).find("Linux") >= 0 and port[0].find("ttyUSB")!=-1:value.append(port[0])
                elif " ".join(platform.uname()).find("Windows") >= 0:value.append(port[0])
        else:value=self.Ports
        return value
    def CheckHardware(self):
        ret=[]
        if self.istest==True and self.serialname=="":
            for port in System.Serials.list:
                if isLinux:port="/dev/"+port
                result=self.Test(port)
                if result==True:ret.append(port)
        return ret

class gsDevSerial(gsSerial):pass