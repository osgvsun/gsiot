#!/bin/python
# _*_ coding:utf-8 _*_
import os,sys,io,numpy,threading,time,urllib2,signal
import subprocess,shlex,errno
from PIL import Image,ImageDraw,ImageFont
from datetime import datetime
import requests
try:import cv2
except:cv2=None

__version__ = '0.2.3'
path=sys.path[0]

class FFmpeg(object):
    def __init__(self, executable='ffmpeg', global_options=None, inputs=None, outputs=None):
        self.executable = executable
        self._cmd = [executable]
        global_options = global_options or []
        if _is_sequence(global_options):
            normalized_global_options = []
            for opt in global_options:
                normalized_global_options += shlex.split(opt)
        else:
            normalized_global_options = shlex.split(global_options)
        self._cmd += normalized_global_options
        self._cmd += _merge_args_opts(inputs, add_input_option=True)
        self._cmd += _merge_args_opts(outputs)

        self.cmd = subprocess.list2cmdline(self._cmd)
        self.process = None
        self.input_data=None
    def __repr__(self):
        return '<{0!r} {1!r}>'.format(self.__class__.__name__, self.cmd)
    def run(self, input_data=None, stdout=None, stderr=None):
        try:
            self.process = subprocess.Popen(
                self._cmd,
                stdin=subprocess.PIPE,
                stdout=stdout,stderr=stderr
            )
        except OSError as e:
            if e.errno == errno.ENOENT:
                raise FFExecutableNotFoundError("Executable '{0}' not found".format(self.executable))
            else:
                raise
        self.input_data=input_data
        return self
    def sync(self):
        out = self.process.communicate(input=self.input_data)
        if self.process.returncode != 0:
            raise FFRuntimeError(self.cmd, self.process.returncode, out[0], out[1])
        return out
    def stop(self,wait=0):
        if wait!=0:time.sleep(wait)
        self.kill()
    def kill(self):
        try:os.kill(self.process.pid, signal.CTRL_C_EVENT)
        except:os.kill(self.process.pid,signal.SIGINT)
class FFprobe(FFmpeg):
    def __init__(self, executable='ffprobe', global_options='', inputs=None):
        super(FFprobe, self).__init__(
            executable=executable,
            global_options=global_options,
            inputs=inputs
        )
class FFExecutableNotFoundError(Exception):
    """Raise when FFmpeg/FFprobe executable was not found."""
class FFRuntimeError(Exception):
    def __init__(self, cmd, exit_code, stdout, stderr):
        self.cmd = cmd
        self.exit_code = exit_code
        self.stdout = stdout
        self.stderr = stderr

        message = "`{0}` exited with status {1}\n\nSTDOUT:\n{2}\n\nSTDERR:\n{3}".format(
            self.cmd,
            exit_code,
            (stdout or b'').decode(),
            (stderr or b'').decode()
        )

        super(FFRuntimeError, self).__init__(message)
def _is_sequence(obj):
    return hasattr(obj, '__iter__') and not isinstance(obj, str)
def _merge_args_opts(args_opts_dict, **kwargs):
    merged = []
    if not args_opts_dict:
        return merged
    for arg, opt in args_opts_dict.items():
        if not _is_sequence(opt):
            opt = shlex.split(opt or '')
        merged += opt
        if not arg:
            continue

        if 'add_input_option' in kwargs:
            merged.append('-i')

        merged.append(arg)

    return merged
# ffmpeg 推流
class FfmpegRemp(object):
    def __init__(self,**argv):
        self.srshost=argv["host"] if "host" in argv else ""
        self.srsport=argv["port"] if "port" in argv else 0
        self.channel=argv["channel"] if "channel" in argv else ""
        self.isRecord=1
        self.islive=0
        self.modevalue=0 # 值的内容有两个，0代表直播推流，1代表录播
        self.file=argv["file"] if "file" in argv else ""
        self.rtmpUrl = "rtmp://{}:{}/live/{}".format(self.srshost,self.srsport,self.channel)
        if self.file!="":self.modevalue=self.isRecord
        self.fontsize=argv["fontsize"] if "fontsize" in argv else 16
        self.font= ImageFont.truetype(argv["font"], self.fontsize) if "font" in argv else None 
        self.input_devices=None
        self.input_webcamstreamer=None
        self.input_mjpgstreamer=None
        self.input_mjpgpicture=None
        self.input_screen=False
        self.WIDTH = 640
        self.HEIGHT = 480
        self.FPS =7
        self.stat = True
        self.addtime=True
        self.windowname=""
        self.p=None
    def Mode(self,value=None):
        if value==None:return self.modevalue
        else:self.modevalue=value
    def run(self,width=None,height=None,fps=None):
        width=self.WIDTH if width==None else width
        height=self.HEIGHT if height==None else height
        fps=self.FPS if fps==None else fps
        # command = ['ffmpeg',
        # '-y',
        # '-f', 'rawvideo',
        # '-vcodec','rawvideo',
        # '-pix_fmt', 'bgr24',
        # '-s', "{}x{}".format(width, height),
        # '-r', str(fps),
        # '-i', '-',
        # '-c:v', 'libx264',
        # '-pix_fmt', 'yuv420p',
        # '-preset', 'ultrafast',
        # '-f', 'flv', 
        # self.rtmpUrl]
        if self.modevalue==self.islive:
            command = ['ffmpeg',
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
            self.rtmpUrl]
        elif self.modevalue==self.isRecord:
            command = ['ffmpeg',
            '-f', 'rawvideo',
            '-vcodec','rawvideo',
            '-pix_fmt', 'bgr24',
            '-s', "{}x{}".format(width, height),
            '-r', str(fps),
            '-i', '-',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-preset', 'ultrafast',
            '-f', 'mp4', 
            self.rtmpUrl]
        return subprocess.Popen(command, stdin=subprocess.PIPE)
    def Open(self):
        self.stat=True
        if self.input_mjpgpicture!=None:self.task(self.open_ffmpeg_mjpgpicture)
        elif self.input_mjpgstreamer!=None:
            self.stream=urllib2.urlopen(self.input_mjpgstreamer)
            self.bytes=''
            self.task(self.open_ffmpeg_mjpgstreamer)
    def task(self,fun):
        # if self.windowname!="":cv2.namedWindow(self.windowname)
        while(self.stat):
            img=fun()
            try:
                if self.p==None:
                    if self.input_mjpgstreamer!=None:fps=10
                    elif self.input_mjpgpicture!=None:fps=5
                    else:fps=self.FPS
                    w,h=img.size
                    self.p=self.run(w,h,fps)
                self.p.stdin.write(img.tobytes())
            except:pass
        self.Close()
    def open_ffmpeg_mjpgpicture(self):
        r = requests.get(self.input_mjpgpicture)
        if r.status_code==200:
            img=Image.open(io.BytesIO(r.content)) 
            img=self.addDatetime(img) if self.addtime else img
            return img
            # return cv2.cvtColor(numpy.asarray(img),cv2.COLOR_RGB2BGR)
        return None
    def open_ffmpeg_mjpgstreamer(self):
        self.bytes+=self.stream.read(1024)
        a = self.bytes.find('\xff\xd8')
        b = self.bytes.find('\xff\xd9')
        if a!=-1 and b!=-1:
            jpg = self.bytes[a:b+2]
            self.bytes= self.bytes[b+2:]
            img=Image.open(io.BytesIO(jpg))
            img=self.addDatetime(img) if self.addtime else img
            return img
            # return cv2.cvtColor(numpy.asarray(img),cv2.COLOR_RGB2BGR)
        return None
    # 关闭直播
    def Close(self):
        self.stat = False
        try:self.cap.release()
        except:pass
        cv2.destroyAllWindows()
        try:self.p.kill()
        except:pass
    def addDatetime(self,im):
        if self.font!=None:
            text=str(datetime.now())[:19]
            width, height = im.size
            ttfont = self.font#设置字体
            draw = ImageDraw.Draw(im)  # 创建画画对象
            draw.text((0, int(height *0.9)), text, font=ttfont) 
            return im
class FFmpegMjpgStreamerRecord():
    def __init__(self,mjpgurl,filename):
        self.filename=filename
        if os.path.exists(self.filename):os.remove(filename)
        self.fps=15
        self.url=mjpgurl
        self.font=None#ttfont =ImageFont.truetype(path+"/simhei.ttf", 20)#设置字体
        self.isruning=False
        self.t=None
        self.p=None
        self.mode="snapshot"
    def setFont(self,fontfile,size):
        self.font=ImageFont.truetype(fontfile, size)
    def addDatetime(self,im):    
        text=str(datetime.now())[:19]
        width, height = im.size
        draw = ImageDraw.Draw(im)  # 创建画画对象
        draw.text((0, int(height *0.9)), text, font=self.font) 
        return im
    def Start(self):
        self.isrunning=True
        self.t=threading.Thread(target=self.task)
        self.t.setDaemon(True)
        self.t.start()
    def Stop(self):
        self.isrunning=False
        self.t.join()
    def run(self,width=None,height=None,fps=None):
        ff=FFmpeg(
            inputs={"-":"-f rawvideo -vcodec rawvideo -pix_fmt bgr24 -s {}x{} -r {}".format(width,height,fps)},
            outputs={self.filename:"-preset:v ultrafast -tune:v zerolatency -pix_fmt {} -r {} -f MP4".format("yuv420p" if cv2 else "bgr24",fps )}
        )
        print ff.cmd
        ff.run()
        return ff
    def task(self):
        stream=None
        bytes=''
        self.p=None
        while self.isrunning==True:
            # print "task"
            if self.mode=="streamer":
                if stream==None:stream=urllib2.urlopen(self.url)
                bytes+=stream.read(1024)
                a = bytes.find('\xff\xd8')
                b = bytes.find('\xff\xd9')
                if a!=-1 and b!=-1:
                    jpg = bytes[a:b+2]
                    bytes= bytes[b+2:]
                    self.getimage(jpg)
            elif self.mode=="snapshot":
                r=requests.get(self.url)
                if r.status_code==200:self.getimage(r.content)
        if self.p!=None:self.p.stop()
    def getimage(self,jpg):
        img=Image.open(io.BytesIO(jpg))
        img=self.addDatetime(img)#.transpose(Image.FLIP_LEFT_RIGHT)
        if self.p==None:
            try:
                img=cv2.cvtColor(numpy.asarray(img),cv2.COLOR_RGB2BGR) 
                size = img.shape
                w = size[1] #宽度
                h = size[0]
            except:w,h=img.size
            self.p=self.run(w,h,self.fps)
        try:
            try:img=cv2.cvtColor(numpy.asarray(img),cv2.COLOR_RGB2BGR) 
            except:pass
            self.p.process.stdin.write(img.tobytes())
        except:pass
    #保证单独运行此模块时，能正常运行
if __name__ == "__main__":
    fr = FfmpegRemp(host="116.236.48.10",port=19513,channel="lipydesktop",font=path+"/simhei.ttf",fontsize=30)
    fr.fps=3
    fr.input_mjpgstreamer="http://127.0.0.1:1891/?action=streamer"
    fr.Open()
    # fr.input_devices=1 # 推送本地摄像头
    # fr = FfmpegRemp(host="116.236.48.10",port=19513,channel="lipydesktop",font=path+"/simhei.ttf",fontsize=30)
    # # fr.input_devices=1 # 推送本地摄像头
    # # fr.input_webcamstreamer="rtmp://116.236.48.10:19513/live/031" # 推送指定rtmp
    # # fr.input_screen=True #推送屏幕
    # fr.input_mjpgstreamer="http://127.0.0.1:1891/?action=streamer" # 推送mjpg_stremaer
    # # fr.input_mjpgpicture="http://192.168.0.110:1891/?action=snapshot"  # 推送mjpg_stremaer
    # # fr.windowname="test" #设定显示窗口 ，可不设定
    # fr.Open()            #开始推送
    # url="http://127.0.0.1:8080/?action=streamer"
    # filename=path+"/test.mp4"
    # job=FFmpegMjpgStreamerRecord(url,filename)
    # # job.font=ImageFont.truetype(path+"/simhei.ttf", 20)
    # job.setFont(path+"/simhei.ttf",20)
    # job.Start()       #开始录像
    # time.sleep(10)  #结束录像
    # job.Stop()