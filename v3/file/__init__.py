#!/usr/bin/python
# -*- coding:utf-8 -*-
from gsiot.v3 import *

class VirutalFileSystem(gsobject):
    pass
class gsFile(gsIO):
    # instances = {}
    def __init__(self,filename=None):
        gsIO.__init__(self,filename)
        self.Name="/"
        self._name=os.path.abspath(filename)
        if self._name!="/":self.Name=self._name.split("/")[-1]
        self.extname=os.path.splitext(self._name)[1]
        self.itemtype="file"
        self.ext=os.path.splitext(self._name)[1]
        self.parentFolder=gsFolder(os.path.dirname(self._name))
        if self.ext in CONTENTTYPE:self.ContentType=CONTENTTYPE[self.ext]
        # gsFile.instances.update({self._name:self})
        self._data=None
        self.defaultmethod="r"
        self.strencoding="utf-8"
        self._file=None
        try:self.attr=os.stat(self._name)
        except:self.attr=None
    def Open(self,mode='r'):
        if mode!=None:self.OpenModel(mode)
        else:self.OpenModel(self.defaultmethod)
        if isPY3:
            # 判断文件编码
            # 如果文件不存在，默认就是utf-8
            if os.path.isfile(self._name)==False:self.strencoding="utf-8"
            else:
                # 如果文件存在，尝试读取，在判断
                self._file= open(self._name, 'rb')        # 注意此处打开方式 'rb'
                str_1 =self.file.read()
                self.strencoding = chardet.detect(str_1)['encoding'].lower()
                if self.strencoding[:5]=="utf-8":self.strencoding="utf-8"
                self._file.close()
            self._file=open(self._name,self.OpenModel(),encoding=self.strencoding)
        else:self._file=open(self._name,self.OpenModel())
        self.isOpen(True)
        # if self.defaultmethod!=None:self.defaultmethod()
    def Close(self):
        self._file.close()
        self.isOpen(False)
    def Read(self):
        if self.isOpen()==True: 
            self._data=self._file.read()
            if isPY3 and self.strencoding=="utf-8":pass#self._data=self._data.encode(self.strencoding).decode(self.strencoding)
            elif type(self._data)==type(b""):pass#self._data=self._data.decode(self.strencoding)
            elif isPY2 and isWindows:self._data=self._data.encode("gbk")
            else:self._data=self._data.encode(self.strencoding)     
            return self._data
        else:return None
    def Write(self,value=None):
        if self.isOpen()==True and self.OpenModel() in ["w"]:
            data=""
            self._file.seek(0)
            if self._data:data+=self._data
            if value!=None:data+=value
            self._file.write(data)
            self.attr=os.stat(self._name)
    def Clear(self):self.Write("")            
    def toJson(self):
        if self.isOpen()==False:self.Open()
        data=edict(self.Read())
        self.Close()
        return data
class gsFolder(gsobject):
    def __init__(self,foldername):
        gsobject.__init__(self)
        self.Name="/"
        self._name=os.path.abspath(foldername)
        if self._name!="/":self.Name=self._name.split("/")[-1]
        self.extname="dir"
        self.itemtype="folder"
        self.attr=os.stat(self._name)
    def __call__(self,name):
        item=os.path.join(self._name,name)
        if not os.path.exists(item):return None
        elif   os.path.isdir(item):return gsFolder(item)
        elif os.path.isfile(item):return gsFile(item)
    def createSubFile(self,name):
        filename=os.path.join(self._name,name)
        if os.path.isfile(filename)==False:return gsFile(filename)
    def createSubFolder(self,name,batch=False):
        # batch是批量的意思，在当前目录下可一次性生成多级目录
        folder=os.path.join(self._name,name)
        if os.path.isdir(folder)==False:
            try:
                if batch:os.mkdirs(folder,mode=0o777)
                else:os.mkdir(folder)
            except:pass
    def getParent(self):
        if self._name!="/":path="/".join(self._name.split("/")[:-1])
        else:path="/"
        if path=="":path="/"
        return path
    def list(self):
        ret=[]
        for item in os.listdir(self._name):
            path=self._name+"/"+item
            ret.append(self(path))
        return ret
    def listdir(self):
        ret=[]
        for item in os.listdir(self._name):
            ret.append(item)
        return ret
# class gsWebFile(gsFile):pass
class gsHighperfFile(gsFile):pass
# FileSystem是一个服务，
# 可绑定、获取文件夹和文件
# 可监控文件夹和文件的变化
class gsFileSystem(gsService):pass


if __name__ == "__main__":
    System.Console(sys.path[0])
    f=gsFolder(sys.path[0])
    for item in f.list():
        System.Console(item.Name,item.extname,"=",item._name)
    time.sleep(3)
