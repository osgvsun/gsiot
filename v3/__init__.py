# -*- coding:utf-8 -*-
import json,os,platform,sys,threading,time,traceback,base64,binascii
from multiprocessing import Process
from datetime import datetime
if __name__=="__main__":
    path=sys.path[0]
    sys.path.append(os.path.abspath(path+"/.."))
isPY2= sys.version_info>(2,0,0)
isPY3= sys.version_info>(3,0,0)
isWindows=platform.uname()[0]=="Windows"
isLinux =platform.uname()[0]=="Linux"
isSerial=False
System=None
if isPY2:
    reload(sys)  
    sys.setdefaultencoding('utf8')  
CONTENTTYPE = {
    ".txt":  "text/html;charset=UTF-8",
    ".py" :  "text/html;charset=UTF-8",
    ".code": "text/html;charset=UTF-8",
    ".md":   "text/html;charset=UTF-8",
    ".csv":  "text/html;charset=UTF-8",
    ".htm":  "text/html;charset=UTF-8",
    ".html": "text/html;charset=UTF-8",
    ".js":   "text/javascript",
    ".css":  "text/css",
    ".json": "application/json;charset=UTF-8;",
    ".jpg":  "image/jpeg",
    ".gif":  "image/gif",
    ".png":  "image/jpg",
    ".ico":  "image/x-icon",
    ".xls":  "application/x-xls",
    ".xlsx": "application/x-xlsx",
    ".mp4":  "video/mpeg4",
    ".mpeg": "video/mpg",
    ".webp": "image/webp"
}
def Singleton(cls):
    _instance = {}
    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton
def AddList(list1,list2):return  [item for item in list1 if item not in list2]+list2#list(set(list1).difference(set(list2)))+list2
def isString(data):
    default=[str]
    if isPY2:default.append(unicode)
    return type(data) in default
def isFunction(fun):return str(type(fun)).find('function')!=-1
def isInstanceMethod(fun):return str(type(fun)).find('instancemethod')!=-1
def isMethod(fun):return str(type(fun)).find('method')!=-1
def printf(*data,**kwvalue):
    value=makedata(*data,**kwvalue)
    if isPY2:
        if isWindows and isString(value):value=value.encode("gbk")
        if 'flag' in kwvalue and kwvalue['flag']==True:exec("print value,")
        else:print(value)
    elif isPY3:
        if 'flag' in kwvalue and kwvalue['flag']==True:exec("print(value,end=\" \")")
        else:print(value)
def makedata(*data,**kwvalue):
    strsplit=" "
    if 'strsplit' in kwvalue:strsplit=kwvalue["strsplit"]
    data=list(data)
    for i in range(0,len(data)):data[i]=str(data[i])
    value=strsplit.join(data)
    # except:print "errpr:", data
    return value
def gsQuerer(**argv):
    size = argv["size"] if "size" in argv else None
    stype= argv["stype"] if "stype" in argv else None
    if stype=="mproc":from multiprocessing import Queue
    elif isPY3:from queue import Queue
    elif isPY2:from Queue import Queue  
    return Queue(size)
class gsError(Exception):"""Raise when gsobject runtime Error"""
class edict(dict):
    def __init__(self,*argv,**kargv):
        dict.__init__(self)
        dict.__setitem__(self,"list",[])
        self(*argv,**kargv)
    def __call__(self,*argv,**kargv):
        for data in argv:
            if   type(data) in [dict,edict] and len(data)!=0:self.update(data)
            elif isString(data) and len(data)!=0:
                if data[0]=="{":self.update(data)
                elif data in self.list:return self[data]
            elif type(data) in [int]:return self[self.list[data]]
        self.update(kargv)
    def __trim__(self,value):
        if (isPY3 and type(value)==str):return value
        elif (isPY2 and type(value) in [str,unicode]):return value.decode("utf-8")
        else:return value
    def __setattr__(self,name,value):
        if name not in self.list and name[0]!="_":self.list.append(name)
        dict.update(self,{name:self.__trim__(value)}) 
    def __getattr__(self, name):
        if name in dict(self):return dict(self)[name]
        else:self.list.append(name)
        if name!="list":dict.__setitem__(self,name,None)
        return None
    def __getitem__(self,item):
        if isinstance(item, str) or (isPY2 and isinstance(item, unicode)):return dict.__getitem__(self,item)
        elif isinstance(item, int):return self[self.list[item]]
        elif isinstance(item, slice):
            ret=edict({key:self[key] for key in self.list[item.start:item.stop]})
            ret.list=self.list[item.start:item.stop]
            return ret        
    def __setitem__(self,name,value):
        if name not in self.list and name[0]!="_":self.list.append(name)
        dict.__setitem__(self,name,self.__trim__(value))
    def size(self):return len(self.list)
    def readdict(self,d):self(d)
    def readstr(self,data):self(data)
    def update(self,d):
        if len(d)!=0:
            # print d
            data=d
            newlist=[]
            if isString(d):
                if d=="":return
                try:data=json.loads(d)
                except:data=eval(data)
            if type(data) in [dict,edict] and len(data)!=0:
                # 再加入的数据需要考虑和之前的不重复，主要是list里不重复
                try:newlist=data["list"]
                except:newlist=[str(key) for key in data.keys()]
                # print newlist
                if self.list==[]:self.list=newlist
                else:self.list+=list(set(newlist).difference(set(self.list)))
                # 重复的数据会被覆盖，但不影响所在的位置
                for key in newlist:
                    # print key,data[key]
                    if type(data[key]) in [dict,edict]:setattr(self,key,edict(data[key]))
                    else:setattr(self,key,data[key])
    def remove(self,key):
        if key in self.list:
            self.pop(key)
            self.list.remove(key)
    def gettokeystr(self,value):
        if type(value) in [edict,dict]:ret=str(value)
        elif isString(value):ret="\""+ value.replace("\n","\\n") +"\""
        elif type(value) in [int,float,bool]:ret=str(value).replace("False","false").replace("True","true") 
        elif type(value)==list:
            ret=""
            for item in value:ret+=self.gettokeystr(item)
            ret="[{}]".format(ret[:-1])
        elif value==None:ret="None"
        else:ret="\""+str(value)+"\""
        return ret+","
    if isPY3:
        def __str__(self):return json.dumps(self,ensure_ascii=False)
        def toJsonString(self,flag=False):
            def dellist(data):
                if "list" in data:del data["list"]
                for key in data:
                    if type(data[key]) in [dict,edict]:data[key]=dellist(dict(data[key]))
                return data
            if flag:data=dellist(dict(self))
            else:data=dict(self)
            return json.dumps(data,indent=4,ensure_ascii=False)
        def toString(self):
            def dellist(data):
                if "list" in data:del data["list"]
                for key in data:
                    if type(data[key]) in [dict,edict]:data[key]=dellist(dict(data[key]))
                return data
            return json.dumps(dellist(dict(self)),ensure_ascii=False)
    elif isPY2:
        def __str__(self):return self.toString()#json.dumps(self)
        def toJsonString(self,flag=False,n=0):
            # self.list.remove("__members__")
            if "list" in self.list:self.list.remove("list")
            ret="" if flag else " "*4*(n+1)+"\"list\":{}\n".format(self.gettokeystr(self.list))
            for name in self.list:
                # print name,getattr(self,name)
                if type(getattr(self,name))==edict:data=getattr(self,name).toJsonString(flag,n+1)+","
                else:data=self.gettokeystr(self.__trim__(getattr(self,name)))
                ret+=self.__trim__("    "*(n+1)+"\"{}\":{}\n").format(name,data)
            return "{\n"+ret[:-2]+"\n"+"    "*(n)+"}"#.format(ret)
        def toString(self):
            ret=""
            value="{}"
            for name in self.list:
                if name not in ["__members__","__methods__"]:
                    if type(getattr(self,name))==edict:data=getattr(self,name).toString()+","
                    else:data=self.gettokeystr(self.__trim__(getattr(self,name)))
                    ret+=self.__trim__("\"{}\":{}").format(name,data)
                    value="{"+ret[:-1]+"}"
            return  value
# 基本的对象模型
class gsobject(object):
    def __init__(self):
        self.LogData=None 
        self.ReadData=None
        self.ErrorMsg=None
        self.modulename="gsobject"
        self.index=None
        self.stopreaddata=False
        self.lasterrormsg=""
        self.lastlogmsg=""
        self.__isopen = False
        self.__model_showlog=True
        self.__isopen_default=[True,False]
        self.__model_open = "r"
        self.__model_open_default = ["r", "w","a","b","+"] 
        self.__data_model=""
        self.__data_model_default=["bin","ascii"]
    def DataModel(self,value=None):
        if value==None:return self.__data_model
        else:self.__data_model=value
    def OpenModel(self, value=None):
        if not value:return self.__model_open  
        else:self.__model_open = value
    def isOpen(self, value=None):
        if value==None:return self.__isopen
        elif value in self.__isopen_default:self.__isopen = value
    # 是否要显示运行信息
    def showlog(self, value=None):
        if value==None:return self.__model_showlog  # value=None的时候，返回设置内容，比如object.DataModel()
        else:self.__model_showlog = value# 如果value的值在指定范围内，则变更    
    # 显示错误信息
    def errormsg(self, *data):
        if self.ErrorMsg:threading.Timer(0.3,self.ErrorMsg,args=("error",System.makedata(*data),)).start()
        else:System.Console(str(datetime.now())[:19],"module:",self.modulename,"error message:", data)
    # 显示读到/接收到的信息
    def readdata(self, data):
        try:
            if not self.ReadData:System.Console(str(datetime.now())[:19],"module:",self.modulename,"readdata:", data)
            elif self.stopreaddata==False:threading.Timer(0.1,self.ReadData,args=(data,)).start()
        except:pass
    # 显示打印/输出到日志的信息
    def logprint(self, *data):
        if self.__model_showlog==True:
            if self.LogData:threading.Timer(0.1,self.LogData,args=("info",System.makedata(*data),)).start()
            else:System.Console(str(datetime.now())[:19],"module:",self.modulename,"log:", *data)
# 基于文件的输入输出模型
class gsIO(gsobject):
    def __init__(self,*argv,**kwargv):
        gsobject.__init__(self)
        self.modulename="gsIO"
        self.showlog(True)
        self.key = kwargv["key"] if "key" in kwargv else ""
        self.dev = kwargv["dev"] if "dev" in kwargv else None
    # 以下4个函数包含了串行通信的精华，所有串行通信均存在以下4个函数
    # 在针对特定对象继承后，需重写这些函数
    def Open(self,*argv,**kwargv):self.isOpen(True) # 虚接口函数，继承后需要扩充 
    def Close(self):                                # 虚接口函数，继承后需要扩充
        self.dev.close()
        self.isOpen(False)
    def read(self):
        return self.dev.read() if self.dev else ""  # 虚接口函数，继承后需要扩充          
    def write(self, data):
        if self.dev:self.dev.write(data)  # 虚接口函数，继承后需要扩充    
# 基于设备的对象模型
class gsDevice(gsobject):pass
# 针对服务的对象模型
class gsService(gsobject,threading.Thread):
    def __init__(self):
        gsobject.__init__(self)
        threading.Thread.__init__(self)
        # self.dev=None
        self.stop = False 
        self.setDaemon(True)
        self.timeinterval=1
        self.task=None
    def Open(self):
        self.stop = False
        self.isOpen(True)
        # if self.dev:self.dev.Open()
        self.start()
    def Close(self):
        self.stop=True
        self.isOpen(False)
        self.join()
    def run(self):
        while not self.stop:
            if self.isOpen() and self.task:self.task()
            time.sleep(self.timeinterval)
class faultCode(gsobject):
    def __init__(self,*argv,**kargv):
        self.start=None
        self.cmds={}
        if len(argv)!=0:
            self.obj=argv[0]
            kargv=argv[1]
        else:self.obj=None
        self.Encore=kargv["Encore"] if "Encore" in kargv else None
        self.Except=kargv["Except"] if "Except" in kargv else None
        self.Report=kargv["Report"] if "Report" in kargv else None
        self.Success=kargv["Success"] if "Success" in kargv else None
        self.Fail=kargv["Fail"] if "Fail" in kargv else None
    def Add(self,*argv,**kargv):pass
    def Call(self,*argv,**kargv):pass
class faultFunction(gsobject):
    def __init__(self,fun,*argv,**keyargv):self(fun,*argv,**keyargv)
    def __exit__(self,exc_type,exc_value,exc_trackback):pass
    def __enter__(self):return self
    def __str__(self):return str({"value":self.value,"code":self.runflag})
    def __call__(self,fun,*argv,**keyargv):
        try:
            self.value=fun(*argv,**keyargv)
            self.runflag=1 # 1代表成功，0代表报错
        except Exception as e:
            data=""
            _, _, exc_tb = sys.exc_info()
            for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
                data+="%-23s:%s '%s' in %s()\n" % (filename, linenum, source, funcname)
            data+=str(e)
            self.value=data
            self.runflag=0
    def fail(self,fun,*argv,**keyargv):
        if self.runflag==1 and self.value in [False,None]:self(fun,*argv,**keyargv)
        return self
    def Then(self,fun,*argv,**keyargv):
        if self.runflag==1:self(fun,self.value,*argv,**keyargv)
        return self
    def Errors(self,fun,*argv,**keyargv):
        if self.runflag==0:self(fun,self.value,*argv,**keyargv)
        return self
# 事务模型
class trAnsaction(gsobject):pass
# 监控服务模型
class gsMonitor(gsService):pass
# 资源池
class PoolManager(gsobject):
    def __init__(self, **argv):
        self.member_number = argv["number"] if "number" in argv else 5
        self.member_size=argv["stype"] if "stype" in argv else None
        self.member_type= argv["stype"] if "stype" in argv else None
        self.work_queue = argv["que"] if "que" in argv else gsQuerer(size=self.member_size,stype=self.member_type)
        self.member_class=argv["class"] if "class" in argv else WorkThread
        self.workers=[]
        self.Start()
    def add_work(self, func, *args,**kargv):self.work_queue.put((func,args,kargv))
    def Start(self):
        for i in range(self.member_number):     # 生成一些线程来执行任务
            worker = self.member_class(self.work_queue)
            worker.start()
            self.workers.append(worker)
    def Close(self):
        for member in self.members:member.stop=True
        self.members=[]
class WorkThread(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.stop = False 
        self.setDaemon(True)
    def run(self):
        while not self.stop:
            func,args,keyargv = self.work_queue.get()
            func(*args,**keyargv)
            self.work_queue.task_done()
class WorkProcess(Process):
    def  __init__( self,queue,ioLock):
        super(WorkProcess,self).__init__()
        self.queue  = queue
        self.ioLock  = ioLock
        self.stop = False 
    def run(self):
        while not self.stop:
            func,args,keyargv = self.queue.get()
            self.ioLock.acquire()
            func(*args,**keyargv)
            self.ioLock.release()
        self.ioLock.acquire()
        self.ioLock.release()
class command_interpreter(gsobject):
    def __init__(self,p=None):
        self.p=p
        self.cmds={}
    def __call__(self,cmd,*options):return self.route(cmd)
    def command(self,cmd,*options):return self.route(cmd)
    def route(self, cmd=None, callback=None):
        def decorator(callback):
            # 没有键值
            if not(cmd in self.cmds):self.cmds.update({cmd:callback})
            # 有键值，但值不是list，如果函数地址不重复，则变成list并添加
            elif type(self.cmds[cmd])!=list and id(self.cmds[cmd])!=id(callback):self.cmds[cmd]=[self.cmds[cmd],callback]
            # 有键值，值是list，且不存在重复
            elif type(self.cmds[cmd])==list and len([item for item in self.cmds[cmd] if id(item)==id(callback)])==0:self.cmds[cmd].append(callback)    
        return decorator(callback) if callback else decorator
    def do(self,cmd,*argv,**keyargv):
        if cmd.find("/")!=-1:
            for item in self.cmds:
                param=()
                urls=cmd.split("/")
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
                        argv=argv+param
                        callbacks=self.cmds[item]
                        break
        else:callbacks=self.cmds[cmd] if cmd in self.cmds else None
        # 执行
        if callbacks:
            if type(callbacks)==list:return [fun(self.p,*argv,**keyargv) for fun in callbacks]
            else:return callbacks(self.p,*argv,**keyargv)
    def update(self,cmds):
        for key in cmds:
            if type(cmds[key])==list:
                for fun in cmds[key]:self.route(key,fun)
            else:self.route(key,cmds[key])
@Singleton
class system(gsobject):
    def __init__(self):
        gsobject.__init__(self)
        try:
            import serial,serial.tools.list_ports
            isSerial=True
            self.Serials=self.getUSBSerial()
        except:self.Serials=[]
        self.print_work = PoolManager()
    # 关于打印
    def getAPI(self,url,method="get",header=None,timeout=1):
        import requests
        if method=="get":
            try:
                del header["list"]
                if header:r=requests.get(url,headers=header,timeout=timeout)
                else:r=requests.get(url,timeout=timeout)
                return r
            except Exception as e:
                System.Console(e)
                return False
    def makedata(self,*data):
        strsplit=" "
        data=list(data)
        for i in range(0,len(data)):data[i]=str(data[i])
        return strsplit.join(data)
    def __printf(self,*data,**kwvalue):
        value=self.makedata(*data)
        if isPY2 and isWindows and (isPY3 and type(data)==str) or (isPY2 and type(data) in [str,unicode]):value=value.encode("gbk")
        print(value)
    def runcmd(self,cmd):return os.popen(cmd).read().strip().split("\n")
    def getUSBSerial(self):
        value=[]
        ret=edict()
        if   isWindows:value=list(serial.tools.list_ports.comports())
        elif isLinux and os.path.isfile("/dev/ttyUSB0"):value=self.runcmd("ls /dev/ttyUSB*")
        for port in value:
            if port!="" and port.replace("/dev/","") not in ret:exec("ret."+port.replace("/dev/","")+"=None")
        return ret
    def Console(self,*argv):self.print_work.add_work(self.__printf,*argv)
    def getVideoList(self):
        ret=edict()
        for devicename in os.popen("ls /dev/video*").read().strip().split("\n"):
            if len(devicename)==11:
                try:ret.update({devicename.replace("/dev/",""):os.popen("v4l2-ctl -d {} --all|grep 'Driver name'".format(devicename)).read().replace("\t","").strip().split("\n")[0].split(":")[1].strip()})
                except:pass
        return ret
    # 关于进程
    def ProcList(self,find=None):
        ret=[]
        field=['USER', 'PID', 'CPU', 'MEM', 'VSZ', 'RSS', 'TTY', 'STAT', 'START', 'TIME', 'COMMAND']
        cmd="ps -aux" if not find else "ps -aux|grep {}".format(find)
        ps=os.popen(cmd).read().strip().split("\n") if find else os.popen(cmd).read().strip().split("\n")[1:]
        l=0
        for line in ps:
            rs={}
            record=line.split()
            l+=1
            for i in range(0,len(field)):
                if i<len(field)-1:rs[field[i]]=record[i]
                elif record[i]=="zenity":rs[field[i]]="zenity --warning --no-wrap --text=SSH"
                else:rs[field[i]]=" ".join(record[i:]).replace("\"","")
            ret.append(rs)
        return ret
    def Process(self,**item):
        if "port"  in item and isLinux:
            cmd="netstat -anp|grep '0:{} '|grep LISTEN".format(item["port"]) if "ip" not in item else "netstat -anp|grep {}:{}".format(item["ip"],item["port"])
            try:return int(os.popen(cmd).read().strip().split('\n')[-1].split()[-1].split("/")[0])
            except:return False
        elif "port"  in item and isWindows:
            cmd="netstat -ano|find \":{}\"|find \"LISTENING\"".format(item["port"])
            try:return int(os.popen(cmd).read().strip().split('\n')[0].split()[-1])
            except:return False
        elif "cmd" in item and isLinux:
            cmd="ps -aux |grep "+"|grep ".join(item["cmd"].split())
            result=[x.split()[1] for x, x in enumerate(os.popen(cmd).read().strip().split('\n')) if x.find('sh -c')==-1 and x.split()[1]!=str(os.getpid())]
            if len(result)!=0: self.logprint("发现重复进程{}".format(result))
            try:return result
            except:return []
    def killProc(self,pid=False):
        if pid:
            self.logprint("删除进程{}".format(pid))
            if   isLinux:cmd="kill -9 {}"
            elif isWindows:cmd="taskkill /F /PID {}"
            if cmd!="":os.system(cmd.format(pid))
    def RemoveDuplicate(self):
        for pid in System.Process(cmd="python "+sys.argv[0])+System.Process(cmd="python "+os.path.abspath(sys.path[0])):self.killProc(pid)
        self.logprint("进程{}开始启动".format(os.getpid()))
    def getSerialModule(self,path=None):
        files=[]
        if path:serialpath=path+"/lib"
        elif __name__=="__main__":serialpath=path 
        else:
            serialpath=os.path.abspath(sys.path[-1])
            System.Console(serialpath)
            if not os.path.exists(serialpath+"/file/gsserial"):serialpath+="/lib"
        for filename in os.listdir(serialpath+"/file/gsserial"):
            if os.path.isfile(os.path.join(serialpath+"/file/gsserial",filename)):
                device=filename.split(".")[0]
                if device not in ["test","backup"] and device[:2]!="__" and not(device in files):
                    files.append(device)
        return files
    def CheckSerials(self,path=None):
        if isSerial:
            self.logprint("正在检测串口")
            for device in self.getSerialModule(path):
                module=__import__("lib.file.gsserial.{}".format(device),fromlist=['xxx'])
                o=getattr(module,"gsDevSerial")()
                result=o.CheckHardware()
                if len(result)!=0:
                    for port in result:exec("self.Serials."+port.replace("/dev/","")+"=device")
                o.Close()
                del module
            self.logprint("检测到串口模块：",self.Serials)
        return self.Serials
    def getDiskCapacity(self):
        ret=edict()
        for line in os.popen("df -hT").read().replace("Mounted on","Mounted").split("\n")[1:-1]:
            record=line.split()
            rs={}
            i=0
            for key in ['Filesystem', 'Type', 'Size', 'Used', 'Avail', 'percUse', 'Mounted']:
                rs[key]=record[i]
                i+=1
            ret["key_"+base64.b64encode(rs["Mounted"]).replace("/","_")]=edict(rs)
        return ret
if not System:System=system() 

if __name__=='__main__':
    o=edict(username="20110032",cname="李品勇",data=edict(card=123,start=123,end=123))
    printf("str(edict):",o)
    printf("toString():",o.toString())
    printf("toJsonString():",o.toJsonString())
    printf("toJsonString(True):",o.toJsonString(True))
    printf(gsQuerer())
    printf(gsQuerer(size=123,stype="mproc"))
