# -*- coding:utf-8 -*-
import sys,os,platform,json,traceback,urllib2,io,cv2,numpy,subprocess
from datetime import datetime
from PIL import Image,ImageDraw,ImageFont
from copy import copy
if __name__=='__main__':
    path=sys.path[0]
    rootpath=os.path.abspath(path+"/../..")
    sys.path.append(rootpath)
    from lib import *
    if isPY2:reload(sys)
    exec("sys.setdefaultencoding('utf-8')")
    assert sys.getdefaultencoding().lower() == "utf-8"
from app.devices import App
import signal
fps=0
p=None
camera=None
start=datetime.now()
def run(width=None,height=None,fps=None):
    command = ['ffmpeg',
    '-hide_banner',
    '-loglevel','info',
    '-f', 'rawvideo',
    '-vcodec','rawvideo',
    '-pix_fmt', 'bgr24',
    '-s', "{}x{}".format(width, height),
    '-r', str(fps),
    '-i', '-',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-preset', 'ultrafast',
    '-f', 'flv', 
    rtmpUrl]
    print "run cmd:"," ".join(command)
    return subprocess.Popen(command, stdin=subprocess.PIPE)
def addDatetime(im):    
    text=str(datetime.now())[:19]
    width, height = im.size
    ttfont =ImageFont.truetype(path+"/../../etc/font/simhei.ttf", 20)#设置字体
    draw = ImageDraw.Draw(im)  # 创建画画对象
    draw.text((0, int(height *0.9)), text, font=ttfont) 
    return im
def getPicture():pass
def pushRtmp():pass
def runcmd(cmd):
    print cmd
    os.system(cmd +"&")
def editConfig(key,node,default):
    if key not in node:node[key]=default
if __name__ == "__main__":
    try:
        app=App(path+"/../..")
        editConfig("camera",app.cfg,{
            "picamera":{
                "picamera_roate":0,
                "mjpgsteamer_picamera":False    
            },
            "usbcamera":false,
            "pushrtmp":false
        })    
        
        if app.cfg.camera.mjpgsteamer_picamera:runcmd("python {}/app/boot/mjpgstreamer.py -x 240 -y 320 -roate {}".format(rootpath,app.cfg.device.picamera_roate))
        if app.cfg.camera.usbcamera:runcmd("python {}/app/boot/mjpgstreamer.py -devtype usbcamera".format(rootpath))
        app.cfg.Savefile()
        app.Open()
        # ip=app.net(app.cfg.device.network).ip.split(".")
        # node=app.servercfg.server.srsserver
        # rtmpUrl="rtmp://{}:{}{}/{}".format(node.ip,node.port,node.url,ip[2]+ip[3])
        # if app.cfg.device.iscamera:
        #     pushpicamera()
            # dev=urllib2.urlopen("http://127.0.0.1:1891/?action=streamer")
            # pushmjpgs(dev,app)
    except Exception,e:
        _, _, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            app.logservice("error","%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname))
        app.logservice("error",e)