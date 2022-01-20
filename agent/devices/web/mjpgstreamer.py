# -*- coding:utf-8 -*-
import sys,os,platform,threading,json,hashlib
from datetime import datetime
from PIL import Image,ImageDraw,ImageFont
from datetime import datetime
from copy import copy
import io
if __name__=='__main__':
    path=sys.path[0]
    sys.path.append(path+"/../..")
from lib import *
from app.devices import App
app=App(sys.path[0]+"/../..")
route=app.webroute
@route.get("/mjpgstreamer/<videotype>")
def mjpgstreamer(route,videotype,request):
    request.write("HTTP/1.1 200 OK\r\n")
    request.write("Content-Type: multipart/x-mixed-replace; boundary=--aaboundary\r\n")
    request.write("\r\n")
    # font=ImageFont.truetype(app.rootpath+"/etc/font/simhei.ttf", 20) 
    while True:
        if videotype=="screen" and app.module.screen:img=copy(app.module.screen.image)
        elif videotype=="picamera":img=copy(app.image)
        try:
            jpg=io.BytesIO()
            img.save(jpg,format="JPEG")
            jpg=jpg.getvalue()
            request.write("--aaboundary\r\n")
            request.write("Content-Type: image/jpeg\r\n")
            request.write("Content-length: "+str(len(jpg))+"\r\n\r\n" )
            request.write(jpg)
            request.write("\r\n\r\n\r\n")
        except:pass
        time.sleep(0.2)
    return {"result":True}
@route.get("/mjpgsnapshot/<videotype>")
def mjpgsnapshot(route,videotype,request):
    img=None
    if videotype=="screen" and app.module.screen:img=copy(app.module.screen.image)
    elif videotype=="picamera":img=copy(app.image)
    if img:
        request.response_head['Content-Type']="image/jpeg"
        request.isbin=True
        jpg=io.BytesIO()
        img.save(jpg,format="JPEG")
        jpg=jpg.getvalue()
        return jpg
    return img