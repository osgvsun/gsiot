# -*- coding:utf-8 -*-
from gsiot.v3 import *
import socket,select
from multiprocessing import Process
from threading import Thread
from datetime import datetime

from gsiot.v3.net.client import Client
# BaseServer是一个标准C/S的对象，建立了连接池，可读取指定连接发送过来的数据
# 缺点是没有timeout，如果客户端一直不发数据，会处于阻塞状态。
class BaseServer(gsIO):
    instances = {}
    key=()
    def __new__(cls,**cfg):
        host="0.0.0.0" if "host" not in cfg else cfg["host"] if cfg["host"]!="" else "0.0.0.0"
        port=9999 if "port" not in cfg else cfg["port"]
        cls.key=(host,port)
        if cls.key in cls.instances:cls.instance=cls.instances[cls.key]
        else:cls.instance=super(BaseServer,cls).__new__(cls)
        return cls.instance
    def __init__(self,**cfg):
        self.cfg=edict()
        self.cfg.readdict(cfg)
        self.host="0.0.0.0" if "host" not in cfg else self.cfg.host if self.cfg.host!="" else "0.0.0.0"
        self.port=9999 if "port" not in cfg else self.cfg.port
        self.key=(self.host,self.port)
        self.runtime_mode=self.cfg.runtime if "runtime" in cfg else "single"
        gsIO.__init__(self,self.key)
        self.interval = self.cfg.interval if "interval" in cfg else 1
        self.modulename="gsSocket.BaseServer"
        self.max=self.cfg.max if "max" in cfg else 128
        self.prototype=self.cfg.prototype if "prototype" in self.cfg else "tcp"
        if   self.prototype == "tcp":self.dev = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif self.prototype == "udp":self.dev = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dev.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        try:self.DataModel(self.cfg.datamodel)
        except:pass
        self.quesocket=Queue(self.max)      # socket请求队列
        self.clients={}
        self.event_newclient=None
    #该方法用于确认当前系统中对应端口已经释放
    def checkportstatus(self):
        while True:
            pid=System.Process(port=self.port)
            if pid==False or pid=="":break
            elif pid!=os.getpid():
                self.logprint("info","发现进程{}占用端口{}:{}，正在删除进程".format(pid,self.host,self.port))
                System.killProc(pid)
            time.sleep(1)
    # 开始建立服务通道，运行服务
    def Open(self):
        if self.isOpen()==False:
            self.checkportstatus()
            self.logprint("网络服务正在启动....")
            self.dev.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            # self.dev.setblocking(False)
            if self.host=="0.0.0.0":self.dev.bind(("", self.port))
            else:self.dev.bind((self.host,self.port))
            self.dev.listen(self.max)
            self.isOpen(True)
            # 建立读取请求的子线程，主进程结束会强制结束子线程
            self.logprint("%s:%s 正在监听中...."%(self.host,str(self.port)))
    def Read(self,addr=None):
        if self.isOpen()==True:
            if not addr:
                try:
                    obj, addr = self.dev.accept()
                    client=Client(obj=obj)
                    client.Closed=self.Client_Closed
                    record={addr:client}
                    self.clients.update(record)
                    if self.event_newclient:self.event_newclient(addr)
                    return record
                except:pass
            elif addr in self.clients:
                data=self.clients[addr].Read()
                # print self.clients[addr].addr
                if data:return data
    # 服务没有写的操作，写操作在每个链接中存在
    def Write(self,addr,data):
        if addr in self.clients:self.clients[addr].Write(data)
    # 新连接
    # def Client_newClient(self,add):
    # 关闭连接
    def Client_Closed(self,addr):
        self.logprint("client {} is closed".format(addr))
        if addr in self.clients:del self.clients[addr]
    def Close(self,addr=None):
        if not addr:
            self.isOpen(False)
            for addr in self.clients:self.clients[item].Close()
            self.dev.close()
        elif addr in self.clients:
            self.clients[addr].Close()
            self.logprint("{} Closed".format(addr))
    def ReOpen(self):
        self.Close()
        self.Open()
# Server对象是在BaseServre基础上，将受到的请求压入Queue堆栈
# 可通过Read方法读取到信息，每个连接都分配一个线程,通过读取s.getpeername()获取addr
class Server(BaseServer,Thread):
    def __init__(self,**cfg):
        BaseServer.__init__(self,**cfg)
        Thread.__init__(self)
        self.modulename="gsSocket.Server"
        self.runtime_mode="multi threading" if "runtime_mode" not in cfg else self.cfg.runtime_mode
        self.readbuff={}
        self.inputs = []
        self.outputs = []
        self.msg_dic = {}
        self.event_message=None
    def Open(self):
        BaseServer.Open(self)
        # 建立读取请求的子线程，主进程结束会强制结束子线程
        self.setDaemon(True)
        self.start()
    def run(self):
        self.inputs.append(self.dev)
        while self.isOpen()==True:
            try:readable,writable,exceptional = select.select(self.inputs,self.outputs,self.inputs)
            except:readable=writable=exceptional=[]
            for r in readable:
                # 说明有新连接过来
                if r is self.dev:   
                    conn,addr = self.dev.accept()
                    conn.setblocking(0) 
                    client=Client(obj=conn)#, addr=addr,host=addr[0],port=addr[1])
                    client.Closed=self.Client_Closed
                    self.clients[addr]=client
                    # 如果有配置，交由外部处理
                    if self.event_newclient:self.newclient(client,addr) 
                    # 如果没有配置，则由select处理
                    else:
                        self.inputs.append(conn)
                        self.readbuff[addr]=[]                   
                else:
                    addr=r.getpeername()
                    data=self.clients[addr].Read()
                    if data:
                        if self.event_message:self.event_message(addr,data)
                        else:self.readbuff[addr].append(data)
            # for w in writable:pass
            # for e in exceptional:pass
    
    def newclient(self,client,addr):
        # 根据模式:单进程
        if   self.runtime_mode=="single":self.event_newclient(addr)
        # 多进程
        elif self.runtime_mode=="multi process":
            p=Process(target=self.event_newclient,args=(addr,))
            p.daemon=True
            p.start()
            # 子进程会复制主进程发的资源，故把主进程的socket关闭。
            client.close()
        # 多线程
        elif self.runtime_mode=="multi threading":
            # 主进程结束会强制结束子线程
            t=Thread(target=self.event_newclient,args=(addr,))
            t.setDaemon(True)
            t.start()
        
                     
    def Read(self,addr):
        if addr in self.readbuff:
            ret="".join(self.readbuff[addr])
            self.readbuff[addr]=[]
            return ret
class ThreadServer(Server):
    def __init__(self,**cfg):
        Server.__init__(self,**cfg)
        self.modulename="gsSocket.ThreadServer"
        self.thread_number=self.max if "thread_number" not in cfg else self.cfg.thread_number
        self.thread_pool=ThreadPoolManger(self.thread_number,self.quesocket)
    def newclient(self,client,addr):
        if self.thread_pool:self.thread_pool.add_work(self.event_newclient, *(client,addr))
    def Open(self):
        Server.Open(self)
    def Close(self):   
        self.thread_pool.Close()
        Server.Close() 
class ServerService(BaseServer,gsService):
    instances = {}
    key=()
    def __new__(cls,**cfg):
        host="0.0.0.0" if "host" not in cfg else cfg["host"] if cfg["host"]!="" else "0.0.0.0"
        port=9999 if "port" not in cfg else cfg["port"]
        cls.key=(host,port)
        if cls.key in cls.instances:cls.instance=cls.instances[cls.key]
        else:cls.instance=super(ServerService,cls).__new__(cls)
        return cls.instance
    def __init__(self,**cfg):
        BaseServer.__init__(self,**cfg)
        gsService.__init__(self)
        self.cfg=edict(cfg)
        self.task=self.event_newRequest
    # 开始建立服务通道，运行服务
    def Open(self):
        BaseServer.Open(self)
        gsService.Open(self)
    def run(self):
        while not self.stop:
            if self.isOpen() and self.dev and self.task:
                printf(self.dev,self.isOpen(),self.task)
                obj, addr = self.dev.accept()
                client=Client(obj=obj)
                client.Closed=self.Client_Closed
                self.clients.update({addr:client})
                self.event_new_request(client,addr)
            #     self.thread_pool.add_work(self.task, *(client,addr,))
            time.sleep(self.timeinterval)
    def Client_Closed(self,addr):
        self.logprint("client {} is closed".format(addr))
        if addr in self.clients:del self.clients[addr]
    def event_newRequest(self,client,addr):
        printf(addr,"recv:",client.Read())
        client.Close()
    
def newRequest(client,addr):
    printf(addr,"recv:",client.Read())
    client.Close()

if __name__=='__main__':
    s=ServerService(host="",port=9999)
    s.Open()
    while True:time.sleep(0.5)