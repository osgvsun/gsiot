#!/usr/bin/env python
# -*- coding: utf8 -*-
import binascii
import time
import RPi.GPIO as GPIO
import signal
import serial
from time import sleep
import os,sys
import datetime
import Image
import ili9341 as TFT
import Adafruit_GPIO.SPI as SPI
import ImageFont
import ImageDraw
import subprocess
import random

path=sys.path[0]
#显示屏SPI接口参数    
DC = 3    #18
RST = 25      #23
SPI_PORT = 0
SPI_DEVICE = 0
#显示屏初始设置
nu=1
x=0
y=0
r=10
g=250
b=200
jd=270
width=240
height=320
backcolor=[(0,0,0)]
backdata=backcolor*(width*height)
# 显示屏函数类Create TFT LCD display class.
disp = TFT.ILI9341(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))
# 初始化显示屏Initialize display.
disp.begin()
# 调入字体.
font = ImageFont.truetype(path+'/simhei.ttf', 24)
#显示屏清屏函数
def clear(disp,backdata):
    disp.buffer.putdata(backdata)
#显示屏清屏函数调用方法
#clear(disp,backdata)
# 创建可旋转显示文字的函数。
def draw_rotated_text(image, text, position, angle, font, fill=(255,255,255)):
    text = text.decode('utf-8')                                    # 转换字符编码.
    draw = ImageDraw.Draw(image)                                # 获取渲染字体的宽度和高度.
    width, height = draw.textsize(text, font=font)
    textimage = Image.new('RGBA', (width, height), (0,0,0,0))    # 创建一个透明背景的图像来存储文字.
    textdraw = ImageDraw.Draw(textimage)                        # 渲染文字.
    textdraw.text((0,0), text, font=font, fill=fill)
    rotated = textimage.rotate(angle, expand=1)                    # 旋转文字图片.
    image.paste(rotated, position, rotated)                        # 把文字粘贴到图像，作为透明遮罩.
#获取IP地址
def myip():
    arg='ip route list' 
    p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE) 
    data = p.communicate() 
    split_data = data[0].split() 
    ipaddr = split_data[split_data.index('src')+1] 
    return ipaddr
#定义串口
ser1 = serial.Serial("/dev/ttyUSB0", baudrate=9600,parity=serial.PARITY_NONE,bytesize=8,stopbits=1, timeout=1)
ser2 = serial.Serial("/dev/ttyUSB1", baudrate=9600,parity=serial.PARITY_NONE,bytesize=8,stopbits=1, timeout=1)
#RFID卡读写函数
def rwcard(c):
    uid=ser2.write(c.decode('hex'))                  
    uid=ser2.read(64)#            
    return uid

#蜂鸣器定义
def buzz(i):
    GPIO.setmode(GPIO.BCM) #BOARD)  
    GPIO.setup(27, GPIO.OUT)  #13
    j=1
    while j<(i+1):
        GPIO.output(27, GPIO.HIGH)  
        time.sleep(0.1)  
        GPIO.output(27, GPIO.LOW)  
        time.sleep(0.1)
        j=j+1
#指示灯定义
def led(i,j):
    if i>2:
        l=18
    elif i==1:
        l=18
    elif i==2:
        l=17
    GPIO.setmode(GPIO.BCM)  
    GPIO.setup(l, GPIO.OUT)  
    if j==1:
        GPIO.output(l, GPIO.HIGH)  
    else:  
        GPIO.output(l, GPIO.LOW) 

#485继电器读写函数
def rw485(c):
    n=ser1.write(c)
    print "send:",binascii.b2a_hex(c)
    str1=ser1.read(20)
    print "recv:",binascii.b2a_hex(str1)
    dy=hexShow(str1)
    return dy
#485继电器读写数据处理
def hexShow(argv):
    result = ""
    hLen = len(argv)
    for i in xrange(hLen):
        hvol = ord(argv[i])
        hhex = "%02x"%hvol
        result += hhex
    return result

# 485继电器指令生成(sn=继电器地址，port=继电器口位，vxoc=操作指令：v-读继电器状态，x-反转继电器状态，o-吸合继电器，c-断开继电器）
def getzl(sn,port,vxoc):
    if vxoc=="allc" or vxoc=="allo":c="13"
    if vxoc=="open":c="12"
    if vxoc=="close":c="11"
    if vxoc=="view":c="10"
    cmd=[0,0,0,0,0,0,0,0,0]
    cmd[1]="55"
    cmd[2]=str(sn)
    if len(cmd[2])<2:cmd[2]="0"+cmd[2]
    cmd[3]=str(c)
    cmd[4]="00"
    cmd[5]="00"
    cmd[6]="00"
    if vxoc=="view" or vxoc=="allc":cmd[7]="00"
    elif vxoc=="allo":cmd[7]="ff"
    else:cmd[7]=str(port)
    if len(cmd[7])<2:cmd[7]="0"+cmd[7]
    crc=0
    for i in range(1,8):
        if crc==0:crc=int(cmd[i],16)%256
        else:crc+=int(cmd[i],16)%256
    crc=hex(crc)
    crc=str(crc)
    if len(crc)>2:crc=crc[-2:]
    if len(crc)<2:crc="0"+crc[-2:]
    zl=""
    for i in range(1,8):
        if zl=="":zl=cmd[i]
        else:zl+=cmd[i]
    zl=zl+crc
    return zl
# 得到sn模块继电器状态
def jdqzt(sn):
    nx=1
    print "sn:",sn
    sncode=getzl(sn,nx,"view")
    c=sncode.decode('hex')
    n=1
    while 1==1:
        print 'jdqzt',binascii.b2a_hex(c)
        cs=rw485(c)
        if len(str(sn))<2:
            snn="0"+str(sn)
        else:
            snn=str(sn)
        if sncode in cs:cs=cs.replace(sncode,"")
        print "cs:",cs
        if "22"+snn in cs:
            zx="1"
            break
        elif n>2:
            zx="0"
            cs="00000000"
            break
        n+=1
    print "第",sn,"模块查询继电器的状态指令",sncode,"返回",cs
    zt="0x"+cs[-4:-2]
    zt=int(zt, 16)
    zt=bin(zt)
    zt=str(zt)[2:]
    xd=8-len(zt)
    ztxs=""
    for i in range(0,xd):
        ztxs=ztxs+"X "
    for i in range(0,len(zt)):
        if zt[i:i+1]=="1":ztxs=ztxs+"O "
        else:ztxs=ztxs+"X "
    num="8 7 6 5 4 3 2 1"
    print "继电器口位编号：",num
    print "继电器开关情况：",ztxs
    print "-----------------------------------------------------------"
    clear(disp,backdata)
    draw_rotated_text(disp.buffer,"继电器开关情况:", (96, 72), jd, font, fill=(125,255,125))        #显示测试次数及时间
    draw_rotated_text(disp.buffer,num, (72, 64), jd, font, fill=(0,255,255))        #显示测试次数及时间
    draw_rotated_text(disp.buffer,ztxs, (48, 64), jd, font, fill=(255,125,255))        #显示测试次数及时间
    disp.display()
    sleep(1)
    return zx
    
# sn模块全部继电器闭合ON
def allopen(sn):
    #  sncode="55 01 13 00 00 00 ff 68"
    nx="1"
    sncode=getzl(sn,nx,"allo")
    sncode=sncode.replace(" ","")
    c=sncode.decode('hex')
    cs=rw485(c)
    if len(str(sn))<2:
        snn="0"+str(sn)
    else:
        snn=str(sn)
    while 1==1:
        if sncode in cs:cs=cs.replace(sncode,"")
        if "22"+snn in cs:break
    print "第",sn,"模块闭合全部继电器指令",sncode,"返回",cs
    sleep(1)
    clear(disp,backdata)
    draw_rotated_text(disp.buffer,sn+"模块全部继电器吸合:", (120, 24), jd, font, fill=(0,255,255))
    disp.display()
# sn模块全部继电器断开OFF
def allclose(sn):
    nx="1"
    #  sncode="55 01 13 00 00 00 00 69"
    sncode=getzl(sn,nx,"allc")
    sncode=sncode.replace(" ","")
    c=sncode.decode('hex')
    cs=rw485(c)
    if len(str(sn))<2:
        snn="0"+str(sn)
    else:
        snn=str(sn)
    while 1==1:
        if sncode in cs:cs=cs.replace(sncode,"")
        if "22"+snn in cs:break
    print "第",sn,"模块断开全部继电器指令",sncode,"返回",cs
    clear(disp,backdata)
    draw_rotated_text(disp.buffer,sn+"模块全部继电器断开:", (120, 24), jd, font, fill=(0,255,255))        #显示测试次数及时间
    disp.display()
# 继电器操作（地址、端口、指令）
def jdqcz(sn,nx,cz):  
    #  while nx<9:
    sncode=getzl(sn,nx,cz)
    c=sncode.decode('hex')
    cs=rw485(c)
    if len(str(sn))<2:
        snn="0"+str(sn)
    else:
        snn=str(sn)
    while 1==1:
        if sncode in cs:cs=cs.replace(sncode,"")
        if "22"+snn in cs:break
    print "第",sn,"模块",nx,"台缝纫机电源",cz,"指令 ",sncode,"返回",cs
    clear(disp,backdata)
    draw_rotated_text(disp.buffer,str(sn)+"模块"+"-"+str(nx)+"台缝纫机"+cz, (124, 48), jd, font, fill=(0,255,255))        #显示测试次数及时间
    disp.display()
    sleep(1)
# 读取继电器模块的地址
def rid():
    sncode="55f540000000008a"
    c=sncode.decode('hex')
    while 1==1:
        cs=rw485(c)
        if sncode+"22" in cs:
            cs=cs.replace(sncode,"")
            break

    sn=cs[2:4]
    print "485jdq模块的地址是：",sn
    return sn
    
##########################
#   程序运行开始
##########################
print "正在自动测试485继电器模块..."
##########################
# 清屏并且显示欢迎词
##########################
clear(disp,backdata)
draw_rotated_text(disp.buffer,"庚商实验室管理系统", (124, 32), jd, font, fill=(r,g,b))
draw_rotated_text(disp.buffer,"缝纫机电源控制测试", (100, 30), jd, font, fill=(r,g,b))
draw_rotated_text(disp.buffer,"采用485继电器控制8台", (60, 20), jd, font, fill=(0,255,0))
disp.display()
sns=["01"]#,"02","03","04","05","06","07","08","09","0a","0b","0c","0d","0e","0f"]
cd=len(sns)
print "预设继电器模块数：",cd 
# 检测实际继电器模块数
print "开始检测有效继电器模块"
print "+++++++++++++++++++++++++++++++++"
i=0                           #有效继电器模块数号
snsa=[]                            #有效继电器模块地址列表
snss=""
snsss=""
clear(disp,backdata)
for i in range(0,cd):
    jc=jdqzt(sns[i])
    # print "jc:"
    draw_rotated_text(disp.buffer,"在线模块：", (196, 48), jd, font, fill=(0,255,255))        #显示测试次数及时间
    draw_rotated_text(disp.buffer,"不在线模块：", (148, 48), jd, font, fill=(0,255,255))        #显示测试次数及时间
    if jc=="1":
        buzz(1)
        print sns[i],"继电器模块在线"
        print "+++++++++++++++++++++++++++++++++"
        snsa.append(sns[i])
        snss+=str(sns[i])+"，"
        draw_rotated_text(disp.buffer,snss, (172, i*24+24), jd, font, fill=(0,255,255))        #显示测试次数及时间
        draw_rotated_text(disp.buffer,snsss, (124, i*24+24), jd, font, fill=(0,255,255))        #显示测试次数及时间
        disp.display()
    else:
        buzz(3)
        print sns[i],"继电器模块不在线"
        print "+++++++++++++++++++++++++++++++++"
        snsss+=str(sns[i])+"，"
        draw_rotated_text(disp.buffer,snss, (172, i*24+24), jd, font, fill=(0,255,255))        #显示测试次数及时间
        draw_rotated_text(disp.buffer,snsss, (124, i*24+24), jd, font, fill=(0,255,255))        #显示测试次数及时间
        disp.display()
    sleep(1)
print snsa
szlen=len(snsa)                      #获得有效电能表的个数
print "有效的设备数：",szlen
for i in range(0,szlen):
    allopen(snsa[i])
    sleep(1)
    allclose(snsa[i])
#jdqzt(sn[i])
print "...................."
print "开始循环测试........"
i=0
while 1==1:
    sn=snsa[i]
    port=1
    ttim1=datetime.datetime.now()
    ttim1=ttim1.strftime("%F-%T")
    print "现在的系统时间是：",ttim1
    while port<9:
    #    port= random.randint(1, 8)
        jdqcz(sn,port,"open")
        jdqzt(sn)
#        sleep(1)
        port+=1
    port=1
    while port<9:
    #    port= random.randint(1, 8)
        jdqcz(sn,port,"close")
        jdqzt(sn)
#        sleep(1)
        port+=1
    i+=1
    if i==szlen:i=0

