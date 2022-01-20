#!/usr/bin/python
# -*- coding:utf-8 -*-
import os,sys,time
import datetime as dt
from datetime import datetime
import paho.mqtt.client as mqtt
from multiprocessing import Process
try:   from Queue import Queue
except:from queue import Queue
from copy import copy,deepcopy
path=sys.path[0]
sys.path.append(path+"/../../..")
from lib import *
from lib.file.log import logFile
from lib.file.jsonfile import JsonFile
from app import AppModule
@Singleton
class power(AppModule):
    def __init__(self,runpath):
        AppModule.__init__(self,runpath)
        self.cfg=self.config.getJsonConfigFile("power.json")
        self.devicename=self.cfg.device.modulename
        self.readcardcfg=self.config.getJsonConfigFile("readcard.json")
        self.cardlog=logFile(self.path+self.readcardcfg.readconfig.readcard_log.value)
        print self.path+self.cfg.device.logpath        
        self.powerlog=logFile(self.path+self.cfg.device.logpath)
        self.serialname=""
        self.power=None
        self.gpbuzz=None
        #最后一次有效授权
        self.lastpower=None
    def publish_power_read(self,data):
        self.lastpower=data
        self.powerlog.info(str(data))      
        if self.ipc!=None:self.ipc.event(self.event.topic.powerread,data)
    def publish_readcard_changereadcardmode(self,data):
        if self.ipc!=None:self.ipc.event(self.event.topic.readcard_changereadcardmode,data)
    def publish_alert(self,data):
        if self.ipc!=None:self.ipc.event(self.event.topic.screen,data)
    def event_receive_auth(self,topic,cardno,status,policy):
        # try:
        print str(self.cfg.data)
        # self.cfg.Savefile()
        # except:pass
        log=data=edict()
        log.devindex=data.devindex=policy.devindex
        print policy
        countdown=0
        log.starttime=policy.starttime
        log.endtime=policy.endtime
        log.username=policy.username
        log.cname=policy.cname
        log.cardnumber=policy.cardnumber
        for level in self.cfg.runtime.list:
            if level!="final":
                if self.cfg.runtime[level].countdown>countdown:
                    countdown=self.cfg.runtime[level].countdown
        delta=dt.timedelta(minutes=countdown)
        if self.lastpower.status==True:
            log.cmd=data.cmd="close"
            self.cfg.lastPaybyCard.cardnumber=self.cfg.lastPaybyCard.username=self.cfg.lastPaybyCard.cname=""
            self.cfg.lastPaybyCard.status=False
            self.cfg.lastPaybyCard.reservation=[]
        else:
            log.cmd=data.cmd="open"
            self.cfg.lastPaybyCard.cardnumber=policy.cardnumber
            self.cfg.lastPaybyCard.username=policy.username
            self.cfg.lastPaybyCard.cname=policy.cname
            p=edict()
            p.starttime=policy.starttime
            p.endtime=policy.endtime
            p.devindex=policy.devindex
            p.checktime=str(datetime.strptime(policy.endtime,'%Y-%m-%d %H:%M:%S')-delta)[:19]
            print "openpower",p
            self.cfg.lastPaybyCard.reservation.append(p)
            p=None
        self.cfg.Savefile()
        self.cardlog.recordjson(log)
        self.event_power_onoff(self.event.topic.poweronoff,data)
    def event_power_onoff(self,topic,data):
        print "event_power_onoff",topic,data
        self.cmds.put(data)
    def checkhardware(self):
        s=copy(self.appcfg.serial.ports)
        module=self.devicename
        exec("from lib.iot.gsserial.{} import gsDevSerial".format(module))
        ser=""
        for port in s:
            dev=gsDevSerial(port)
            ret=dev.test()
            if type(ret)==type(()):flag=ret[0]
            elif type(ret)==type(False):flag=ret
            if flag==True:
                self.printf("%s is    %s"%(port,module))
                ser=port
                self.cfg.Savefile()
                s.remove(port)
                break
            else:self.printf("%s isn't %s"%(port,module)) 
        if ser=="":self.printf("检测模块{}异常,请人工检查......".format(module))
        else:self.cfg.device.serials =ser
        self.appcfg.serial.ports=copy(s) 
    def power_init(self,serialname):
        if self.power==None:
            exec("from lib.iot.gspower.{} import Power".format(self.cfg.device.modulename))
            self.power=Power(serialname) 
        self.power.showlog(True)
        self.power.ErrorMsg=self.errormsg
        self.power.ReadData=self.readdata
        self.power.Open()
    def errormsg(self,data):
        data.add(datetime=str(datetime.now()))
        data.type="errormsg"
        self.publish_alert(data)
        if data.code==200:self.publish_readcard_changereadcardmode(True)
        elif data.code==500:self.publish_readcard_changereadcardmode(False)
    def readdata(self,data):
        # self.lastpower=data
        self.publish_power_read(data)
    def task(self):
        while self.isReadRuning==True:
            if self.power.isOpen()==True:
                # printf("read power:",cfg.power.isReadElecData , cfg.power.lastdata.status)
                if self.cmds.empty()==False:
                    value=self.cmds.get()
                    printf("run self.cmds",value)
                    if "cmd" in value.list:
                        if   value.cmd=="open"  :
                            ret=self.poweron()
                            self.cfg.lastPaybyCard.status=ret
                            self.logservice("info","{}{}".format("power.on.recv:",ret))
                        elif value.cmd=="close" :
                            ret=self.poweroff()
                            self.cfg.lastPaybyCard.status=not ret
                            self.logservice("info","{}{}".format("power.off.recv:",ret))
                        # self.readdata(self.power.lastdata)
                elif len(self.cfg.lastPaybyCard.reservation):
                    for p in self.cfg.lastPaybyCard.reservation:
                        d=edict()
                        d.readstr(str(p))
                        d.username=self.cfg.lastPaybyCard.username
                        # print d.username
                        d.cname=self.cfg.lastPaybyCard.cname
                        # print d.cname
                        d.cardnumber=self.cfg.lastPaybyCard.cardnumber
                        # print d
                        if str(datetime.now())[:19]>d.endtime:self.event_receive_auth("","",False,d)
                        else:
                            days=(datetime.strptime(d.endtime,'%Y-%m-%d %H:%M:%S')-datetime.now()).days
                            seconds=(datetime.strptime(d.endtime,'%Y-%m-%d %H:%M:%S')-datetime.now()).seconds
                            # print p,datetime.now(),p["endtime"], days,seconds
                            if days<=0 and seconds<=int(self.cfg.runtime.final):self.event_receive_auth("","",False,d)
                            else:
                                for level in self.cfg.runtime:
                                    if level!="list" and level!="final":
                                        # print level,type(level)
                                        # print seconds,self.cfg.runtime[level]["countdown"]*60
                                        if seconds<=self.cfg.runtime[level].countdown*60:
                                            delta=dt.timedelta(seconds=self.cfg.runtime[level].interval)
                                            if seconds<self.cfg.runtime[level].interval:pass
                                            # printf(str(datetime.now())[:19],self.cfg.lastPaybyCard.reservation.checktime,str(datetime.now())[:19]==self.cfg.lastPaybyCard.checktime)
                                            else:
                                                if str(datetime.now())[:19]==d.checktime:
                                                    msg=edict()
                                                    msg.type="showmsg"
                                                    self.gpbuzz.OnOff()
                                                    msg.text="本次预约即将结束\n还剩{}分{}秒".format(seconds/60,seconds%60)
                                                    printf("本次预约即将结束\n还剩{}分{}秒".format(seconds/60,seconds%60))
                                                    self.publish_alert(msg)
                                                    p.checktime=str(datetime.strptime(d.checktime,'%Y-%m-%d %H:%M:%S')+delta)[:19]
                                                    # try:
                                                    self.cfg.Savefile()
                                                    # except:pass
                                                    printf("下次检测时间为{}".format(p.checktime))
                                            # time.sleep(self.cfg.runtime[level]["interval"])
                                            # break
                        # self.cfg.lastPaybyCard.reservation.remove(p)
                elif self.power.isReadElecData==True:
                    data=self.power.ReadPower()
                    if self.power.lastdata.status==True:
                        if self.power.lastdatetime==None:self.power.lastdatetime=time.time()
                        elif time.time()-self.power.lastdatetime>=self.power.intervaltime:
                            if data.vol!=None:
                                self.readdata(data)
                                self.power.lastdatetime=None
                    elif self.power.lastdata.status==False and self.power.lastdatetime!=None:self.power.lastdatetime=None
                    # else:infomsg(data)
            else:
                self.power.test_error()   
            time.sleep(0.5)
    def gpobject_init(self,pin):
        if self.gpbuzz==None:
            from lib.iot.gsgpio import gsGPIO
            self.gpbuzz=gsGPIO(pin,"buzz")
        self.gpbuzz.setmode=self.readcardcfg.gpio.setmode
        self.gpbuzz.showlog(False)
        self.gpbuzz.Open()
    def remoteonoff(self,cmd):
        if len(self.cfg.RelatedEquipment)>0:
            client = mqtt.Client()
            client.connect(self.appcfg.service.mqttserver.ip, self.appcfg.service.mqttserver.port,600)
            for ip in self.cfg.RelatedEquipment:
                printf("topic:{}_onoff,publish:{}".format(ip,cmd))
                client.publish("{}_onoff".format(ip),payload=cmd,qos=0)
            client.disconnect()
    def poweron(self):
        ret=False
        self.publish_readcard_changereadcardmode(False)
        while self.power.lastdata.status==False:
            if self.cfg.device.actionmode.value=="onoff":ret=self.power.OnOff()
            else:
                ret=self.power.On()
                self.remoteonoff("on")
            data=edict()
            data.type="errormsg"
            if ret==False:
                data.code=500
                data.text="打开电源异常"
            else:
                data.code=200
                data.text="打开电源完成"
            self.publish_alert(data)
            time.sleep(0.3)
        self.publish_readcard_changereadcardmode(True)
        self.cfg.lastPaybyCard.status=self.power.lastdata.status
        return ret
    def poweroff(self):       
        msg=edict()
        msg.type="showmsg"
        self.publish_readcard_changereadcardmode(False)
        delay=self.cfg.runtime.final
        if self.power.lastdata.status==True:
            for i in range(0,delay):
                self.gpbuzz.OnOff()
                msg.text="正在关闭电源，还剩{}秒".format(delay-i)
                self.publish_alert(msg)
                time.sleep(1)
        ret=False
        while self.power.lastdata.status==True:
            ret=self.power.Off()
            self.remoteonoff("off")
            data=edict()
            data.type="errormsg"
            if ret==False:
                data.code=500
                data.text="关闭电源异常"
            else:
                data.code=200
                data.text="关闭电源完成"
            self.publish_alert(data)
            time.sleep(0.3)
        self.publish_readcard_changereadcardmode(True)
        return ret
    def Open(self,*argv):
        try:self.devicename=argv[0]
        except:self.devicename=self.cfg.device.modulename
        try:self.serialname=argv[1]
        except:self.serialname=self.cfg.device.serials   
        
        self.power_init(self.serialname)
        self.gpobject_init(self.readcardcfg.gpio.buzz)
        self.isReadRuning=True
        self.t=threading.Thread(target=self.task)
        self.t.setDaemon(True)
        self.t.start()

        self.ipc.registr(self.event.topic.poweronoff,self.event_power_onoff)
        self.ipc.registr(self.event.topic.getauth,self.event_receive_auth)

    

