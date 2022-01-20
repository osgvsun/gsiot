# -*- coding: utf-8 -*-
from datetime import datetime
import Tkinter as tk
from PIL import Image,ImageFont,ImageDraw,ImageTk
from gsiot.v3 import *
from gsiot.v3.file.gsdisplay import device
# from lib.gui import *
# tk窗口显示
class container(device):
    def __init__(self, **argv):
        device.__init__(self,**argv)
        self.Form = tk.Tk()
        self.Form.title("模拟显示终端")
        screenWidth,screenHeight = self.Form.maxsize()
        self.left=(screenWidth-self.width)/2
        self.top=(screenHeight-self.height)/2-20
        self.Form.geometry('%dx%d+%d+%d'%(self.width,self.height,self.left,self.top)) 
        self.Form.update()
        self.lblback=Label(self.Form)
        self.lblback.move(0,0,self.width,self.height)
    def display(self):self.lblback.image(self.buffer)
    def start(self):self.Form.mainloop()



if __name__=="__main__":
    dev=container()
    # dev.begin()
    dev.loadfont(fontname=16,font=ImageFont.truetype(path+"/font/simhei.ttf", 16))
    dev.loadfont(fontname=32,font=ImageFont.truetype(path+"/font/simhei.ttf", 32))
    data=['如果安装失败，根据提示先把缺失','的包（比如openjpeg）装上']
    for i in range(0,len(data)):
        o=dev.getunit()
        o.type="image"
        o.left=0
        o.top=i*16
        o.font=ImageFont.truetype(path+"/font/simhei.ttf", 16)
        o.text=data[i]#str(i).rjust(2,"0")+":"
        o.value=dev.getimagefromtext(o)
        dev.layers.append(o)
    dev.show()
    dev.start()

