# # -*- coding:utf-8 -*-
# import sys,os,platform,threading,re,hashlib
# from socket import *
# from copy import copy
# from datetime import datetime
# path=sys.path[0]
# sys.path.append(path+"/../../..")
# from lib import *
# from lib.app.devices import DeviceUnit
# from app.devices import App
# from app.devices.web.route import websiteRouter
# from lib.file.dbfile import dbFile
# from lib.net.server import Server
# from lib.net.client import Client
# @Singleton
# class websiteUnit(DeviceUnit):
#     cmd=command_interpreter()
#     def __init__(self,app,*argv):
#         DeviceUnit.__init__(self,"/etc/conf/web.json",app,*argv)
#         self.dev=server_socket = socket(AF_INET, SOCK_STREAM)
#         self.dev.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
#         self.webroot=app.rootpath+self.cfg.website.services.webroot
#         # self.dev_task=self.main
#         self.addr="websiteUnit"
#         self.webroot=app.rootpath+self.cfg.website.services.webroot
#         # self.tokens=dbFile(app.rootpath+self.cfg.website.services.tokenfile)
#         self.conttype=edict(CONTENTYPE)
#         self.route=websiteRouter(self)
#         self.responses_code= {
#             100: ('Continue', 'Request received, please continue'),
#             101: ('Switching Protocols',
#                 'Switching to new protocol; obey Upgrade header'),

#             200: ('OK', 'Request fulfilled, document follows'),
#             201: ('Created', 'Document created, URL follows'),
#             202: ('Accepted',
#                 'Request accepted, processing continues off-line'),
#             203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
#             204: ('No Content', 'Request fulfilled, nothing follows'),
#             205: ('Reset Content', 'Clear input form for further input.'),
#             206: ('Partial Content', 'Partial content follows.'),

#             300: ('Multiple Choices',
#                 'Object has several resources -- see URI list'),
#             301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
#             302: ('Found', 'Object moved temporarily -- see URI list'),
#             303: ('See Other', 'Object moved -- see Method and URL list'),
#             304: ('Not Modified',
#                 'Document has not changed since given time'),
#             305: ('Use Proxy',
#                 'You must use proxy specified in Location to access this '
#                 'resource.'),
#             307: ('Temporary Redirect',
#                 'Object moved temporarily -- see URI list'),

#             400: ('Bad Request',
#                 'Bad request syntax or unsupported method'),
#             401: ('Unauthorized',
#                 'No permission -- see authorization schemes'),
#             402: ('Payment Required',
#                 'No payment -- see charging schemes'),
#             403: ('Forbidden',
#                 'Request forbidden -- authorization will not help'),
#             404: ('Not Found', 'Nothing matches the given URI'),
#             405: ('Method Not Allowed',
#                 'Specified method is invalid for this resource.'),
#             406: ('Not Acceptable', 'URI not available in preferred format.'),
#             407: ('Proxy Authentication Required', 'You must authenticate with '
#                 'this proxy before proceeding.'),
#             408: ('Request Timeout', 'Request timed out; try again later.'),
#             409: ('Conflict', 'Request conflict.'),
#             410: ('Gone',
#                 'URI no longer exists and has been permanently removed.'),
#             411: ('Length Required', 'Client must specify Content-Length.'),
#             412: ('Precondition Failed', 'Precondition in headers is false.'),
#             413: ('Request Entity Too Large', 'Entity is too large.'),
#             414: ('Request-URI Too Long', 'URI is too long.'),
#             415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
#             416: ('Requested Range Not Satisfiable',
#                 'Cannot satisfy request range.'),
#             417: ('Expectation Failed',
#                 'Expect condition could not be satisfied.'),

#             500: ('Internal Server Error', 'Server got itself in trouble'),
#             501: ('Not Implemented',
#                 'Server does not support this operation'),
#             502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
#             503: ('Service Unavailable',
#                 'The server cannot process the request due to a high load'),
#             504: ('Gateway Timeout',
#                 'The gateway server did not receive a timely response'),
#             505: ('HTTP Version Not Supported', 'Cannot fulfill request.')
#         }
#     def getheaders(self,protocol,code):return "{} {} {}\r\n".format(protocol,code,self.responses_code[code][0])
#     def checkhardware(self):
#         while True:
#             pid=FindfromPort(self.cfg.website.services.port)
#             if pid==False or pid=="":break
#             else:
#                 self.app.logservice("info","发现进程{}占用端口{}，正在删除进程".format(pid,self.cfg.website.services.port))
#                 killprocess(pid)
#             time.sleep(1)
#     def Open(self,*argv):
#         self.checkhardware()
#         DeviceUnit.Open(self,*argv)
#         self.app.logservice("info","正在启动web服务({})...".format(self.cfg.website.services.port))
#         self.dev.bind(('', self.cfg.website.services.port))
#         self.dev.listen(128) #最多可以监听128个连接
#         self.LoadModule()
#         self.work=threading.Thread(target=self.main)
#         if __name__!="__main__":self.work.setDaemon(True)
#         self.work.start() # 开启线程
#     def Close(self):
#         DeviceUnit.Close(self)
#         self.work.join()
#     def handle_client(self,client_socket,addr):
#         """为一个客户端服务"""
#         # 接收对方发送的数据
#         recv_data = client_socket.recv(1024).decode("utf-8") #  1024表示本次接收的最大字节数
#         if len(recv_data)!=0:
#             request=self.getRequest(recv_data)
#             request.client=client_socket
#             response=edict()
#             response.client=client_socket
#             response.addr=addr
#             response.write=client_socket.send
#             response.close=client_socket.close
#             response.headers=""
#             response.code=0
#             response.body=self.route(request.url,request.method,request,response)
#             if response.body!=None:
#                 if response.code==0:response.code=200
#                 if   response.code==200:response.headers = "HTTP/1.1 200 OK\r\n" # 200 表示找到这个资源
#                 elif response.code==500:response.headers = "HTTP/1.1 500 Error\r\n"
#                 if type(response.body)==type(edict()):
#                     self.app.printf("web request:",response.body)
#                     response.headers +="Content-Type: {}\r\n".format(self.conttype.json)
#                     response.body=str(response.body).replace("None","null").encode("utf-8")
#                 else:response.headers +="Content-Type: {}\r\n".format(self.conttype.txt)
#                 response.headers += "\r\n\r\n" # 空一行与body隔开
#             else:
#                 if os.path.isdir(request.webroot+request.url):request.url+="index.html"  #访问目录时，默认访问的文件
#                 if os.path.exists(request.webroot+request.url)==True:
#                     file=request.webroot+request.url
#                     response.code=200
#                     response.headers = "HTTP/1.1 200 OK\r\n" # 200 表示找到这个资源
#                     # response.headers +="Content-Type: {}\r\n".format(self.conttype.txt)
#                     response.headers += "\r\n" # 空一行与body隔开
#                     if file[-3:]==".md":
#                         print path+"/web/markdown.txt"
#                         f=open(path+"/web/markdown.txt","r")
#                         response.body = f.read().replace("<%=filedata%>",open(file,"r").read())
#                         response.body=response.body.encode("utf-8")
#                         f.close()   
#                     else:
#                         response.headers=response.headers.encode("utf-8")
#                         f = open(file,"rb") # 以二进制读取文件内容
#                         response.body = bytearray(f.read())
#                         f.close()   
#                 else:
#                     response.code=404
#                     response.headers = "HTTP/1.1 404 not found\r\n" # 200 表示找到这个资源
#                     response.headers +="Content-Type: {}\r\n".format(self.conttype.txt)
#                     response.headers += "\r\n" # 空一行与body隔开
#                     response.body = "<h1>sorry,file not found</h1>".encode("utf-8")
#                     response.body += request.toJsonString()
#             response.write(response.headers)   
#             response.write(response.body)   
#             response.close()
#             self.app.logservice("info","weblog client:",str(addr),">>>>>> webserver:",str((self.cfg.website.services.host.encode("ascii"),self.cfg.website.services.port)),request.method,request.url,str(response.code))
#     def getRequest(self,data):
#         headers=data.split("\r\n\r\n")[0]
#         content=data.split("\r\n\r\n")[1]
#         result=edict()
#         result.webroot=self.webroot
#         result.website=self        
#         result.flag=False
#         result.body=edict()
#         result.strbody=""
#         result.code=0
#         result.responsedata=""
#         result.url=""
#         result.cmd=None
#         result.param=edict()
#         for line in headers.splitlines():#data.split("\r\n"):
#             if result.flag==False:
#                 if line.find("GET")==0 or line.find("POST")==0:
#                     result.method=line.split()[0].lower()
#                     result.url=line.split()[1]
#                 elif line.find("Host")==0:result.host=line.replace("Host:","").strip()
#                 elif line.find("Upgrade")==0:result.Upgrade=line.replace("Upgrade:","")
#                 elif line.find("Connection")==0:result.Connection=line.replace("Connection:","")
#                 elif line.find("User-Agent")!=-1:result.UserAgent=line.replace("User-Agent:","")
#                 elif line.find("Accept-Language")==0:result.Language=line.replace("Accept-Language:","")
#                 elif line.find("Accept-Encoding")==0:result.Encoding=line.replace("Accept-Encoding:","")
#                 elif line.find("Accept")==0:result.Accept=line.replace("Accept:","")
#                 elif line.find("Cache-Control")==0:result.CacheControl=line.replace("Cache-Control:","")
#                 elif line.find("Upgrade-Insecure-results")==0:result.UpgradeInsecureresults=line.replace("Upgrade-Insecure-results:","")
#                 elif line.find("Authorization")==0:result.Authorization=line.replace("Authorization:","").strip()
#                 elif line.find("Token")!=-1:result.Token=line.split(":")[-1]
#                 elif line.find("Content-Type")==0:result.ContentType=line.replace("Content-Type:","").strip()
#                 elif line.find("Content-Length")==0:result.ContentLength=line.replace("Content-Length","")
#                 elif line=="":result.flag=True
#                 # else:result.toString+=line+"\r\n"
#             else:result.strbody+=line+"\r\n"
#         # 处理url中带的参数
#         if result.url!="":
#             if result.url.find("?")==-1:result.filename=result.url
#             else:
#                 result.filename=result.url.split("?")[0]
#                 for item in result.url.split("?")[1].split("&"):
#                     key=item.split("=")[0]
#                     value=item.split("=")[1]
#                     exec("result.param.{}=value".format(key))
#         if result.strbody!="":
#             if result.ContentType=="application/x-www-form-urlencoded":
#                 for item in result.strbody.replace("\r\n","").split("&"):
#                     key=item.split("=")[0]
#                     value=item.split("=")[1]
#                     exec("result.body.{}=value".format(key))
#             elif result.ContentType=="application/json":result.body.readstr(result.strbody)
#         return result
#     def main(self):
#         while self.isOpen()==True:
#             client_socket, clientAddr = self.dev.accept()
#             try:
#                 new_thread = threading.Thread(target=self.handle_client,args=(client_socket,clientAddr,))
#                 new_thread.setDaemon(True)
#                 new_thread.start() # 开启线程    
#             except:client_socket.close()
#     def LoadModule(self):
#         for modulename in self.cfg.website.modules.list:__import__("app.devices.web.{}".format(modulename),fromlist=['xxx'])
#         # for cmd in self.route.routes["get"]:print cmd,self.route.routes["get"][cmd]
#     @cmd.command("event")
#     def web_event(self,*argv,**keyargv):pass