# -*- coding:utf-8 -*-
from gsiot.v3 import *
class gsPipe(gsIO):
    def __init__(self, cfg):
        gsIO.__init__(self,cfg.readfile)
        self.cfg = cfg
        self.index=None
        self.__model_type = type
        self.LogData=self.cfg.LogData
        self.ReadData=self.cfg.ReadData
        self.fin = None
        self.fout = None
    def task(self):
        while True:
            self.read()
            time.sleep(0.5)
    def open(self, value=None):
        if value != None: self.OpenModel(value)
        try:
            # 创建命名管道
            if "readfile" in self.cfg:
                filename = self.cfg.readfile
                if self.OpenModel().find("r") >= 0: 
                    if os.path.exists(filename):os.remove(filename)
                    os.mkfifo(filename)
            if "writefile" in self.cfg:
                filename = self.cfg.writefile
                if self.OpenModel().find("w") >= 0 and os.path.exists(filename) == False: os.mkfifo(filename)
            threading.Thread(target=self.task).start()
        except OSError as e:
            # 如果命名管道已经创建过了，那么无所谓  
            self.errormsg("mkfifo error:"+filename+str(e))
        if "writefile" in self.cfg and len(self.cfg.writefile) != 0: self.fout = os.open(self.cfg.writefile, os.O_SYNC | os.O_CREAT | os.O_RDWR)
        self.isOpen(True)
    def close(self):
        if self.fin!=None:os.close(self.fin)
        if self.fout!=None:os.close(self.fout)
        self.isOpen(False)
    def read(self):
        data = ""
        if self.isOpen():
            if self.fin == None and len(self.cfg.readfile) != 0: self.fin = os.open(self.cfg.readfile, os.O_RDONLY)
            while True:
                s = os.read(self.fin, 1)
                if len(s) == 0 or s == "\n":break
                else:data += s
        if data!="":
            self.logprint("recv:"+data)
            self.readdata(data)
        return data
    def write(self, data):
        if self.isOpen():os.write(self.fout, data)

# def receive_data(data):
#     printf(data)
# if __name__ == "__main__":
#     cfg=edict()
#     cfg.LogData=None
#     cfg.ReadData=receive_data
#     cfg.readfile="/tmp/data.in"
#     o=gsPipe(cfg)
#     o.showlog(False)
#     o.open()
    