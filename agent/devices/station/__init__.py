#!/usr/bin/python
# -*- coding:utf-8 -*-
import os,sys,time,json,io,requests
from PIL import Image,ImageFont,ImageDraw
from datetime import datetime
if __name__=="__main__":
    path=sys.path[0]
    sys.path.append(path+"/../../..")
from lib import *
from lib.app.devices import DeviceUnit
from lib.file.jsonfile import gsJsonFile as JsonFile
from lib.net.client.sshclient import Client
from lib.file.ffmpy import FFmpeg,FFmpegMjpgStreamerRecord
@Singleton
class StationUnit(DeviceUnit):
    cmd=command_interpreter()
    def __init__(self,app,*argv):
        DeviceUnit.__init__(self,"/app/etc/station.json",app,"/etc/conf/station.json",*argv)
        self.addr="station"
        self.istask=False
        self.isrecord=False
        self.TestItemRecord=None
        self.usbjob=None
        self.networkjob=None
        self.ff=None
    def Open(self):
        self.app("stop detect face")
        self.isOpen(True)
    @cmd.command("read runtime mode")
    def getruntimemode(self):return self.app.module.station.cfg.debug
    @cmd.command("show library today")
    def showlibrarytoday(self,data):return self.app("show library",str(datetime.now()))
    @cmd.command("show library")
    def showlibrary(self,enddatetime):
        data=edict()
        data.result=[]
        this=self.app.module.station
        System.Console("station.show library","{}{}".format(self.app.rootpath,this.cfg.webroot))
        for root,dirs,files in os.walk("{}{}".format(self.app.rootpath,this.cfg.webroot)):
            for name in dirs:
                filename="{}/{}/record.json".format(root,name)
                if os.path.exists(filename)==True:
                    f=JsonFile(filename) 
                    record=edict()       
                    record.course=f.data.course
                    record.InspectionRecord=[]
                    self.logservice("info","station:",len(f.data.InspectionRecord))
                    self.logservice("info","station:",f.data.InspectionRecord)
                    for rs in f.data.InspectionRecord:
                        item=edict(rs)
                        if item.datetime.endtime > enddatetime[:19]:
                            sub=edict()
                            sub.experiment=item.experiment
                            sub.datetime=item.datetime
                            sub.teachers=item.teachers
                            record.InspectionRecord.append(sub)
                            self.logservice("info","station:",sub)
                    data.result.append(record)
        return data
    @cmd.command("show library id")
    def showlibraryid(self,**argv):
        data=edict(argv)
        System.Console(data)
        this=self.app.module.station
        data.filename="{}{}/{}/record.json".format(self.app.rootpath,this.cfg.webroot,data.courseid)
        if os.path.exists(data.filename):
            data.code=200
            record=JsonFile(data.filename)
            data.Path="{}{}/{}/{}".format(self.app.rootpath,this.cfg.webroot,data.courseid,data.experimentid)
            os.system("mkdir -p "+data.Path)
            self.app.logservice("info",record,data.experimentid)
            data.InspectionRecord=this.getTestTermData(record,data.experimentid)
            # self.app("mjpg-streamer start")
        else:
            data.code=404
        return data
    @cmd.command("take picture")
    def getPicture(self,**argv):
        data=edict(argv)
        this=self.app.module.station
        try:os.makedirs("{}/data/inspection/{}/{}/".format(self.app.rootpath+self.app.cfg.services.webroot,data.courseid,data.experimentid))
        except:pass
        data.filename="{}/data/inspection/{}/{}/{}.jpg".format(self.app.rootpath+self.app.cfg.services.webroot,data.courseid,data.experimentid,self.app("getNewDatetimeflag"))
        data.soururl="http://{}:{}{}".format(
            self.app.servercfg.webservice.ip,
            self.app.servercfg.webservice.uvccamera.port,
            self.app.servercfg.webservice.uvccamera.picture
        )
        System.Console(data.soururl)
        try:response = requests.get(data.soururl)
        except:
            data.code=300
            data.msg="拍照失败，请再试一次"
            response=edict()
            response.status_code=404
        if response.status_code == 200:
            data.url=self.app("saveImgFile",data.filename,response.content)
            if data.url!=None:
                record=this.getNewTestItemRecord()
                record.Type="image"
                record.Path=self.app.rootpath+self.app.cfg.services.webroot+"/data/inspection/{}/{}/".format(data.courseid,data.experimentid)
                data.File=record.File=data.filename.replace(record.Path,"")
                record.OperatorUserName=data.OperatorUserName
                record.courseid=data.courseid
                record.experimentid=data.experimentid
                
                jsoncfg=JsonFile("{}/data/inspection/{}/record.json".format(self.app.rootpath+self.app.cfg.services.webroot,data.courseid))
                threading.Thread(target=this.UpLoadFile,args=(jsoncfg,record,)).start()
                # data.eventType="take picture"
                self.app("event",eventType="broadcast",result=data)
        return data
    @cmd.command("start record moive")
    def moviestart(self,**argv):
        data=edict(argv)   
        this=self.app.module.station
        #/lubanlou/gvsun-business/provider-api/station/web
        webroot=self.app.rootpath+self.app.cfg.services.webroot
        if this.istask==False:
            web=self.app.module.web
            this.istask=True
            this.isrecord=True
            this.TestItemRecord=this.getNewTestItemRecord()
            this.TestItemRecord.OperatorUserName=data.OperatorUserName
            this.TestItemRecord.start=datetime.now()
            this.TestItemRecord.nowimgrecord="{}/data/inspection/{}/{}/{}".format(webroot,data.courseid,data.experimentid,self.app("getNewDatetimeflag"))
            this.TestItemRecord.filepath="{}/data/inspection/{}/{}".format(webroot,data.courseid,data.experimentid)
            data.code=200
            data.url="http://{}:{}{}".format(
                self.app.servercfg.webservice.ip,
                self.app.servercfg.webservice.uvccamera.port,
                self.app.servercfg.webservice.uvccamera.streamer
            )
            os.makedirs(this.TestItemRecord.nowimgrecord)
            filename=this.TestItemRecord.nowimgrecord+".mp4"
            self.usbjob=FFmpegMjpgStreamerRecord(data.url,filename)
            self.usbjob.fps=this.cfg.fps
            self.usbjob.mode=this.cfg.mode
            self.usbjob.setFont(self.app.rootpath+'/etc/font/simhei.ttf',20)
            self.usbjob.Start()
        else:
            data.code=300
            data.msg="正在录制视频，当前操作无法进行"
        return data
    @cmd.command("end record moive")
    def moviestop(self,**argv):
        data=edict(argv)
        this=self.app.module.station
        webroot=self.app.rootpath+self.app.cfg.services.webroot
        if this.istask==True:
            this.isrecord=False
            # time.sleep(3)
            self.usbjob.Stop()
            # this("mjpg-streamer stop",data)
            this.TestItemRecord.end=datetime.now()
            data.filename=self.usbjob.filename.replace("{}/data/inspection/{}/{}/".format(webroot,data.courseid,data.experimentid),"")
            record=edict()
            record.Type="video"
            record.File=data.filename
            record.Start=str(this.TestItemRecord.start)[:19]
            record.End=str(this.TestItemRecord.end)[:19]
            record.OperatorUserName=this.TestItemRecord.OperatorUserName
            record.courseid=data.courseid
            record.experimentid=data.experimentid
            record.Path=this.TestItemRecord.filepath
            data.id=data.clientid
            data.url=""
            self.app("event",eventType="broadcast",result=data)
            data.url="/data/inspection/{}/{}".format(data.courseid,data.experimentid)+"/"+data.filename
            i=0               
            try:
                threading.Thread(target=this.UpLoadFile,args=(JsonFile("{}/data/inspection/{}/record.json".format(webroot,data.courseid)),record,)).start()
                os.system("rm -rf {}".format(this.TestItemRecord.nowimgrecord))
            except:self.System.Console("upload {} error".format(filename))
            this.istask=False
            System.Console("makemovie:",data.toJsonString())
        # self.app.module.websocket.dev.send(data) 
        self.app("event",eventType="broadcast",result=data)
        return data
    @cmd.command("start record moive 1")
    def moviestart1(self,**argv):
        data=edict(argv)
        this=self.app.module.station
        webroot=self.app.rootpath+self.app.cfg.services.webroot
        if this.istask==False:
            web=self.app.module.web
            this.istask=True
            this.isrecord=True
            this.TestItemRecord=this.getNewTestItemRecord()
            this.TestItemRecord.OperatorUserName=data.OperatorUserName
            this.TestItemRecord.start=datetime.now()
            this.TestItemRecord.nowimgrecord="{}/data/inspection/{}/{}/{}".format(webroot,data.courseid,data.experimentid,self.app("getNewDatetimeflag"))
            this.TestItemRecord.filepath="{}/data/inspection/{}/{}".format(webroot,data.courseid,data.experimentid)
            data.code=200
            data.url="http://{}:{}{}".format(
                self.app.servercfg.webservice.ip,
                self.app.servercfg.webservice.uvccamera.port,
                self.app.servercfg.webservice.uvccamera.streamer
            )
            os.makedirs(this.TestItemRecord.nowimgrecord)
            filename=this.TestItemRecord.nowimgrecord+".mp4"
            if this.usbjob==None:
                this.usbjob=FFmpeg(
                    inputs={data.url:"-f mjpeg"},
                    outputs={this.usbjob_filename:"-vcodec libx264 -f MP4"})
            System.Console("摄像头开始录像",this.usbjob.cmd)
            this.istask=True
            this.usbjob.run()
            this.usbjob_start=datetime.now()
            data.code=200
        else:
            data.code=500
            data.msg="正在录制，不能重复操作"
        return data
    @cmd.command("end record moive 1")
    def movieend1(self,**argv):
        data=edict(argv)
        this=self.app.module.station
        webroot=self.app.rootpath+self.app.cfg.services.webroot
        if  this.istask==True:
            this.istask=False
            # this.TestItemRecord.t.join()
            # time.sleep(2)
            this.usbjob.stop()  
            this.app.printf("结束录像，等待收尾")
            System.Console("录像文件已生成")
            this.usbjob=None
            record=edict()
            record.Type="video"
            record.Path="{}/data/inspection/{}/{}".format(webroot,data.courseid,data.experimentid)
            record.File=this.usbjob_filename.replace(record.Path+"/","")
            record.Start=str(this.usbjob_start)[:19]
            record.End=str(datetime.now())[:19]
            record.OperatorUserName=data.username
            record.courseid=data.courseid
            record.experimentid=data.experimentid
            data.url=""
            data.filename=record.File
            data.cmd="end record moive"
            self.app("event",eventType="broadcast",result=data)
            data.url=this.usbjob_filename.replace(webroot,"")
            try:
                # threading.Thread(target=this.UpLoadFile,args=(JsonFile("{}/data/inspection/{}/record.json".format(webroot,data.courseid)).data,record,)).start()
                this.UpLoadFile(JsonFile("{}/data/inspection/{}/record.json".format(webroot,data.courseid)).data,record)
                self.app("event",eventType="broadcast",result=data)
            except:pass
        return data
    def logprint(self,data):pass
    @cmd.command("getNewDatetimeflag")
    def getNewDatetimeflag(self):return str(datetime.now()).replace("-","").replace(":","").replace(" ","").replace(".","")
    @cmd.command("saveImgFile")
    def saveImgFile(self,file,imgdata):
        text=str(datetime.now())[:19]
        byte_stream = io.BytesIO(imgdata)
        # imgByteArr = io.BytesIO()
        im=Image.open(byte_stream)
        width, height = im.size
        ttfont = ImageFont.truetype(self.app.rootpath+'/etc/font/simhei.ttf', int(height / 20)) #设置字体
        draw = ImageDraw.Draw(im)  # 创建画画对象
        
        draw.text((0, int(height *0.9)), text, font=ttfont)  # 添加文字
        im.save(file)
        url=file.replace(self.app.cfg.services.webroot,"")
        # except:url=None
        return url
    @cmd.command("start network video record")
    def start_network_video(self,**argv):
        data=edict(argv)
        this=self.app.module.station
        webroot=self.app.rootpath+self.app.cfg.services.webroot
        if this.cfg.webcam!="":
            cmd="mkdir -p {}/data/inspection/{}/{}".format(webroot,data.courseid,data.experimentid)
            System.Console(cmd)
            os.system(cmd)
            this.networkjob_filename="{}/data/inspection/{}/{}/{}.mp4".format(webroot,data.courseid,data.experimentid,self.app("getNewDatetimeflag"))
            data.file=this.networkjob_filename.replace(webroot,"")
            if this.networkjob==None:
                this.networkjob=FFmpeg(
                    inputs={this.cfg.webcam:None},
                    outputs={this.networkjob_filename:"-vcodec libx264 -f MP4"})
                System.Console("网络摄像头开始录像",this.networkjob.cmd)
                this.networkjob.run()
                this.networkjob_start=datetime.now()
                data.code=200
            else:
                data.code=500
                data.msg="正在录制，不能重复操作"
        else:
            data.code=500
            data.msg="网络摄像头配置错误"
        return data
    @cmd.command("end network video record")
    def end_network_video(self,**argv):
        data=edict(argv)
        this=self.app.module.station
        webroot=self.app.rootpath+self.app.cfg.services.webroot
        if this.networkjob!=None:
            this.networkjob.stop()
            System.Console("结束录像，等待收尾")
            time.sleep(2)
            System.Console("录像文件已生成")
            this.networkjob=None
            record=edict()
            record.Type="video"
            record.Path="{}/data/inspection/{}/{}".format(webroot,data.courseid,data.experimentid)
            record.File=this.networkjob_filename.replace(record.Path+"/","")
            record.Start=str(this.networkjob_start)[:19]
            record.End=str(datetime.now())[:19]
            record.OperatorUserName=data.username
            record.courseid=data.courseid
            record.experimentid=data.experimentid
            data.url=""
            data.filename=record.File
            data.cmd="end record moive"
            self.app("event",eventType="broadcast",result=data)
            data.url=this.networkjob_filename.replace(webroot,"")
            #try:
                # threading.Thread(target=this.UpLoadFile,args=(JsonFile("{}/data/inspection/{}/record.json".format(webroot,data.courseid)).data,record,)).start()
            threading.Thread(target=this.UpLoadFile,args=(JsonFile("{}/data/inspection/{}/record.json".format(webroot,data.courseid)),record,)).start()
            # os.system("rm -rf {}".format(this.TestItemRecord.nowimgrecord))
            #except:pass
            this.istask=False
            System.Console("makemovie:",data.toJsonString())
        # self.app.module.websocket.dev.send(data) 
        self.app("event",eventType="broadcast",result=data)
        return data
    def task_record_moive(self,path,url):
        i=0
        while self.istask==True and self.isrecord==True:
            response = requests.get(url)
            if response.status_code == 200:
                imgfile="{}/{}.jpg".format(path,str(i).rjust(8,"0"))
                i=i+1
                System.Console(imgfile)
                threading.Thread(target=self.app,args=("saveImgFile",imgfile,response.content,)).start()
            time.sleep(0.1)
    def task_record_moive1(self):
        while self.istask==True:
            self.usbjob.run().sync()
        self.usbjob.stop()  
        System.Console("结束录像，等待收尾")
    def task_record_moive2(self):
        pass
    def getTestTermData(self,jsonrecord,experimentid):
        ret=None
        self.app.logservice("info",jsonrecord.data.InspectionRecord)
        for item in jsonrecord.data.InspectionRecord:
            record=edict(item)
            System.Console("getTermData:",record)
            if record.experiment.id==experimentid and (record.datetime.starttime<=str(datetime.now())[:19]<record.datetime.endtime):
                ret=record
                # ret=edict()
                ret.datetime=record.datetime
                ret.Record=record.Record
                ret.UpLoad=record.UpLoad
                break
        return ret
    def getNewTestItemRecord(self):
        ret=edict()
        ret.Type=""
        ret.File=""
        ret.Start=str(datetime.now())[:19]
        ret.OperatorUserName=""
        return ret
    def UpLoadFile(self,jsonRecord,rs):       
        def task():
            ssh=None
            # jsonRecord=JsonFile("{}/data/inspection/{}/record.json".format(self.app.module.web.webroot,rs.courseid))
            #如果课程id是share则不将相关资源存入资源容器中
            if rs.courseid=="share":pass
            elif self.cfg.upload_resourse==True:
                rs.FileID=self.resourcereport(rs.Path,rs.OperatorUserName,"",rs.File,self.createDirectory(jsonRecord.device.ip,rs.OperatorUserName,"",rs.courseid,rs.experimentid))
            # System.Console(jsonRecord.device.ip)
            elif self.cfg.upload_iotserver==True:
                ssh=self.getNewSshClient(
                    self.app.servercfg.server.iotserver.host,
                    self.app.servercfg.server.iotserver.port.ssh,
                    self.app.servercfg.server.iotserver.ssh.user,
                    self.app.servercfg.server.iotserver.ssh.passwd
                )
                System.Console("物联服务器{}在线".format(self.app.servercfg.server.iotserver.host))
                ssh.open()
                remotepath=self.app.servercfg.server.iotserver.station.format(self.app.net.nic[self.app.cfg.device.network].ip)
                remotepath+="/{}".format(rs.courseid)
                cmd="mkdir -p {}/{}/{}".format(remotepath,rs.experimentid,rs.OperatorUserName)
                ssh.runas(cmd)
                ssh.putfile(rs.Path,"{}/{}/{}".format(remotepath,rs.experimentid,rs.OperatorUserName),rs.File)
                cmd=self.app.servercfg.server.iotserver.station.format("report.py {}/{}/{}/{}".format(remotepath,rs.experimentid,rs.OperatorUserName,rs.File))
                System.Console("远程从物联服务器上传资源容器："+cmd+",结果")
                System.Console(ssh.runas("python "+cmd))
                
            System.Console("jsonRecord:",jsonRecord)
            System.Console("rs:",rs)
            res=self.getTestTermData(jsonRecord,rs.experimentid)
            System.Console("res:",res)
            try:
                res.Record.append(edict(rs))
                jsonRecord.Savefile()
            except:pass
            if ssh!=None:ssh.close()
            System.Console("uploadfile finished")
        t=threading.Thread(target=task)
        t.start()
    def getNewSshClient(self,host,port,user,passwd):
        self.app.logservice("info","ssh client",host,port,user,passwd)
        o=Client(host=host,port=port,user=user,passwd=passwd,timeout=1)
        o.LogData=self.logprint
        return o
    def createDirectory(self,ip,username,cname,course,experiment):
        resserver=self.app.servercfg.server.resourceserve.host
        resport=self.app.servercfg.server.resourceserve.port
        url="http://{}:{}/gvsunDirectory/createDirectory?path=物联/工位仪/{}/{}/{}".format(resserver,resport,ip,course,experiment)
        params={"siteName":"物联","username":username,"userCname":cname}
        header = {"x-datasource":self.app.module.auth.cfg.fromcard_username.webservice.header["x-datasource"]}
        directory= requests.get(url,params,headers=header)
        print ("==========================================")
        System.Console(directory.json()) 
        return directory.json()["data"]
    # 上传资源容器返回ID
    def resourcereport(self,folder,username,cname,f,directoryId):
        resserver=self.app.servercfg.server.resourceserve.host
        resport=self.app.servercfg.server.resourceserve.port
        url="http://{}:{}/gvsunResource/uploadFile".format(resserver,resport)
        System.Console(folder,username,cname,f,directoryId)
        files = {'files':open(folder+"/"+f,'rb')}
        params={"siteName":"物联","username":username,"userCname":cname,"directoryId":directoryId}
        header = {"x-datasource":self.app.module.auth.cfg.fromcard_username.webservice.header["x-datasource"]}
        System.Console("url:",url)
        System.Console("header:",header)
        System.Console("params:",params)
        System.Console("files:",files)
        resource=requests.post(url,params,files=files,headers=header)
        print ("==========================================")
        print resource.json()
        fileId=resource.json()["data"][0]
        return fileId