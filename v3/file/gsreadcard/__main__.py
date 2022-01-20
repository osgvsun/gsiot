# -*- coding:utf-8 -*-
import sys,os,threading,platform,time,binascii,serial,serial.tools.list_ports,atexit
from datetime import datetime
if __name__=="__main__":
    path=sys.path[0]
    sys.path.append(os.path.abspath(path+"/../../.."))
from lib import *
from lib.file.gsserial import *
from lib.file.gsreadcard import *

def readdata(data):
    if data!="":pass #print str(datetime.now())[:19],"read:",data
def logdata(data):
    if data!="":pass #print "log:",data
def errordata(*data):
    if data[1]!="":
        print edict(data[1]).msg
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
def Read_Card():
    s.ErrorMsg=errordata
    s.Open()
    print s.serialname, s.isOpen()
    while s.isOpen():
        card=s.ReadCard()
        if card=="" and s.LastCard!="":
            print s.LastCard,True
            s.LastCard=""
        elif card!=s.LastCard and card!="":
            print card,False
            s.LastCard=card
if __name__=="__main__":
    try:modulename=sys.argv[1]
    except:modulename=None
    System.CheckSerials()
    print System.getSerialModule(),System.Serials
    if modulename and modulename in System.getSerialModule():s=ReadCard(modulename)
    else:s=ReadCard()
    Read_Card()
    # while True:time.sleep(1)
    