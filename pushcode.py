# -*- coding:utf-8 -*-
import sys,os,binascii,platform,time,socket,argparse,datetime as dt
from gsiot.v3 import * 
import argparse,datetime
def runcmd(cmd):
    print cmd
    os.system(cmd +"&")
if __name__=="__main__":
    rootpath=os.path.abspath(sys.path[0])
    try:commit=sys.argv[1]
    except:commit=""
    # 首先启动外置摄像头
    runcmd("cd {} && git add -f * && git commit -a -m \"{}自动更新:{}\" && git push".format(sys.path[0],str(dt.date.today()),commit))
    pass