#!/usr/bin/python
# -*- coding:utf-8 -*-
import os,sys,time,json,requests,io
from datetime import datetime
from copy import copy
if __name__=="__main__":
    path=sys.path[0]
    sys.path.append(path+"/../../..")
from lib import *
from app.devices import App
from lib.app.devices import DeviceUnit
from lib.file.log import logFile
from aip import AipFace

@Singleton
class faceUnit(DeviceUnit):
    cmd=command_interpreter()
    def __init__(self,app,*argv):
        DeviceUnit.__init__(self,"/app/etc/face.json",app,"/etc/conf/face.json",*argv)
        self.log=logFile(self.app.rootpath+"/etc/log/face")
        self.addr="face"
        self.path=self.app.rootpath
        self.dev= AipFace(self.cfg.interface.appid, self.cfg.interface.apikey, self.cfg.interface.secretkey)
        self.statuslog=""
        self.running=self.cfg.interface.autostart
        self.dev_task=self.task
        self.showuser=False
        self.url="http://{}:{}{}".format(self.app.servercfg.webservice.ip,self.app.servercfg.webservice.rpicamera.port,self.app.servercfg.webservice.rpicamera.picture) 
    def printf(self,data):
        printf(datetime.now(),self.addr,data)
        self.log.info(data)
    @cmd.command("facereadmode")
    def face_readmode(self,status):
        this=self.app.module.face
        System.Console("facereadmode:",status)
        this.running=status
        if status==False:this.cfg.lastBrush.user_id=""
        return True
    # @cmd.command("face.detect")
    def detect(self,image):
        this=self.app.module.face
        imagetype = "BASE64"
        # try:
        face_group=this.cfg.interface.face_group.encode("ascii")
        ret=this.dev.search(image,imagetype,face_group)
        if not self.cfg.interface.autostart:System.Console(ret)
        if "result" in ret and ret["result"]:
            for user in ret["result"]["user_list"] if "user_list" in ret["result"] else []:
                if self.showuser:System.Console(user)
                if "score" in user and user["score"]>=this.cfg.interface.score:
                    user_id,score=user["user_id"],user["score"]
                    return {"error_code":0,"user":user_id,"score":score}
        # except:self.app.logservice("info","提交人脸失败")
    @cmd.command("start detect face")
    def start_detect_face(self):
        this=self.app
        this.logservice("info","start detect face")
        this.module.face.running=True   
        this.module.face.showuser=True
        return True    
    @cmd.command("stop detect face")
    def stop_detect_face(self):
        this=self.app
        this.module.face.running=False
        this.module.face.cfg.lastBrush.user_id=""
        this.module.face.showuser=False
        this.logservice("info","stop detect face")
        return True
    def Open(self,*argv):
        self.app.logservice("info","face.cfg.autostart:{}".format(self.cfg.interface.autostart))
        self.app("facereadmode",self.cfg.interface.autostart)
        DeviceUnit.Open(self)
    def task(self):
        if self.running==True:
            jpg=None
            if self.app.image:
                jpg=io.BytesIO()
                self.app.image.save(jpg,format="JPEG")
                jpg=jpg.getvalue()
            else:
                try:r = requests.get(self.url)
                except:
                    r=edict()
                    r.status_code=500
                if r.status_code == 200:jpg=r.content
                else:self.app.logservice("info","访问摄像头失败",self.url)
            if jpg:
                ret=self.detect(base64.b64encode(jpg))
                if not self.cfg.interface.autostart:System.Console("face.detect:",ret)
                if ret==None:pass
                elif "error_code" in ret and ret["error_code"]==0:
                    flag=False
                    user_id=ret["user"]
                    score=ret["score"]
                    self.app.logservice("info","工号:{},相似度:{},上次识别工号:{},上次识别时间:{}".format(user_id,score,self.cfg.lastBrush.user_id,self.cfg.lastBrush.datetime))
                    # self.app("gpio.operation",**{"pinname":"buzz"})
                    if self.cfg.lastBrush.user_id!=user_id:flag=True
                    else:
                        days=(datetime.now()-datetime.strptime(self.cfg.lastBrush.datetime,'%Y-%m-%d %H:%M:%S')).days
                        seconds=(datetime.now()-datetime.strptime(self.cfg.lastBrush.datetime,'%Y-%m-%d %H:%M:%S')).seconds
                        if seconds>=self.cfg.interface.EffectiveTime:flag=True
                    if flag==True and score>=self.cfg.interface.score:
                        self.cfg.lastBrush.score=score
                        self.cfg.lastBrush.user_id=user_id
                        self.cfg.lastBrush.datetime=str(datetime.now())[:19]
                        if not self.cfg.interface.autostart:System.Console("{}:{}".format(user_id,score))
                        ret=self.app("auth.from_user",username=user_id)
                        if ret:return ret
                        else:
                            self.app.logservice("info","未加载认证模块")
                            self.app("gpio.operation",**{"pinname":"buzz"})
                            self.app("event",type="alert",msg="卡号：{}\n未加载认证模块".format(card))
                    else:self.app.logservice("info","重复识别工号：{}，距离下次上报还有{}天{}秒".format(user_id,days,seconds))      
    @cmd.command("event")
    def face_event(self,*argv,**keyargv):pass  
