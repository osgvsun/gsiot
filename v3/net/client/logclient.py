# -*- coding:utf-8 -*-
import socket,json
# from multiprocessing import Process
from gsiot.v3 import *
from gsiot.v3.net.client import *

class logClient(gsobject):
    def __init__(self,host,port,servicename):
        gsobject.__init__(self)
        self.cfg=edict()
        self.cfg.host=host#="192.168.1.185"
        self.cfg.port=port#=10517
        self.servicename=servicename
        self.cfg.prototype="tcp"
        self.cfg.datamodel="ascii"
        self.cfg.show_log_data=False
        self.cfg.timeout=1
        self.dev=Client(self.cfg)
    def __getlog(self,**data):
        log=edict()
        log.source_ip=self.dev.localip
        log.datetime=str(datetime.now())[:19]
        log.logger_name=self.servicename
        log.message=data["message"]
        log.detail=data["detail"]
        # printf(data["test"])
        return log
    def Open(self):
        if self.isOpen()==False:
            self.dev.Open()
            self.isOpen(True)
    def Close(self):
        if self.isOpen()==True:
            self.dev.Close()
            self.isOpen(False)
    def info(self,**data):
        if self.isOpen()==True:
            log=self.__getlog(**data)
            log.level="info"
            self.logprint(log)
            self.dev.Write(str(log))
    def debug(self,**data):
        if self.isOpen()==True:
            log=self.__getlog(**data)
            log.level="debug"
            self.logprint(log)
            self.dev.Write(str(log))  
    def warning(self,**data):
        if self.isOpen()==True:
            log=self.__getlog(**data)
            log.level="warning"
            self.logprint(log)
            self.dev.Write(str(log))   
    def error(self,**data):
        if self.isOpen()==True:
            log=self.__getlog(**data)
            log.level="error"
            self.logprint(log)
            self.dev.Write(str(log))  

def logprint(data):
    value=data[0]
    logfile=logFile(path+"/log")
    if   value.level=="info":logfile.info(str(value))
    elif value.level=="debug":logfile.debug(str(value))
    elif value.level=="warning":logfile.warning(str(value))
    elif value.level=="error":logfile.error(str(value))
    printf(value)

if __name__ == "__main__":
    from lib.file.log import logFile
    log=logClient("192.168.1.185",10516,"python-test")
    log.LogData=logprint
    log.Open()
    log.info(message="李品勇的测试文件,用python{}在操作系统{}下运行".format(int(pathversion[0]),platform.uname()[0]),detail={"key":"value"})
    log.Close()