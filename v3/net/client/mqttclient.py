# -*- coding:utf-8 -*-
import socket
# from multiprocessing import Process
from datetime import datetime
import paho.mqtt.client as mqtt
from gsiot.v3 import *

class mqSocket(gsobject):
    def __init__(self,addr):
        # addr包含三个部分，ip,port,topic,
        # 其中ip是mqtt服务器地址，port是mqtt服务器端口
        # topic是指本连接订阅的主题词
        gsobject.__init__(self)
        self.addr=addr
        self.ip,self.port=addr
        self.dev=None
        self.timeout=2
        self.recv=Queue(128)
        self.mode="sync"
        self.readdata=None
    def Open(self,topic=None):
        # try:
        self.dev= mqtt.Client()
        self.dev.connect(self.ip, self.port, 600) # 600为keepalive的时间间隔
        if topic!=None:self.topic=topic
        else:self.topic=str(datetime.now()).replace(" ","").replace(".","").replace(":","").replace("-","")
        if type(self.topic)==list:
            for t in self.topic:self.dev.subscribe(t)
        else:self.dev.subscribe(self.topic)
        self.dev.on_connect=self.__on_connect
        self.dev.on_message=self.__on_message
        # 使用单独线程解决阻断问题
        self.t=threading.Thread(target=self.run)
        if __name__!='__main__':self.t.setDaemon(True)
        self.t.start()
        s=datetime.now()
        while self.isOpen()==False:
            if (datetime.now()-s).seconds>=self.timeout:break
            time.sleep(0.1)
        if self.isOpen()==False:self.logprint("连接mqtt服务[{}:{}]".format(self.ip,self.port)+"超时")
        return self.isOpen()
    def run(self):self.dev.loop_forever()
    def __on_connect(self,client, userdata, flags, rc):
        if rc==0:
            self.isOpen(True)
            self.logprint("连接mqtt服务[{}:{}]".format(self.ip,self.port) +"成功")
        else:
            self.isOpen(False)
            self.logprint("连接mqtt服务[{}:{}]".format(self.ip,self.port)+":"+str(rc))
    def __on_message(self,client, userdata, msg):
        try:
            value=edict(msg.payload)
            if "sour" not in value:value.sour=msg.topic
        except:
            value=edict()
            value.result=msg.payload
            value.sour=msg.topic
            value.dest=self.topic
        value.datetime=str(datetime.now())[:19]
        if self.mode!="async":self.recv.put(value)
        elif self.readdata!=None:self.readdata(value)
    def Close(self):
        self.isOpen(False)
        self.dev.disconnect()
    def Write(self,topic,data,desc=None):
        if self.isOpen()==True:
            msg=edict()
            msg.sour=self.topic
            msg.dest=desc if desc else topic
            msg.datetime=str(datetime.now())[:19]
            msg.result=data
            self.Send(topic,msg.toString())
    def Send(self,topic,data):self.dev.publish(topic,data,1)
    def Read(self):
        result=None
        startdatetime=datetime.now()
        def __read__():
            while True:
                if self.recv.empty()==False:break #or (datetime.now()-datetime.strptime(startdatetime,'%Y-%m-%d %H:%M:%S')).seconds>self.timeout
                if (datetime.now()-startdatetime).seconds>self.timeout:break
                time.sleep(0.1)
        if self.isOpen()==True:
            t=threading.Thread(target=__read__)
            t.setDaemon(True)
            t.start()
            t.join()
            result=self.recv.get() if self.recv.empty()==False else ""
        return result


if __name__ == "__main__":
    mq=mqSocket(("192.168.1.11",1883))
    if mq.Open(["/sys/gbliOqbJoL8/#"]):
        while mq.isOpen():
            data=mq.Read()
            if data:printf(datetime.now(),data)
            time.sleep(1)
        