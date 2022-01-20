#!/usr/bin/python
# -*- coding:utf-8 -*-
import os,sys,time,json
from datetime import datetime
if __name__=="__main__":
    path=sys.path[0]
    sys.path.append(path+"/../../..")
from lib import *
from app.devices import App
from lib.app.devices import DeviceUnit
from lib.file.gspipe import gsPipe
from lib.net.client.mqttclient import mqSocket
@Singleton
class InputUnit(DeviceUnit):
    cmd=command_interpreter()
    def __init__(self,app,*argv):
        DeviceUnit.__init__(self,"/app/etc/input.json",app,"/etc/conf/input.json",*argv)
        self.timeinternel=self.cfg.mqtt.timeinternel
        pipecfg=self.cfg.pipe
        pipecfg.ReadData=self.pipe_received
        self.pipe=None
        self.websocket=None
        self.clients=None
        self.gpio=None
        # System.Console(self.app.servercfg.server.iotserver.host,self.app.servercfg.server.iotserver.port.mqServer)
        self.mq=mqSocket((self.app.servercfg.server.iotserver.host,self.app.servercfg.server.iotserver.port.mqServer)) if self.cfg.device.mqtt else None
    def __call__(self,d):
        result=None
        if type(d) in [str,unicode]:
            if d=="":return False
            data=edict(d)
        elif type(d) in [edict,dict]:data=dict(d)
        if "list" in data:del data["list"]
        cmd=data["cmd"]
        del data["cmd"]
        self.logservice("info",json.dumps(data))
        result=self.app.cmd.do(cmd,self.app,**data)
        if type(result) in [dict,edict]:result=edict(result)
        else:result=edict({"result":result})
        return result
    def Open(self,*argv):
        if isLinux and self.cfg.device.pipe:
            pipecfg=self.cfg.pipe
            pipecfg.ReadData=self.pipe_received
            self.pipe=gsPipe(pipecfg)
            self.pipe.showlog(False)
            self.pipe.open()
        if isLinux and self.cfg.gpio:
            module=__import__(self.cfg.gpio.modname,fromlist=['xxx'])
            try:self.gpio=getattr(module,"GPIOCtrl")
            except:self.gpio=getattr(module,"gsGPIO")
            for key in self.cfg.gpio.lists:
                node=eval("self.cfg.gpio."+key)
                node.obj=self.gpio(node.pin)
                node.obj.setmode=self.cfg.gpio.setmode
                node.obj.Open()
        if self.cfg.device.websocket:
            try:
                from lib.net.server.websocket import webSockServer
                for key in self.cfg.device.MmonitorPort:self.checkportstatus(eval("self.cfg."+key))
                self.websocket=webSockServer(self.cfg.websocket.port)
                self.websocket.new_client=self.websocket_newclient
                self.websocket.client_left=self.websocket_clientleft
                self.websocket.message_received=self.websocket_received
                self.clients=edict()
                self.app.logservice("info","正在启动websock服务({})".format(self.cfg.websocket.port),self.websocket.Open())
            except:self.app.logservice("info","启动websock服务失败({})".format(self.cfg.websocket.port),self.websocket.Open())
        if self.mq:
            # self.mq.LogData=self.app.logservice
            self.mq.mode="async"
            self.mq.readdata=self.mq_received
            self.app.logservice("info","正在连接mqtt服务({}:{})".format(self.app.servercfg.server.iotserver.host,self.app.servercfg.server.iotserver.port.mqServer))
            self.mq.Open(self.app.cfg.version.sn)
            self.mq_work()
            # threading.Thread(
            #     target=self.mq.Open,args=("{}".format(self.cfg.mqtt.topic if self.cfg.mqtt.topic else self.app.cfg.version.sn),)).start()
            self.dev_task=self.mq_work
        DeviceUnit.Open(self,*argv)
    def checkportstatus(self,port):
        while True:
            pid=System.Process(port=port)
            if pid==False or pid=="":break
            elif pid!=os.getpid():
                self.logprint("info","发现端口{}被进程{}占用，正在删除进程".format(port,pid))
                System.killProc(pid)
            time.sleep(1)
    def logservice(self,*data):
        System.Console(str(datetime.now())[:19],"info",*data)
        self.log.info(System.makedata(*data))
    def websocket_newclient(self,client, server):
        self.logservice("websocket","新客户端连接，ID:{},地址:{}".format(client['id'],client["address"]))
        exec("self.clients.p{}=edict()".format(client['id']))
        record=eval("self.clients.p{}".format(client['id']))
        record.update(client)
        record.loginUser=None
        record.record=None
    def websocket_clientleft(self,client, server):
        try:
            self.logservice("websocket","client {} closed".format(client['id']))
            self.clients.remove("p{}".format(client['id']))
        except:pass
    # 接收外部信息指令
    def pipe_received(self,message):
        result=edict(message)
        self.logservice("pipe 接收到",message)
        cmd=result["cmd"]
        result=self(result)
        if result:
            self.logservice("pipe 返回:",result.toString() if type(result)==edict else edict(result).toString() if type(result)==dict else str(result))
            result.cmd=cmd
        return result
    def websocket_received(self,client, server, message):
        result=edict(message).result
        self.logservice("websocket 接收到:",message)
        cmd=result["cmd"]
        result=self(result)
        if result:
            result.cmd=cmd
            self.logservice("websocket 返回:",result.toString() if type(result)==edict else edict(result).toString() if type(result)==dict else str(result))
            result.cmd=cmd
            result.clientid=client["id"]
            self.websocket.send(result,client)
        return result
    def mq_received(self,data):
        result=None
        self.logservice(data.dest,"mqtt 从{}接收到:{}".format(data.sour,data))
        if "method" in result and result.method=="thing.event.property.post":
            result=self("mqtt.tablecards",data)  
        elif "result" in data and "cmd" in data["result"]:
            cmd=data["result"]["cmd"]
            result=self(data["result"])
        if result:
            self.logservice("mqtt 返回",result.toString() if type(result)==edict else edict(result).toString() if type(result)==dict else str(result))
            result.cmd=cmd
            self.mq.Write(data.sour,result)
        return result
    # 心跳
    def mq_work(self):
        data={"cmd":"hi","ip":self.app.cfg.device.ip,"devicetype":self.app.cfg.device.type,"version":self.app.cfg.version}
        self.mq.Write(self.app.servercfg.server.iotserver.mq_topic,data)  
    @cmd.command("mqtt.tablecards")
    def mqtt_tablecards_receive(self,data):
        pass
    # 进程事件路由
    @cmd.command("websocket.test")
    def websocket_test(self,**data):return data
    @cmd.command("gpio.operation")
    def Operation(self,pinname,cmd=None):
        this=self.app.module.input
        if pinname in this.cfg.gpio.lists:
            node=eval("this.cfg.gpio."+pinname)
            if   node.mode=="touch off":node.obj.OnOff()
            elif node.mode=="onoff":
                if   cmd=="on":node.obj.On()
                elif cmd=="off":node.obj.Off()
        return True
    @cmd.command("event")
    def input_event(self,*argv,**keyargv):pass
    @cmd.command("/api/agent/<id>/powerswitch/<value>")
    def powerswitch(self,id,value):
        this=self.app.module.input
        mq=mqSocket((self.app.servercfg.server.iotserver.host,self.app.servercfg.server.iotserver.port.mqServer)) 
        mq.Open("/sys/gbliOqbJoL8/{}/thing/event/property/post".format(id))
        mq.Send("/sys/gbliOqbJoL8/{}/thing/service/property/set".format(id),edict({"params":{"PowerSwitch":1 if value=="on" else 0 if value=="off" else 0}}).toString())
        return {"result":mq.Read()}


        