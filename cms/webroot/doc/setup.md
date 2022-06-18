## 基于树莓派的物联硬件研发版本
## 说明
- 本版本应用在python的dist-packages目录下，在系统中全局调用，因此对应的引用需全部修改
- 本版本导入了v2和v3，v2支持当前的物联服务应用(web-iot-flask)，v3用于支持agent三合一版本
- 新的agent版本(agent_20211125_new分支)将应用本版本

## 安装部署
### 克隆版本库
```shell
root@raspberry:/home/pi/codes# git clone http://gitee.com/gvsun/gsiot
正克隆到 'gsiot'...
warning: 重定向到 https://gitee.com/gvsun/gsiot/
remote: Enumerating objects: 2439, done.
remote: Counting objects: 100% (2439/2439), done.
remote: Compressing objects: 100% (2058/2058), done.
remote: Total 2439 (delta 350), reused 2337 (delta 302), pack-reused 0
接收对象中: 100% (2439/2439), 30.64 MiB | 1.63 MiB/s, 完成.
处理 delta 中: 100% (350/350), 完成.
正在检出文件: 100% (2217/2217), 完成.
```
### 安装附加组件
```shell
root@raspberry:/home/pi/codes# cd gsiot
root@raspberry:/home/pi/codes/gsiot# ls
agent             haarcascade_frontalface_default.xml  __init__.pyc  opencv.face.py  readme.md  requirements.txt  setup     setup.sh  test.jpg
baiduaip.face.py  __init__.py                          LICENSE       pushcode.py     README.md  server            setup.py  test      v3
root@raspberry:/home/pi/codes/gsiot# ./setup/run.py
mkdir /usr/local/lib/python2.7/dist-packages/gsiot
cp -r /home/pi/codes/gsiot/* /usr/local/lib/python2.7/dist-packages/gsiot
安装模块：build-essential                          成功
安装模块：cmake                                    成功
安装模块：ffmpeg                                   成功
安装模块：gir1.2-gst-plugins-base-1.0              成功
安装模块：gir1.2-gstreamer-1.0                     成功
安装模块：git                                      成功
安装模块：gstreamer1.0-alsa                        成功
安装模块：gstreamer1.0-doc                         成功
安装模块：gstreamer1.0-omx                         成功
安装模块：gstreamer1.0-plugins-bad                 成功
安装模块：gstreamer1.0-plugins-bad-dbg             成功
安装模块：gstreamer1.0-plugins-bad-doc             成功
安装模块：gstreamer1.0-plugins-base                成功
安装模块：gstreamer1.0-plugins-base-apps           成功
安装模块：gstreamer1.0-plugins-base-dbg            成功
安装模块：gstreamer1.0-plugins-base-doc            成功
安装模块：gstreamer1.0-plugins-good                成功
安装模块：gstreamer1.0-plugins-good-dbg            成功
安装模块：gstreamer1.0-plugins-good-doc            成功
安装模块：gstreamer1.0-plugins-ugly                成功
安装模块：gstreamer1.0-plugins-ugly-dbg            成功
安装模块：gstreamer1.0-plugins-ugly-doc            成功
安装模块：gstreamer1.0-pulseaudio                  成功
安装模块：gstreamer1.0-tools                       成功
安装模块：gstreamer1.0-x                           成功
安装模块：imagemagick                              成功
安装模块：libevent-dev                             成功
安装模块：libffi-dev                               成功
安装模块：libgstreamer-plugins-bad1.0-0            成功
安装模块：libgstreamer-plugins-bad1.0-dev          成功
安装模块：libgstreamer-plugins-base1.0-0           成功
安装模块：libgstreamer-plugins-base1.0-dev         成功
安装模块：libgstreamer1.0-0                        成功
安装模块：libgstreamer1.0-0-dbg                    成功
安装模块：libgstreamer1.0-dev                      成功
安装模块：liborc-0.4-0                             成功
安装模块：liborc-0.4-0-dbg                         成功
安装模块：liborc-0.4-dev                           成功
安装模块：liborc-0.4-doc                           成功
安装模块：libssl-dev                               成功
安装模块：libv4l-dev                               成功
安装模块：nginx                                    成功
安装模块：nodejs                                   成功
安装模块：python-mysqldb                           成功
安装模块：python-pil                               成功
安装模块：python-pip                               成功
安装模块：python-smbus                             成功
安装模块：python-serial                            成功
安装模块：python-setuptools                        成功
安装模块：python-opencv                            成功
安装模块：docker.io                                成功
安装python组件：numpy                              成功
安装python组件：cffi==1.15.0                       成功
安装python组件：Pillow==4.0.0                      成功
安装python组件：chardet==4.0.0                     成功
安装python组件：requests==2.12.4                   成功
安装python组件：qrcode==6.0                        成功
安装python组件：spidev==3.4                        成功
安装python组件：sqlit==0.1.6                       成功
安装python组件：websocket-client==0.57.0           成功
安装python组件：websocket-server==0.4              成功
安装python组件：paho-mqtt==1.6.1                   成功
安装python组件：baidu-aip==2.2.11.0                成功
安装python组件：phatbeat==0.1.1                    成功
安装python组件：pianohat==0.1.0                    成功
安装python组件：picraft==1.0                       成功
安装python组件：piglow==1.2.4                      成功
安装python组件：pigpio==1.38                       成功
安装python组件：psutil==5.7.3                      成功
安装python组件：pyasn1==0.1.9                      成功
安装python组件：pycparser==2.20                    成功
安装python组件：pycrypto==2.6.1                    成功
安装python组件：paramiko==2.7.2                    成功
安装python组件：PyJWT==1.4.2                       成功
安装python组件：pantilthat==0.0.5                  成功
安装python组件：pyOpenSSL==16.2.0                  成功
安装python组件：pyserial==3.2.1                    成功
安装python组件：pytz==2018.7                       成功
安装python组件：pyxdg==0.25                        成功
安装python组件：rainbowhat==0.1.0                  成功
安装python组件：requests-oauthlib==0.7.0           成功
安装python组件：sense-emu==1.0                     成功
安装python组件：sense-hat==2.2.0                   成功
安装python组件：simplejson==3.10.0                 成功
安装python组件：six==1.10.0                        成功
安装python组件：sn3218==1.2.7                      成功
安装python组件：touchphat==0.0.1                   成功
安装python组件：twython==3.4.0                     成功
安装python组件：unicodecsv==0.14.1                 成功
安装python组件：unicornhathd==0.0.3                成功
安装python组件：urllib3==1.19.1                    成功
安装python组件：Werkzeug==0.11.15                  成功
安装python组件：zope.event==4.5.0                  成功
安装python组件：zope.interface==5.1.2              成功
root@raspberry:/home/pi/codes/gsiot/setup# 
```