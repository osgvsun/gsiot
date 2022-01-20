# -*- coding:utf-8 -*-
import sys,os,platform,threading,json,hashlib
from datetime import datetime
if __name__=='__main__':
    path=sys.path[0]
    sys.path.append(path+"/../..")
from lib import *
from app.devices import App
app=App(sys.path[0]+"/../..")
route=app.webroute
@route.get("/api/login/<user>/<pass>")
def login(route,user,passwd,request):
    result=app("auth.login",username=user,passwd=passwd)
    if not result:result=edict({"code":404})
    return result
@route.get("/api/login/phone/<phone>/<pass>")
def login(route,phone,passwd,request):
    result=app("auth.login",phone=phone,passwd=passwd)
    if not result:result=edict({"code":404})
    return result
@route.get("/api/policy/<deviceid>/<courseid>/<experimentid>/<username>")
def getPolicy(route,deviceid,courseid,experimentid,username,request):
    data=app.module.auth.policy.Filter(username=username,devindex="{}_{}_{}".format(deviceid,courseid,experimentid))
    return data
@route.get("/api/courseid/<courseid>")
def getPolicy(route,courseid,request):
    data=edict()
    webdataroot="/data/inspection"
    data.path="{}{}/{}/record.json".format(app.cfg.services.webroot,webdataroot,courseid)
    data.courseid=courseid
    # data.body=request.body
    # data.param=request.param
    return data
@route.get("/api/login/openface")
def face_open(route,request):return {"result":app("facereadmode",True)}
@route.get("/api/login/closeface")
def face_close(route,request):return {"result":app("facereadmode",False)}