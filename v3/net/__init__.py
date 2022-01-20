# -*- coding:utf-8 -*-
# import sys,os,platform,threading,hashlib
# from datetime import datetime
from gsiot.v3 import *
from gsiot.v3.file import gsFile
@Singleton
class Net():
    def __init__(self):
        self.nic=edict()
        self.route=[]
        self.dns=[]
        self.dirlist()
        self.interval=0
        self.taskrunning =False
        self.event=None
        self.wificonf="/etc/wpa.conf"
    def __call__(self,adapter=None):return self.toDict() if adapter==None else self.nic[adapter].data if adapter in self.nic.list else None
    def __task__(self):
        while self.taskrunning==True:
            for key in self.nic.list:
                if key!="lo":self.nic[key].reLoad()
            time.sleep(self.interval)  
    def dirlist(self):
        if platform.uname()[0]=="Linux":
            result=os.popen("cat /etc/network/interfaces|grep dns-nameservers").read()
            if result!="":self.dns=result.replace("dns-nameservers","").strip().split("\n")
            value=os.popen("cat /etc/resolv.conf|grep nameserver").read().replace("nameserver","").strip().split("\n")
            if len(value)>0:self.dns+=value
            for adapter in os.listdir("/sys/class/net"):self.nic[adapter]=NetworkInterface(adapter)
            for line in os.popen("ifconfig |grep flags").read().strip().split('\n'):
                if line!="":
                    adapter=line.split()[0][:-1]
                    if adapter not in self.nic.list:self.nic[adapter.replace(":","_")]=NetworkInterface(adapter)
                
        elif platform.uname()[0]=="Windows":pass
    def reLoad(self):
        for key in self.nic.list:threading.Thread(target=self.nic[key]).start()
    def toDict(self):
        data=edict(dns=self.dns,adapters=edict(),interfaces=self.nic.list)
        for key in self.nic.list:data.adapters.update({key:self.nic[key].data})
        return data
    def OpenEvent(self,s):
        self.interval=s
        self.taskrunning =True
        self.event=threading.Thread(target=self.__task__)
        self.event.setDaemon(True)
        self.event.start()
    def CloseEvent(self):
        self.taskrunning=False
        self.event.join()
    def setConfigFile(self):
        data="# interfaces(5) file used by ifup(8) and ifdown(8)\n\n"
        data+="# Please note that this file is written to be used with dhcpcd\n"
        data+="# For static IP, consult /etc/dhcpcd.conf and 'man dhcpcd.conf'\n\n"
        data+="# Include files from /etc/network/interfaces.d:\n"
        data+="source-directory /etc/network/interfaces.d\n\nauto lo\n"
        data+="iface lo inet loopback\n\n"
        for adapter in self.nic.list:
            if adapter!="lo" and self(adapter).running:
                data+="auto {}\n".format(adapter)
                if self(adapter).iswireless:data+="allow-hotplug {} \n".format(adapter)
                data+="iface {} inet {} \n".format(adapter,"dhcp" if self(adapter).dhcp else "static")
                if self(adapter).iswireless and self.wificonf!="":data+="wpa-conf {}\n".format(self.wificonf)
                if not self(adapter).dhcp and self(adapter).ip!="":
                    data+="address {}\n".format(self(adapter).ip)
                    data+="netmask {}\n".format(self(adapter).netmask)
                    if self(adapter).gateway!="":data+="gateway {}\n".format(self(adapter).gateway)
                data+="\n"
        for rs in self.dns:
            if rs!="127.0.0.1":data+="dns-nameservers {}\n".format(rs)
        return data.replace("_",":")
    def setWifiConfig(self,value):
        self.wificonf=value
        for adapter in self.nic.list:
            if adapter!="" and self(adapter).iswireless:self(adapter).wificonf=value
    def checkip(self,ip):
        flag=True
        for key in self.nic.list:
            if self(key).ip==ip:
                flag=False
                break
        return flag
class NetworkInterface():
    def __init__(self,adapter=None):
        self.adapter=adapter
        self.data=edict(device=adapter,ip="",mac="",netmask="",gateway="",dns="",dhcp=False if self.isdhcp()==False else True,running=False,islinked=False,iswireless=os.path.exists("/sys/class/net/{}/wireless".format(self.adapter)))
        if self.data.iswireless:
            self.data.wifi=edict(signallevel=0,essid="",access_point="",mode="",isinit=False if os.path.isdir("/run/wpa_supplicant")==False else adapter in os.listdir("/run/wpa_supplicant"))
        self.data.flow=edict(rx=0,tx=0)
        self.wificonf="/etc/wpa.conf"
        self.tmpwificonf="/tmp/wpa.conf"
        self()
    def __cmd__(self,cmd):return os.popen(cmd).read().strip().split("\n")
    def __call__(self):
        self.data.islinked=False
        self.data.running=False
        # self.data.iswireless=os.path.exists("/sys/class/net/{}/wireless".format(self.adapter))
        if self.data.iswireless and self.data.wifi.isinit:self.__cmd__("wpa_cli -i {} scan".format(self.adapter))
        for line in self.__cmd__("ifconfig {}".format(self.adapter)):
            try:
                record=line.replace("inet6 addr","inet6_addr").split()
                if   line.find("HWaddr")!=-1:self.data.mac=record[-1]
                elif record[0]=="inet":
                    self.data.ip=record[1].replace("addr:","")
                    self.data.netmask=record[-1].replace("Mask:","")
                    if record[2]=="netmask":self.data.netmask=record[3]
                elif record[0]=="ether":self.data.mac=record[1] if record[1].find(":")!=-1 else record[2]
                elif line.find("UP")!=-1:
                    self.data.islinked=True
                    self.data.running=True if line.find("RUNNING")!=-1 else False
                elif record[0]=="RX":self.data.flow.rx=record[1].replace("packets:") if line.find("packets:")!=-1 else record[2]
                elif record[0]=="TX":self.data.flow.tx=record[1].replace("packets:") if line.find("packets:")!=-1 else record[2]
            except:pass
        for line in self.__cmd__("ip route show|grep default|grep {}".format(self.adapter)):
            if line!="":
                self.data.gateway=line.split()[2]
                break   
        # 如果是无线
        if self.data.iswireless:self.iwConfig()
        # print "ok"
    def ChangeIP(self,**keyargv):
        data=edict(keyargv)
        try:
            result=os.system("ifconfig {} {} netmask {}".format(self.adapter,data.ip,data.netmask))
            self.data.ip=data.ip
            self.data.netmask=data.netmask
            self.data.dhcp=False
            if "gw" in data.list and data.gw!="":
                result=os.system("route add default gw {}".format(data.gw))
                self.data.gateway=data.gw            
        except:return False
    def changeWPConnect(self,**keyargv):
        if self.data.wifi.isinit:self.__cmd__("wpa_cli -i {} disable_network 0".format(self.adapter))
        else:self.ifdown()
        data=edict(keyargv)
        ssid=data.ssid if "ssid" in data.list else self.data.wifi.essid
        psk=data.psk   if "psk"  in data.list else ""
        if psk!="" and ssid!=self.data.wifi.essid:
            self.saveAPconf(ssid=ssid,psk=psk)
            if self.data.running==False:self.ifup()
            self.setInitWifi()
            result=self.__cmd__("wpa_cli -i {} list_network".format(self.adapter))
            flag=False 
            for line in result[1:]:
                try:
                    if line.split()[0]=="Failed":continue
                    id,rs_ssid,_,status=line.split("\t")
                    printf(id,rs_ssid,_,status,flag,ssid)
                    if rs_ssid==ssid:
                        flag=True
                        break
                except:print(line)
            if not flag:
                printf("wpa_cli -i {} add_network".format(self.adapter))
                printf("wpa_cli -i {} set_network 0 ssid '\"{}\"'".format(self.adapter,ssid))
                printf("wpa_cli -i {} set_network 0 psk '\"{}\"'".format(self.adapter,psk))
                printf("wpa_cli -i {} enable_network 0".format(self.adapter))

                self.__cmd__("wpa_cli -i {} add_network".format(self.adapter))
                self.__cmd__("wpa_cli -i {} set_network 0 ssid '\"{}\"'".format(self.adapter,ssid))
                self.__cmd__("wpa_cli -i {} set_network 0 psk '\"{}\"'".format(self.adapter,psk))
                self.__cmd__("wpa_cli -i {} enable_network 0".format(self.adapter))
            else:
                printf("wpa_cli -i {} select_network {}".format(self.adapter,id))
                printf("wpa_cli -i {} enable_network {}".format(self.adapter,id))
                self.__cmd__("wpa_cli -i {} select_network {}".format(self.adapter,id))
                self.__cmd__("wpa_cli -i {} enable_network {}".format(self.adapter,id))
    def setInitWifi(self):
        if not self.data.wifi.isinit:
            printf("wpa_supplicant -Dnl80211 -B -i {} -c {}".format(self.adapter,self.tmpwificonf))
            printf(self.__cmd__("wpa_supplicant -Dnl80211 -B -i {} -c {}".format(self.adapter,self.tmpwificonf)))
            self.data.wifi.isinit=True
            time.sleep(2)
    def ifup(self):
        try:
            if not self.data.islinked:self.__cmd__("ifconfig {} up".format(self.adapter))
            self.data.islinked=True
        except:pass
    def ifdown(self):
        try:
            if self.data.islinked:self.__cmd__("ifconfig {} down".format(self.adapter))
            self.data.islinked=False
        except:pass
    def reDhcp(self):self.__cmd__("dhclient {} &".format(self.adapter))
    def saveAPconf(self,**data):
        f=open(self.tmpwificonf,"w")
        f.write("ctrl_interface=/var/run/wpa_supplicant\n")
        f.write("update_config=1\n")

        f.write("network={\n")
        f.write("\tssid=\"{}\"\n".format(data["ssid"]))
        f.write("\tpsk=\"{}\"\n".format(data["psk"]))
        f.write("}")
        f.close()
    def ScanAP(self):
        aplist=edict()
        self.setInitWifi()
        for line in self.__cmd__("wpa_cli -i {} scan_result".format(self.adapter))[1:-1]:
            value=line.split()
            if len(value)>4:aplist.update(
                {"key_"+value[0].replace(":",""):{
                    "ssid":value[4],"bssid":value[0],
                    "frequency":value[1],"signallevel":int(value[2]),
                    "flags":value[3][1:-1].replace("][",","),
                    "islinked":value[0]==self.data.wifi.access_point
                }})
        return aplist
    def iwConfig(self):
        for line in self.__cmd__("iwconfig {}".format(self.adapter)):
            values=line.replace("Access Point","Access_Point").replace(" GHz","_GHz").replace("ESSID:","ESSID: ").strip().split()
            if   values[0][:4]=="Mode":
                self.data.wifi.mode=values[0].replace("Mode:","")
                self.data.wifi.access_point=values[-1].lower()
                if values[-1]=="Not-Associated":self.data.wifi.access_point=""
            elif len(values)>3 and values[3]=="ESSID:":self.data.wifi.essid=values[4].replace("\"","")
            elif line.find("Signal level")!=-1:
                if line.find("=")!=-1:key,value=line.replace("Signal level","Signal_level").split()[2].split("=",1)
                elif line.find(":")!=-1:key,value=line.replace("Signal level","Signal_level").split()[2].split(":",1)
                if value.find("/")!=-1:
                    a,b =value.split("/",1)
                    self.data.wifi.signallevel=float(a)/float(b)
                else:self.data.wifi.signallevel=int(value)
    def isdhcp(self):
        result=self.__cmd__("cat /etc/network/interfaces|grep '{} inet static'".format(self.adapter))
        if len(result)!=0 and len(result[0])!=0 and result[0][0]!="#":return False
    
if __name__ == "__main__":
    try:adapter=sys.argv[1]
    except:adapter=""
    net=Net()
    if adapter=="":print (net().toJsonString(True))
    elif adapter in net.nic:print net.nic[adapter].data.toJsonString(True)
    else:printf("网卡{}不存在".format(adapter))
    # wlan=net.nic["wlan1"]
    # wlan.changeWPConnect(ssid="GVSUN_SH",psk="5424412888")
    # time.sleep(3)
    # wlan.iwConfig()
    # wlan.ChangeIP(ip="192.168.0.92",netmask="255.255.255.0",gw="192.168.0.1")

    # wlan=net.nic["wlan2"]
    # wlan.changeWPConnect(ssid="GVSUN_TEST",psk="gengshang")
    # time.sleep(3)
    # wlan.iwConfig()
    # wlan.ChangeIP(ip="192.168.96.111",netmask="255.255.255.0",gw="192.168.96.1")
    


