# -*- coding:utf-8 -*-
import socket,traceback,hashlib
from multiprocessing import Process
from datetime import datetime
from gsiot.v3 import *
from gsiot.v3.file.jsonfile import gsJsonFile
from gsiot.v3.net.server import Server,ThreadServer
from gsiot.v3.net.client import Client
# class ErrorCode(object):
#     OK = "HTTP/1.1 200 OK\r\n"
#     NOT_FOUND = "HTTP/1.1 404 Not Found\r\n"
#     ERROR="HTTP/1.1 500 Internal Server Error\r\n"
class ResponseCode(object):
    OK=200
    NOT_FOUND=404
    ERROR=500
    MSG={
        200:('OK','请求成功接收并处理，一般响应中都会有 body'),
        201:('Created','请求已完成，并导致了一个或者多个资源被创建，最常用在 POST 创建资源的时候'),
        202:('Accepted','请求已经接收并开始处理，但是处理还没有完成。一般用在异步处理的情况，响应 body 中应该告诉客户端去哪里查看任务的状态'),
        204:('No Content','请求已经处理完成，但是没有信息要返回，经常用在 PUT 更新资源的时候（客户端提供资源的所有属性，因此不需要服务端返回）。如果有重要的 metadata，可以放到头部返回'),
        301:('Moved Permanently','请求的资源已经永久性地移动到另外一个地方，后续所有的请求都应该直接访问新地址。服务端会把新地址写在 Location 头部字段，方便客户端使用。允许客户端把 POST 请求修改为 GET。'),
        304:('Not Modified','请求的资源和之前的版本一样，没有发生改变。用来缓存资源，和条件性请求（conditional request）一起出现'),
        307:('Temporary Redirect','目标资源暂时性地移动到新的地址，客户端需要去新地址进行操作，但是 不能 修改请求的方法。'),
        308:('Permanent Redirect','和 301 类似，除了客户端 不能 修改原请求的方法'),
        400:('Bad Request','客户端发送的请求有错误（请求语法错误，body 数据格式有误，body 缺少必须的字段等），导致服务端无法处理'),
        401:('Unauthorized','请求的资源需要认证，客户端没有提供认证信息或者认证信息不正确'),
        403:('Forbidden','服务器端接收到并理解客户端的请求，但是客户端的权限不足。比如，普通用户想操作只有管理员才有权限的资源。'),
        404:('Not Found','客户端要访问的资源不存在，链接失效或者客户端伪造 URL 的时候回遇到这个情况'),
        405:('Method Not Allowed','服务端接收到了请求，而且要访问的资源也存在，但是不支持对应的方法。服务端 必须 返回 Allow 头部，告诉客户端哪些方法是允许的'),
        415:('Unsupported Media Type','服务端不支持客户端请求的资源格式，一般是因为客户端在 Content-Type 或者 Content-Encoding 中申明了希望的返回格式，但是服务端没有实现。比如，客户端希望收到 xml返回，但是服务端支持 Json'),
        429:('Too Many Requests','客户端在规定的时间里发送了太多请求，在进行限流的时候会用到'),
        500:('Internal Server Error','服务器内部错误，导致无法完成请求的内容'),
        503:('Service Unavailable','服务器因为负载过高或者维护，暂时无法提供服务。服务器端应该返回 Retry-After 头部，告诉客户端过一段时间再来重试')
    }
class Session(object):
    def __init__(self):
        self.data = dict()
        self.cook_file = None

    def getCookie(self, key):
        if key in self.data.keys():
            return self.data[key]
        return None

    def setCookie(self, key, value):
        self.data[key] = value

    def loadFromXML(self):
        import xml.dom.minidom as minidom
        root = minidom.parse(self.cook_file).documentElement
        for node in root.childNodes:
            if node.nodeName == '#text':
                continue
            else:
                self.setCookie(node.nodeName, node.childNodes[0].nodeValue)        

    def write2XML(self):
        import xml.dom.minidom as minidom
        dom = xml.dom.minidom.getDOMImplementation().createDocument(None, 'Root', None)
        root = dom.documentElement
        for key in self.data:
            node = dom.createElement(key)
            node.appendChild(dom.createTextNode(self.data[key]))
            root.appendChild(node)
        print(self.cook_file)
        with open(self.cook_file, 'w') as f:
            dom.writexml(f, addindent='\t', newl='\n', encoding='utf-8')
class websiteRouter(object):
    cmd=command_interpreter()
    def __init__(self,parent=None):
        self.routes={"get":{},"post":{}}
        self.addr="station_agent"
        self.parent=parent
        self.auth=None
        #能调用对象像调用函数那样：即能调用实例对象 并执行__call__方法中的内容，即如  self.route=websiteRouter(self)  == return self.route(path)
    def __call__(self, path,*option):return self.route(path)
    def get(self, path,*options):return self.route(path,"get")
    def post(self, path,*options):return self.route(path,"post")

    def route(self, path=None, method=None,callback=None):
        def decorator(callback):
            if method:
                if not(path in self.routes[method]):self.routes[method].update({path:callback})
            else:
                if not(path in self.routes["get"]):self.routes["get"].update({path:callback})
                if not(path in self.routes["post"]):self.routes["post"].update({path:callback})
        return decorator(callback) if callback else decorator


    def call(self,path,method,*argv,**keyargv):   
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
                    if flag==False or index>=len(urls):break
                    else:index+=1
                if flag==True:
                    argv=param+argv
                    ret=self.routes[method][item](self,*argv,**keyargv)
                    return ret
        return ret
    def do(self,cmd,method,*argv,**keyargv):
        printf(cmd,method,argv)
class HttpService(Server):
    def __init__(self,**cfg):
        self.cfg=edict(cfg)
        self.cfg.host="0.0.0.0" if "host" not in cfg else self.cfg.host if self.cfg.host!="" else "0.0.0.0"
        self.cfg.port=9999 if "port" not in cfg else self.cfg.port
        self.cfg.interval = self.cfg.interval if "interval" in cfg else 1
        self.cfg.max=self.cfg.max if "max" in cfg else 128
        self.cfg.prototype="tcp"
        Server.__init__(self,**self.cfg)
        # ThreadServer.__init__(self,**self.cfg)
        self.modulename="gsSocket.ThreadServer.HttpService"
        self.event_newclient=self.newRequest
        self.conttype=edict(CONTENTTYPE)
        self.route=websiteRouter(self)
        self.thread_pool=ThreadPoolManger(self.max,self.quesocket)
    def newclient(self,client,addr):
        if self.thread_pool:self.thread_pool.add_work(self.event_newclient, *(client,addr))
    def newRequest(self,client,addr):
        try:
            request = client.recv(1024)
            http_req = HttpRequest(addr,self.route,request,rootpath=self.cfg.webroot)
            if http_req.url!="":client.send(http_req.getResponse().encode('utf-8'))
        except Exception as e:pass
        client.Close()
class HttpServ(gsobject,threading.Thread):
    def __init__(self,**cfg):
        gsobject.__init__(self)
        threading.Thread.__init__(self)
        self.cfg=edict(cfg)
        self.host="0.0.0.0" if "host" not in cfg else self.cfg.host if self.cfg.host!="" else "0.0.0.0"
        self.port=9999 if "port" not in cfg else self.cfg.port
        self.interval = self.cfg.interval if "interval" in cfg else 1
        self.max=self.cfg.max if "max" in cfg else 128
        self.modulename="gsSocket.ThreadServer.HttpService"
        self.domainstring="domain" if "domainstring" not in cfg else self.cfg.domainstring
        self.event_newclient=self.newRequest
        self.conttype=edict(CONTENTTYPE)
        self.binfiles=[]
        self.txtfiles=[]
        self.route=websiteRouter(self)
        if "logprint" in cfg:self.LogData=cfg["logprint"]
        if "errormsg" in cfg:self.ErrorMsg=cfg["errormsg"]
    def newRequest(self,sock, addr):
        client=Client(obj=sock)
        http_req = HttpRequest(client,addr,self.route,rootpath=self.cfg.webroot)
        http_req.LogData=self.LogData
        http_req.ErrorMsg=self.ErrorMsg
        http_req.domainstring=self.domainstring
        http_req.binfiles=self.binfiles
        http_req.txtfiles=self.txtfiles
        http_req.passRequest(client.Read())
        if http_req.url and http_req.url!="" and http_req.method:
            data=http_req.getResponse()
            client.send(data if http_req.isbin else data.encode('utf-8') )
        client.Close()
    def Open(self):
        self.checkportstatus()
        self.dev = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dev.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        # self.dev.setblocking(False)
        if self.host=="0.0.0.0":self.dev.bind(('', self.port))
        else:self.dev.bind((self.host, self.port))
        self.dev.listen(self.max)
        self.thread_pool=ThreadPoolManger(self.max)
        self.logprint("{}:{} 正在监听中....".format(self.host,self.port))
        self.setDaemon(True)
        self.start()
    def run(self):
        while True:
            sock, addr = self.dev.accept()
            self.thread_pool.add_work(self.event_newclient, *(sock, addr))
    def checkportstatus(self):
        while True:
            pid=System.Process(port=self.cfg.port)
            if pid==False or pid=="":break
            elif pid!=os.getpid():
                self.logprint("info","发现进程{}占用端口{}:{}，正在删除进程".format(pid,self.host,self.port))
                System.killProc(pid)
            time.sleep(1)
class HttpRequest(gsobject):
    def __init__(self,client,addr,route,rootpath='root'):
        gsobject.__init__(self)
        self.dev=client
        self.code=ResponseCode.OK
        self.addr=addr
        self.domainstring="domain"
        self.route=route
        self.method = None
        self.url = None
        self.protocol = None
        self.head = dict()
        self.Cookie = None
        self.request_data = dict()
        self.response_head = dict()
        self.response_line = ''
        self.response_body = ''
        self.session = None
        self.RootDir =os.path.abspath(rootpath)
        self.NotFoundHtml = self.RootDir+"/404.html"
        self.CookieDir = self.RootDir+"/cookie/"
        self.defaults="index.py index.html index.htm".split()
        if not os.path.exists(self.CookieDir):os.mkdir(self.CookieDir)
        self.binfiles=[]
        self.txtfiles=[]
        self.isbin=False
        # self.passRequest(client.Read())
    def passRequestLine(self, request_line):
        header_list = request_line.split(' ')
        self.method = header_list[0].upper()
        self.url = header_list[1]
        if self.url == '/':self.url = '/index.html'
        self.protocol = header_list[2]
    def passRequestHead(self, request_head):
        head_options = request_head.split('\r\n')
        for option in head_options:
            key, val = option.split(': ', 1)
            self.head[key] = val
        if 'Cookie' in self.head:
            self.Cookie = self.head['Cookie']
    def passRequest(self, request):
        request = request.decode('utf-8')
        # self.logprint("info",request)
        if len(request.split('\r\n', 1)) != 2:return
        request_line, body = request.split('\r\n', 1)
        request_head,request_body= body.split('\r\n\r\n', 1)     # 头部信息
        self.passRequestLine(request_line)
        self.passRequestHead(request_head)
        if self.dev.readbufflength<0 if "Content-Length" not in self.head else self.head["Content-Length"]:
            self.dev.readbufflength=5000
            while True:
                data=self.dev.Read()
                request_body+=data
                if len(data)!=self.dev.readbufflength:break
        self.request_data = {}
        params=[]

        if "Content-Type" in self.head and self.head["Content-Type"]=="application/json":self.request_data.update(json.loads(request_body))
        elif "content-type" in self.head and self.head["content-type"]=="application/json":self.request_data.update(json.loads(request_body))
        else:
            params=request_body.split('&')
            if self.url.find('?') != -1:
                self.url,req=self.url.split('?', 1)
                params+=req.split('&')
            for i in params:
                if i=='':continue
                key, val = i.split('=',1)
                self.request_data[key] = val
               
        # self.logprint("request_data:",edict(self.request_data).toJsonString(True))
        try:self.response_body=self.route.call(self.url,self.method.lower(),self)    
        except Exception as e:
                data=""
                _, _, exc_tb = sys.exc_info()
                for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
                    data+="%-23s:%s \r\n\t'%s' in %s()\r\n" % (filename, linenum, source, funcname)
                data+=str(e)
                self.errormsg(data)
                self.code=ResponseCode.ERROR
                self.response_body="""
                    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
                    <title>Internal Server Error</title>
                    <h1>500 Internal Server Error</h1>
                    <p>{}</p>
                """.format(data.replace("\r\n","<br>"))
    # 只提供制定类型的静态文件
    def staticRequest(self, path):
        if not os.path.isfile(path):
            f = open(self.NotFoundHtml, 'r')
            self.code = ResponseCode.NOT_FOUND
            self.response_head['Content-Type'] = 'text/html'
            self.response_body = f.read()
        else:
            extension_name = os.path.splitext(path)[1]  # 扩展名
            if extension_name in self.binfiles:
                f = open(path, 'rb')
                self.code = ResponseCode.OK
                self.response_head['Content-Type'] = CONTENTTYPE[extension_name]
                self.response_body = f.read()
                self.isbin=True
            elif extension_name in self.txtfiles:
                f = open(path, 'r')
                self.code = ResponseCode.OK
                self.response_head['Content-Type'] =CONTENTTYPE[extension_name]
                self.response_body = f.read()
            elif extension_name == '.py':
                self.dynamicRequest(path)
            # 其他文件不返回
            else:
                f = open(self.NotFoundHtml, 'r')
                self.code = ResponseCode.NOT_FOUND
                self.response_head['Content-Type'] = 'text/html'
                self.response_body = f.read()
    def processSession(self):
        self.session = Session()
        # 没有提交cookie，创建cookie
        if self.Cookie is None:
            self.Cookie = self.generateCookie()
            cookie_file = self.CookieDir + self.Cookie
            self.session.cook_file = cookie_file
            self.session.write2XML()
        else:            
            cookie_file = self.CookieDir + self.Cookie
            self.session.cook_file = cookie_file
            if os.path.exists(cookie_file):
                self.session.loadFromXML()                
            # 当前cookie不存在，自动创建
            else:
                self.Cookie = self.generateCookie()
                cookie_file = self.CookieDir+self.Cookie
                self.session.cook_file = cookie_file
                self.session.write2XML()                
        return self.session
    def generateCookie(self):
        import time, hashlib
        cookie = str(int(round(time.time() * 1000)))
        hl = hashlib.md5()
        hl.update(cookie.encode(encoding='utf-8'))
        return cookie
    def dynamicRequest(self, path):
        # 如果找不到或者后缀名不是py则输出404
        if not os.path.isfile(path) or os.path.splitext(path)[1] != '.py':
            f = open(HttpRequest.NotFoundHtml, 'r')
            self.code = ResponseCode.NOT_FOUND
            self.response_head['Content-Type'] = 'text/html'
            self.response_body = f.read()
        else:
            # 获取文件名，并且将/替换成.
            file_path = path.split('.', 1)[0].replace('/', '.')
            self.code = ResponseCode.OK
            m = __import__(file_path)
            m.main.SESSION = self.processSession()            
            if self.method == 'POST':
                m.main.POST = self.request_data
                m.main.GET = None
            else:
                m.main.POST = None
                m.main.GET = self.request_data
            self.response_body = m.main.app()            
            self.response_head['Content-Type'] = 'text/html'
            self.response_head['Set-Cookie'] = self.Cookie
    def getResponse(self):
        # print self.RootDir + self.url,os.path.exists(self.RootDir + self.url)
        if self.response_body:
            self.code = ResponseCode.OK
            if 'Content-Type' in self.response_head:pass
            elif type(self.response_body) in [edict,dict]:
                value=edict(self.response_body)
                self.response_head['Content-Type'] = 'application/json;charset=UTF-8;'
                data=value.toJsonString(True).replace("'","\"").replace("u\"","\"").replace("None","null").replace("True","true").replace("False","false").encode("utf-8")
                if self.domainstring in self.request_data:self.response_head["Access-Control-Allow-Origin"]="*"
                self.response_body="{}{}{}{}".format(self.request_data[self.domainstring],"(",data,")") if self.domainstring in self.request_data else data
            elif 'Content-Type' not in self.response_head or self.response_head['Content-Type']=="":self.response_head['Content-Type'] = 'text/html;charset=UTF-8;'
        elif self.url and os.path.exists(self.RootDir + self.url):
            if os.path.isfile(self.RootDir + self.url):self.staticRequest(self.RootDir + self.url)
            else:
                for defaultfile in self.defaults:
                    filename=self.RootDir + self.url+"/"+defaultfile
                    # self.logprint(filename,os.path.isfile(filename))
                    if os.path.isfile(self.RootDir + self.url+"/"+defaultfile):
                        self.staticRequest(os.path.abspath(self.RootDir + self.url+"/"+defaultfile))
                        break
        elif self.url:self.staticRequest(self.RootDir + self.url)
        self.logprint(self.addr[0],self.addr[1],self.method,self.url,self.code)

        data="HTTP/1.1 {} {}\r\n".format(self.code,ResponseCode.MSG[self.code][0])+self.dict2str(self.response_head)
        if self.response_body:data+="Content-Length: {}\r\n\r\n".format(len(self.response_body))+self.response_body
        else:data+=""
        return data
    # 将字典转成字符串
    def dict2str(self,d):
        s = ''
        if d:
            for i in d:s = s + i+': '+d[i]+'\r\n'
        return s
if __name__ == "__main__":
    def LogData(*data):System.Console(str(datetime.now()),*data)
    http=HttpServ(port=80,webroot=os.path.abspath(path+"/../../../web"),logprint=LogData)
    http.Open()
    @http.route.get("/username/<username>")
    def getusername(route,username,request):
        return {"result":"Hello {}".format(username)}
    while True:time.sleep(1)
