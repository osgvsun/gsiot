# -*- coding:utf-8 -*-
import sys,os,platform,threading,json,hashlib
from datetime import datetime
path=sys.path[0]
sys.path.append(path+"/../../..")
from lib import *

from lib.app.devices import DeviceUnit
from app.devices.web.route import websiteRouter
from lib.file.jsonfile import JsonFile
from lib.file.dbfile import dbFile
route=websiteRouter()
@route.get("/login/<user>/<pass>")
def login(route,user,passwd,request,response=None):
    print "login:",user,passwd
    # modname=http.cfg.website.login.modname
    modname="gvsun"
    module=__import__("app.devices.auth.{}".format(modname),fromlist=["xxxx"])
    auth=getattr(module,"AppWebService")()
    result=auth("webservice.password",username=user,password=passwd) 
    if result["code"]==200:
        data=result["data"]["user"]
        user=edict()
        user.code=200
        user.username=data["username"]
        user.cname=data["cname"]
        user.phone=data["phone"]
        user.id=data["unionid"]
        return user
    else:return result
@route.get("/login/phone/<phone>/<pass>")
def login(route,phone,passwd,request,response=None):
    print "login:",phone,passwd
    # modname=http.cfg.website.login.modname
    modname="gvsun"
    module=__import__("app.devices.auth.{}".format(modname),fromlist=["xxxx"])
    auth=getattr(module,"AppWebService")()
    result=auth("webservice.phonepassword",phone=phone,password=passwd) 
    try:
        if result["code"]==200:
            data=result["data"]["user"]
            user=edict()
            user.code=200
            user.username=data["username"]
            user.cname=data["cname"]
            user.phone=data["phone"]
            user.id=data["unionid"]
            return user
    except:route.parent.app.logservice("info",result)
    return result
@route.get("/policy/<deviceid>/<courseid>/<experimentid>/<username>")
def getPolicy(route,deviceid,courseid,experimentid,username,request,response=None):
    data=edict()
    # data.path="{}{}/{}/record.json".format(route.parent.webroot,route.webdataroot,courseid)
    data.path=route.parent.app.rootpath+"/etc/conf/cardpolicy.json"
    data.deviceid=deviceid
    data.courseid=courseid
    data.experimentid=experimentid
    data.username=username
    policy=route.parent.app.module.auth.policy
    rs=policy.filter(username=username,devindex="{}".format(deviceid))
    data.length=len(rs.list)
    if len(rs.list)==0:
        rs=policy.filter(username=username,devindex="{}_{}_{}".format(deviceid,courseid,experimentid))
        if len(rs.list)==0:
            data.result=False
            data.msg="没权限"
            data.code=404
        else:
            data.result=False
            data.code=200
            data.start=""
            data.end=""
            data.now=str(datetime.now())[:19]
            for key in rs.list:
                item=rs[key]
                print item.start,"<",data.now,item.start<data.now
                if item.end<data.now:
                    # 已过期
                    if data.end<item.end and data.code==200:
                        data.start=item.start
                        data.end=item.end
                elif item.start<data.now:
                    # 命中
                    data.start=item.start
                    data.end=item.end
                    data.code=201
                    data.result=True
                    break
                else:
                    # 未到
                    if data.start>item.start and data.code<203:
                        data.code=202
                        data.start=item.start
                        data.end=item.end
            data.msg="已过期" if data.code==200 else "时间未到" if data.code==202 else "命中"
    else:
        data.result=True
        data.code=220
        data.start=rs[rs.list[0]].start
        data.end=rs[rs.list[0]].end
        data.msg="管理员"
    
    return data
@route.get("/policy/<courseid>")
def getPolicy(route,courseid,request,response=None):
    data=edict()
    data.path="{}{}/{}/record.json".format(route.parent.webroot,route.webdataroot,courseid)
    data.courseid=courseid
    data.body=request.body
    data.param=request.param
    return request
# def getPolicy(username):
#     ret=False
#     for user in users:
#         if user.username==username:
#             ret=True
#             break
#     return ret
@route.get("/login/openface")
def face_open(route,request,response=None):
    route.parent.app("facereadmode",True)
    return {"result":True}
@route.get("/login/closeface")
def face_close(route,request,response=None):
    route.parent.app("facereadmode",False)
    return {"result":True}