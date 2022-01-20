## 基于树莓派的物联硬件研发版本
## 说明
- 本版本应用在python的dist-packages目录下，在系统中全局调用，因此对应的引用需全部修改
- 本版本导入了v2和v3，v2支持当前的物联服务应用(web-iot-flask)，v3用于支持agent三合一版本
- 新的agent版本(agent_20211125_new分支)将应用本版本

## 安装部署
由于没有编写setup.py,所以部署时需找到dist-packages目录并执行如下命令，以python2.7为例:
```shell
# 2021年11月25日
cd /usr/local/lib/python2.7/dist-packages \
&& git clone -b lib http://library.gvsun.net/lipinyong/research \
&& mv research gsiot
```

2021年11月25日下班后，编写了setup.py,比较简单，使用方法如下：
```shell
# 使用python2运行
&& git clone -b lib http://library.gvsun.net/lipinyong/research \
&& python ./research/setup.py
# 使用python3运行
&& git clone -b lib http://library.gvsun.net/lipinyong/research \
&& python3 ./research/setup.py
```

验证是否可用：
```shell
root@iot-agent:~# python
Python 2.7.16 (default, Oct 10 2019, 22:02:15)
[GCC 8.3.0] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from gsiot.v3 import *
>>> edict
<class 'gsiot.v3.edict'>
>>> exit()

root@iot-agent:~# python3
Python 3.7.3 (default, Jul 25 2020, 13:03:44)
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from gsiot.v3 import *
>>> edict
<class 'gsiot.v3.edict'>
>>> exit()
```