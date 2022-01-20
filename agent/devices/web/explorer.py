# -*- coding:utf-8 -*-
import sys,os,platform,threading,json,base64
from datetime import datetime
if __name__=='__main__':
    path=sys.path[0]
    sys.path.append(path+"/../..")
from lib import *
from lib.net import *
from app.devices import App
from lib.file import gsFile,gsFolder
from lib.file.jsonfile import gsJsonFile
app=App(sys.path[0]+"/../..")
route=app.webroute
@route("/api/getsystemfolder")
def getfolder(route,request):return {"webroot":app.cfg.services.webroot,"rootpath":app.rootpath}
@route("/api/folder/<name>")
def folderlist(route,name,request):
    if name=="" and request.request_data!={} and "pathfile" in request.request_data:
        path=request.request_data["pathfile"]
    elif name.find("$$")!=-1:path=name.replace("$$","/")
    else:
        try:path=base64.b64decode(name.replace("_","/"))
        except TypeError:path=base64.b64decode(name+"u".replace("_","/"))
        except Exception:return {"result":False,"code":500}
    if os.path.exists(path):
        folder=gsFolder(path)
        data=edict(parentpath=folder.getParent(),parent="/api/folder/"+base64.b64encode(folder.getParent()),folder=edict(),file=edict())
        for item in folder.list():
            if item:
                key=linkdata=""
                try:
                    key=base64.b64encode(item.Name).replace("/","_")
                    linkdata="/api/"+item.itemtype+"/"+base64.b64encode(item._name).replace("/","_")
                    data[item.itemtype].update({key:{"ext":item.extname,"path":item._name,"path0":"/api/"+item.itemtype+"/?pathfile="+item._name,"filename":item.Name,"link":linkdata,"Size":long(item.attr.st_size),"datetime":str(datetime.fromtimestamp(item.attr.st_mtime))[:19]}})
                except:pass
        return {"result":data}
    else:return {"result":False,"folder":path}
@route("/api/file/md/<name>")
def getfile(route,name,request):
    if request.request_data!={} and "pathfile" in request.request_data:
        name=request.request_data["pathfile"]
        del request.request_data["pathfile"]
    elif request.request_data!={} and "filename" in request.request_data:
        name=request.request_data["filename"]
        del request.request_data["filename"]
    if name.find("$$")!=-1:file=name.replace("$$","/")
    elif name.find("/")!=-1:file=name
    else:
        try:file=base64.b64decode(name.replace("_","/"))
        except TypeError,e:file=base64.b64decode(name+"u".replace("_","/"))
    if request.request_data!={}:
        f=gsJsonFile(file)
        print request.request_data
        f.data=edict(request.request_data)
        f.Savefile()
        return {"result":True}
    elif os.path.isfile(file):
        f=gsFile(file)
        if f.extname in request.binfiles:
            request.isbin=True
            f.Open('rb')
        else:f.Open()
        data=msg=f.Read()
        f.Close()
        request.response_head['Content-Type'] = CONTENTTYPE[".html"]
        mdfile=open(app.rootpath+"/app/devices/web/markdown.txt","r")
        data=mdfile.read().replace("<%=filedata%>",msg)
        return data
@route("/api/file/<name>")
def getfile(route,name,request):
    if request.request_data!={} and "pathfile" in request.request_data:
        name=request.request_data["pathfile"]
        del request.request_data["pathfile"]
    elif request.request_data!={} and "filename" in request.request_data:
        name=request.request_data["filename"]
        del request.request_data["filename"]
    if name.find("$$")!=-1:file=name.replace("$$","/")
    elif name.find("/")!=-1:file=name
    else:
        try:file=base64.b64decode(name.replace("_","/"))
        except TypeError,e:file=base64.b64decode(name+"u".replace("_","/"))
    System.Console(request.request_data)
    if request.request_data!={}:
        f=gsJsonFile(file)
        print request.request_data
        f.data=edict(request.request_data)
        f.Savefile()
        return {"result":True}
    elif os.path.isfile(file):
        f=gsFile(file)
        if f.extname in request.binfiles:
            request.isbin=True
            f.Open('rb')
        else:f.Open()
        data=msg=f.Read()
        f.Close()
        if f.extname==".json":data=edict(msg)
        elif f.extname in CONTENTTYPE:request.response_head['Content-Type'] = CONTENTTYPE[f.extname]
        elif not request.isbin:request.response_head['Content-Type'] = CONTENTTYPE[".txt"]
        return data
@route("/api/cp/<sname>/<dname>")
def getfile(route,sname,dname,request):
    if sname.find("$$")!=-1:sitem=sname.replace("$$","/")
    else:
        try:sitem=base64.b64decode(sname.replace("_","/"))
        except TypeError,e:sitem=base64.b64decode(sname+"u".replace("_","/"))

    if dname.find("$$")!=-1:ditem=dname.replace("$$","/")
    else:
        try:ditem=base64.b64decode(dname.replace("_","/"))
        except TypeError,e:ditem=base64.b64decode(dname+"u".replace("_","/"))
    print "cp -r {} {}".format(sitem,ditem),os.path.exists(sitem)
    if os.path.exists(sitem):
        print "cp -r {} {}".format(sitem,ditem)
        os.system("cp -r {} {}".format(sitem,ditem))
    return {"result":True}
@route("/api/delfile/<name>")
def getfile(route,name,request):
    try:item=base64.b64decode(name)
    except TypeError,e:item=base64.b64decode(name+"u")
    cmd="rm -rf {}".format(item)
    print cmd
    os.system(cmd)
    return {"result":True}
@route("/edit/md/*")
def getfile(route,name,request):
    file=app.rootpath+app.cfg.services.webroot+"/"+name
    if not os.path.isfile(file):file+=".md"
    if not os.path.isfile(file):file="/"+name
    if not os.path.isfile(file):file+=".md"
    if os.path.isfile(file):
        f=gsFile(file)
        if f.extname in request.binfiles:
            request.isbin=True
            f.Open('rb')
            request.response_head['Content-Type'] = CONTENTTYPE[f.extname]
            data=f.Read()
            f.Close()
            return data
        else:
            f.Open()
            data=msg=f.Read()
            f.Close()
            request.response_head['Content-Type'] = CONTENTTYPE[".html"]
            mdfile=open(app.rootpath+"/app/devices/web/markdown.txt","r")
            data=mdfile.read().replace("<%=filedata%>",msg)
            return data
    elif name=="wiki/index":
        msg="## 这是李品勇的研发项目]]\n"
        msg+="- 基本算法\n"
        msg+="\t- [关于lib库](./aboutlib)\n"
        msg+="\t- [庚商公司k3s agent添加操作文档](./k3agent)\n"
        msg+="\t- [关于装饰器](./decorator)\n"
        msg+="- 特定组件\n"
        msg+="\t- [Adafruit_GPIO 1.0.3](./setup/Adafruit_GPIO-1.0.3.rar)\n"
        request.response_head['Content-Type'] = CONTENTTYPE[".html"]
        mdfile=open(app.rootpath+"/app/devices/web/markdown.txt","r")
        data=mdfile.read().replace("<%=filedata%>",msg)
        return data
    return {"result":"no file","name":name,"file":file}
@route("/fs/folder/*")
def folderlist(route,name,request):
    if name=="$$":path="/"
    else:path=app.rootpath+app.cfg.services.webroot+"/"+name
    if not os.path.isdir(path):path="/"+name+"/"
    if os.path.isdir(path):
        folder=gsFolder(path)
        data=edict(
            parent="/fs/folder"+"/$$" if folder.getParent()=="/" else folder.getParent(),
            folder=edict(),file=edict())
        for item in folder.list():
            if item:
                key=linkdata=""
                try:
                    key=base64.b64encode(item.Name)
                    linkdata="/fs/"+item.itemtype+path+item.Name
                    data[item.itemtype].update({
                        key:{
                            "ext":item.extname,
                            "path":path+item.Name,
                            "path0":"/api/"+item.itemtype+"/?pathfile="+path+item.Name,
                            "filename":item.Name,
                            "link":linkdata,
                            "Size":long(item.attr.st_size),
                            "datetime":str(datetime.fromtimestamp(item.attr.st_mtime))[:19]}})
                    if item.extname==".md":
                        data[item.itemtype][key]["editLink"]="/edit/md"+path+item.Name
                except:pass
        return {"result":data}
    else:return {"result":False,"folder":path}
@route("/fs/file/*")
def getfile(route,name,request):
    file=app.rootpath+app.cfg.services.webroot+"/"+name
    if not os.path.isfile(file):file="/"+name
    if request.request_data!={}:
        #上传文件
        pass
    elif os.path.isfile(file):
        f=gsFile(file)
        if f.extname in request.binfiles:
            request.isbin=True
            f.Open('rb')
            request.response_head['Content-Type'] = "application/octet-stream" if f.extname not in CONTENTTYPE else CONTENTTYPE[f.extname]
        else:
            f.Open()
            request.response_head['Content-Type'] = CONTENTTYPE[".txt"] if f.extname not in CONTENTTYPE else CONTENTTYPE[f.extname]
        data=f.Read()
        f.Close()
        return data    
    return {"result":"no file","name":name,"file":file}
@route("/fs/bin/file/*")
def getfile(route,name,request):
    file=app.rootpath+app.cfg.services.webroot+"/"+name
    if not os.path.isfile(file):file="/"+name
    if request.request_data!={}:
        #上传文件
        pass
    elif os.path.isfile(file):
        f=gsFile(file)
        request.isbin=True
        f.Open('rb')
        request.response_head['Content-Type'] = "application/octet-stream" if f.extname not in CONTENTTYPE else CONTENTTYPE[f.extname]
        data=f.Read()
        f.Close()
        return data    
    return {"result":"no file","name":name,"file":file}
@route("/fs/ascii/file/*")
def getfile(route,name,request):
    file=app.rootpath+app.cfg.services.webroot+"/"+name
    if not os.path.isfile(file):file="/"+name
    if request.request_data!={}:
        #上传文件
        pass
    elif os.path.isfile(file):
        f=gsFile(file)
        f.Open()
        request.response_head['Content-Type'] = CONTENTTYPE[".txt"] if f.extname not in CONTENTTYPE else CONTENTTYPE[f.extname]
        data=f.Read()
        f.Close()
        return data    
    return {"result":"no file","name":name,"file":file}