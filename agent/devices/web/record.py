# -*- coding:utf-8 -*-
import sys,os,platform,threading,json,hashlib,requests,io,base64
from datetime import datetime
from multiprocessing import Process
if __name__=='__main__':
    path=sys.path[0]
    sys.path.append(path+"/../..")
from lib import *
from app.devices import App
from lib.file.jsonfile import gsJsonFile as JsonFile
from lib.net.client.sshclient import Client

app=App(sys.path[0]+"/../..")
route=app.webroute
cfg=edict()
cfg.makemoive=False
cfg.makemoive_t=None
cfg.makemoive_startdatetime=None
cfg.makemoive_enddatetime=None
cfg.record=None

@route.get("/api/makeshare")
def makeshare(route,request):
    os.system("mkdir -p {}/web/data/inspection/share".format(app.rootpath))
    file="{}/web/data/inspection/share/record.json".format(app.rootpath)
    nowdate=str(datetime.now())[:10]
    makeRecord(file,"{} 00:00:00".format(nowdate),"{} 23:59:59".format(nowdate),"share","nobody","nobody")
    return {"result":True}
@route("/api/data/inspection/<courseid>")
def setConfig(route,courseid,request):
    filename=app.rootpath+"/web/data/inspection/{}/record.json".format(courseid)
    app.logservice("/api/data/inspection/"+str(courseid),request.request_data)
    if request.request_data!={}:
        file=JsonFile(filename)
        file.data=edict(request.request_data)
        file.Savefile()
        app.logservice("info",request.request_data)
        return {"result":True}
    else:
        ret={"filename":filename,"isexists":os.path.isfile(filename)}
        if ret["isexists"]:ret=json.load(open(filename))
        return ret
@route("/api/setPolciy")
def getername(route,request,response=None):
    auth=app.module.auth
    webdatapath=app.rootpath+app.cfg.services.webroot+"/data/inspection"
    for item in request.request_data["data"]:
        rs=edict(item)
        if rs.endDate>str(datetime.now())[:19]:
            recordfile="{}/{}".format(webdatapath,rs.courses[0]["courseId"])
            if not os.path.isdir(recordfile):
                os.system("mkdir -p "+recordfile)
                app.logservice("info","生成目录:"+recordfile)
            if not os.path.isfile(recordfile+"/record.json"):
                record=edict()
                record.device=edict({"ip":rs.devices[0]["hardwareIp"],"id":app.cfg.device.id,"name": rs.devices[0]["deviceName"]})
                record.course=edict({"id": rs.courses[0]["courseId"],"name":rs.courses[0]["courseName"]})
                record.lab=edict(id=app.cfg.device.labid,name=rs.rooms[0]["roomName"])
            
                inspectRS=edict({"Record":[],"UpLoad":[]})
                inspectRS.datetime={"starttime":rs.startDate,"endtime":rs.endDate}
                inspectRS.experiment=edict({"id":item["items"][0]["itemId"],"name":item["items"][0]["itemName"]})
                inspectRS.manager=[]
                for item1 in item["managers"]:
                    inspectRS.manager.append(edict(
                        username=item1["managerId"],
                        cname= item1["managerName"],
                        card= item1["managerCard"]
                    ))
                    app.logservice("info","添加管理员:[{}]{}".format(item1["managerId"],item1["managerName"]))
                    auth.policy(
                        username=item1["managerId"],
                        cname= item1["managerName"],
                        card= item1["managerCard"],
                        starttime="2001-01-01 00:00:00",
                        endtime="2029-12-31 23:59:59",
                        devindex="{}".format(record.device.id)
                    )
                    
                inspectRS.students=[]
                for item1 in item["students"]:
                    # app.logservice("添加学生:",item1)
                    inspectRS.students.append(edict(
                        username= item1["studentId"],
                        cname= item1["studentName"],
                        card= item1["studentCard"]
                    ))
                    app.logservice("info","添加学生:[{}]{}".format(item1["studentId"],item1["studentName"]))
                    auth.policy(
                        username= item1["studentId"],
                        cname= item1["studentName"],
                        card= item1["studentCard"],
                        starttime=rs.startDate,
                        endtime=rs.endDate,
                        devindex="{}_{}_{}".format(record.device.id,record.course.id,inspectRS.experiment.id)
                    )
                    
                inspectRS.teachers=[]
                for item1 in item["teachers"]:
                    inspectRS.teachers.append(edict({
                        "username": item1["teacherId"],
                        "cname": item1["teacherName"],
                        "card": item1["teacherCard"]
                    }))
                    app.logservice("info","添加教师:[{}]{}".format(item1["teacherId"],item1["teacherName"]))
                    auth.policy(
                        username=item1["teacherId"],
                        cname= item1["teacherName"],
                        card=  item1["teacherCard"],
                        starttime=rs.startDate,
                        endtime=rs.endDate,
                        devindex="{}_{}_{}".format(record.device.id,record.course.id,inspectRS.experiment.id)
                    )
                record.InspectionRecord=[inspectRS]
                f=open(recordfile+"/record.json","w")
                f.write(record.toJsonString(True).replace("u'","\"").replace("'","\""))
                f.close()
                app.logservice("info","生成文件:"+recordfile+"/record.json")
        else:
            app.logservice("info","放弃生成课程{}的实验项目{},因为时间{}过期".format(rs.courses[0]["courseId"],item["items"][0]["itemId"],rs.endDate))
            # app.logservice("info",".format())


    return {"result":True}
@route.get("/api/order/<crc>")
def getername(route,crc,request,response=None):
    print base64.b64decode(crc)
    request.response_head['Content-Type'] = 'text/html'
    return open(request.RootDir+"/order.html", 'r').read()
@route.get("/api/getuser/<username>")
def getername(route,username,request,response=None):
    result=getUser(username=username)
    result.username=username
    result.code=404 if "code" not in result else result.code
    print result
    return result
@route.get("/api/getcard/<card>")
def getername(route,card,request,response=None):
    result=getUser(card=card)
    result.card=card
    result.code=404 if "code" not in result else result.code
    print result
    return result
@route.get("/api/getpolicy/user/<username>")
def getername(route,username,request,response=None):return app("auth.searchuser",username=username)
@route.get("/api/getpolicy/card/<card>")
def getername(route,card,request,response=None):return app("auth.searchuser",card=card)
@route.get("/api/order/user/<username>/datetime/<datetime>")
def addOrder(route,username,dt,request,response=None):
    # web=route.parent
    auth=app.module.auth
    websocket=app.module.input
    client=checkwebsocketclient(request.addr[0])
    if not client:client=checkwebsocketclient("127.0.0.1")
    # result=app("auth.searchuser",username=username)
    result=getUser(username=username)
    if result and result.code==200:#result=edict({code=result.code,record.code=404record.msg="找不到预约人记录"})
        user=edict(username=result.username,cname=result.cname)
        data=edict({"cmd": "show library id", "result":edict(),"datetime": str(datetime.now())[:19]})
        record=edict()
        courseid=str(datetime.now())[:19].replace(":","").replace(" ","").replace("-","")
        datapath=os.path.abspath(os.path.join(app.rootpath,"."+app.cfg.services.webroot,"./data/inspection"))
        orderpath=os.path.join(datapath,courseid)
        os.mkdir(orderpath)
        orderfile=os.path.join(orderpath,"record.json")
        # 生成实验项目
        start=str(datetime.now())[:19]
        end=str(datetime.now())[:10]+" "+dt
        makeRecord(orderfile,start,end,courseid,username,user.cname)
        #生成白名单
        user.update(edict({"starttime":start,"endtime":end}))
        user.devindex="{}_{}_01".format(app.cfg.device.id,courseid)
        auth.policy(**user)
        app.logservice("info",auth.policy)
        # 发送到前端
        data.result.username=username
        data.result.cname=user.cname
        data.result.courseid=courseid
        data.result.cmd="show library id"
        data.result.experimentid="01"
        if client:data.result.clientid=client["id"]
        data.result.filename= orderfile
        data.result.code=200
        data.result.Path=orderpath+"/01"
        data.result.InspectionRecord=edict({"experiment": {"id": "01","name": "现场预约"},"teachers":[],"UpLoad":[],"Record": [],"datetime":{"starttime":start,"endtime":end}})
        websocket.websocket.send(data,client)
        app.logservice("info","websocket send{}:".format(client),data) 
        return data
    return {"result":result}
@route.get("/api/order/user/<username>/<passwd>/datetime/<datetime>")
def addOrder(route,username,passwd,dt,request,response=None):
    # web=route.parent
    auth=app.module.auth
    websocket=app.module.input
    client=checkwebsocketclient(request.addr[0])
    if not client:client=checkwebsocketclient("127.0.0.1")
    result = getUser(username = username)
    if result and result.code==200:#result=edict({code=result.code,record.code=404record.msg="找不到预约人记录"})
        user=edict(username=result.username,cname=result.cname)
        data=edict({"cmd": "show library id", "result":edict(),"datetime": str(datetime.now())[:19]})
        record=edict()
        courseid=str(datetime.now())[:19].replace(":","").replace(" ","").replace("-","")
        datapath=os.path.abspath(os.path.join(app.rootpath,"."+app.cfg.services.webroot,"./data/inspection"))
        orderpath=os.path.join(datapath,courseid)
        os.mkdir(orderpath)
        orderfile=os.path.join(orderpath,"record.json")
        # 生成实验项目
        start=str(datetime.now())[:19]
        end=str(datetime.now())[:10]+" "+dt
        makeRecord(orderfile,start,end,courseid,username,user.cname)
        #生成白名单
        user.update(edict({"starttime":start,"endtime":end}))
        user.devindex="{}_{}_01".format(app.cfg.device.id,courseid)
        auth.policy(**user)
        app.logservice("info",auth.policy)
        # 发送到前端
        data.result.username=username
        data.result.cname=user.cname
        data.result.courseid=courseid
        data.result.cmd="show library id"
        data.result.experimentid="01"
        if client:data.result.clientid=client["id"]
        data.result.filename= orderfile
        data.result.code=200
        data.result.Path=orderpath+"/01"
        data.result.InspectionRecord=edict({"experiment": {"id": "01","name": "现场预约"},"teachers":[],"UpLoad":[],"Record": [],"datetime":{"starttime":start,"endtime":end}})
        websocket.websocket.send(data,client)
        app.logservice("info","websocket send{}:".format(client),data) 
        return data
    return {"result":result}
@route.get("/api/uvccamer")
def openuvccamer(route,request,response=None):return str(app.mjpgstreamer)
@route.get("/api/openuvccamer")
def openuvccamer(route,request,response=None):return app("mjpg-streamer start")
@route.get("/api/device/picamera/url")
def getRPiCameraURL(route,request,response=None):
    this=app.servercfg.webservice.rpicamera
    url="http://<host>:{}{}".format(this.port,this.streamer)
    return str(url)
@route.get("/api/device/uvccamera/url")
def getUVCCameraURL(route,request,response=None):
    this=app.servercfg.webservice.uvccamera
    url="http://<host>:{}{}".format(this.port,this.streamer)
    return str(url)
@route.get("/api/record/showlibrary/today")
def showlibrary(route,request,response=None):return app("show library",str(datetime.now()))
@route.get("/api/showlibraryid/<username>/<courseid>/<id>")
def showlibraryid(route,username,courseid,experimentid,request,response=None):
    data=edict()
    data.username=username
    data.courseid=courseid
    data.experimentid=experimentid
    result=app("show library id",**data)
    return result
@route.get("/api/takepicture/<username>/<courseid>/<id>")
def getPicture(route,username,courseid,experimentid,request,response=None):
    data=edict()
    data.OperatorUserName=username
    data.courseid=courseid
    data.experimentid=experimentid
    data.cmd="take picture"
    return app("take picture",OperatorUserName=username,courseid=courseid,experimentid=experimentid,type="take picture")
@route.get("/startrecord/<moivetype>/<username>/<courseid>/<id>")
def startmovierecord(route,moivetype,username,courseid,experimentid,request,response=None):
    data=edict()
    if   moivetype=="usb"    :data.cmd="start record moive"
    elif moivetype=="network":data.cmd="start network video record"
    data.OperatorUserName=username
    data.courseid=courseid
    data.experimentid=experimentid
    result=app(data.cmd,data)
    return result
@route.get("/endrecord/<moivetype>/<username>/<courseid>/<id>")
def endmovierecord(route,moivetype,username,courseid,experimentid,request,response=None):
    data=edict()
    if   moivetype=="usb"    :data.cmd="end record moive"
    elif moivetype=="network":data.cmd="end network video record"
    data.username=username
    data.courseid=courseid
    data.experimentid=experimentid
    return app(data.cmd,data)
def getUser(**argv):
    result=app("auth.searchuser",**argv)
    user=edict({'username':argv["username"] if "username" in argv else "",'cname':""})
    if result:
        user=edict(result.user)
        app.module.auth.userbuff(**result.user)
        user.code=200
        user.msg=""
    else:
        user.code=404
        user.msg="用户不存在！"
    return user
def checkwebsocketclient(ip):
    client=None
    for key in app.module.input.clients:
        client=app.module.input.clients[key]
        if "address" in client and client.address[0]==ip:break
        else:client=None
    return client
def makeRecord(filename,start,end,courseid,username,cname):
    f=JsonFile(filename)
    powerdate=edict({"starttime":start,"endtime":end})
    record=edict()
    record.device=edict({"ip":app.cfg.device.ip,"id":app.cfg.device.id,"name":app.cfg.device.name})
    record.course=edict({"id":courseid,"name":"公共开放实验" if courseid=="share" else "现场预约" })
    experiment=edict({"experiment": {"id": "01","name": "现场预约"},"teachers":[],"UpLoad":[],"Record": [],"datetime":powerdate})
    if courseid!="share":experiment.teachers.append(edict({"username":username,"cname":cname}))
    record.InspectionRecord=[experiment]
    record.lab=edict({"id": app.cfg.device.labid,"name":app.cfg.device.labname})
    f.data=record
    f.Savefile()

