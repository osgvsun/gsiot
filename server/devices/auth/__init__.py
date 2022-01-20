#!/usr/bin/python
# -*- coding:utf-8 -*-
import os,sys,time,io,json
from datetime import datetime,timedelta
import sqlite3
from copy import copy
if __name__=='__main__':
    path=sys.path[0]
    sys.path.append(path+"/../../..")
from lib import *
from app.devices import App
from lib.app.devices import DeviceUnit
from lib.file.jsonfile import UserBuffFile,PolicyFile
from lib.file.log import logFile

@Singleton
class AuthUnit(DeviceUnit):
    cmd=command_interpreter()
    def __init__(self,app,*argv):
        DeviceUnit.__init__(self,"/app/etc/auth.json",app,"/etc/conf/auth.json",*argv)
        self.userbuff=UserBuffFile(self.app.rootpath+self.cfg.fromcard_username.userbuff,10)
        self.policy=PolicyFile(self.app.rootpath+self.cfg.fromcard_username.policyfile)
        self.runlog=logFile(self.app.rootpath+self.cfg.device.runlog)
    def clearpolicy(self):
        try:self.policy.ReClear()
        except:self.app.logservice("info","清除过期权限保存失败")
    def Open(self,*argv):self.isOpen(True)#采用此种写法可避免模块自动启动后台工作线程
    # 验证成功
    def AuthSuccess(self,**argv):                                                                                                                          
        data=edict()
        data.code=200
        data.sour="auth"
        if "card" in argv:data.msg="认证成功({})\n工号:{}\n姓名:{}".format(argv["card"],argv["username"],argv["cname"])
        else:data.msg="认证成功\n工号:{}\n姓名:{}".format(argv["username"],argv["cname"])
        data.data=argv
        data.autopolicy=1 if self.cfg.fromcard_username.checkpower=="auto" else 0 if self.cfg.fromcard_username.checkpower=="no" else None
        self.app.logservice("info",data.msg)
        self.app("event",type="event_auth",result=data)     
        return data
    # 有预约，但时间没到或时间过期
    def NoTime(self,**argv):
        # self.app.logservice("info","NoTime.argv:",argv)
        data=edict()
        data.code=302
        data.sour="auth"
        data.data=argv
        if "card" in argv:data.msg="认证失败({})\n工号:{}\n姓名:{}\n预约时间为{}-{}".format(argv["card"],argv["username"],argv["cname"],argv["starttime"],argv["endtime"])
        else:data.msg="认证失败\n工号:{}\n姓名:{}\n预约时间为{}-{}".format(argv["username"],argv["cname"],argv["starttime"],argv["endtime"])
        self.app.logservice("info",data.msg)
        self.app("event",type="event_auth",result=data)  
        return data.toString()
    # 找到人了，但没有预约
    def NoPolicy(self,**argv):
        data=edict()
        data.code=301
        data.data=argv
        data.sour="auth"
        if "card" in argv:data.msg="没有相关记录({})\n工号:{}\n姓名:{}".format(argv["card"],argv["username"],argv["cname"])
        else:data.msg="没有相关记录\n工号:{}\n姓名:{}".format(argv["username"],argv["cname"])
        # 人脸不注册是找不到工号的，所以这个不存在
        self.app.logservice("info",data.msg)
        self.app("event",type="event_auth",result=data)
        return data
    # 没有找到人
    def NoUser(self,**argv):
        data=edict()
        data.data=argv
        data.code=404
        data.sour="auth"
        username=None if "username" not in argv else argv["username"]
        card=None if "card" not in argv else argv["card"]
        # 没找到人和权限
        if card!=None:data.msg="认证失败\n卡号{}未注册".format(card)
        # 人脸不注册是找不到工号的，所以这个不存在
        elif username!=None:msg="没有相关记录\n工号：{}".format(username)
        self.app.logservice("info",data.msg)
        self.app("event",type="event_auth",result=data)
        return data
    # 没有资源
    def NoResuce(self,**argv):self.app("event",type="alert",msg="通道已满")
    # 在本地缓存中查找人员
    def getUserBuffDB(self,**argv):
        ret=edict()
        ret.policy=[]
        conn = sqlite3.connect(self.app.rootpath+'/etc/conf/db/userbuff.db')
        #创建一个cursor：
        cursor = conn.cursor()
        #执行查询语句：
        cursor.execute('select * from user where {}={}'.format(argv.keys(),argv.values()))
        #使用featchall获得结果集（list）
        values = cursor.fetchall()
        if len(values):ret.user=values[0]
        #关闭cursor
        #关闭conn
        cursor.close()
        conn.close()
        if len(values):return ret
    def getUserBuff(self,**argv):
        self.app.logservice("info","auth.getUserBuff.argv:",argv) 
        result=self.userbuff.Filter(**argv)
        if result and len(result.list)!=0:
            ret=edict()
            ret.policy=[]
            ret.user=result
            return ret
    # 在物联服务查找权限
    def getPolicyfromIOTServer(self,**argv):
        self.app.logservice("info","getPolicyfromIOTServer.argv:",argv)
        if self.cfg.fromcard_username.authfromiotserver:
            username=None if "username" not in argv else argv["username"]
            card=None if "card" not in argv else argv["card"]
            self.app.logservice("info","根据配置到物联服务上确认权限")
            host=self.app.servercfg.server.iotserver.ip
            port=self.app.servercfg.server.iotserver.port.http
            if card!=None:url=self.cfg.fromcard_username.iotwebservice.fromcard.format(self.app.cfg.device.type,self.app.net(self.app.cfg.device.network).ip,card)
            elif username!=None:url=self.cfg.fromcard_username.iotwebservice.fromusername.format(self.app.cfg.device.type,self.app.net(self.app.cfg.device.network).ip,username)
            url="http://{}:{}{}".format(host,port,url)
            self.app.logservice("info","访问物联服务验证权限：",url)
            r=System.getAPI(url)
            self.app.logservice("info","访问r：",r)
            if r!=False and r.status_code==200:
                # 数据转成json
                record=json.loads(r.content)
                self.app.logservice("info","访问物联服务验证权限：",record)
                result=edict()
                # 如果返回的不是{"key_result":{"err_code":1}}，则加载返回值
                if "err_code" not in record["key_result"]:
                    result.user=edict()
                    result.user.readdict(record["key_result"])
                    result.user.remove("start")
                    result.user.remove("end")
                    result.user.remove("devindex")
                    result.policy=[]
                    result.policy.append(record["key_result"])

                    return result
        else:return False
    # 在用户中心查找人员
    def getUserfromUserCenter(self,**argv):
        if self.cfg.fromcard_username.searchuser=="webservice":
            host=self.app.servercfg.server.usercenter.ip
            port=self.app.servercfg.server.usercenter.port
            if "username" in argv:url=self.cfg.fromcard_username.webservice.username.format(host,port,argv["username"])
            elif "card" in argv :url=self.cfg.fromcard_username.webservice.card.format(host,port,argv["card"])
            header=dict(self.cfg.fromcard_username.webservice.header)
            r=System.getAPI(url,header=header)
            if r!=False and r.status_code==200:
                # 数据转成json
                try:
                    record=json.loads(r.content)
                    result=edict()
                    result.user=edict()
                    result.user.username=record["data"]["username"]
                    result.user.cname=record["data"]["userDetail"]["cname"]
                    try:result.user.card=argv["card"] if "card" in argv else record["data"]["cardList"][0]["cardNo"]
                    except:result.user.card=""
                    result.policy=[]
                    return result
                except:return None
        else:return False
    # 显示错误
    def showErrors(self,e):print "e:",e
    def getPermisssion(self,**argv):
        ret=True
        data={"card":argv["card"]} if "card" in argv else {"username":argv["username"]} if "username" in argv else {}
        self.app.logservice("info","getPermisssion.argv:",data)
        nowdatetime=str(datetime.now())[:19]
        # # 先检查缓存文件
        result=self.app("auth.searchuser",**data)
        self.app.logservice("info","getPermisssion.runtime:",result)
        if result:
            user=result.user
            if "card" not in user and "card" in argv:user.card=argv["card"]
            self.app.logservice("info",user)
            policys=result.policy
            self.userbuff(**user)
            self.userbuff.Savefile()
            logmsg=edict()
            logmsg.username=user["username"]
            logmsg.cname=user["cname"]
            logmsg.cardnumber="" if "card" not in user else user["card"]
            logmsg.datetime=str(datetime.now())[:19]
            self.runlog.writefile(",{}\n".format(logmsg))
            if self.cfg.fromcard_username.checkpower in ["no","auto"]:ret=self.AuthSuccess(**user)
            elif len(policys)!=0:
                policys.sort()
                p=policys[0]
                if p.starttime<=nowdatetime:return self.AuthSuccess(**p)
                else:return self.NoTime(**p)
            else:ret=self.NoPolicy(**result.value.user)
        else:ret=self.NoUser(**argv)
        return ret
    @cmd.command("auth.login")
    def login(self,**argv):
        this=self.app.module.auth
        data=edict(argv)
        if this.cfg.fromlogin.mode=="webservice":
            if "username" in data.list:
                url=this.cfg.fromlogin.webservice.passwd.format(
                    this.app.servercfg.server.usercenter.ip,
                    this.app.servercfg.server.usercenter.port,
                    data.username,
                    data.passwd
                )
            elif "phone" in data.list:
                url=this.cfg.fromlogin.webservice.phone.format(
                    this.app.servercfg.server.usercenter.ip,
                    this.app.servercfg.server.usercenter.port,
                    data.phone,
                    data.passwd
                )
        elif this.cfg.fromlogin.mode=="iotwebservice":pass
        header=dict(this.cfg.device.datasource)
        r=System.getAPI(url,header=header)
        self.app.logservice("info",url,r.status_code if r!=False else r)
        if r!=False and r.status_code==200:
            result=edict(json.loads(r.content))
            self.app.logservice("info",url,result)
            user=edict()
            if   this.cfg.fromlogin.mode=="webservice":
                if result.code==200:
                    user=edict(result.data.user)
                    user.code=200
                else:
                    user=edict(result)
                    user.code=404
            elif this.cfg.fromlogin.mode=="iotwebservice":pass
            System.Console("----user---:",user)
            return user
    @cmd.command("auth.searchuser")
    def searchuser(self,**argv):
        this=self.app.module.auth
        result=gsFaultTolerant(this.policy.Filter,**argv).fail(this.getUserBuff,**argv).fail(this.getPolicyfromIOTServer,**argv).fail(this.getUserfromUserCenter,**argv)
        self.app.logservice("error" if result.runflag==0 else "info searchuser.runtime:",result.value)
        if result.runflag==1 and result.value:
            return result.value
    @cmd.command("auth.checkattendance")
    def auth_setcheckpower(self):
        self.app.module.auth.cfg.fromcard_username.checkpower="no"
        return True
    @cmd.command("auth.checkpowerauto")
    def auth_setcheckpower(self):
        self.app.module.auth.cfg.fromcard_username.checkpower="auto"
        return True
    @cmd.command("auth.checkpower")
    def auth_setcheckpower(self):
        self.app.module.auth.cfg.fromcard_username.checkpower="yes"
        return True

    # 输入
    @cmd.command("auth.from_card")
    def auth_from_card(self,card,status=False):
        this=self.app.module.auth
        ret= self.app("event",card=card,status=status,type="readcard_read")
        if not ret:
            self.app.logservice("info","刷卡事件无返回")
            if status==False:self.app("gpio.operation",**{"pinname":"buzz"})
            elif status and this.cfg.device.mode=="resident":self.app("gpio.operation",**{"pinname":"buzz"})
            if (not status and this.cfg.device.mode=="touchoff") or this.cfg.device.mode=="resident":
                # 检查当前状态，如果有，则
                return self.app.module.auth.getPermisssion(card=card,status=status)
            else:return True
    @cmd.command("auth.from_user")
    def auth_from_username(self,username,score=100.00):
        this=self.app.module.auth
        ret= self.app("event",username=username,score=score,type="face_read")
        if not ret:
            self.app.logservice("info","刷脸事件无返回")
            if score:self.app("gpio.operation",**{"pinname":"buzz"})
            return self.app.module.auth.getPermisssion(username=username)


    # 权限配置
    @cmd.command("clear user buff")
    def auth_userbuff_clear(self):
        self.app.module.auth.userbuff.Clear()
        return True
    @cmd.command("open cardnumber registr")
    def auth_open(self,data=None):
        try:
            self.app.module.auth.policy.Readfile()
            ret=True
        except:ret=False
        return ret
    @cmd.command("close cardnumber registr")
    def auth_close(self,data=None):
        try:
            self.app.module.auth.policy.Savefile()
            self.app.module.auth.clearpolicy()
            ret=True
        except:ret=False
        return ret
    @cmd.command("add cardnumber registr")
    def auth_add(self,**keyargv):
        data=edict(keyargv)
        ret=False
        if data.end >str(datetime.now())[:19]:
            self.app.module.auth.policy(username=data.username,cname=data.cname,card=data.user,starttime=data.start,endtime=data.end,devindex=int(data.guardindex))
            ret=True
            print self.app.module.auth.policy
        return ret
    @cmd.command("clear cardnumber registr")
    def auth_clear(self,data):self.app.module.auth.policy.Clear()
    @cmd.command("event")
    def auth_event(self,*argv,**keyargv):pass