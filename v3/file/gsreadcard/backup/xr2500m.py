# -*- coding:utf-8 -*-
import sys,os,threading,platform,time
path=sys.path[0]
sys.path.append(path+"/../../..")
from lib import *
try:   from Queue import Queue
except:from queue import Queue
from lib.iot.gsreadcard import ReadCard
def readdata(card,status):
    print card,status
def logdata(data):
    if data!="":pass #print "log:",data
def errordata(data):
    if data!="":pass

if __name__ == "__main__":
    o=ReadCard()
    o.modulename="xr2500m"
    o.serialname="/dev/ttyUSB1"
    # o=ReadCard(port,device)
    o.ReadData=readdata
    o.Open()
    print o.isOpen()