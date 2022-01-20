# -*- coding:utf-8 -*-
from multiprocessing import Process
from inspect import getargspec
from gsiot.v3 import *
from gsiot.v3.file.log import logFile
from gsiot.v3.file.jsonfile import gsJsonFile as JsonFile
# 一个模块的基本模型
class DeviceUnit(gsobject):
    cmd=command_interpreter()
    def __init__(self,cfgfile,app,*argv):
        gsobject.__init__(self)
        # 进程主模块
        self.app=app 
        # # 通讯总线
        # self.bus=busSocket(app.busdev)
        # 本模块地址
        self.addr="deviceUnit"
        # 本模块配置文件
        self.cfgfile=app.rootpath+cfgfile
        self.cfg=JsonFile(self.cfgfile)
        # 本模块日志输出
        if type(self.cfg.device.log) in [str,unicode]:self.log=logFile(app.rootpath+self.cfg.device.log)
        # 任务启动标志
        self.istask=False
        # 单次任务运行的间隔时间
        self.timeinternel=1
        # 本模块主要操作对象
        self.dev=None
        # 针对操作对象运行的任务
        self.dev_task=None
        self.runmode="threading"
        self.dev_task_mode="once"
        # 用于主进程和当前进程之间共享数据
        self.share_data={}
        try:self.app.cmd.update(self.cmd.cmds)
        except:pass
    # 命令响应接口
    def __call__(self,cmd,*argv,**kargv):
        if cmd in self.cmd.cmds:
            fun=self.cmd.cmds[cmd]
            if str(type(fun)).find('function')!=-1:return fun(self._app,*argv,**kargv)
            elif str(type(fun)).find('instance')!=-1:return fun(*argv,**kargv)
    # 初始化self.dev         
    def Open(self,*argv):
        self.getInterface(self.addr)
        if self.dev!=None:
            try:self.dev.Open()
            except:pass
        self.isOpen(True)
        # 启动主线程
        if self.dev_task_mode=="once":target=self._Task
        elif self.dev_task:target=self.dev_task
        if self.runmode=="threading":
            self.t=threading.Thread(target=target)
            self.t.setDaemon(True)
        elif self.runmode=="process":
            self.t=Process(target=target)
            self.t.daemon = True
        self.t.start()
    # 停止self.dev
    def Close(self):
        self.isOpen(False)
        self.t.join()
    # 检查硬件环境
    def CheckHardware(self):return True    
    def getInterface(self,key):
        for name in [item for item in dir(self) if item[:len(key)]==key]:
            func=eval("self."+name)        
            path=("/"+key+"/"+name.replace(key,"")).replace("_","/").replace("//","/")
            # path = '/' + func.__name__.replace('__','/').lstrip('/')
            spec = getargspec(func)
            argc = len(spec[0]) - len(spec[3] or [])
            params=[item for item in list(spec[0][:argc]) if item!="self"]
            if len(params)!=0:path += ('/<%s>' * argc) % tuple(params)
            self.cmd.cmds.update({path:func})
            for arg in spec[0][argc:]:
                path += '/<%s>' % arg
                self.cmd.cmds.update({path:func})   
    def _Task(self):
        while self.isOpen()==True:
            try:
                if self.dev_task!=None:self.dev_task()
            except Exception,e:
                _, _, exc_tb = sys.exc_info()
                for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
                    self.app.logservice("error","%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname))
                self.app.logservice("error","msg:",e)
            time.sleep(self.timeinternel)

    