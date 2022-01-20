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
@Singleton
class websiteUnit(DeviceUnit):
    def __init__(self,app,*argv):
        DeviceUnit.__init__(self,"/etc/conf/web.json",app,*argv)
        self.route=websiteRouter()
        self.dev=server_socket = socket(AF_INET, SOCK_STREAM)
        self.dev.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.webroot=app.rootpath+self.cfg.website.services.webroot
        self.dev_task=self.main
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
    def Open(self,*argv):
        self.checkhardware()
        DeviceUnit.Open(self,*argv)
        self.app.logservice("info","正在启动web服务({})...".format(self.cfg.website.services.port))
        self.dev.bind(('', self.cfg.website.services.port))
        self.dev.listen(128) #最多可以监听128个连接
        for modulename in self.cfg.website.modules.list:__import__("app.devices.web.{}".format(modulename),fromlist=['xxx'])
        print self.route.routes
        self.work=threading.Thread(target=self.main)
        self.work.setDaemon(True)
        self.work.start() # 开启线程
    def Close(self):
        DeviceUnit.Close(self)
        self.work.join()
    def handle_client(self,client_socket,addr):
        """为一个客户端服务"""
        # 接收对方发送的数据
        recv_data = client_socket.recv(1024).decode("utf-8") #  1024表示本次接收的最大字节数
        if len(recv_data)!=0:
            request=self.getRequest(recv_data)
            request.client=client_socket
            response=edict()
            response.client=client_socket
            response.addr=addr
            response.write=client_socket.send
            response.close=client_socket.close
            response.headers=""
            response.code=0
            response.body=self.route(request.url,request.method,request,response)
            if response.body!=None:
                if response.code==0:response.code=200
                if   response.code==200:response.headers = "HTTP/1.1 200 OK\r\n" # 200 表示找到这个资源
                elif response.code==500:response.headers = "HTTP/1.1 500 Error\r\n"
                response.body=str(response.body).replace("None","null").encode("utf-8")
                if type(response.body)==type(edict()):
                    response.headers +="Content-Type: {}\r\n".format(self.conttype.json)
                    response.body=json.dumps(eval(response.body))
                else:response.headers +="Content-Type: {}\r\n".format(self.conttype.txt)
                response.headers += "\r\n\r\n" # 空一行与body隔开
            else:
                if os.path.isdir(request.webroot+request.url):request.url+="index.html"  #访问目录时，默认访问的文件
                if os.path.exists(request.webroot+request.url)==True:
                    file=request.webroot+request.url
                    response.code=200
                    response.headers = "HTTP/1.1 200 OK\r\n" # 200 表示找到这个资源
                    # response.headers +="Content-Type: {}\r\n".format(self.conttype.txt)
                    response.headers += "\r\n" # 空一行与body隔开
                    if file[-3:]==".md":
                        print path+"/web/markdown.txt"
                        f=open(path+"/web/markdown.txt","r")
                        response.body = f.read().replace("<%=filedata%>",open(file,"r").read())
                        response.body=response.body.encode("utf-8")
                        f.close()   
                    # elif file[-5:]==".json":
                    #     f=open(file,"r")
                    #     response.headers=response.headers.encode("utf-8")
                    #     response.body = f.read()
                    #     response.body=response.body.encode("utf-8")
                    #     f.close() 
                    else:
                        response.headers=response.headers.encode("utf-8")
                        f = open(file,"rb") # 以二进制读取文件内容
                        response.body = bytearray(f.read())
                        f.close()   
                else:
                    response.code=404
                    response.headers = "HTTP/1.1 404 not found\r\n" # 200 表示找到这个资源
                    response.headers +="Content-Type: {}\r\n".format(self.conttype.txt)
                    response.headers += "\r\n" # 空一行与body隔开
                    response.body = "<h1>sorry,file not found</h1>".encode("utf-8")
                    response.body += request.toJsonString()
            response.write(response.headers)   
            response.write(response.body)   
            response.close()
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
    def main(self):
        while self.isOpen()==True:
            client_socket, clientAddr = self.dev.accept()
            try:self.handle_client(client_socket,clientAddr)
            except:pass
    
    


if __name__ == "__main__":
    appmodule=App(path+"/../..")
    serv=websiteUnit(appmodule)
    serv.Open()
    result= serv.route("/login/20110032/gvsun@123","get",1)
    if result.code==200:
        if "token" not in result.data.user:result.data.user.token=hashlib.new('md5', str(datetime.now())).hexdigest()
        self.tokens(token=result.data.user.token,datetime=str(datetime.now())[:19])
    print result.toJsonString()
    # print serv.route.routes
    # print serv.route("/login/peter/123456","get",1)
