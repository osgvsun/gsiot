# -*- coding:utf-8 -*-
from gsiot.v3 import *

class gsThread(gsobject):
    def __init__(self,fun):
        self.fun=fun
        self.runing=False
        self.timeInterval=1
        self.t=None
    def Open(self,*argv):
        self.runing=True
        self.t=threading.Thread(target=self.task,args=argv)
        self.t.setDaemon(True)
        self.t.start()
    def task(self,*argv):
        while self.runing==True:
            try:self.fun(*argv)
            except:pass
            time.sleep(self.timeInterval)
    def Close(self):
        if self.runing==True and self.t!=None:self.t.join()
        self.runing=False
        



class test(gsobject):
    data="1"
    def do(self,*argv):
        self.data=datetime.now()
        print self.data


if __name__ == "__main__":
    o=test()
    t=gsThread(o.do)
    t.Open()
    time.sleep(10)
    t.Close()
    print o.data