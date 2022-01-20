# -*- coding:utf-8 -*-
import sys,os,threading,platform,time,binascii,serial,serial.tools.list_ports
path=sys.path[0]
sys.path.append(path+"/../../..")
from lib import *
from lib.file.gsserial import *
from lib.file.gspower import *
from datetime import datetime
def readdata(data):
    if data!="":pass #print str(datetime.now())[:19],"read:",data
def logdata(data):
    if data!="":pass #print "log:",data
def errordata(data):
    if data!="":pass
def getModule():
        files=[]
        for filename in os.listdir(path+"/../gsserial"):
            device=filename.split(".")[0]
            if device!="test" and device[:2]!="__" and not(device in files):
                files.append(device)
        return files

if __name__=="__main__":
    try:modulename=sys.argv[1]
    except:modulename=None
    System.CheckSerials()
    if modulename and modulename in System.getSerialModule():s=gsOnOff(modulename)
    else:s=gsOnOff()
    # Read_Card()
#    for device in getModule():
#         if device!="backup":
#             module=__import__("lib.file.gsserial.{}".format(device),fromlist=['xxx'])
#             o=getattr(module,"gsDevSerial")()
#             if o.moduletype=="power":
#                 result=o.CheckHardware(sysserials)
#                 print device
#                 for port in result:
#                     print device,port,"ok"
#                     s=gsOnOff(device)
#                     s.Open()
#                     print s.serialname,s.isOpen()
#                     while True:
#                         # for i in range(0,8):s.On(i)
#                         for i in range(0,8):s.Off(i)
#                     s.Close()
