# -*- coding:utf-8 -*-
import sys,os,platform,traceback,cv2,numpy,subprocess,signal,urllib2,io
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
# from lib.file.jsonfile import gsJsonFile as JsonFile
fps=0
p=None
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
    # os.system("killall -9 ffmpeg")
    return subprocess.Popen(command, stdin=subprocess.PIPE)
def addDatetime(im):    
    text=str(datetime.now())[:19]
    width, height = im.size
    ttfont =ImageFont.truetype(path+"/../../etc/font/simhei.ttf", 20)#设置字体
    draw = ImageDraw.Draw(im)  # 创建画画对象
    draw.text((0, int(height *0.9)), text, font=ttfont) 
    return im
def pushpicamera():
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 10
    rawCapture = PiRGBArray(camera, size=(640, 480))
    bytes=''
    p=None
    time.sleep(0.1)
    for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
        img=frame.array
        img=Image.fromarray(img).transpose(Image.FLIP_LEFT_RIGHT)
        app.image=copy(img)
        img=addDatetime(img)
        
       
        if app.cfg.data.device.pushrtmp:
            try:p.stdin.write(img.tobytes())
            except:
                size=camera.resolution
                w = size[0] #宽度
                h = size[1]
                p=run(w,h,camera.framerate)
        rawCapture.truncate(0)
def pushmjpgs(dev,app):
    bytes=''
    p=None
    while True:
        bytes+=dev.read(1024)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')
        if a!=-1 and b!=-1:
            jpg = bytes[a:b+2]
            bytes=bytes[b+2:]
            img=Image.open(io.BytesIO(jpg))
            app.image=copy(img)
            
def pushrtmp(img):
    if app.cfg.data.device.pushrtmp:
        img=addDatetime(img.transpose(Image.FLIP_LEFT_RIGHT))
        img=cv2.cvtColor(numpy.asarray(img),cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        try:p.stdin.write(img.tobytes())
        except:
            size=app.image.size
            w = size[0] #宽度
            h = size[1]
            p=run(w,h,5)
def editConfig(key,node,default):
    if key not in node:node[key]=default
def runcmd(cmd):
    print cmd
    os.system(cmd +"&")
if __name__ == "__main__":
    try:
        app=App(path+"/../..")
        ip=app.net(app.cfg.data.device.network).ip.split(".")
        node=app.servercfg.server.srsserver
        rtmpUrl="rtmp://{}:{}{}/{}".format(node.ip,node.port,node.url,ip[2]+ip[3])
        editConfig("isscreen",app.cfg.device,False)
        editConfig("camera",app.cfg.data,{})
        editConfig("picamera",app.cfg.data.camera,False)
        editConfig("picamera_roate",app.cfg.data.camera,0)
        editConfig("picamera_size",app.cfg.data.camera,"(640,480)")
        editConfig("picamera_mjpgsteamer",app.cfg.data.camera,False)
        editConfig("usbcamera",app.cfg.data.camera,False)
        editConfig("pushrtmp",app.cfg.data.camera,False)
        app.cfg.Savefile()
        app.Open()
        if app.cfg.camera.picamera_mjpgsteamer:
            runcmd("python {}/app/boot/mjpgstreamer.py -x 480 -y 640 -roate {}".format(rootpath,app.cfg.camera.picamera_roate))
            dev=urllib2.urlopen("http://127.0.0.1:1891/?action=streamer")
            pushmjpgs(dev,app)
        else:runcmd("python {}/app/boot/mjpgstreamer.py -cmd stop".format(rootpath))
        if app.cfg.camera.usbcamera:runcmd("python {}/app/boot/mjpgstreamer.py -devtype usbcamera".format(rootpath))
        else:runcmd("python {}/app/boot/mjpgstreamer.py -cmd stop -devtype usbcamera".format(rootpath))
        
    except Exception,e:
        _, _, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            app.logservice("error","%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname))
        app.logservice("error",e)
