# -*- coding:utf-8 -*-
import serial,serial.tools.list_ports,atexit
from gsiot.v3.file.gsserial import *
from gsiot.v3.file.gspower import *

def readdata(data):
    if data!="":print str(datetime.now())[:19],"read:",data
def logdata(data):
    if data!="":pass #print "log:",data
def errordata(*data):
    if data[1]!="":print edict(data[1]).msg
def getModule():
        files=[]
        for filename in os.listdir(path+"/../gsserial"):
            device=filename.split(".")[0]
            if device not in ["test","backup"] and device[:2]!="__" and not(device in files):
                files.append(device)
        return files
def close(s):
    print "close"
    s.Close()
def Read_Power():
    s.ErrorMsg=errordata
    s.Open()
    while s.isOpen() and s.isReadElecData:
        print s.dev.ReadPower()
        time.sleep(1)
        
if __name__=="__main__":
    try:modulename=sys.argv[1]
    except:modulename=None
    System.CheckSerials()
    print System.getSerialModule(),System.Serials
    if modulename and modulename in System.getSerialModule():s=gsOnOff(modulename)
    else:s=gsOnOff()
    Read_Power()
    # while True:time.sleep(1)
    