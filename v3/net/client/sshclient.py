# -*- coding:utf-8 -*-
import sys,os,threading,binascii,platform,time
# from multiprocessing import Process
from datetime import datetime
import paramiko
path=sys.path[0]
sys.path.append(path+"/../../..")
from lib import *

class Client(gsobject):
    def __init__(self, **cfg):
        self.cfg = edict()
        self.cfg.readdict(cfg)
        gsobject.__init__(self)
        self.modulename="sshclinet"
    def open(self, value=None):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.st=paramiko.Transport((self.cfg.host,self.cfg.port))
        self.st.connect(username=self.cfg.user,password=self.cfg.passwd)
        self.ssh.connect(self.cfg.host,self.cfg.port,self.cfg.user,self.cfg.passwd,timeout=self.cfg.timeout)
        self.sftp=paramiko.SFTPClient.from_transport(self.st)
        self.isOpen(True)
        # self.logprint("open [ok]")
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.st=paramiko.Transport((self.cfg.host,self.cfg.port))
            self.st.connect(username=self.cfg.user,password=self.cfg.passwd)
            self.ssh.connect(self.cfg.host,self.cfg.port,self.cfg.user,self.cfg.passwd,timeout=self.cfg.timeout)
            self.sftp=paramiko.SFTPClient.from_transport(self.st)
            self.isOpen(True)
            self.logprint("open [ok]")
        except:
            self.isOpen(False)
            self.logprint("open [fail]")
    def close(self):
        self.ssh.close()
        self.st.close()
        self.isOpen(False)
    # 以下是基本功能，可以看成是读和写两种方法的扩展融合
    def runas(self,cmd):
        if self.isOpen()==True:
            stdin, stdout, stderr = self.ssh.exec_command(cmd)
            self.logprint(cmd+"[ok]")
            return stdout.readlines()
        else:return ['False']
    def getList(self,path):
        return self.sftp.listdir(path)
    def getfile(self,spath,dpath,filename,dfile=None):
        sfilename=spath+filename
        if not dfile:dfilename=dpath+filename
        else:dfilename=dpath+dfile
        self.sftp.get(sfilename,dfilename)  
    def putfile(self,spath,dpath,filename):
        sfile=os.path.join(spath,filename).replace("\\","/")
        dfile=os.path.join(dpath,filename).replace("\\","/")
        if os.path.exists(sfile)==True:
            printf("从{}上传到{}".format(sfile,dfile),flag=True)
            self.sftp.put(sfile,dfile)
            printf("完成")
            self.logprint("从{}上传到{}".format(sfile,dfile))
       
if __name__ == "__main__":
    o=Client(host="192.168.0.132",port=22,user="root",passwd="gengshang",timeout=1)
    o.open()
    o.runas("cat /etc/issue")
    o.close()