# -*- coding:utf-8 -*-
from gsiot.v3 import *
from gsiot.v3.file.gsserial import *

class gsDevSerial(gsSerial):
    def __init__(self):
        gsSerial.__init__(self)
        self.baudrate = 2400
        self.parity=self.PARITY_EVEN
        self.modulename="gsSerial.dds253"
        self.istest=True
        self.timeout=0.5
        self.show_log_data=False
        self.isReadElecData=True
        self.readlength=0
        self.moduletype="power"
        # 操作代码
        self.head=b"fefefefe68"
        self.notfind = b""
        self.__findsn = b"fefefefe68999999999999681104353733375116"
        # self.sn="999999999999"
        self.sn=""
        self.indexs=1
    def Test(self,Port):
        ret=False
        self.Open(Port)
        if self.isOpen():
            if self.findsn()!=False:ret=True 
            self.Close()  
            return ret
        else:return False
    def initcmd(self):
        cmd=[]
        for i in range(0,8):cmd.append("00")
        c,d=0,2
        while self.sn=="":
            if self.findsn()==False:c+=1
            if c==d:break
        if self.sn!="":
            sncode=str(self.sn).rjust(12,"0")
            cmd[0]="68"
            cmd[1]=sncode[10:12]
            cmd[2]=sncode[8:10]
            cmd[3]=sncode[6:8]
            cmd[4]=sncode[4:6]
            cmd[5]=sncode[2:4]
            cmd[6]=sncode[0:2]
            cmd[7]="68"
        return cmd
    def getcrc(self,cmd):
        try:
            crc=0
            for i in range(0,len(cmd)):
                if crc==0:crc=int(cmd[i],16)%256
                else:crc+=int(cmd[i],16)%256
            crc=hex(crc)
            crc=str(crc)
            if len(crc)<2:crc="0"+crc
            if len(crc)>2:crc=crc[-2:]
            cmd.append(crc)
            cmd.append("16")
            data="fefefefe"+"".join(cmd)
        except:data=""
        return data
    def findsn(self):
        ret=False
        print self.Read()
        value=self.SendCMD(self.__findsn).replace(self.__findsn,"")
        # print self.serialname,"dds253 send:",self.__findsn
        # print self.serialname,"dds253 recv:",value
        if value!=False and len(value)>11:
            ret=value[14:16]
            ret+=value[12:14]
            ret+=value[10:12]
            ret+=value[8:10]
            ret+=value[6:8]
            ret+=value[4:6]
            self.sn=ret
        else:self.sn=""
        return ret
    def On(self,index=0):
        if self.isOpen()==True:
            cmd=self.initcmd()
            cmd.append("1c")
            cmd.append("09")
            cmd.append("33")
            cmd.append("33")
            cmd.append("33")
            cmd.append("33")    
            cmd.append("87")
            cmd.append("86")
            cmd.append("74")
            cmd.append("78")
            cmd.append("4e")   
            code=self.getcrc(cmd)
            data=self.SendCMD(code).replace(code,"")
            if data=="":return False
            else:return True if data[-6:-4]=="4e" else False
                # result=edict()
                # result.sn=self.sn
                # result.status=self.__getonoffstatus(data)
                # result.vol=self.__getvol(data)
                # result.power=self.__getpower(data)
                # result.current=self.__getcurrent(result.power,result.vol)
                # return result
    def Off(self,index=0):
        if self.isOpen()==True:
            cmd=self.initcmd()
            cmd.append("1c")
            cmd.append("09")
            cmd.append("33")
            cmd.append("33")
            cmd.append("33")
            cmd.append("33")    
            cmd.append("87")
            cmd.append("86")
            cmd.append("74")
            cmd.append("78")
            cmd.append("4d")  
            code=self.getcrc(cmd)
            data=self.SendCMD(code).replace(code,"")
            if data=="":return False
            else:return False if data[-6:-4]=="4d" else True
                # result=edict()
                # result.sn=self.sn
                # result.status=self.__getonoffstatus(data)
                # result.vol=self.__getvol(data)
                # result.power=self.__getpower(data)
                # result.current=self.__getcurrent(result.power,result.vol)
                # return result         
    def ReadPower(self,index=0):
        if self.isOpen()==True:
            cmd=self.initcmd()
            cmd.append("11")
            cmd.append("04")
            cmd.append("33")
            cmd.append("32")
            cmd.append("33")
            cmd.append("b3")
            code=self.getcrc(cmd)
            value=self.SendCMD(code).replace(code,"")
            if value!="":
                result=edict()
                result.sn=self.sn
                result.status=self.__getonoffstatus(value)
                result.vol=self.__getvol(value)
                result.power=self.__getpower(value)
                result.current=self.__getcurrent(result.power,result.vol)
                result.datetime=str(datetime.now())[:19]
                return result
    def ReadStatus(self,index=0):
        if self.isOpen()==True:
            cmd=self.initcmd()
            cmd.append("11")
            cmd.append("04")
            cmd.append("33")
            cmd.append("32")
            cmd.append("33")
            cmd.append("b3")
            code=self.getcrc(cmd)
            value=self.SendCMD(code).replace(code,"")
            if value!="":return self.__getonoffstatus(value)
    def __getonoffstatus(self,value):
        ret=False
        if len(value)<66:status_start,status_end=54,56
        else:status_start,status_end=92,94
        try:
            status_value=value[status_start:status_end]
            if   status_value=="33":ret=True
            elif status_value=="43":ret=False
        except:pass
        return ret
    def __getpower(self,value):
        if len(value)<66: c_start,c_number,ret=48,1,0
        else: c_start,c_number,ret=68,4,(0,0,0,0)
        try:
            for phase in range(0,c_number):
                dy1_value=value[c_start:c_start+2]
                c_start+=2
                dy2_value=value[c_start:c_start+2]
                c_start+=2
                dy3_value=value[c_start:c_start+2]
                c_start+=2
                dy1=hex(int(dy1_value,16)-0x33).replace("0x","")
                dy2=hex(int(dy2_value,16)-0x33).replace("0x","")
                dy3=hex(int(dy3_value,16)-0x33).replace("0x","")
                if c_number==1:ret=round(float(dy3+dy2+dy1)/10,4)
                else:ret[phase]=round(float(dy3+dy2+dy1)/10,4)
        except:pass
        return ret
    def __getvol(self,value):
        if len(value)<66: c_start,c_number,ret=38,1,0
        else: c_start,c_number,ret=38,3,(0,0,0)
        try:
            for phase in range(0,c_number):
                dy1_value=value[c_start:c_start+2]
                c_start+=2
                dy2_value=value[c_start:c_start+2]
                c_start+=2
                dy1="0x"+dy1_value
                dy2="0x"+dy2_value
                dy1=str(hex(int(dy1,16)-0x33))
                dy1=dy1[2:]
                if len(dy1)<2:dy1=dy1+"0"
                dy2=str(hex(int(dy2,16)-0x33))
                dy2=dy2[2:]
                if c_number==1:ret=round(float(dy2+dy1)/10,1)
                else:ret[phase]=round(float(dy2+dy1)/10,1)
        except:pass
        return ret
    def __getcurrent(self,capacity,vol):
        if type(capacity)==type(()):c_number,ret=3,(0,0,0)
        else:c_number,ret=1,0
        try:
            for phase in range(0,c_number):
                if c_number==1:ret=round(float(capacity)/float(vol),4)
                else:ret[phase]=round(float(capacity[phase])/float(vol[phase]),4)
        except:pass
        return ret

if __name__=="__main__":
    dev=gsDevSerial()
    for port in dev.CheckHardware():
        print "%s is    %s"%(port,"dds253")
    dev.Open(port)
    print dev.On()
    # print dev.ReadStatus()
    # time.sleep(0.3)
    # print dev.ReadStatus()
    # print dev.Off()
    # print dev.ReadStatus()
    # # time.sleep(1)
    # # print dev.ReadStatus()
    print dev.ReadPower()
    dev.Close()

   
