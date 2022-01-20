def __init__(self,runpath):
        ModuleUnit.__init__(self,runpath)
        self.scrcfg=self.config.getJsonConfigFile("screen.json")
        self.ipc.registr(self.event.topic.screen,self.event_receive)
        self.releasecfg=self.config.getJsonConfigFile("release.json")
        self.iotserver=self.releasecfg.service.iotserver.ip
        self.__isTerminal=True
        self.__isScreen=False
        self.__isFace=False
        self.__isCard=True
        self.onlinestatus=None
        self.lines=[]
        self.backcolor=(4,77,128,0)
        self.font={
            32:ImageFont.truetype(self.path+self.scrcfg.display.fontfile.value, 32),
            24:ImageFont.truetype(self.path+self.scrcfg.display.fontfile.value, 24),
            20:ImageFont.truetype(self.path+self.scrcfg.display.fontfile.value, 20),
            16:ImageFont.truetype(self.path+self.scrcfg.display.fontfile.value, 16),
            12:ImageFont.truetype(self.path+self.scrcfg.display.fontfile.value, 12),
            10:ImageFont.truetype(self.path+self.scrcfg.display.fontfile.value, 10)
        }

        self.message=None
        self.message_lastdatetime=None
    def event_receive(self,topic,data):
        if self.message!=None and self.message.type=="errormsg" and data.type!="errormsg":return None
        self.message=data
        self.message_lastdatetime=datetime.now()
    # 屏幕状态：图形
    def Screen(self):
        self.__isScreen=True
        self.__isTerminal=False
        # self.dev.buffer=Image.new('RGB', (self.dev.width,self.dev.height),self.backcolor)
    # 屏幕状态：命令行
    def Terminal(self):
        self.__isTerminal=True
        self.__isScreen=False
        # self.dev.buffer=Image.new('RGB', (self.dev.width,self.dev.height),self.dev.backcolor)
    # 认证状态：刷脸
    def Face(self):
        if  self.__isScreen==True and platform.uname[0]=="Linux":
            self.__isFace=True
            self.__isCard=False
            from io import BytesIO
            from picamera import PiCamera
    # 认证状态：刷卡
    def Card(self):
        if  self.__isScreen==True:
            self.__isFace=False
            self.__isCard=True
    def loadScreenRes(self):
        self.isonline=Image.open(self.path+self.scrcfg.display.imagefiles.isonlinefile)
        self.offline=Image.open(self.path+self.scrcfg.display.imagefiles.offlinefile)
        self.welcome=Image.open(self.path+self.scrcfg.display.imagefiles.welcomefile)
        self.back=Image.open(self.path+self.scrcfg.display.imagefiles.backfile)
        self.sqlfile=Image.open(self.path+self.scrcfg.display.imagefiles.sqlfile)
        self.nosqlfile=Image.open(self.path+self.scrcfg.display.imagefiles.nosqlfile)
        self.wifi=Image.open(self.path+self.scrcfg.display.imagefiles.wififile)
        self.nowifi=Image.open(self.path+self.scrcfg.display.imagefiles.nowififile)
        self.errormessage=Image.open(self.path+self.scrcfg.display.imagefiles.error_msg501_file)
        self.errormsg=Image.open(self.path+self.scrcfg.display.imagefiles.error_msg_file)
        self.msg=Image.open(self.path+self.scrcfg.display.imagefiles.msg_file)
    # 屏幕刷新线程
    def task(self):
        while True:
            self.dev.layers=[]
            if    self.__isTerminal==True and len(self.lines)!=0:
                if len(self.lines)>15:lines=self.lines[-15:]
                else:lines=self.lines
                key=16
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
            elif  self.__isScreen==True:
                self.showbackimage()
                self.showdatetime()
                self.showtitle()
                self.showversion()
                if platform.uname()[0]=="Linux":self.showipaddress()
                self.showmessage()
                self.showonlinestatus()
            self.dev.show()
            time.sleep(0.1)
    def showversion(self):
        o=self.dev.getunit()
        o.type="image"
        o.font=self.font[10]
        # o.backcolor=self.backcolor
        o.text=self.appcfg.version.software_version
        o.value=self.dev.getimagefromtext(o)
        o.width,o.height=o.value.size
        o.top=self.dev.height-o.height
        self.dev.layers.append(o)
    def showbackimage(self):
        o=self.dev.getunit()
        o.type="image"
        o.left,o.top,o.width,o.height=(0,0,320,240)
        o.value=self.welcome
        self.dev.layers.append(o)
    def showdatetime(self):
        o=self.dev.getunit()
        o.top=0
        o.type="image"
        o.font=self.font[20]
        # o.backcolor=self.backcolor
        o.text=str(datetime.now())[11:19]
        o.value=self.dev.getimagefromtext(o)
        o.left=self.dev.width-o.width
        self.dev.layers.append(o)
    def showipaddress(self):
        net=Net()
        # adas=
        o=self.dev.getunit()
        o.top=180
        o.type="image"
        o.font=self.font[12]
        # o.backcolor=self.backcolor
        o.text=net.nic["eth0"].ip+"\n"+net.nic["wlan0"].ip
        o.value=self.dev.getimagefromtext(o)
        o.width,o.height=o.value.size
        o.left=(self.dev.width-o.width)/2
        self.dev.layers.append(o)
    def showtitle(self):
        o=self.dev.getunit()
        o.top=140
        o.type="image"
        o.font=self.font[16]
        # o.backcolor=self.backcolor
        try:o.text=self.scrcfg.display.text.value
        except:o.text=self.scrcfg.display.text.value.decode("gbk")
        o.value=self.dev.getimagefromtext(o)
        o.width,o.height=o.value.size
        o.left=(self.dev.width-o.width)/2
        self.dev.layers.append(o)
    def showmessage(self):
        if self.message!=None:
           if   self.message.type=="showmsg":
                self.getAlert(self.message.text,self.msg)
                days=(datetime.now()-self.message_lastdatetime).days
                seconds=(datetime.now()-self.message_lastdatetime).seconds
                if days==0 and seconds>=int(self.scrcfg.display.showdelay.value):self.message=None
           elif self.message.type=="errormsg":
                if self.message.code==500:self.getAlert(self.message.text,self.errormsg)
                elif self.message.code==200:self.message.type="showmsg"
    def showonlinestatus(self):
        o=self.dev.getunit()
        o.top=0
        o.left=0
        o.type="image"
        o.value=None
        if self.onlinestatus==True:o.value=self.isonline
        elif self.onlinestatus==False:o.value=self.offline
        if o.value!=None:
            self.dev.layers.append(o)
    def checkonline(self):
        while True:
            self.onlinestatus=icmp.ping(self.iotserver)
            time.sleep(5)
    def getAlert(self,text,image):
         # 建立
        o=self.dev.getunit()
        o.type="image"
        o.font=self.font[16]
        o.backcolor=(154,217,234,0)
        o.fillcolor=(0,0,0,0)
        try:o.text=text
        except:o.text=self.message.decode("gbk")
        img=self.dev.getimagefromtext(o)
        msgimg=copy(image)
        w,h=img.size
        w1,h1=msgimg.size
        msgimg.paste(img,((w1-w)/2,(h1-h)/2+18))
        o.value= msgimg
        o.width,o.height=o.value.size
        o.top=(self.dev.height-o.height)/2
        o.left=(self.dev.width-o.width)/2
        self.dev.layers.append(o)            
    # def show(self):
    #     try:self.dev.show()
    #     except:pass
    def Open(self):
         # 根据配置加载屏幕
        devicemodule=self.scrcfg.device.devicemodule
        exec("from lib.iot.gsdisplay.{} import container".format(devicemodule))
        if devicemodule=="tft":
            self.dev=container(dc=self.scrcfg.device.dc.value,
                            rst=self.scrcfg.device.rst.value,
                            angle=self.scrcfg.device.angle.value,
                            expend=self.scrcfg.device.expend.value)
        elif devicemodule=="gui":self.dev=container()
        self.t=threading.Thread(target=self.task)
        self.c=threading.Thread(target=self.checkonline)
        self.t.setDaemon=self.c.setDaemon=True
        self.t.start()
        self.c.start()
        self.dev.start()