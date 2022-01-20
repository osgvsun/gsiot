
# -*- coding:utf-8 -*-
import socket
# from multiprocessing import Process
from datetime import datetime
from websocket_server import WebsocketServer
from gsiot.v3 import *
from gsiot.v3.net.server import *

class webSockServer(gsIO):
    def __init__(self,port,ip="0.0.0.0"):
        gsIO.__init__(self,(ip,port))
        self.ip=ip
        self.port=port
        self.istask=False
        self.cmd=command_interpreter()
        self.container=None
        self.new_client=None
        self.client_left=None
        self.message_received=None
    def __call__(self,cmdline,*argv,**keyargv):return self.do(cmdline,*argv,**keyargv)
    def do(self,cmdline,*argv,**keyargv):
        return self.cmd(cmdline,self if self.container==None else self.container,*argv,**keyargv)
    def Open(self):
        self.dev= WebsocketServer(self.port,self.ip)
        self.dev.set_fn_new_client(self.new_client)
        self.dev.set_fn_client_left(self.client_left)
        self.dev.set_fn_message_received(self.message_received)
        self.t=threading.Thread(target=self.dev.run_forever)
        if __name__ != "lib.net.server.webserver.websocket" and __name__!="__main__":self.t.setDaemon(True)
        self.t.start() 
        return True
    def Close(self):
        self.dev.close()
        self.isOpen(False)
        # except:pass #self.logservice("info","")
    def send(self,msg,client=None):
         # 组包
        if msg!=None:
            frame=edict()
            if "cmd" in msg:frame.cmd=msg.cmd
            if "type" in msg:frame.type=msg["type"]
            frame.result=msg
            frame.datetime=str(datetime.now())[:19]
            if client!=None:
                frame.id=client["id"]
                try:self.dev.send_message(client,str(frame).replace("None","null").replace("True","true").replace("False","false").replace("u'","\"").replace("'","\""))
                except:print str(frame)
            else:self.dev.send_message_to_all(str(frame).replace("None","null").replace("True","true").replace("False","false").replace("u'","\"").replace("'","\""))
if __name__ == "__main__":
    serv=webCommand(9503)
    print serv.cmd.cmds
    serv.Open()
