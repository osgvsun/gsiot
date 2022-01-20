# -*- coding:utf-8 -*-
import sys,os,platform,threading,json,hashlib,requests,io
from datetime import datetime
from PIL import Image,ImageFont,ImageDraw
path=sys.path[0]
sys.path.append(path+"/../../..")
from lib import *
from lib.app.devices import DeviceUnit
from app.devices.web.route import websiteRouter
from lib.file.jsonfile import JsonFile
from lib.net.client.sshclient import Client

route=websiteRouter()
cfg=edict()
cfg.makemoive=False
cfg.makemoive_t=None
cfg.makemoive_startdatetime=None
cfg.makemoive_enddatetime=None
cfg.record=None

@route.get("/runtime/debug")
def getRPiCameraURL(route,request,response=None):
    return {"result":route.parent.app("read runtime mode")}
@route.get("/device/picamera/url")
def getRPiCameraURL(route,request,response=None):
    this=route.parent.app.servercfg.webservice.rpicamera
    url="http://<host>:{}{}".format(this.port,this.streamer)
    return str(url)
@route.get("/device/uvccamera/url")
def getUVCCameraURL(route,request,response=None):
    this=route.parent.app.servercfg.webservice.uvccamera
    url="http://<host>:{}{}".format(this.port,this.streamer)
    return str(url)
@route.get("/device/id")
def getDevice(route,request,response=None):
    return str(route.parent.app.cfg.device.id)
@route.get("/lab/id")
def getDevice(route,request,response=None):
    return str(route.parent.app.cfg.device.labid)
@route.get("/record/showlibrary/today")
def showlibrary(route,request,response=None):
    data=route.parent.app("show library",str(datetime.now()))
    print data
    return data
@route.get("/showlibraryid/<username>/<courseid>/<id>")
def showlibraryid(route,username,courseid,experimentid,request,response=None):
    data=edict()
    data.username=username
    data.courseid=courseid
    data.experimentid=experimentid
    result=route.parent.app("show library id",data)
    route.parent.app.printf("get showlibraryid:",result)
    return result
@route.get("/takepicture/<username>/<courseid>/<id>")
def getPicture(route,username,courseid,experimentid,request,response=None):
    data=edict()
    data.OperatorUserName=username
    data.courseid=courseid
    data.experimentid=experimentid
    data.cmd="take picture"
    return route.parent.app("take picture",data)
@route.get("/startrecord/<moivetype>/<username>/<courseid>/<id>")
def startmovierecord(route,moivetype,username,courseid,experimentid,request,response=None):
    data=edict()
    if   moivetype=="usb"    :data.cmd="start record moive"
    elif moivetype=="network":data.cmd="start network video record"
    data.OperatorUserName=username
    data.courseid=courseid
    data.experimentid=experimentid
    # route.parent.app.printf(route.parent.app,data)
    # route.parent.app.printf(route.parent.app.cmd.cmds[data.cmd])
    result=route.parent.app(data.cmd,data)
    route.parent.app.printf("start record moive 1:",result)
    return result
@route.get("/endrecord/<moivetype>/<username>/<courseid>/<id>")
def endmovierecord(route,moivetype,username,courseid,experimentid,request,response=None):
    data=edict()
    if   moivetype=="usb"    :data.cmd="end record moive"
    elif moivetype=="network":data.cmd="end network video record"
    data.username=username
    data.courseid=courseid
    data.experimentid=experimentid
    return route.parent.app(data.cmd,data)