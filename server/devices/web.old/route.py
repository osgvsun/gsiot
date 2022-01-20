# -*- coding:utf-8 -*-
import sys,os,platform,threading
from datetime import datetime
path=sys.path[0]
sys.path.append(path+"/../../..")
from lib import *
from lib.net.client.mqttclient import mqSocket
from lib.file.jsonfile import gsJsonFile
from lib.file.dbfile import dbFile
@Singleton
class websiteRouter(object):
    cmd=command_interpreter()
    def __init__(self,parent=None):
        self.routes={"get":{},"post":{}}
        self.addr="station_agent"
        self.parent=parent
        # self.mqServ=mqSocket(("127.0.0.1",1883))
        # self.mqServ.Open(self.addr)
        self.tmpBuff=JsonFile(path+"/../etc/conf/online.json")
        self.cfg=JsonFile(os.path.abspath(path+"/../etc/conf/web.json"))
        self.webdataroot="/data/inspection"
        self.auth=None
    def get(self, path,*options):
        return self.route("get",path)
    def post(self, path,*options):
        return self.route("post",path)
    def route(self,method, path=None, callback=None):
        def decorator(callback):
            if not(path in self.routes[method]):
                self.routes[method].update({path:callback})
        return decorator(callback) if callback else decorator
    def __call__(self,path,method,*argv,**keyargv):  
        ret=None
        for item in self.routes[method]:
            param=()
            urls=path.split("/")
            rs=item.split("/")
            if len(rs)==len(urls):
                flag=False
                index=1
                for folder in urls[1:]:
                    flag=folder==rs[index] 
                    if rs[index][0]=="<" and rs[index][-1]==">":
                        flag=True
                        param+=(folder,) 
                    #print folder,rs[index],folder==rs[index],param           
                    if flag==False or index>=len(urls):break
                    else:index+=1
                # print path,item,flag,param
                if flag==True:
                    argv=param+argv
                    ret=self.routes[method][item](self,*argv,**keyargv)
                    # print ret
                    return ret
        return ret
    def do(self,cmd,method,*argv,**keyargv):
        print cmd,method,argv
