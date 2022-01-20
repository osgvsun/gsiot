# -*- code:utf-8 -*-
import time, os, sys, platform,datetime
# -------------------------------------------------------------
path = sys.path[0]
if path.find("sync") >= 0:
    if " ".join(platform.uname()).find("Windows") >= 0:sys.path.append(path + "\\..\\..")
    elif " ".join(platform.uname()).find("Linux") >= 0:sys.path.append(path + "/../..")
else:sys.path.append(path + "/lib")
reload(sys)                                                             # 须^^

                                                                               sys.setdefaultencoding('utf8')
from lib.data.edict import edict
import urllib2
def getResponse(url):
    response=urllib2.urlopen(url,timeout=10)
    return response.read()
def checkcard(data):
    result=edict()
    result.readdict(eval(data))
    ps=result.result
    flag=True
    # print ps.toJsonString()
    for key in ps.list:
        p=ps[key]
        # print p,type(p)
        if type(p)==type(False):
            flag=False
            break
    # print p,type(p),flag
    return flag
try:
    url='http://192.168.5.201:8082/services/ofthings/data.asp?modname=acldoor&modcmd=list'
    acls=edict()
    acls.readdict(eval(getResponse(url)))
except urllib2.URLError,e:
    print e

# try:
for acl in acls.result:
    print acl
    try:
        url="http://192.168.5.201:8082/services/ofthings/acldoor.asp?cmd=%s&ip=%s"
        ip=str(acl["hardware_ip"])
        mnf=str(acl["manufacturer"])
        getResponse(url%('syncdate',ip))
        print u"%sm%ip
        if mnf=="wiegand":
            while not checkcard(getResponse(url%('readregcard',ip))):
                print u"%s^ְ"%ip
                getResponse(url%('regcard',ip))
            print u"%s%s"%(mnf,ip)
        else:
            getResponse(url%('regcard',ip))
            print u"%s%s^m%(mnf,ip)
    except:
        print u""+ip
# except:pass
