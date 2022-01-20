# -*- coding:utf-8 -*-
import sys,os,binascii,platform,time,socket,argparse 
from multiprocessing import Process
from threading import Thread
from datetime import datetime
path=sys.path[0]
sys.path.append(path+"/../../..")
from lib import *
from lib.net.client import Client
from lib.net.server import BaseServer,Server,ThreadServer

def receive(addr,data):
    # print serv.clients,addr,data
    client=serv.clients[addr]
    client.send("HTTP/1.1 200 OK\r\n")
    client.send("Content-Type:text/html;\r\n")
    client.send("\r\n\r\n")
    client.send("<h1>sorry,file not found</h1>")
    serv.close(addr)
def task():
    try:
        value=serv.Read()
        if value:printf(datetime.now(),"new client:",value)
    except:pass
    for addr in list(serv.clients.keys()):
        data=serv.Read(addr)
        if data:printf(datetime.now(),addr,"said:",data)
    time.sleep(1)
if __name__ == '__main__':
    # 创建解析器
    parser = argparse.ArgumentParser() 
    parser.add_argument('-host', type=str,help='input a host',default="0.0.0.0")
    parser.add_argument('-port', type=int,help='input a port')
    parser.add_argument('-prototype', type=str,help='input a prototype',default="tcp")
    parser.add_argument('-module', type=str,help='input a run module',default="threadserver")
    args = edict(vars(parser.parse_args()))

    # 调用模块
    # print args.host,args.port,args.module,args.prototype,type(args)
    if not args.port:args.remove("port")
    if args.module=="base":
        serv=BaseServer(host=args.host,port=args.port,prototype=args.prototype)
        serv.Open()
        while True:task()
    elif args.module=="server":
        serv=Server(host=args.host,port=args.port,prototype=args.prototype)
        serv.Open()
        while True:task()
    elif args.module=="threadserver":
        serv=ThreadServer(**args)
        serv.Open()
        print getInterface(serv)#.toJsonString()
        while True:task()
    
