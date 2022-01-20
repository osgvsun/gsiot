# -*- coding:utf-8 -*-
import sys,os,platform,threading,re,hashlib
from socket import *
from copy import copy
from datetime import datetime
path=sys.path[0]
sys.path.append(path+"/../../..")
from lib import *
from lib.app.devices import DeviceUnit
from app.devices import App
from app.devices.web.route import websiteRouter
from lib.file.dbfile import dbFile
from lib.net.server import Server
from lib.net.client import Client
@Singleton
class websiteUnit(DeviceUnit):
    cmd=command_interpreter()
    def __init__(self,app,*argv):
        DeviceUnit.__init__(self,"/etc/conf/web.json",app,*argv)
        self.route=websiteRouter(self)
        self.dev=Server(host="0.0.0.0",port=9523,prototype="tcp")
        self.dev.LogData=self.web_logdata
        self.dev_task=self.Task_Daemon
        self.webroot=app.rootpath+self.cfg.website.services.webroot
        self.addr="websiteUnit"
        # self.tokens=dbFile(app.rootpath+self.cfg.website.services.tokenfile)
        self.conttype=edict()
        self.conttype.readdict({
            "txt":"text/html;charset=UTF-8",
            "md":"text/html;charset=UTF-8",
            "csv":"text/html;charset=UTF-8",
            "htm":"text/html;charset=UTF-8",
            "html":"text/html;charset=UTF-8",
            "jpg":"image/jpeg",
            "gif":"image/gif",
            "png":"image/jpg",
            "ico":"image/x-icon",
            "js":"text/javascript",
            "css":"text/css",
            "json":"application/json;charset=UTF-8",
            "xls":"application/x-xls"
        })
    def checkhardware(self):
        while True:
            pid=FindfromPort(self.cfg.website.services.port)
            if pid==False:break
            else:
                self.app.logservice("info","发现进程{}占用端口{}，正在删除进程".format(pid,self.cfg.website.services.port))
                killprocess(pid)
            time.sleep(1)
    def LoadModule(self):
        for modulename in self.cfg.website.modules.list:
            __import__("app.devices.web.{}".format(modulename),fromlist=['xxx'])
    def Open(self,*argv):
        self.checkhardware()
        self.dev.Open()
        DeviceUnit.Open(self)
        self.LoadModule()
        self.app.printf(self.route.routes)
    def web_logdata(self,data):
        self.app.logservice("info",data)
    def Task_Daemon(self):
        if self.dev.quesocket.empty()==False:
            addr,clientobj=self.dev.quesocket.get()
            client=edict()
            client.read=clientobj.recv
            client.close=clientobj.close
            client.send=clientobj.send
            # 接收对方发送的数据
            recv_data = client.read(1024).decode("utf-8") #  1024表示本次接收的最大字节数
            if len(recv_data)!=0:
                print addr,recv_data
                request=self.getRequest(recv_data)
                request.client=client
                response=edict()
                response.client=client
                response.addr=addr
                response.write=client.send
                # response.Close=
                response.headers=""
                response.code=0
                try:
                    response.body=self.route(request.url,request.method,request,response)
                    if response.body==None:
                        response.code=404
                        response.headers = "HTTP/1.1 404 not found\r\n" # 200 表示找到这个资源
                        response.headers +="Content-Type: {}\r\n".format(self.conttype.txt)
                        response.headers += "\r\n" # 空一行与body隔开
                        response.body = "<h1>sorry,file not found</h1>".encode("utf-8")
                    else:
                        response.code=200
                        zesponse.headers = "HTTP/1.1 200 OK\r\n"r
                except:
                    response.code=500
                    response.headers = "HTTP/1.1 500 Error\r\n"
                if type(response.body)==type(edict()):
                    print response.body
                    response.headers +="Content-Type: {}\r\n".format(self.conttype.json)
                    try:response.body=json.dumps(eval(response.body))
                    except:pass#response.body=json.dumps(json.loads(response.body))
                    response.body=str(response.body).replace("None","null").encode("utf-8")
                else:response.headers +="Content-Type: {}\r\n".format(self.conttype.txt)
                response.headers += "\r\n\r\n"
                response.write(response.headers)   
                response.write(response.body)   
                print "close client"
                clientobj.close()
                self.app.logservice("info","weblog client:",str(addr),">>>>>> webserver:",str((self.cfg.website.services.host.encode("ascii"),self.cfg.website.services.port)),request.method,request.url,str(response.code))
    def getRequest(self,data):
        # print data
        result=edict()
        result.webroot=self.webroot
        result.website=self        
        result.flag=False
        result.body=edict()
        result.strbody=""
        result.code=0
        result.responsedata=""
        result.url=""
        result.cmd=None
        result.param=edict()
        result.todata=data
        for line in data.splitlines():#data.split("\r\n"):
            if result.flag==False:
                if line.find("GET")==0 or line.find("POST")==0:
                    result.method=line.split()[0].lower()
                    result.url=line.split()[1]
                elif line.find("Host")==0:result.host=line.replace("Host:","").strip()
                elif line.find("Upgrade")==0:result.Upgrade=line.replace("Upgrade:","")
                elif line.find("Connection")==0:result.Connection=line.replace("Connection:","")
                elif line.find("User-Agent")!=-1:result.UserAgent=line.replace("User-Agent:","")
                elif line.find("Accept-Language")==0:result.Language=line.replace("Accept-Language:","")
                elif line.find("Accept-Encoding")==0:result.Encoding=line.replace("Accept-Encoding:","")
                elif line.find("Accept")==0:result.Accept=line.replace("Accept:","")
                elif line.find("Cache-Control")==0:result.CacheControl=line.replace("Cache-Control:","")
                elif line.find("Upgrade-Insecure-results")==0:result.UpgradeInsecureresults=line.replace("Upgrade-Insecure-results:","")
                elif line.find("Authorization")==0:result.Authorization=line.replace("Authorization:","").strip()
                elif line.find("Token")!=-1:result.Token=line.split(":")[-1]
                elif line.find("Content-Type")==0:result.ContentType=line.replace("Content-Type:","").strip()
                elif line.find("Content-Length")==0:result.ContentLength=line.replace("Content-Length","")
                elif line=="":result.flag=True
                # else:result.toString+=line+"\r\n"
            else:result.strbody+=line+"\r\n"
        # 处理url中带的参数
        if result.url!="":
            if result.url.find("?")==-1:result.filename=result.url
            else:
                result.filename=result.url.split("?")[0]
                for item in result.url.split("?")[1].split("&"):
                    key=item.split("=")[0]
                    value=item.split("=")[1]
                    exec("result.param.{}=value".format(key))
        if result.strbody!="":
            if result.ContentType=="application/x-www-form-urlencoded":
                for item in result.strbody.replace("\r\n","").split("&"):
                    key=item.split("=")[0]
                    value=item.split("=")[1]
                    exec("result.body.{}=value".format(key))
            elif result.ContentType=="application/json":result.body.readstr(result.strbody)
            # elif result.ContentType.find("multipart/form-data;")!=-1:
            #     strsplit=result.ContentType.split()[1]
            #     for item in result.strbody.replace("\r\n\r\n","=").replace("\r\n","").replace("\"","").replace("Content-Disposition: form-data; ","").split("--"+strsplit.replace("boundary=",""))[1:-1]:
            #         items=item.split("=")
            #         key=items[1]
            #         value=items[2]
            #         exec("result.body.{}=value".format(key))
                    
        
        return result
        print addr,newclient.Read()
    @cmd.command("event")
    def web_event(self,*argv,**keyargv):pass