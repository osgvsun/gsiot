# -*- coding:utf-8 -*-
import sys,os,platform,threading,requests
from datetime import datetime
if __name__=='__main__':
    path=sys.path[0]
    sys.path.append(path+"/../../..")
from lib import *
from app.devices import App
from lib.file.jsonfile import gsJsonFile as JsonFile
from lib.file.dbfile import dbFile
class AppWebService(gsobject):
    cmd=command_interpreter()
    def __init__(self,Host=None,Port=None):
        gsobject.__init__(self)
        self.cfg=JsonFile(path+"/../../etc/conf/server.json")
        if Host==None:Host=self.cfg.server.usercenter.ip
        if Port==None:Port=self.cfg.server.usercenter.port
        self.url="http://{}:{}".format(Host,Port)
    def __call__(self,cmd,*argv,**keyargv):
        if cmd in self.cmd.cmds:return self.cmd.cmds[cmd](self,*argv,**keyargv)
        else:return None
    def do(self,url):
        ret=edict()
        ret.error_code=0
        try:
            print url
            header = {"x-datasource": "limsproduct"}
            r=requests.get(url,headers=header)
            ret.error_code=r.status_code
            if r.status_code == 200:ret.readstr(r.text.encode("utf-8"))
        except:ret.error_code=1
        return ret
    @cmd.command("webservice.card")
    def cardauthority(self,**value):
        # tmp=self.buff.filter(card=value["cardno"])
        ret=None
        # if tmp==edict():
        result=self.do("{}/api/usercenter/share/getUserByNumber?cardNo={}".format(self.url,value["cardno"]))
        user=result.data if result.code==0 else None 
        username,cname=(user.username,user.userDetail.cname) if user!=None else (None,None)
        ret=username,cname,value["cardno"],result.code
        return ret
        #return self.do("{}/share/getUserByNumber?cardNo={}".format(self.url,value["cardno"]))
    @cmd.command("webservice.password")
    def passwordauthority(self,**value):
        # print "passgvsunlala",value
        return self.do("{}/uaa/apiForMiniProgram/loginByUsernameAndPassword?username={}&password={}".format(self.url,value["username"],value["password"]))
    @cmd.command("webservice.phonepassword")
    def phonepasswordauthority(self,**value):
        result=self.do("{}/uaa/apiForMiniProgram/loginByPhone?phone={}&password={}".format(self.url,value["phone"],value["password"]))
        # user=result.data.user if result.code==200 else None 
        # username,cname=(user.username,user.cname) if user!=None else (None,None)
        # ret=username,cname,result.code
        return result
    @cmd.command("webservice.face")
    def faceauthority(self,**value):return None
    @cmd.command("webservice.username")
    def usernameauthority(self,**value):
        ret=None
        result=self.do("{}/api/usercenter/share/getUserByNumber?employeeNo={}".format(self.url,value["username"]))
        cname=result.data.userDetail.cname if result.code==0 else None
        try:
            if len(result.data.cardList)!=0:card=result.data.cardList[0].cardNo if result.code==0 else None
        except:card=None
        ret=value["username"],cname,card,result.code
        return ret
        #return self.do("{}/share/getUserByNumber?employeeNo={}".format(self.url,value["username"]))
    @cmd.command("webservice.idcard")
    def idcardauthority(self,**value):return self.do("{}/api/usercenter/share/getUserByNumber?idNo={}".format(self.url,value["idcard"]))
    @cmd.command("webservice.phone")
    def phoneauthority(self,**value):return self.do("{}/api/usercenter/share/getUserByNumber?phoneNo={}".format(self.url,value["phone"]))
    @cmd.command("webservice.authority")
    def getAuthority(self,**value):
        url="http://{}:{}/agent/whitepolicy/{}/{}/{}".format(self.cfg.server.iotserver.ip,self.cfg.server.iotserver.port,value["agenttype"],value["ip"],value["username"])
        print url
        return self.do(url)
if __name__ == "__main__":
    path=path+"/../.."
    auth=AppWebService("www.lubanlou.com",80)
    # auth.url="http://www.lubanlou.com"
    print datetime.now()
    print auth("webservice.username",username="20110032")
    print auth("webservice.card",cardno="164887559")
    # print datetime.now()
    # print auth("password",username="20110032",password="gvsun@123").toJsonString()
    # 通过卡号查找是否有权限
    # result=auth("card",cardno="164887559")
    # if result.code==0:print auth("authority",agenttype="guard",ip="192.168.0.152",username=result.data.username).toJsonString()
    # else:print result.toJsonString()
