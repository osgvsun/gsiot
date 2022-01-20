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
@Singleton
class websiteUnit(DeviceUnit):
    def __init__(self,app,*argv):
        DeviceUnit.__init__(self,"/etc/conf/web.json",app,*argv)
        self.route=websiteRouter(self)
        print self.cfg.website.services.webroot
        self.webroot=self.app.rootpath+self.cfg.website.services.webroot
        self.dev=Server(host="192.168.1.11",port=self.cfg.website.services.port,runtime="multi threading",prototype="tcp")
        self.dev.event_newclient=self.http_handle
        self.dev_task=None
        self.addr="websiteUnit"
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
        self.responses_code= {
            100: ('Continue', 'Request received, please continue'),
            101: ('Switching Protocols',
                'Switching to new protocol; obey Upgrade header'),

            200: ('OK', 'Request fulfilled, document follows'),
            201: ('Created', 'Document created, URL follows'),
            202: ('Accepted',
                'Request accepted, processing continues off-line'),
            203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
            204: ('No Content', 'Request fulfilled, nothing follows'),
            205: ('Reset Content', 'Clear input form for further input.'),
            206: ('Partial Content', 'Partial content follows.'),

            300: ('Multiple Choices',
                'Object has several resources -- see URI list'),
            301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
            302: ('Found', 'Object moved temporarily -- see URI list'),
            303: ('See Other', 'Object moved -- see Method and URL list'),
            304: ('Not Modified',
                'Document has not changed since given time'),
            305: ('Use Proxy',
                'You must use proxy specified in Location to access this '
                'resource.'),
            307: ('Temporary Redirect',
                'Object moved temporarily -- see URI list'),

            400: ('Bad Request',
                'Bad request syntax or unsupported method'),
            401: ('Unauthorized',
                'No permission -- see authorization schemes'),
            402: ('Payment Required',
                'No payment -- see charging schemes'),
            403: ('Forbidden',
                'Request forbidden -- authorization will not help'),
            404: ('Not Found', 'Nothing matches the given URI'),
            405: ('Method Not Allowed',
                'Specified method is invalid for this resource.'),
            406: ('Not Acceptable', 'URI not available in preferred format.'),
            407: ('Proxy Authentication Required', 'You must authenticate with '
                'this proxy before proceeding.'),
            408: ('Request Timeout', 'Request timed out; try again later.'),
            409: ('Conflict', 'Request conflict.'),
            410: ('Gone',
                'URI no longer exists and has been permanently removed.'),
            411: ('Length Required', 'Client must specify Content-Length.'),
            412: ('Precondition Failed', 'Precondition in headers is false.'),
            413: ('Request Entity Too Large', 'Entity is too large.'),
            414: ('Request-URI Too Long', 'URI is too long.'),
            415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
            416: ('Requested Range Not Satisfiable',
                'Cannot satisfy request range.'),
            417: ('Expectation Failed',
                'Expect condition could not be satisfied.'),

            500: ('Internal Server Error', 'Server got itself in trouble'),
            501: ('Not Implemented',
                'Server does not support this operation'),
            502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
            503: ('Service Unavailable',
                'The server cannot process the request due to a high load'),
            504: ('Gateway Timeout',
                'The gateway server did not receive a timely response'),
            505: ('HTTP Version Not Supported', 'Cannot fulfill request.')
        }
    def getheaders(self,protocol,code):return "{} {} {}\r\n".format(protocol,code,self.responses_code[code][0])
    def checkhardware(self):
        while True:
            pid=FindfromPort(self.cfg.website.services.port)
            if pid==False or pid=="":break
            else:
                self.app.logservice("info","发现进程{}占用端口{}，正在删除进程".format(pid,self.cfg.website.services.port))
                killprocess(pid)
            time.sleep(1)
    def Open(self,*argv):
        self.checkhardware()
        DeviceUnit.Open(self,*argv)
        # self.dev.Open()
        for modulename in self.cfg.website.modules.list:__import__("app.devices.web.{}".format(modulename),fromlist=['xxx'])
        for key in self.route.routes["get"]:
            print key,self.route.routes["get"][key]
    def Close(self):
        DeviceUnit.Close(self)
        self.work.join()
    def http_handle(self,addr,client):
        """为一个客户端服务"""
        # 接收对方发送的数据
        data=client.recv(8096)
        request=self.getRequest(addr,data)
        request.client=client
        print request.toJsonString()
        response=edict()
        response.client=client
        response.addr=addr
        response.write=client.send
        response.close=client.close
        response.headers=""
        response.body=""
        response.conttype=self.conttype.txt
        response.code=0
        if "method" in request:
            # websocket
            if request.Connection=="Upgrade" and request.Upgrade=="websocket":
                response.headers = self.getheaders(101)
                response.headers+="Upgrade: websocket\r\n"
                response.headers+="Connection: {}\r\n".format(request.Connection)
                response.headers+="Sec-WebSocket-Accept: {}\r\n".format(base64.b64encode(hashlib.sha1(request.SecWebSocketKey+"258EAFA5-E914-47DA-95CA-C5AB0DC85B11".encode('utf-8')).digest()))
                response.headers+="sec-WebSocket-Location: {}\r\n".format(request.Origin.replace("http://","ws://"))
                print "send:",response.headers
                client.sendall(bytes(response.headers))
                client.send("welcome to you")
            # http
            else:
                # try:
                response.body=self.route(request.url,request.method,request,response)
                if response.body!=None:
                    if type(response.body)==type(edict()):
                        response.conttype=self.conttype.json
                        response.body=str(response.body).replace("None","null").encode("utf-8")
                    else:
                        response.conttype=self.conttype.txt
                        response.body=response.body.encode("utf-8")
                elif request.method=="get" and os.path.isfile(self.webroot+request.filename)==True:
                    file=self.webroot+request.filename
                    response.code=200
                    response.conttype=self.conttype.txt
                    if file[-3:]==".md":
                        print path+"/web/markdown.txt"
                        f=open(path+"/web/markdown.txt","r")
                        response.body = f.read().replace("<%=filedata%>",open(file,"r").read())
                        response.body=response.body.encode("utf-8")
                        f.close()   
                    else:
                        response.headers=response.headers.encode("utf-8")
                        f = open(file,"rb") # 以二进制读取文件内容
                        response.body = bytearray(f.read())
                        f.close()   
                # elif request.method=="post":
                #     print request.toJsonString()
                #     print data
                #     response.code=500
                elif response.code==500 and response.body!=None:
                    html="""
                    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
                    <title>Internal Server Error</title>
                    <h1>500 Internal Server Error</h1>
                    <p>{}</p>
                    """
                    response.body=htmll.format(response.body)
                else:
                    response.code=404
                    response.body="""
                    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
                    <title>404 Not Found</title>
                    <h1>Not Found</h1>
                    <p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
                    """

                response.write(self.getheaders(request.protocol,response.code))  
                response.write("Content-Type: {}\r\n".format(response.conttype))
                response.write("\r\n") 
                response.write(response.body) 
                self.logprint(request.method,request.url,response.code)
                client.close()
        
            self.app.logservice("info","weblog client:",str(addr),">>>>>> webserver:",str((self.cfg.website.services.host.encode("ascii"),self.cfg.website.services.port)),request.method,request.url,str(response.code))
    def getRequest(self,addr,data):
        try:
            headers=data.split("\r\n\r\n")[0]
            contect=data.split("\r\n\r\n")[1]
        except:contect=""
        result=edict()
        result.remoteaddr=addr
        result.website=self        
        result.flag=False
        result.body=edict()
        result.strbody=""
        result.code=0
        result.responsedata=""
        result.url=""
        result.cmd=None
        result.param=edict()
        result.content=contect.replace("\r","0r").replace("\n","0n")
        result.file=[]
        result.todata=data
        for line in headers.splitlines():
            record=line.split()
            if record[0].lower()=="get" or record[0].lower()=="post":
                result.method=record[0].lower()
                result.url=record[1]
                result.protocol=record[2]
            elif record[0]=="Content-Type:":
                result.ContentType=record[1].strip()
                for item in record[2:]:
                    try:exec("result."+item.replace("=","=\"")+"\"")
                    except:pass
            elif record[0]!="":exec("result.{}'{}'".format(record[0].replace(":","=").replace("-","")," ".join(record[1:])))
        # 处理url中带的参数
        if result.url!="":
            if result.url.find("?")==-1:result.filename=result.url
            else:
                result.filename=result.url.split("?")[0]
                for item in result.url.split("?")[1].split("&"):
                    key=item.split("=")[0]
                    value=item.split("=")[1]
                    exec("result.param.{}=value".format(key))
                result.url=result.filename
        if contect!="":
            if result.ContentType=="application/x-www-form-urlencoded":
                for item in contect.replace("\r\n","").split("&"):
                    key=item.split("=")[0]
                    value=item.split("=")[1]
                    exec("result.body.{}=value".format(key))
            elif result.ContentType=="application/json":result.body.readstr(result.strbody)
            elif result.ContentType=="text/plain":result.body=eval(contect)
            elif "boundary" in result.list:
                data=contect.split(result.boundary)[1]
        # print result.toJsonString()
        return result
    


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
