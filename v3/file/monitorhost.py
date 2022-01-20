#!/usr/bin/python
# -*- coding:utf-8 -*-
from gsiot.v3 import *

class MonitorHost():
    def __init__(self,host=None,user=None,passwd=None,port=22):
        self.host=host
        self.user=user
        self.passwd=passwd
        self.port=port
        if host:
            from lib.net.client.sshclient import Client
            self.ssh=Client(host=self.host,port=self.port,user=self.user,passwd=self.passwd,timeout=5)
        else:self.ssh=None
    def runas(self,cmd):
        if self.ssh:return self.ssh.runas(cmd)
        else:return os.popen(cmd).read().strip().split("\n")
    def logprint(self,*data):pass
    def Open(self):
        if self.ssh:
            self.ssh.open()
            self.ssh.LogData=self.logprint
    def Close(self):
        if self.ssh:self.ssh.close()
    def memory_stat(self):
        mem = edict()
        lines=self.runas("cat /proc/meminfo")
        for line in lines:
            rs=line.replace(':',"").split()
            line=line[:-1]
            if len(line) < 2:continue
            name = rs[0]
            var = rs[1]
            mem[name] = float(var)
        mem.MemUsed= mem.MemTotal - mem.MemFree - mem.Buffers - mem.Cached
        # #记录内存使用率 已使用 总内存和缓存大小
        res = edict()
        res.percent = int(round(mem.MemUsed / mem.MemTotal * 100))
        res.used= round(mem.MemUsed / (1024 * 1024), 2)
        res.MemTotal = round(mem.MemTotal / (1024 * 1024), 2)
        res.Buffers = round(mem.Buffers / (1024 * 1024), 2)
        return res
    def load_stat(self):
        loadavg = edict()
        con=self.runas("cat /proc/loadavg")[0][:-1].split()
        loadavg.lavg_1=float(con[0])
        loadavg.lavg_5=float(con[1])
        loadavg.lavg_15=float(con[2])
        loadavg.running_process=int(con[3].split('/')[0])
        loadavg.total_process=int(con[3].split('/')[1])
        loadavg.last_pid=int(con[4])
        loadavg.proc=self.getProcess()
        return loadavg
    def disk_stat(self):
        res=[]
        for line in self.runas("df -h")[1:]:
            values=line.split()
            u=edict()
            u.Filesystem,u.Size,u.Used,u.Available,u.percentage,u.point=values         
            res.append(u)
        return res
    def net_stat(self):
        res=edict()
        for line in self.runas("cat /proc/net/dev")[2:]:
            key,values=line[:-1].split(":")
            key=key.strip()
            values=values.strip().split()
            try:
                exec("res.{}.receive={}".format(key,round(float(values[0]) / (1024.0 * 1024.0),2)))
                exec("res.{}.transmit={}".format(key,round(float(values[8]) / (1024.0 * 1024.0),2)))
            except:res.update({key:{"receive":0,"transmit":0}})
        return res
    def searhprocess(self,pname,cmd=None):
        if cmd==None:
            pid=[]
            for item in self.runas("ps -C {} -o pid".format(pname))[1:]:pid.append(int(item[:-1]))
        else:
            try:pid=self.runas("ps -C {} -o pid,cmd |grep {}".format(pname,cmd))[0]
            except:pid=0
        return pid
    def getNetAdapter(self,netadpatername):
        ret=edict()
        values=self.runas("ifconfig {}|grep 'inet '".format(netadpatername))[0].split()
        ret.ipaddress=values[1].replace("addr:","")
        try:ret.netmask=values[3].replace("Mask","")
        except:ret.netmask="255.0.0.0"
        return ret
    def getPortList(self):
        ret=[]
        for item in self.runas("netstat -tpln")[2:]:#netstat -anp|grep LISTEN|grep ':\*'")：
            record=edict()
            value=item.split()[:6]+" ".join(item.split()[6:]).split("/")
            try:record.pid=value[6]
            except:record.pid="-"
            try:record.proc=value[7]
            except:record.proc="-"
            record.iptype=value[0]
            record.host=":".join(value[3].split(":")[:-1])
            record.serviceport=int(value[3].split(":")[-1])
            ret.append(record)
        return ret
    def getProcess(self):
        ret=[]
        for line in self.runas("ps -aux")[1:]:
            record=line.split()
            try:
                ret.append(edict(
                    user=record[0],
                    pid=record[1],
                    cpu=float(record[2]),
                    mem=float(record[3]),
                    vsz=record[4],
                    rss=record[5],
                    tty=record[6],
                    stat=record[7],
                    start=record[8],
                    time=record[9],
                    cmd=" ".join(record[10:])
                ))
            except:printf(len(record),record
        return [rs for rs in ret if rs.cpu!=0.0 ]
if __name__=='__main__':
    o=MonitorHost()
    o.Open()
    printf(o.memory_stat())
    printf(o.load_stat())
    printf(o.net_stat())
    printf(o.disk_stat())
    o.Close()
    printf(
    o=MonitorHost("192.168.0.132","root","gengshang")
    o.showlog(True)
    o.Open()
    printf(o.memory_stat())
    printf(o.load_stat())
    printf(o.net_stat())
    printf(o.disk_stat())
    o.Close()
    print
    o=MonitorHost("192.168.1.11","root","gs123!@#GS")
    o.showlog(True)
    o.Open()
    printf(o.memory_stat())
    printf(o.load_stat())
    printf(o.net_stat())
    printf(o.disk_stat())
    o.Close()
