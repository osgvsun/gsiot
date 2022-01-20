# -*- coding:utf-8 -*-
import sys,os,platform,threading,requests
from hashlib import md5
from datetime import datetime
path=sys.path[0]
sys.path.append(path+"/../../..")
from lib import *

class AppWebService(gsobject):
    cmd=command_interpreter()
    def __init__(self,Host=None,Port=None):
        gsobject.__init__(self)
        self.cfg=JsonFile(path+"/../etc/conf/server.json")
        if Host==None:Host=self.cfg.server.usercenter.ip
        if Port==None:Port=self.cfg.server.usercenter.port
        self.url=edict()
        self.url.root="http://{}:{}".format(Host,Port)
        self.url.login="/Account/Logon"
        self.url.getpatientid="/Patient/Query"
        self.url.uploadfile="/File/Temp"
        self.url.submitcase="/Patient/MedicalRecord"
        self.local=""#webdataroot
        self.LoginUser=edict()
        self.token=None
        self.Patient=edict()
    def __call__(self,cmd,*argv,**keyargv):
        if cmd in self.cmd.cmds:return self.cmd.cmds[cmd](self,*argv,**keyargv)
        else:return None
    def do(self,url):
        ret=edict()
        ret.error_code=0
        try:
            r=requests.get(url)
            ret.error_code=r.status_code
            if r.status_code == 200:ret.readstr(r.text.encode("utf-8"))
        except:ret.error_code=1
        return ret
    @cmd.command("webservice.password")
    def Login(self,**value):
        url="{}{}".format(self.url.root,self.url.login)
        passmd5=md5(value["password"].encode('utf8')).hexdigest()
        data={"userName":value["username"],"password":passmd5}
        response=requests.post(url,data=data)
        if response.status_code==200:
            value=edict()
            result=edict()
            value.readstr(response.content)
            self.LoginUser=edict()
            self.token=None
            if value.status==True:
                result.msg="success"
                result.code=200
                result.data=edict()
                result.data.user=value.data
                result.data.user.token=value.msg
                self.token=value.msg
                self.LoginUser=value.data
            else:
                result.msg="用户不存在"
                result.code=404
                result.data=None
        return result
    @cmd.command("webservice.getPatient")
    def getPatient(self,**user):
        url="{}{}".format(self.url.root,self.url.getpatientid)
        if self.token!=None:
            data=user
            headers={"authorization":self.token}
            response=requests.post(url,data=data,headers=headers)
            if response.status_code==200:
                result=edict()
                result.readstr(response.content)
                self.Patient=result
                return result
    @cmd.command("webservice.uploadfiles")
    def upLoadFile(self,file):
        url="{}{}".format(self.url.root,self.url.uploadfile)
        if self.token!=None:
            headers={"authorization":self.token}
            files = {'file':open(file,'rb')}
            response=requests.post(url,files=files,headers=headers)
            if response.status_code==200:
                result=edict()
                result.readstr(response.content)
                print result
                return result
    @cmd.command("webservice.uploadcase")
    def submitcase(self):
        url="{}{}".format(self.url.root,self.url.submitcase)
        data=edict()
        data.readdict({"patientid":self.Patient.msg,"doctorid":self.LoginUser.id,"images":[]})
        if self.token!=None:
            for root,dirs,files in os.walk(self.local):
                for file in files:
                    if file!="record.json":
                        data["images"].append(self.upLoadFile(root+"/"+file).msg)
            headers={"authorization":self.token}
            print "submit case:", data.toJsonString()
            response=requests.post(url,data=json.loads(str(data)),headers=headers)
            if response.status_code==200:
                result=edict()
                result.readstr(response.content)
                return result


if __name__ == "__main__":
    auth=AppWebService("testapi.bonjourmed.com")
    # result=auth("password",username="20110032",password="gvsun@123")
    # print result.toJsonString()
    # for item in result.data.schoolList:print item.toJsonString()
    # print auth("username",username="20110032").toJsonString()
    # print auth("card",cardno="3761967508").toJsonString()
    # print auth("phone",phone="18817655325").toJsonString()
    # ("peter","123456")
    print auth("password",username="peter",password="123456").toJsonString()
