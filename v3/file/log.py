# -*- coding:utf-8 -*-
from gsiot.v3 import *
from gsiot.v3.file import gsFile

class logFile(gsobject):
    def __init__(self,filepath):
        gsobject.__init__(self)
        self.filepath=filepath
        self.__isfolder=False
        self.__isfile=False
        if os.path.isdir(self.filepath):
            self.__isfolder=True
            self.__isfile=False
        elif os.path.isfile(self.filepath):
            self.__isfolder=False
            self.__isfile=True
    def writefile(self,data,file=None):
        if file==None:filepath=self.filepath
        else:filepath=file
        if self.__isfolder==True:filepath=self.filepath+"/{}.log".format(str(datetime.now())[:10].replace('-', '').replace(' ',''))
        if isPY3:
            f=open(filepath,"a",encoding="utf-8")
            data=data.encode("utf-8")
        else:f=open(filepath,"a")
        f.write(str(data))
        f.close()
    def info(self,data):self.writefile("{}--{}:{}\n".format(str(datetime.now())[:19], 'info', data))
    def debug(self,data):self.writefile("{}--{}:{}\n".format(str(datetime.now())[:19], 'debug', data))
    def warning(self,data):self.writefile("{}--{}:{}\n".format(str(datetime.now())[:19], 'warning', data))
    def error(self,data):self.writefile("{}--{}:{}\n".format(str(datetime.now())[:19], 'error', data))
    def log(self,cardno,status=1,username="",cname=""):self.writefile("{},{},{},{},{}\n".format(str(datetime.now())[:19],cardno,username,cname,str(status)))
    def record(self,data,status):self.writefile("{}--{}:{}\n".format(str(datetime.now())[:19],data,str(status)))
    def recordcard(self,data):
        value=edict()
        value.datetime=str(datetime.now())[:19]
        value.cardnumber=data
        self.writefile(",{}\n".format(value))
    def recordusername(self,data):
        value=edict()
        value.datetime=str(datetime.now())[:19]
        value.username=data
        self.writefile(",{}\n".format(value))
    def recordjson(self,jsondata):
        try:
            if not("datetime" in jsondata.list):jsondata.datetime=str(datetime.now())[:19]
        except:pass
        if "list" in jsondata:del jsondata["list"]
        self.writefile(",{}\n".format(jsondata))
    def infos(self,data):self.info(data)


    
