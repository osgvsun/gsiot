# -*- coding: utf-8 -*-
from PIL import Image,ImageFont,ImageDraw
from copy import copy
from gsiot.v3 import * 
# 显示设备接口
class device(gsobject):
    def __init__(self,**argv):
        # 背景图片
        # self.__backimage=None
        # 缓存显示资源
        self.res=edict()
        # 显示设备
        self._display=None
        # 图层
        self.layers=[]
        self.angle=0
        self.expend=None
        if not(argv=={}):
            if ("width" in argv)==True:self.width=argv["width"]
            if ("height" in argv)==True:self.height=argv["height"]
            if ("angle" in argv)==True:self.angle=argv["angle"] 
            if ("expend" in argv)==True:self.expend=argv["expend"] 
        # 图像缓存
        
        self.backcolor=(0,0,0,0)#(4,77,128,0)   #背景颜色
        self.fillcolor=(255,255,255,0)#文字颜色
        self.buffer=Image.new('RGB', (self.width,self.height),self.backcolor)
    def getunit(self):
        ret=edict()
        ret.type     =""
        ret.value    =None
        #位置尺寸
        ret.left     =0      
        ret.top      =0
        ret.width    =0    
        ret.height   =0
        ret.autosize =False#针对文字和图片，自动改变尺寸
        ret.angle    =0    #旋转角度
        # 文字专用
        ret.font     =None #所使用字体
        ret.backcolor=self.backcolor
        ret.fillcolor=self.fillcolor
        ret.isLine   =False#是否全行，当autosize=True and isLine=True时，高度自动变化，宽度为最大宽度
        ret.align    ="center"     #居中，靠左，靠右
        ret.text=""
        return ret
    # 加载资源
    def backimage(self,value=None):
        if value!=None:self.buffer=value
        else:return self.buff
    def loadfont(self,**value):
        if "fontname" in value:
            if "font" in value:
                exec("self.res.f{}=value['font']".format(value["fontname"]))
            else:return eval("self.res.f{}".format(value["fontname"]))
    def loadimage(self,**value):
        if "imagename" in value:
            f=eval("self.res.{}".format(value["imagename"]))
            if "image" in value:f=value["image"]
            else:return f
    # 将文字转换成图片
    def getimagefromtext(self,unit,image=None):
        caption=unit.text.split("\n")
        w,h=(0,0)
        parent=image
        if parent==None:parent=Image.new('RGBA', (self.width,self.height),unit.backcolor)
        draw = ImageDraw.Draw(parent) 
        for text in caption:
            if platform.uname()[0]=="Windows":text = text.decode("gbk")
            else:text = text.decode('utf-8')  # 转换字符编码.
            width, height = draw.textsize(text, font=unit.font)
            if w<width:w=width
            h+=height+5
        if image==None:image = Image.new('RGBA', (w, h), unit.backcolor)
        h=0
        for text in caption:
            if platform.uname()[0]=="Windows":text = text.decode("gbk")
            else:text = text.decode('utf-8') 
            width, height = draw.textsize(text, font=unit.font)
            textdraw = ImageDraw.Draw(image)  
            textdraw.text(((w-width)/2, h), text, font=unit.font, fill=unit.fillcolor)
            h+=height+5
        unit.width, unit.height=width, height
        return image
    # 显示图片
    def display(self):self.buffer.show()
    def show(self):
        self.buffer.paste(Image.new('RGBA', (self.width,self.height),self.backcolor),(0,0))
        for layer in self.layers:
            if   layer.type=="image":self.buffer.paste(layer.value,(layer.left,layer.top))
            elif layer.type=="text" :pass
        if self.expend==None:self.buffer=self.buffer.rotate(self.angle)
        else:self.buffer=self.buffer.rotate(self.angle,expand=self.expend)
        self.display()
    def start(self):pass
    def begin(self):pass
       
if __name__=="__main__":
    dev=device()
    dev.loadfont(fontname=16,font=ImageFont.truetype(path+"/font/simhei.ttf", 16))
    dev.loadfont(fontname=32,font=ImageFont.truetype(path+"/font/simhei.ttf", 32))
    data=['如果安装失败，根据提示先把缺失','的包（比如openjpeg）装上']
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
    dev.start()