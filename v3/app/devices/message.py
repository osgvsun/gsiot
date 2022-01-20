# -*- coding:utf-8 -*-
from gsiot.v3 import *

class gvDataBus(gsobject):
    def __init__(self):
        gsobject.__init__(self)
        self.units=edict()
    def connect(self,addr,unit):self.subscribe(addr,unit.switch_receive)
    def sendmessage(self,data):self.publish(data.dest,data)
    def subscribe(self,topic,fun):
        if topic not in self.units.list:exec("self.units.{}=[]".format(topic))
        node=self.units[topic]
        node.append(fun)
    def publish(self,topic,*argv):
        if topic in self.units.list:
            for fun in self.units[topic]:
                threading.Thread(target=fun,args=argv).start()

class busSocket(gsobject):
    def __init__(self,dev=None):
        gsobject.__init__(self)
        self.dev=dev if dev!=None else gvDataBus()
        self.recv=Queue(128)
    def switch_receive(self,data):self.recv.put(data)
    def Open(self,topic=None):
        if topic!=None:self.topic=topic
        else:self.topic=str(datetime.now()).replace(" ","").replace("-","").replace(":","").replace(".","")
        self.dev.connect(self.topic,self)
    def Write(self,topic,data):
        msg=edict()
        msg.sour=self.topic
        msg.dest=topic
        msg.result=data 
        self.dev.sendmessage(msg)
    def Read(self):
        msg=self.ReadAllInformation()
        try:ret=(msg.sour,msg.result)
        except:ret=None
        return ret
    def ReadAllInformation(self):
        def __read__():
            while True:
                if self.recv.empty()==False:break
                time.sleep(0.01)   #是否延时需要通过实际验证，看实际运行效果才能决定
        t=threading.Thread(target=__read__)
        t.setDaemon(True)
        t.start()
        t.join()
        return self.recv.get()
    def bind(self,topic,fun):self.dev.subscribe(topic,fun)
    def public_data(self,addr,data,fn=None):
        if type(data)!=type(edict()):
            value=edict()
            value.result=data
        else:value=data
        value.sour=self.topic
        value.dest=addr
        value.datetime=str(datetime.now())[:19]
        self.dev.sendmessage(value)