# -*- coding:utf-8 -*-
import sys,os,platform,traceback
from datetime import datetime
if __name__=='__main__':
    path=sys.path[0]
    rootpath=os.path.abspath(path+"/../..")
    sys.path.append(rootpath)
from lib import *
# from lib.app.devices.message import gvDataBus
from lib.file.gspipe import gsPipe
from lib.net import Net
from lib.app.devices import DeviceUnit
from lib.file.jsonfile import gsJsonFile
from lib.file.log import logFile
from lib.net.server.httpd import HttpServ

@Singleton
class App(DeviceUnit):
    cmd=command_interpreter()
    def __init__(self,rootpath):
        self.rootpath=os.path.abspath(rootpath)
        DeviceUnit.__init__(self,"/app/etc/release.json",self,"/etc/conf/release.json")
        self.servercfg=self.initCfgfile(rootpath+"/app/etc/server.json","/etc/conf/server.json")
        self.weblog=logFile(self.rootpath+self.cfg.services.log)
        self.dev=HttpServ(
            port=self.cfg.services.port,
            webroot=rootpath+self.cfg.services.webroot,
            domainstring=self.cfg.services.domainstring,
            logprint=self.weblogservice,
            errormsg=self.logservice
        )
        self.dev.binfiles=self.cfg.services.binfiles
        self.dev.txtfiles=self.cfg.services.txtfiles
        self.printlines=[]
        self.webroute=self.dev.route
        self.addr="app"
        #self.log=logFile(os.path.abspath(rootpath+self.cfg.))
        self.module=edict()
        self.module.screen=None
        self.image=None
        self.net=Net()
        sn=self.net(self.cfg.device.network).mac.replace(":","").upper()
        if sn!=self.cfg.version.sn or self.cfg.device.ip!=self.net(self.cfg.device.network).ip:
            self.cfg.device.ip=self.net(self.cfg.device.network).ip
            self.cfg.version.sn=sn
            self.cfg.Savefile()
        self.subproc=None#ProcessPoolManger(10)
        System.LogData=self.logservice
        self.initlogpath(self.rootpath+"/etc/log/devices")
        self.initlogpath(self.rootpath+"/etc/log/web")
        self.initlogpath(self.rootpath+"/etc/log/readcard")
        self.initlogpath(self.rootpath+"/etc/log/face")
        self.initlogpath(self.rootpath+"/etc/log/input")
        self.initlogpath(self.rootpath+"/etc/log/power")
        self.initlogpath(self.rootpath+"/etc/log/monitor")
        self.initlogpath(self.rootpath+"/web/cookie")
    def __call__(self,cmd,*argv,**keyargv):return self.cmd.do(cmd,self.app,*argv,**keyargv)
    def initlogpath(self,path):
        if os.path.isdir(path)==False:
            if os.path.isfile(path):os.system("rm -rf "+path)
            os.system("mkdir "+self.rootpath+"/etc/log/monitor")
    def LoadDevice(self):
        for adapter in self.net.nic.list:
            if adapter!="lo":self.logservice("info",adapter,":",self.net(adapter).ip)
        flag=True
        defMod=["screen"] if len([item for item in os.popen("ls /dev|grep spi").read().strip().split("\n") if item!=""])!=0 else []
        defMod+=["auth","input"]
        mods=defMod+[item for item in self.cfg.module.slots if item not in defMod]
        for module_name in mods:
            flag=True
            try:
                module = __import__(module_name) 
                setattr(self.module,module_name, getattr(module,self.cfg.module[module_name])(self))
                self.module[module_name].Open()
                flag=flag and self.module[module_name].isOpen()
                self.logservice("info","加载模块{}".format(module_name),"成功" if flag==True else "失败")
            except Exception,e:
                _, _, exc_tb = sys.exc_info()
                for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
                    self.logservice("error","%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname))
                self.logservice("error",e)
                self.logservice("info","加载模块{}".format(module_name), "失败")
        return flag
    def Open(self,*argv):
        self.logservice("info","开始启动...")
        System.RemoveDuplicate()
        System.CheckSerials(self.rootpath)
        self.logservice("info","正在启动web服务")
        self.dev.Open()
        for modulename in self.cfg.services.webmodules:
            self.logservice("info","Load {}".format(modulename))
            __import__("app.devices.web.{}".format(modulename),fromlist=['xxx'])
        keys=self.dev.route.routes["get"].keys()
        keys.sort(reverse=True)
        for item in keys:
            print item
        ret=self.LoadDevice()
        # for key in self.cmd.cmds:
        #     if type(self.cmd.cmds[key])==list:
        #         System.Console(key,":")
        #         for item in self.cmd.cmds[key]:System.Console(item)
        #     else:System.Console(key,":",self.cmd.cmds[key])
        # for key in self.module.screen.cmd.cmds:System.Console(key,":",self.module.screen.cmd.cmds[key])

        self.logservice("info","加载完成")
        self("gpio.operation",**{"pinname":"buzz"})
        self("screen.mode.screen")
    def logservice(self,*data):
        value=System.makedata(*data)
        for line in value.replace(data[0],"").split("\n"):
            System.Console(str(datetime.now())[:19],data[0],line)
            if not self.module.screen:self.printlines.append(System.makedata(line))
            if   data[0]=="error":self.log.error(line)
            else :self.log.info(line)#data[0]=="info"
    def weblogservice(self,*data):
        value=System.makedata(*data)
        for line in value.replace(data[0],"").split("\n"):
            System.Console(str(datetime.now())[:19],data[0],line)
            if not self.module.screen:self.printlines.append(System.makedata(str(datetime.now())[:19],data[0],line))
            if   data[0]=="error":self.weblog.error(line)
            else :self.weblog.info(line)
    @cmd.command("event")
    def app_event(self,*argv,**keyargv):
        pass