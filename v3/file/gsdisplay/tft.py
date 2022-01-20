# -*- coding: utf-8 -*-
from datetime import datetime
from PIL import Image,ImageFont,ImageDraw
from copy import copy
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
from gsiot.v3 import *
from gsiot.v3.file.gsdisplay import device
from gsiot.v3.file.gsdisplay.ili9341 import ILI9341
# tk窗口显示
class container(device):
    def __init__(self, **argv):
        device.__init__(self,**argv)
        self.disp=None
        self.buff=None
        self.backimg=None
        self.layers=[]
        self.angle=0
        self.expand=None
        if ("angle" in argv): self.angle =argv["angle"]
        if ("expand" in argv): self.expand =argv["expand"]
        #self.backcolor=(4,77,128)
        self.backcolor=(0,0,0)
        self.fillcolor=(255,255,255)
        self.isonline_interval=0
        self.dc = 3  # 18
        if ("dc" in argv): self.dc =argv["dc"]
        self.RST = 25  # 23
        SPI_PORT = 0
        SPI_DEVICE = 0
        self.disp=Image.new('RGBA', (self.width,self.height),(0, 0, 0, 0))
        if " ".join(platform.uname()).find("Linux") >= 0:
            self.dev = ILI9341(self.dc, rst=self.RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))
            self.dev.begin()
    def backimage(self,value=None):
        if value==None:return self.backimg
        else:self.backimg=Image.open(value)
    def display(self):
        self.buff=copy(self.disp)
        if self.backimg!=None:self.buff.paste(self.backimg,(0,0))
        for layer in self.layers:
            if layer.value!=None:
                strtype=layer.type
                if   strtype=="image":self.buff.paste(layer.value,(layer.left,layer.top))
                elif strtype=="text" :pass
        if self.expend==None:self.buff=self.buff.rotate(self.angle)
        else:self.buff=self.buff.rotate(self.angle,expand=self.expend)
        if " ".join(platform.uname()).find("Windows") >= 0:self.buff.show()
        elif " ".join(platform.uname()).find("Linux") >= 0:
            self.dev.buffer.paste(self.buff,(0,0))
            self.dev.display()
    def getImagefromText(self,data,txtfont,backcolor,fillcolor,parent=None):
        w,h=(0,0)
        if parent==None:parent=self.disp
        draw = ImageDraw.Draw(parent) 
        for text in data.split("\n"):
            text = text.decode('utf-8')  # 转换字符编码.
            # print text
            width, height = draw.textsize(text, font=txtfont)
            # textdraw = ImageDraw.Draw(textimage)  
            draw.text(((w-width)/2, h), text, font=txtfont, fill=fillcolor)
            h+=height+5
        #return self.transparent_back(textimage)
    def getFont(self,fontpath,size):return ImageFont.truetype(fontpath, size)
    def getImage(self,imagefile):return Image.open(imagefile)
    def transparent_back(self,img):
        img=img.convert('RGBA')
        L,H=img.size
        color_0=img.getpixel((0,0))
        for h in range(H):
            for l in range(L):
                dot=(l,h)
                color_1=img.getpixel(dot)
                if color_1==color_0:
                    color_1=color_1[:-1]+(0,)
                    img.putpixel(dot,color_1)
        return img


if __name__=="__main__":
    dev=container(dc=4,angle=0,width=240,height=320)
    dev.loadfont(fontname=16,font=ImageFont.truetype(path+"/font/simhei.ttf", 16))
    dev.loadfont(fontname=32,font=ImageFont.truetype(path+"/font/simhei.ttf", 32))

    data=['如果安装失败，根据提示先把缺失','的包（比如openjpeg）装上']
    for i in range(0,18):data.append(str(i))
    for i in range(0,len(data)):
        o=dev.getunit()
        o.type="image"
        o.left=0
        o.top=i*16
        o.font=ImageFont.truetype(path+"/font/simhei.ttf", 16)
        o.text=data[i]
        o.value=dev.getimagefromtext(o,Image.new('RGB', (320,16),(0,0,0,0)))
        dev.layers.append(o)
    dev.show()
    # dev.start()
