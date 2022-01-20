# -*- coding:utf-8 -*-
import sys,os,time
from datetime import datetime
if __name__=="__main__":
    path=os.path.abspath(sys.path[0])
    sys.path.append(os.path.abspath(path+"/../../.."))
from lib import *
from lib.file.gsserial import *

def readdata(data):
    if data!="":pass #print str(datetime.now())[:19],"read:",data
def logdata(data):
    if data!="":pass #print "log:",data
def errordata(data):
    if data!="":pass
def getModule():
    files=[]
    for filename in os.listdir(path):
        if os.path.isfile(os.path.join(path,filename)):
            device=filename.split(".")[0]
            if device not in ["test","backup"] and device[:2]!="__" and not(device in files):
                files.append(device)
    return files
if __name__=="__main__":
    ret=System.Serials
    for device in getModule():
        print "\rchecking",device,
        module=__import__("lib.file.gsserial.{}".format(device),fromlist=['xxx'])
        o=getattr(module,"gsDevSerial")()
        for port in o.CheckHardware():
            ret[port[5:]]=device
        time.sleep(1)
        print "ok"
    print "\rresult:"," "*50
    print ret.toJsonString()
            # print "\r",
           