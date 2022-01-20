#!/usr/bin/python
# -*- coding:utf-8 -*-
import os,sys,time,json,io,requests
from PIL import Image,ImageFont,ImageDraw
from datetime import datetime
from copy import copy
if __name__=="__main__":
    path=sys.path[0]
    sys.path.append(path+"/../../..")
from lib import *
from lib.net import Net
from app.devices import App
from lib.app.devices import DeviceUnit
import lib.file.gsdisplay.qrlib as qr

@Singleton
class ScreenUnit(DeviceUnit):
    cmd=command_interpreter()
    def __init__(self,app,*argv):
        DeviceUnit.__init__(self,"/app/etc/screen.json",app,"/etc/conf/screen.json",*argv)
        self.addr="screen"
        # self.runmode="process"
        self.isTerminal=True
        self.isScreen=False
        self.isFace=False
        self.isCard=True
        self.onlinestatus=None
        # self.timeinternel=0.3
        self.lines=self.app.printlines
        self.backcolor=(4,77,128,0)
        self.font={
            32:ImageFont.truetype(self.app.rootpath+self.cfg.display.fontfile.value, 32),
            24:ImageFont.truetype(self.app.rootpath+self.cfg.display.fontfile.value, 24),
            20:ImageFont.truetype(self.app.rootpath+self.cfg.display.fontfile.value, 20),
            16:ImageFont.truetype(self.app.rootpath+self.cfg.display.fontfile.value, 16),
            14:ImageFont.truetype(self.app.rootpath+self.cfg.display.fontfile.value, 14),
            12:ImageFont.truetype(self.app.rootpath+self.cfg.display.fontfile.value, 12),
            10:ImageFont.truetype(self.app.rootpath+self.cfg.display.fontfile.value, 10)
        }
        self.alertText=""
        self.alertDatetime=None
        self.buff_images=[]
        self.qrimage=None
        self.image=None
        self.picback=self.app.image
        self.dev=None   
    def getBuffImagesItem(self):
        item=edict()
        item.text=""
        item.image=None
        item.backupimage=None
        return item
    # 屏幕状态：图形
    @cmd.command("screen.mode.screen")
    def Screen(self):
        this=self.app.module.screen
        this.isScreen=True
        this.isTerminal=False
        return True
    # 屏幕状态：命令行
    @cmd.command("screen.mode.termnal")
    def Terminal(self):
        self.isTerminal=True
        self.isScreen=False
    @cmd.command("event")
    def screen_event(self,*argv,**keyargv):
        System.Console("screen.event:",argv,keyargv)
        try:
            this=self.app.module.screen
            if keyargv["result"]["sour"]=="auth" and keyargv["type"]=="event_auth":
                this.alertText=keyargv["result"]["msg"]
                self.app.logservice("info",keyargv["result"]["msg"].replace("\n",""))
                this.alertDatetime=datetime.now()
        except:pass
    @cmd.command("screen.print")
    def printf(self,data):
        this=self.app.module.screen
        if this.isTerminal and this.dev:
            this.lines.append(data)
            if len(this.lines)>15:lines=this.lines[-15:]
            else:lines=this.lines
            this.showlines(lines)  
            this.dev.show() 
        return True
    @cmd.command("showlayer")
    def showlayer(self,value,bakcimg,filecolor=None):
        this=self.app.module.screen
        data=edict()
        data.readdict(value)
        if data.eval==1:text=eval(data.text)
        else:text=data.text
        if data.type=="text":
            num=0
            for line in text.split("\n"):
                if num<len(line):num=len(line)
            width=num*data.fontsize/2
            height=data.fontsize*len(data.text.split("\n"))
        elif data.type=="image":width,height=text.size
        W,H=bakcimg.size
        if "align" in data:
            if   data.align=="right"  :data.left=W-width
            elif data.align=="center" :data.left=(W-data.left-width)/2
        if "valign" in data:
            if   data.valign=="bottom":data.top=H-height
            elif data.valign=="center":data.top=(H-data.top-height)/2
        if data.type=="text":
            draw = ImageDraw.Draw(bakcimg)  # 创建画画对象
            if not filecolor:draw.text((data.left,data.top), text, font=this.font[data.fontsize]) 
            else:draw.text((data.left,data.top), text,filecolor, font=this.font[data.fontsize]) 
        elif data.type=="image":bakcimg.paste(text,(data.left,data.top))
        return bakcimg
    def loadScreenRes(self):
        self.isonline=Image.open(self.app.rootpath+self.cfg.display.imagefiles.isonlinefile)
        self.offline=Image.open(self.app.rootpath+self.cfg.display.imagefiles.offlinefile)
        self.welcome=Image.open(self.app.rootpath+self.cfg.display.imagefiles.welcomefile)
        self.back=Image.open(self.app.rootpath+self.cfg.display.imagefiles.backfile)
        self.sqlfile=Image.open(self.app.rootpath+self.cfg.display.imagefiles.sqlfile)
        self.nosqlfile=Image.open(self.app.rootpath+self.cfg.display.imagefiles.nosqlfile)
        self.wifi=Image.open(self.app.rootpath+self.cfg.display.imagefiles.wififile)
        self.nowifi=Image.open(self.app.rootpath+self.cfg.display.imagefiles.nowififile)
        self.errormessage=Image.open(self.app.rootpath+self.cfg.display.imagefiles.error_msg501_file)
        self.errormsg=Image.open(self.app.rootpath+self.cfg.display.imagefiles.error_msg_file)
        self.msg=Image.open(self.app.rootpath+self.cfg.display.imagefiles.msg_file)
    def Open(self,*argv):
        self.loadScreenRes()
        devicemodule=self.cfg.device.devicemodule
        exec("from lib.file.gsdisplay.{} import container".format(devicemodule))
        if devicemodule=="tft":
            self.dev=container(dc=self.cfg.device.dc.value,
                            rst=self.cfg.device.rst.value,
                            angle=self.cfg.device.angle.value,
                            expend=self.cfg.device.expand.value,
                            width=320,height=240)
        elif devicemodule=="gui":self.dev=container()
        DeviceUnit.Open(self,*argv)
        self.dev_task=self.worke_job
        self.dev.start()
    def getImage(self):
        img=None
        if self.app.image:img=copy(self.app.image).resize((self.dev.width,self.dev.height)).transpose(Image.FLIP_LEFT_RIGHT)
        elif self.cfg.display.iscamera.value and System.getCamera()["detected"]==1 and self.cfg.display.imagefiles.face!="":
            r = requests.get(self.cfg.display.imagefiles.face)
            if r.status_code==200:img=Image.open(io.BytesIO(r.content)).resize((self.dev.width,self.dev.height))
        else:img=copy(self.welcome)
        if img:
            if not self.app.image:self.app.image=copy(img)
            for key in self.cfg.tmpl.lists:
                key=str(key)
                img=self.app("showlayer",self.cfg.tmpl[key],img)
            if self.alertText!="":
                s=(datetime.now()-self.alertDatetime).seconds
                d=(datetime.now()-self.alertDatetime).days
                System.Console("screen.alertText:",self.alertText)
                System.Console("screen.alertDatetime:",self.alertDatetime)
                System.Console(s,self.cfg.display.showdelay.value,s>self.cfg.display.showdelay.value)
                if ((d==0 and s>self.cfg.display.showdelay.value) or (d!=0 and s>0)):self.alertText=""
                else:
                    alertimg=copy(self.msg)
                    item=edict()
                    item.readdict({"type":"text","eval":0,"left":30,"top":-30,"text":self.alertText,"fontsize":16,"align":"center","valign":"center"})
                    alertimg=self.app("showlayer",item,alertimg,(0,0,0))
                    img.paste(alertimg,((img.size[0]-alertimg.size[0])/2,(img.size[1]-alertimg.size[1])/2))
            self.image=img
            return img  
    def worke_job(self):
        this=self.app.module.screen
        if this.isTerminal and this.dev:
            if len(this.lines)>15:lines=this.lines[-15:]
            else:lines=this.lines
            this.showlines(lines)  
            this.dev.show() 
        elif this.isScreen and this.dev:
            img=self.getImage()
            if img:
                o=self.dev.getunit()
                o.type="image"
                o.left,o.top,o.width,o.height=(0,0,320,240)
                o.value=img
                self.dev.layers=[o]
                self.dev.show()
        return True
    def showlines(self,lines):
        if self.dev:
            key=14
            for i in range(0,len(lines)):
                line=lines[i]
                o=self.dev.getunit()
                o.type="image"
                o.left=0
                o.top=i*key+5
                o.font=self.font[key]
                # if platform.uname()[0]=="Windows":o.text=line.decode("utf-8")
                o.text=line
                o.value=self.dev.getimagefromtext(o,Image.new('RGBA', (self.dev.width,self.dev.height), (0,0,0,0)))
                self.dev.layers.append(o)
    def make_qr(self):
        if self.qrimage==None:
            url=self.cfg.display.qrcode.url.format(self.app.cfg.device.type,self.app.net(self.app.cfg.device.network).ip)
            self.app.logservice("info","二维码生成内容：",url)
            self.qrimage=qr.make_qr(url).resize((self.cfg.display.qrcode.width,self.cfg.display.qrcode.height))
        return self.qrimage
    
    
        