#!/usr/bin/python
# -*- coding:utf-8 -*-
from gsiot.v3 import *
from gsiot.v3.file import gsFile
from datetime import datetime,timedelta
# 原型：操作所有Json文件
class gsJsonFile(gsFile):
    def __init__(self,filename):
        gsFile.__init__(self,filename)
        self.flag=True     
        self.list=[]
        self.fields=[]
        self.data=None
        self.Readfile() 
    def __call__(self,**keyargv):return self.newRecord(**keyargv)
    def __str__(self):return self.data.toString(self.flag)  
    def Clear(self):
        for name in self.list:self.__dict__.remove(key)
    def toJsonString(self):return self.data.toJsonString(self.flag)
    def Savefile(self):
        #标记位flag可控制输出中是否包含list
        self._data=self.data.toJsonString(self.flag).replace("u'","\"").replace("'","\"")
        self.Open("w")
        self.Write()
        self.Close()
    def Readfile(self):
        if os.path.isfile(self._name):
            self.Open()
            self.data=edict(self.Read())
            self.Close()
            self.Clear()
            self.list=self.data.list
            for key in self.list:
                if key not in dir(self):setattr(self,key,getattr(self.data,key))
    def newRecord(self,**keyargv):
        keys=[]
        if len(self.fields)==0:self.fields=keyargv.keys()
        else:keys=list(set(self.fields)^set(keyargv.keys()))
        for key in keys:
            try:del keyargv[key]
            except:pass
        if "list" in keyargv:del keyargv["list"]
        key=hashlib.new('md5', str(keyargv)).hexdigest()
        if not self.data:self.data=edict()
        if "key_"+key not in self.data.list:
            exec("self.data.key_{}=edict({})".format(key,keyargv))
        self.Savefile()
        return "key_"+key
    def Remove(self,key):
        self.data.remove(key)
        self.Savefile()
    def Filter(self,**keyargv):
        ret=edict()
        if self.data:
            # System.Console("JsonFile.Filter.data:",self.data.list)
            for prmkey in self.data.list:
                record=self.data[prmkey]
                flag=True
                for key in keyargv:
                    # System.Console("JsonFile.Filter.data:",key)
                    if key in record:
                        if type(keyargv[key]) in [dict,edict] and "between" in keyargv[key]:flag=flag and keyargv[key]["between"]<=record[key]<=keyargv[key]["and"]
                        elif type(keyargv[key]) in [str,unicode] and len(keyargv[key])!=0 and keyargv[key][0]==" ":flag = flag and eval("record[key]"+keyargv[key])
                        elif type(keyargv[key]) in [str,unicode]:flag = flag and keyargv[key].replace("[SPACE]"," ")==record[key]
                        else:flag = flag and keyargv[key]==record[key]
                if flag:ret.update({prmkey:record})
        return  ret
# 扩展：用户缓存
class UserBuffFile(gsJsonFile):
    def __init__(self,filename,delay=1):
        gsJsonFile.__init__(self,filename)
        self.delay=delay
    def newRecord(self,**keyargv):
        nowdatetime=str(datetime.now())[:19]
        lastaccesstime=str(datetime.now()+timedelta(days=self.delay))[:19]
        result=gsJsonFile.Filter(self,username=keyargv["username"])
        if result!=False and len(result.list)!=0 and result[result.list[0]].lastaccesstime>=nowdatetime:
            self.data[result.list[0]].lastaccesstime=lastaccesstime
        else:
            keyargv["list"].append("lastaccesstime")
            gsJsonFile.newRecord(self,lastaccesstime=lastaccesstime,**keyargv)
        self.ReClear()
    def Filter(self,**keyargv):
        result=edict()
        nowdatetime=str(datetime.now())[:19]
        # System.Console("UserBuff.Filter.keyargv:",keyargv)
        r=gsJsonFile.Filter(self,**keyargv)
        # System.Console("UserBuff.Filter:",r)
        for key in r.list:
            record=self.data[key]
            if record.lastaccesstime>=nowdatetime:result.readdict(record)
            else:self.Remove(key)
        return result  
    def ReClear(self):
        if type(self.data)==edict:
            nowdatetime =str(datetime.now())[:19]
            for key in self.data.list:
                record=self.data[key]
                if record.lastaccesstime < nowdatetime:self.Remove(key)
        self.Savefile()
# 扩展：本地权限
class PolicyFile(gsJsonFile):
    def newRecord(self,**keyargv):
        nowdatetime =str(datetime.now())[:19]
        starttime="" if "starttime" not in keyargv else keyargv["starttime"]
        endtime=""   if "endtime"   not in keyargv else keyargv["endtime"]
        if endtime >=nowdatetime:gsJsonFile.newRecord(self,**keyargv)
        self.ReClear()
    def Filter(self,**keyargv):
        nowdatetime =str(datetime.now())[:19]
        records= gsJsonFile.Filter(self,**keyargv)
        if "list" in records.list:records.list.remove("list")
        if records!=False and len(records.list)!=0:
            result=edict()
            result.user=edict()
            result.policy=[]
            for key in records.list:
                record=self.data[key]
                if record.endtime >=nowdatetime:
                    result.user.readdict({"username":record["username"],"cname":record["cname"]})
                    if "card" in record:result.user.card=record["card"]
                    result.policy.append(record)
                else:self.Remove(key)
            if len(result.policy)==0:result=None
            return result
    def ReClear(self):
        if type(self.data)==edict:
            nowdatetime =str(datetime.now())[:19]
            for key in self.data.list:
                record=self.data[key]
                if record.endtime < nowdatetime:self.Remove(key)
        self.Savefile()
# 扩展：电源管理
class ChannelFile(gsJsonFile):
    def __init__(self,filename,channelmax=1):
        gsJsonFile.__init__(self,filename)
        self.flag=False
        self.channelmax=0
        self.channelmax=channelmax
        if len( self.data.list)!=channelmax:self.ClearChannels()
    def ClearChannel(self,node=None):
        if node:
            node.username=""
            node.cname=""
            node.card=""
            node.starttime=""
            node.endtime=""
            self.Savefile()
    def ClearChannels(self):
        self.data.list=[]
        for i in range(1,self.channelmax+1):
            node=edict()
            node.devindex=i
            node.username=""
            node.cname=""
            node.card=""
            node.starttime=""
            node.endtime=""
            nodename="n{}".format(str(i).rjust(2,"0"))
            # self(**{nodename:node})
            setattr(self.data,nodename,node)
            if nodename not in self.data.list:self.data.list.append(nodename)
        self.Savefile()
    def Assign(self):
        records=self.Filter(endtime=" <str(datetime.now())[:19]")
        ret=False if len(records.list)==0 else records[records.list[0]]
        return ret
    def Set(self,**argv):
        devindex=0 if "devindex" not in argv else argv["devindex"]
        channelnode="n{}".format(str(devindex).rjust(2,"0"))
        if channelnode in self.data.list:
            node=self.data[channelnode]
            node.devindex=devindex
            node.username="" if "username" not in argv else argv["username"]
            node.cname="" if "cname" not in argv else argv["cname"]
            node.card="" if "card" not in argv else argv["card"]
            node.starttime="" if "starttime" not in argv else argv["starttime"]
            node.endtime="" if "endtime" not in argv else argv["endtime"]
            self.Savefile()
# 扩展：管理会话，支持http使用
class SessionFile(gsJsonFile):pass


if __name__ == "__main__":
    f=PolicyFile("/research/src/agent/etc/conf/cardpolicy.json")
    result=f.Filter(username="20110032")
    if result:
        # result.flag=False
        print result.toJsonString()
        if len(result.policy)!=0:
            for p in result.policy:
                print p.toJsonString(True)
    else:print result
    # jsonfile=gsJsonFile("/research/src/lib/web/data/inspection/20210705192833/record.json")
    # jsonfile.flag=False
    # print type(jsonfile.data)
    # print jsonfile.toJsonString()
   
    # channel=ChannelFile(path+"/power_runtime.json",4)
    # print channel.Filter(endtime=" <str(datetime.now())[:19]").toJsonString()
    # print channel.Assign().toJsonString()
    # print channel.toJsonString(),channel.data
    # data={"policy": [], "list": ["user", "policy"], "user": {"username": "20110032", "cname": "李品勇", "list": ["username", "cname", "card"], "card": "164887559"}}
    # userbuff=UserBuffFile(path+"/userbuff.json")
    # userbuff(**data["user"])
    # print userbuff
