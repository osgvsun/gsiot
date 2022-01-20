# -*- coding:utf-8 -*-
import sys,os,threading,binascii,platform,time,socket
# from multiprocessing import Process
from datetime import datetime
path=sys.path[0]
sys.path.append(path+"/../../..")
from lib import *
import websocket 

class Client(gsIO):
    def __init__(self,ip,port=8131):
        gsIO.__init__(self,(ip,port))
        self.ip=ip
        self.port=port
        self.dev=None
        self.addr=str(datetime.now()).replace(" ","").replace(".","").replace(":","").replace("-","")
    def Open(self):
        try:
            self.dev= websocket.WebSocket()
            self.dev.connect("ws://{}:{}".format(self.ip,self.port))
            self.isOpen(True)
        except:
            self.isOpen(False)
    def Close(self):
        if self.dev!=None:self.dev.close()
    def Write(self,data):
        frame = {
            "sour":self.addr,
            "datetime":str(datetime.now())[:19],
            "cmd":data["cmd"],
            "result":data
        }
        if self.isOpen()==True:
            print("send:",frame)
            self.dev.send(json.dumps(frame))    
    def Read(self):
        message=self.dev.recv() if self.isOpen()==True else None
        if message!=None:
            frame=json.loads(message)
            return frame["result"] 

if __name__ == "__main__":
    c=Client("192.168.0.203")
    c.Open()
    c.Write({"cmd":"show library"})
    print c.Read()
    c.Close()





