# -*- coding:utf-8 -*-
import socket
from gsiot.v3 import *
class Client(gsobject):
    def __init__(self,**cfg):
        gsobject.__init__(self)
        self.Closed=None
        self.cfg = edict()
        self.cfg.readdict(cfg)
        (self.localip,self.localport)=("",0) if "obj" not in self.cfg or self.cfg.obj==None else self.cfg.obj.getsockname()
        self.dev = None  # socket对象
        if   "obj" in self.cfg and self.cfg.obj!=None:
            self.dev=self.cfg.obj
            # self.dev.settimeout(1 if "timeout" not in self.cfg else self.cfg.timeout)
            self.dev.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            self.send=self.dev.send
            self.recv=self.dev.recv
            self.close=self.dev.close
            self.addr=self.dev.getpeername()
            self.cfg.host=self.addr[0]
            self.cfg.port=self.addr[1]
            self.isOpen(True)
        elif "prototype" not in self.cfg:self.dev = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif self.cfg.prototype == "udp":self.dev = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:self.DataModel("ascii" if "datamodel" not in self.cfg else self.cfg.datamodel)
        except:pass
        self.readbufflength = 1024
        self.heartbeatstring="\r"
        self.showlog(False if "show_log_data" not in self.cfg else self.cfg.show_log_data)
    # 打开socket，初始化对象
    def Open(self):
        try:
            self.logprint(datetime.now(),"connect %s:%d"%(self.cfg.host, self.cfg.port))
            self.dev.connect((self.cfg.host, self.cfg.port))
            self.dev.settimeout(1 if "timeout" not in self.cfg else self.cfg.timeout)
            self.send=self.dev.send
            self.recv=self.dev.recv
            self.close=self.dev.close
            self.isOpen(True)
        except Exception as e:
            self.errormsg("module:gsSocketClient,function:open error," + e.message)
            self.isOpen(False)
    # 关闭socket对象
    def Close(self):
        self.logprint(datetime.now(),"Client Close {}:{}".format(self.cfg.host,self.cfg.port))
        self.dev.close()
        if self.Closed:self.Closed((self.cfg.host,self.cfg.port))
        self.isOpen(False)
    # 读返回数据
    def Read(self):
        ret = ""
        try:
            if self.isOpen():
                data = self.dev.recv(self.readbufflength)
                self.logprint(self.cfg.host,self.cfg.port,"recv:",data)
                if self.DataModel() == "bin":ret = binascii.b2a_hex(data)
                else:ret = data
                # 触发测试是否断开连接
                if ret=="":self.Write(self.heartbeatstring)  
                else:ret="".join([ele for ele in ret.split(self.heartbeatstring) if ele!=""]).replace("\n","\r\n")
                return ret
        except Exception as e:
            # print str(e)=="[Errno 10053]"
            if str(e)=="timed out":self.Write(self.heartbeatstring)
            elif str(e).strip()=="[Errno 10053]":self.Close()
            else:self.errormsg(str(e))
        return ret
    # 发送数据
    def Write(self, data):
        # try:
        if self.isOpen():
            # printf(self.cfg.host,self.cfg.port,"send:",data)
            self.dev.sendall(data)
        # except Exception, e:
        #     if str(e)=="[Errno 32] Broken pipe":self.Close()
            # else:self.errormsg(e)
if __name__ == '__main__':
    c=Client(host="127.0.0.1",port=80)
    c.logprint=System.Console
    c.Open()
    System.Console(datetime.now(),c.isOpen())
    c.Write("hello world!")
    time.sleep(10)
    ret=c.Read()
    if ret!="":System.Console(ret)
    c.Close()
    

