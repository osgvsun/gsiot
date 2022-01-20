#!/usr/bin/python
# -*- coding:utf-8 -*-
import os,sys,time,json,io
from datetime import datetime
if __name__=="__main__":
    path=sys.path[0]
    sys.path.append(path+"/../../..")
from lib import *
from lib.file.gspower import gsOnOff
from app.devices import App
from lib.app.devices import DeviceUnit
from lib.file.log import logFile
from lib.file.jsonfile import ChannelFile as ChannelJsonFile
@Singleton
class powerUnit(DeviceUnit):
    cmd=command_interpreter()
    def __init__(self,app,*argv):
        DeviceUnit.__init__(self,"/app/etc/power.json",app,"/etc/conf/power.json",*argv)
        self.powerruntime=None
        if self.cfg.device.runtime!="" and self.cfg.device.switchmode=="onoff":self.powerruntime=ChannelJsonFile(self.app.rootpath+self.cfg.device.runtime,self.cfg.device.channel)
        self.addr="power"
        self.dev=gsOnOff(self.cfg.device.modulename)
        # self.dev.dev.Ports=self.app.Ports
        self.dev.ErrorMsg=self.error_log
        self.dev.LogData=self.logservice
        self.log=logFile(self.app.rootpath+self.cfg.device.logpath)
        self.isOpen=self.dev.isOpen
        self.quedata=Queue(128)
        self.timeinternel=1
        self.dev_task=self.work_job
        self.timeLength=0
    def Open(self,*argv):
        DeviceUnit.Open(self,*argv)
        try:del self.app.Ports[self.app.Ports.index(self.dev.dev.serialname)]
        except:self.app.logservice("error","在缓存中清除已用串口失败")
    def showcountdownmsg(self,times,index=None):
        self.app.logservice("info","倒计时{}秒关闭{}通道电源".format(times,index if index else ""))
        self.app("gpio.operation",**{"pinname":"buzz"})
    def On(self,index=None):
        self.app.logservice("info","正在打开{}通道电源".format(index if index else ""))
        self.dev.On(index)
    def Off(self,index=None):
        countdown=self.cfg.runtime.final
        if countdown>3:
            for i in range(0,countdown):
                self.showcountdownmsg(countdown-i,index)
                time.sleep(1)
        self.app.logservice("info","正在关闭{}通道电源".format(index if index else ""))
        self.dev.Off(index)
    def OnOff(self,index=None):
        self.app.logservice("info","正在打开{}通道门".format(index if index else ""))
        self.dev.OnOff(index)
    def logservice(self,data):pass#self.app.logservice("info",data)
    def error_log(self,data):self.app.logservice("error",data["msg"])
    def work_job(self):
        if self.isOpen():
            if self.quedata.qsize()!=0:
                data=self.quedata.get(False)
                cmd="" if "cmd" not in data else data["cmd"]
                if   cmd=="on"   :
                    self.On(data["devindex"])
                    if this.powerruntime:self.powerruntime.Set(**data)
                elif cmd=="off"  :
                    self.Off(data["devindex"])
                    if this.powerruntime:self.powerruntime.ClearChannel(self.powerruntime(data["devindex"]))
                elif cmd=="onoff":self.OnOff(data["devindex"])    
            elif self.dev.isReadElecData and self.cfg.device.readpower and self.timeLength>=self.cfg.readpower.readtimeinternel:
                data=self.dev.ReadData(0)
                # System.Console(data)
                if type(data["vol"])==float:self.log.info(data)  
                self.timeLength=-1
            self.timeLength+=1
            # 同步处理power_runtime里的信息
            # if self.powerruntime:
            #     for key in self.powerruntime.Filter(endtime=" <=str(datetime.now())[:19]",starttime=" <>''"):
            #         if key!="list":
            #             data=self.powerruntime.data[key]
            #             data.cmd="onoff" if self.cfg.device.switchmode=="touchoff" else "off"
            #             self.quedata.put(data)
    @cmd.command("power.on")
    def power_on(self,devindex):
        this=self.app.module.power
        this.quedata.put({'cmd':'on',"devindex":devindex})
        return True
    @cmd.command("power.off")
    def power_off(self,devindex):
        this=self.app.module.power
        print "poweroff recv:",{'cmd':'off',"devindex":devindex}
        this.quedata.put({'cmd':'off',"devindex":devindex})
        return True
    @cmd.command("power.onoff")
    def power_onoff(self,devindex):
        this=self.app.module.power
        print "poweroff recv:",{'cmd':'onoff',"devindex":devindex}
        this.quedata.put({'cmd':'onoff',"devindex":devindex})
        return True
    @cmd.command("power.search")
    def power_search(self):
        ret=False
        this=self.app.module.power
        if this.powerruntime:
            result=this.powerruntime.filter(endtime="")
            this.app.logservice("info",result)
            if len(result.list)!=0:ret=result[result.list[0]].devindex
        return ret
    @cmd.command("searchfromruntime")
    def power_searchfromruntime(self,argv):
        ret=False
        this=self.app.module.power
        if this.powerruntime:
            argv.update({"endtime":" > str(datetime.now())[:19]"})
            result=this.powerruntime.filter(**argv)
            if len(result.list)!=0:ret=result[result.list[0]]
        return ret
    @cmd.command("todo")
    def power_todo(self,argv):
        this=self.app.module.power
        data=edict(**argv) if type(argv) in [dict,edict] else edict(argv) if type(argv) in [str,unicode] else None
        data.cmd="onoff" if this.cfg.device.switchmode=="touchoff" else data.cmd
        if data:
            ret=copy(data["devindex"])
            if type(ret)==list:
                for devindex in data["devindex"]:
                    data["devindex"]=devindex
                    this.quedata.put(data)    
            else:this.quedata.put(data)
        return True
    # @cmd.command("event")
    # def power_event(self,*argv,**keyargv):
        # this=self.app.module.power
        # def _comp(cmd,index):
        #     self.app("event",type="alert",msg="正在进行开关操作\n{}".format(index))
        #     if cmd=="on":self.app.logservice("info","port close {} gsOnOff Switch status:{}".format(index,"off" if this.dev.Off(int(index))==False else "On"
        #     elif cmd=="off":self.app.logservice("info","port open {} gsOnOff Switch status:{}".format(index,"off" if this.dev.On(int(index))==False else "On"))
        #     elif cmd=="onoff":self.app.logservice("info","port onoff {} gsOnOff Switch status:{}".format(index,this.dev.OnOff(int(index))))
        # if "sour" in keyargv:
        #     if keyargv["sour"]=="auth" and keyargv["code"]==200:
        #         if type(keyargv["devindex"])==type([]):
        #             for index in keyargv["devindex"]:            
        #                 if "cmd" in keyargv:_comp(keyargv["cmd"],index)
        #                 elif this.dev.ReadStatus(int(index)):_comp("on",index)
        #                 else:_comp("off",index)
        #         else:
        #             self.app("event",type="alert",msg="正在进行开关操作")
        #             _comp(keyargv["cmd"],keyargv["devindex"])
                