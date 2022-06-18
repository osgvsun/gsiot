# 前言 
## 讲师介绍
先花点时间介绍一下自己，我叫李品勇，96年自动控制专业毕业。先进入一个国营单位做电工，那是受到了邻居的影响。后来发现对计算机编程更感兴趣，开始自学。那时没啥资料，电脑也没普及，单位里有台386，装的是dos6.2.2,还装了一个win3.2,每次都要敲命令才能进窗口界面，很古老的。dos系统自带了一个qbasic编辑器，还有basic的帮助。我的英语不太好，基本只能依靠学校学的知识和帮助里的代码去学习编程语言了。每次没看懂help的时候就把代码敲一遍，运行一下，然后改改输入参数，再运行看输出结果。这个方式对我影响很大，至今我的习惯仍旧是先搭一个开发环境，然后输入一段代码，再修改研究，这是一种注重体验的学习方法，感触很深，更适合应用方面，不太适合算法。

兜兜转转从进入编程行业第一家公司开始就一直和硬件打交道，虽然读书的时候也学过Z80的开发，单独去设计并写嵌入代码的场景实在太少，更多的是将不同的硬件像积木一样搭在一起，然后通过接口去对接。当公司接到东华项目开始进入实验室管理领域的时候，我也就接手设计门禁解决方案，通过对接第三方的设备，将相关业务数据整理成权限格式并推送到门禁设备，实现对实验室的管理。

如今，公司在硬件开发这块主要是使用树莓派、Nano派这类计算平台做的，也开始进入需嵌入编程开发的硬件领域。今天就已有的经验和大家交流一下关于我对物联网IoT和WoT的成果，其中也涉及到智能AIoT。

## 回顾
可以确定的是未来的世界是一个数字化的世界。数字化是下一个风口浪尖，万物互联是数字化的具体体现，物联网(Internet of Things)利用认知、AI、云计算等进行数字化重塑，构建具有前瞻性业务模式。而未来社会的发展，这会是一个重要方面。

互联网一路走来，从最开始的万维网，可以通过链接从一个页面跳到另一个，实现了数据的组织，使用分类排序创造出信息门户，使用搜索引擎实现了内容的查询。然后国内开始信息化了，2002年轰轰烈烈的政务信息化，让人们开始意识到数据和信息的重要。

后知后觉的我们站在当前时代的浪尖，回看信息化和现在的数字化浪潮，我们需要总结过去，看清楚技术发展的脉络去试着推演未来。本课程简单的阐述了物联网子系统的网络拓扑、通信协议、节点/设备配置、开源库及二次开发，为未来做好准备。

# 搭建一个基础环境
为实验方便，先简单搭建一个边缘计算环境。物联系统从层次上可以分为感知层、网络层、平台层和应用层。在感知层更多的是从事嵌入方面的硬件开发，这个维度和本次课程有点不同，本课程希望通过云的角度从上往下的去介绍相关的知识，感知层所需要的相关硬件在这里没法演示，只好暂时略去。

课程从边缘计算入手，边缘计算是指在靠近物或数据源头的一侧，采用网络、计算、存储、应用核心能力为一体的开放平台，就近提供最近端服务。其应用程序在边缘侧发起，产生更快的网络服务响应，满足行业在实时业务、应用智能、安全与隐私保护等方面的基本需求。边缘计算处于物理实体和工业连接之间，或处于物理实体的顶端。而云端计算，仍然可以访问边缘计算的历史数据。

我在准备实验时使用了两种方式搭建了虚拟环境：vmware和hyper-v，windows11专业版更适合使用hyper-v。在应用里安装了linux虚机，linux的版本使用的时2021-01-11日发布的raspios ([2021-01-11-raspios-buster-i386](https://pan.baidu.com/s/1oVPaYB56vyoBh11UdCJGMQ),提取码：87s9。树莓派系统是一个比较流行的开源硬件项目，算是庚商进入物联开发以来使用的最多的硬件系统环境了 ，

## 需要安装的组件
实验需要使用：
- 安装linux的虚拟机：作为程序执行的环境，首先需安装部署一台linux系统，照顾到实验最开始是针对树莓派设计的，虚机所安装的系统建议选择raspiOS from PC。
- DroidCam:安装在手机端，运行后建立了一个MJPG-Streamer服务，使用http协议对外提供服务。当然也可以使用其他的APP软件，只要支持MJPG-Streamer视频流发布就可以了。
- 软件版本库：我们为python项目在硬件上进行物联开发方面工作，整理了一个常用的代码库，gsiot。使用git克隆相关的[版本](http://gitee.com/gvsun/gsiot)：http://gitee.com/gvsun/gsiot。
版本库里包含了一个安装模块的[列表](http://gitee.com/gvsun/gsiot/blob/master/setup/run.py),[文档](http://gitee.com/gvsun/gsiot/blob/master/setup/readme.md)

## 安装IDE工具
在虚机内编程的话可以使用两种工具：
- VsCode：微软开源的离线编辑器，也有PC版本
- Code-Server：github上的开源项目，提供在线编辑器功能

# 设计一个基于消息队列的端到端通信协议
## 工业物联网架构

1. 设备层：架构的底层是设备层。设备可以是各种类型，作为物联网设备，他们必定有一些交流，间接或直接连接到互联网。
2. 通信层：通信层支持连接的设备。在设计时特别注意物联设备可能工作在无法连接物联云的情况，因此，其通信流程大致如下：
     ```sequence
        物联设备->物联网关: 注册物联设备
        物联网关-->物联设备: 返回信息，设置心跳上报周期
        物联网关->物联网关: 缓存物联设备数据
        物联网关->物联平台: 上报注册事件
        物联平台-->物联网关: 返回OK
        
        物联网关->物联网关:定期检查缓存数据
        
        物联设备->物联网关: 上报心跳事件
        物联网关-->物联设备:下发当前在线设备列表
        
        物联平台->物联网关: 发送请求
        物联网关->物联网关: dest是否是自己
        物联网关-->物联平台: 运行请求后返回结果
        物联网关->物联网关: dest是下属物联设备
        物联网关->物联设备: 发送请求
        物联设备-->物联网关: 返回结果
        
        Note over 物联网关,物联平台: 云端MQTT，部署在物联平台上
        Note over 物联设备,物联网关: 地端MQTT，部署在物联网关上
    ```
    在设备和云之间有多个潜在协议通信。最著名的三个潜在的协议：
    - HTTP/HTTPS (RESTful) 
    - MQTT 3.1/3.1.1 (RESTful风格) 
    - CoAP(RESTful风格，该协议在升级到python3时考虑)
3. 聚合/总线层：体系结构的一个重要的层是聚合和代理沟通层。这是一个重要的层有三个原因：
    - 能够支持与设备HTTP服务器和/或MQTT代理;
    - 聚合和组合来自不同的设备和通信路由到一个特定的设备（可能是通过一个网关）
    - 桥和不同协议之间的转换，例如提供基于HTTP 的 api到设备的MQTT消息。

4. 事件处理和分析层：这一层需要事件总线和提供这些事件过程和行动的能力。客户端/外部通信层，参考体系结构需要为这些设备提供了一种与外部系统交流的方法。

5. 身份和访问管理层：最后一层是身份和访问管理层。这一层需要提供以下服务：
    - oauth2令牌发放和验证
    - 其他身份服务包括SAML2 SSO和OpenID连接，支持识别从Web层的入站请求
    - xacml PDP
    - 用户目录（例如LDAP）
    - 访问控制策略管理（策略控制点）

### 设备注册
```sequence
 物联设备->物联网关: 注册物联设备
 物联网关-->物联设备: 返回信息，设置心跳上报周期
 物联网关->物联网关: 缓存物联设备数据
 物联网关->物联平台: 上报注册事件
 物联平台-->物联网关: 返回OK


 物联网关->物联网关:定期检查缓存数据

 物联设备->物联网关:上报心跳事件
 物联网关->物联设备:下发当前在线设备列表

 物联平台->物联网关: 发送请求
 物联网关->物联网关: dest是否是自己
 物联网关-->物联平台: 运行请求后返回结果
 物联网关->物联网关: dest是下属物联设备
 物联网关->物联设备: 发送请求
 物联设备-->物联网关: 返回结果

 Note over 物联网关,物联平台: 云端MQTT，部署在物联平台上
 Note over 物联设备,物联网关: 地端MQTT，部署在物联网关上

 ```
### 简单通信过程
无论是使用mqtt或是http，都是用RESTful风格的命令来访问主题，并得到返回的信息。如果是http协议的话，发送心跳的例子如下：
```python
import requests
r=requests.get("http://iot-gateway/agent/B827EB6712D1/hi")
if r.status_code==200:
    print("上报成功")
else：
    print("提交失败") 
```
和http相比，mqtt则需要标注返回给哪个主题，所以数据结构如下：

|参数|说明|
|---|---|
|sour|发送端订阅号|
|cmd|远程调用的功能指令|
|datetime|数据发送时间，年月日时分秒|
|CRC|数据包中除去CRC外，所有json内容的字符串的md5|

地端设备发送心跳报文的例子是:
```json
{
    "sour":"B827EB6712D1_202203011459.245045",                 // 发布者
    "url":"iot://iot-gateway/B827EB6712D1/agent/Heartbeat",    // http restful风格
    "datetime":"2022-02-28 08:58:03",
    "network":{
        "eth0":"",
        "wlan0":"192.168.31.75",
        "wlan1":"192.168.12.1",
        "tun0":"10.106.0.190"
    },
    "version":{
        "software_version":"3.4.1.20220214102541",
        "softversion":"3.4.1",
        "hardware_version":"1.0.201903151730",
        "lib_version":"3.1.202109280215",
    },
    //hashlib.md5(json.dumps(data)).hexdigest()
    "crc":"6f263b00f4c98e59c6b8ca15c820561e" 
}
```
在使用mqSocket模块时，访问iot://iot-gateway/B827EB6712D1/Heartbeat，即转换为向iot-gateway主题发送报文。大致如下：B827EB6712D1_
```python
import mqSocket
mq=mqSocket((app.servcfg.server.ip,app.servcfg.server.port.mqtt),timeout=5)
mq.Open()
r=mq.get("iot://iot-gateway/B827EB6712D1/agent/Heartbeat")
if r.result=="ok":
    print("上报成功")
else：
    print("提交超时") 
mq.Close()
```
和http类似的是，使用mqSocket进行通信时，会临时生成一个随机的使用SN_DATETIME的形式的主题，诸如：B827EB6712D1_202203011459.245045，返回的数据将直接从订阅的主题获取到，而发布的数据内容就分析get方法中提交的url参数：iot-gateway。

由于物联云端是无法直接访问到物联设备的，因此所访问的url将出现如下的变化：
```sequence
    物联平台->物联网关: 发送请求\niot://iot-gateway/B827EB6712D1/readlog/today
    Note right of 物联平台:iot-gateway替换成实际物联网关的订阅主题
    Note right of 物联平台:返回主题是iot-platform-202203011459.245045
    物联网关->物联设备: 发送请求\niot://B827EB6712D1/readlog/today
    Note right of 物联网关:B827EB6712D1替换成实际物联设备的订阅主题
    Note right of 物联网关:返回主题是iot-gateway-202203011459.3010232
    物联设备->物联设备: 响应请求\n/readlog/today
    物联设备-->物联网关:返回结果
    物联网关-->物联平台:返回结果
    
    Note over 物联网关,物联平台: 云端MQTT，部署在物联平台上
    Note over 物联设备,物联网关: 地端MQTT，部署在物联网关上
```
# 使用baidu-aip实现人脸识别
## 从摄像头获取图片
实验室用的摄像头是外部的，从手持设备而来，或得到的也不是一张图片，而是一个视频流。使用浏览器访问以下地址，将[ip]改成手机的实际地址：
```shell
http://[ip]:4747/mjpegfeed
```
当然，实际配置是可以调整的，可百度一下查找相关资料。另外注意一点，该app仅支持一路通信，如果连接异常（如下），请重新启动app，然后再次运行程序。

```shell
root@raspberry:/home/pi/codes/gsiot/test/face# python baiduaip.face.py 
Traceback (most recent call last):
  File "baiduaip.face.py", line 15, in <module>
    dev=urllib2.urlopen(url)
  File "/usr/lib/python2.7/urllib2.py", line 154, in urlopen
    return opener.open(url, data, timeout)
  File "/usr/lib/python2.7/urllib2.py", line 429, in open
    response = self._open(req, data)
  File "/usr/lib/python2.7/urllib2.py", line 447, in _open
    '_open', req)
  File "/usr/lib/python2.7/urllib2.py", line 407, in _call_chain
    result = func(*args)
  File "/usr/lib/python2.7/urllib2.py", line 1228, in http_open
    return self.do_open(httplib.HTTPConnection, req)
  File "/usr/lib/python2.7/urllib2.py", line 1198, in do_open
    raise URLError(err)
urllib2.URLError: <urlopen error [Errno 111] Connection refused>
```
另外，关于PILImage和某些视频帧的互相转换应用，可参考v3/file/ffmpy.py中的FfmpegRemp对象，在该对象中有不少应用。

示例代码：
```python
# -*- coding:utf-8 -*-
import requests,urllib2,io
from PIL import Image,ImageDraw,ImageFont

url="http://192.168.199.208:4747/mjpegfeed"
bytes=''
dev=urllib2.urlopen(url)
while True:
    bytes+=dev.read(1024)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    if a!=-1 and b!=-1:
	    # 图片内容
        jpg = bytes[a:b+2]
        bytes=bytes[b+2:]
		# 初始化Image对象
        img=Image.open(io.BytesIO(jpg))
		# 将Image对象保存为图片
        img.save("./test.jpg")
        break
```
代码运行后，在当前目录下会生成一个test.jpg的文件，就是一帧画面的内容。之所以会是一帧，是图片保存了以后，break终止了。如果不终止，就会不断的获取图片。

## 使用百度AIP进行人脸识别
当对一种事物不熟悉时，最好的办法就是模仿，所以先借用一个成熟的方案来进行。在安装模块的时候已经安装了baidu-aip，相关的参数请到百度云平台去申请。如果需要单独安装的话，步骤如下：
### 安装baidu-aip模块
```shell
root@raspberry:/home/pi/codes/gsiot/test/face# pip install baidu-aip #当前的python版本
Looking in indexes: https://pypi.org/simple, https://www.piwheels.org/simple
Collecting baidu-aip
  Downloading https://files.pythonhosted.org/packages/d8/1c/d88a59822982d19c8e0995d76186b35ae9df86418f1eb5119c86ea7f3cf8/baidu_aip-4.16.3-py2-none-any.whl
Requirement already satisfied: requests in /usr/local/lib/python2.7/dist-packages (from baidu-aip) (2.12.4)
Installing collected packages: baidu-aip
Successfully installed baidu-aip-4.16.3
root@raspberry:/home/pi/codes/gsiot# pip3 install baidu-aip #python3版本
```
### 获取百度AI接口密钥
在百度云平台上申请人脸识别项目，就会得到两个参数aipkey和secretkey，然后建立一个人脸库，设置人脸组face_group
```json
{
    "apikey":"根据实际情况填写",
    "face_group":"根据实际情况填写",
    "secretkey":"根据实际情况填写"
}
```
### 调用百度接口识别人脸
- 请求URL

```python
# encoding:utf-8
import requests 

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=【官网获取的AK】&client_secret=【官网获取的SK】'
response = requests.get(host)
if response:
  print(response.json())
```
- 图片转换

```python
data = 'image.jpg'
data = base64.b64encode(img_data)
image = data.decode()
imageType = "BASE64"
```

- 人脸对比

```python
# encoding:utf-8

import requests

'''
人脸对比
'''

request_url = "https://aip.baidubce.com/rest/2.0/face/v3/match"

params = "[{\"image\": \"sfasq35sadvsvqwr5q...\", \"image_type\": \"BASE64\", \"face_type\": \"LIVE\", \"quality_control\": \"LOW\"},
{\"image\": \"sfasq35sadvsvqwr5q...\", \"image_type\": \"BASE64\", \"face_type\": \"IDCARD\", \"quality_control\": \"LOW\"}]"
access_token = '[调用鉴权接口获取的token]'
request_url = request_url + "?access_token=" + access_token
headers = {'content-type": 'application/json'}
response = requests.post(request_url, json=params, headers=headers)
if response:
    print (response.json())

```
返回实例
```json
{
	"score": 44.3,
	"face_list": [  //返回的顺序与传入的顺序保持一致
		{
			"face_token": "fid1"
		},
		{
			"face_token": "fid2"
		}
	]
}
```


|参数名|必选|类型|说明|
|--|--|--|--|
|score|是|float|人脸相似度|
|face_list|array|人脸的信息列表|
|face_token|是|sring|人脸的唯一标志|

### 示例程序（使用baidu-aip组件）
```python
# -*- coding:utf-8 -*-
import requests,urllib2,io
import base64
import json
from aip import AipFace
from PIL import Image,ImageDraw,ImageFont
from gsiot.v3 import *
apikey="your apikey"
secretkey="your secretkey"
appid="your appid"
face_group="your face group"

def getReturn(data):
	result=edict(data)
	print result.toJsonString(True)
	if result.error_code==0:return result.result
	else:return False
url="http://[ip]:4747/mjpegfeed"
bytes=''
imagetype = "BASE64"
dev=urllib2.urlopen(url)
tools=AipFace(appid, apikey, secretkey)
while True:
	bytes+=dev.read(1024)
	a = bytes.find('\xff\xd8')
	b = bytes.find('\xff\xd9')
	if a!=-1 and b!=-1:
		jpg = bytes[a:b+2]
		bytes=bytes[b+2:]
		faces=getReturn(tools.detect(base64.b64encode(jpg), imagetype))
		if faces:
			for f in faces.face_list:
				face=edict(f)
				# 无法根据这个数据找到人脸
				# box=(face.location.left,face.location.top,face.location.width,face.location.height)
				# img.crop(box).save("./test.jpg")
				users=getReturn(tools.search(image,imagetype,face_group))
				if users:
					for u in users.user_list:
						user=edict(u)
						print user.toJsonString(True)
	break
```
返回实例
```json
{
	"log_id":2184375986,
	"timestamp":1651808184,
	"cached":0,
	"result":{
		"face_list":[
			{
				"face_probability": 1, 
				"angle": {"yaw": 36.85, "roll": -7.47, "pitch": -2.4}, 
				"location": {"width": 233, "top": 268.95, "height": 222, "rotation": -11, "left": 133.95}, 
				"face_token": "3962757c7df8c4585f1a156486d97ca4"
			}
		],
		"face_num":1
	},
	"error_code":0,
	"error_msg":"SUCCESS"
}
```
```json
{
	"log_id":731823973,
	"timestamp":1651810331,
	"cached":0,
	"result":{
		"user_list":[
			{
				"user_info": "",
				"group_id": "ilkkzm", 
				"user_id": "20110032", 
				"score": 77.344009399414
			}
		],
		"face_token":"30b284a883a454f9c6eaff9364c85f55"
	},
	"error_code":0,
	"error_msg":"SUCCESS"
}
```
```json
{
	"user_info":"",
	"group_id":"ilkkzm",
	"user_id":"20110032",
	"score":77.3440093994
}
```
这样就可以实现使用百度aip进行人脸识别了。当然，这里也有一个弱点：
- 人脸检测和人脸识别使用的是一张照片，按照逻辑，人脸识别应该从需要检测的照片裁剪出来才对，这样就可以减小传输量。
- 检测一张照片后，将所有识别的人脸数据应该全部提取并处理，这样可以减少提交次数。
应用哪个策略应该根据不同的场景进行选择，你试试看？

## 使用Opencv进行人脸识别训练和检测

###  检测人脸
这应该是最基本的，给我们一张图片，我们要先检测出人脸的区域，然后才能进行操作，opencv已经内置了很多分类检测器，我们这次用haarcascade_frontalface_default.xml，可以在[这里](https://gitee.com/mirrors/opencv/blob/4.x/data/haarcascades/haarcascade_frontalface_default.xml)找到，另外注意参数img是用opencv.imread方法读出的，这个内容实际和PIL.Image的格式是不同的，需要转化，方法如下：
```python
def getOpenCVImagefromPILImage(img):
    return cv2.cvtColor(numpy.asarray(img),cv2.COLOR_RGB2BGR)
def detect_face(img):
    #将测试图像转换为灰度图像，因为opencv人脸检测器需要灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #加载OpenCV人脸检测分类器Haar
    face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
    
    #检测多尺度图像，返回值是一张脸部区域信息的列表（x,y,宽,高）
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
    # 如果未检测到面部，则返回原始图像
    if (len(faces) == 0):
    return None, None
    #目前假设只有一张脸，xy为左上角坐标，wh为矩形的宽高
    (x, y, w, h) = faces[0]
    #返回图像的正面部分
    return gray[y:y + w, x:x + h], faces[0]
```

### 人脸训练
首先返回所有训练图片的人脸检测信息和标签：
```python
# 该函数将读取所有的训练图像，从每个图像检测人脸并将返回两个相同大小的列表，分别为脸部信息和标签
def prepare_training_data(data_folder_path):
    # 获取数据文件夹中的目录（每个主题的一个目录）
    dirs = os.listdir(data_folder_path)
    # 两个列表分别保存所有的脸部和标签
    faces = []
    labels = []
    # 浏览每个目录并访问其中的图像
    for dir_name in dirs:
    # dir_name(str类型)即标签
    label = int(dir_name)
    # 建立包含当前主题主题图像的目录路径
    subject_dir_path = data_folder_path + "/" + dir_name
    # 获取给定主题目录内的图像名称
    subject_images_names = os.listdir(subject_dir_path)
    # 浏览每张图片并检测脸部，然后将脸部信息添加到脸部列表faces[]
    for image_name in subject_images_names:
    # 建立图像路径
    image_path = subject_dir_path + "/" + image_name
    # 读取图像
    image = cv2.imread(image_path)
    # 显示图像0.1s
    cv2.imshow("Training on image...", image)
    cv2.waitKey(100)
    # 检测脸部
    face, rect = detect_face(image)
    # 我们忽略未检测到的脸部
    if face is not None:
    #将脸添加到脸部列表并添加相应的标签
    faces.append(face)
    labels.append(label)
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    #最终返回值为人脸和标签列表
    return faces, labels
```
有了脸部信息和对应标签后，我们就可以使用opencv自带的识别器来进行训练了：
```python
#调用prepare_training_data（）函数
faces, labels = prepare_training_data("training_data")
#创建LBPH识别器并开始训练，当然也可以选择Eigen或者Fisher识别器
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.train(faces, np.array(labels))
```

### 人脸预测
在这之前我们可以设定一下预测的格式，包括用矩形框框出人脸并标出其名字，当然最后别忘了建立标签与真实姓名直接的映射表：
```python
#根据给定的（x，y）坐标和宽度高度在图像上绘制矩形
def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x + w, y + h), (128, 128, 0), 2)
# 根据给定的（x，y）坐标标识出人名
def draw_text(img, text, x, y):
    
#建立标签与人名的映射列表（标签只能为整数）
subjects = ["jiaju", "jiaqiang"]

# 此函数识别传递的图像中的人物并在检测到的脸部周围绘制一个矩形及其名称
def predict(test_img):
    #生成图像的副本，这样就能保留原始图像
    img = test_img.copy()
    #检测人脸
    face, rect = detect_face(img)
    #预测人脸
    label = face_recognizer.predict(face)
    # 获取由人脸识别器返回的相应标签的名称
    label_text = subjects[label[0]]
    # 在检测到的脸部周围画一个矩形
    draw_rectangle(img, rect)
    # 标出预测的名字
    draw_text(img, label_text, rect[0], rect[1] - 5)
    #返回预测的图像
    return img
```

### 示例代码
```python
# # -*- coding:utf-8 -*-
import cv2
import os
import numpy as np
# 检测人脸
def detect_face(img):
    #将测试图像转换为灰度图像，因为opencv人脸检测器需要灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #加载OpenCV人脸检测分类器Haar
    face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
    #检测多尺度图像，返回值是一张脸部区域信息的列表（x,y,宽,高）
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
    # 如果未检测到面部，则返回原始图像
    if (len(faces) == 0):
    return None, None
    #目前假设只有一张脸，xy为左上角坐标，wh为矩形的宽高
    (x, y, w, h) = faces[0]
    #返回图像的正面部分
    return gray[y:y + w, x:x + h], faces[0]
# 该函数将读取所有的训练图像，从每个图像检测人脸并将返回两个相同大小的列表，分别为脸部信息和标签
def prepare_training_data(data_folder_path):
    # 获取数据文件夹中的目录（每个主题的一个目录）
    dirs = os.listdir(data_folder_path)
    # 两个列表分别保存所有的脸部和标签
    faces = []
    labels = []
    # 浏览每个目录并访问其中的图像
    for dir_name in dirs:
    # dir_name(str类型)即标签
    label = int(dir_name)
    # 建立包含当前主题主题图像的目录路径
    subject_dir_path = data_folder_path + "/" + dir_name
    # 获取给定主题目录内的图像名称
    subject_images_names = os.listdir(subject_dir_path)
    # 浏览每张图片并检测脸部，然后将脸部信息添加到脸部列表faces[]
    for image_name in subject_images_names:
        # 建立图像路径
        image_path = subject_dir_path + "/" + image_name
        # 读取图像
        image = cv2.imread(image_path)
        # 显示图像0.1s
        cv2.imshow("Training on image...", image)
        cv2.waitKey(100)
        # 检测脸部
        face, rect = detect_face(image)
        # 我们忽略未检测到的脸部
        if face is not None:
            #将脸添加到脸部列表并添加相应的标签
            faces.append(face)
            labels.append(label)
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    #最终返回值为人脸和标签列表
    return faces, labels
#调用prepare_training_data（）函数
faces, labels = prepare_training_data("training_data")
#创建LBPH识别器并开始训练，当然也可以选择Eigen或者Fisher识别器
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.train(faces, np.array(labels))
#根据给定的（x，y）坐标和宽度高度在图像上绘制矩形
def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x + w, y + h), (128, 128, 0), 2)
# 根据给定的（x，y）坐标标识出人名
def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (128, 128, 0), 2)
#建立标签与人名的映射列表（标签只能为整数）
subjects = ["jiaju", "jiaqiang"]
# 此函数识别传递的图像中的人物并在检测到的脸部周围绘制一个矩形及其名称
def predict(test_img):
    #生成图像的副本，这样就能保留原始图像
    img = test_img.copy()
    #检测人脸
    face, rect = detect_face(img)
    #预测人脸
    label = face_recognizer.predict(face)
    # 获取由人脸识别器返回的相应标签的名称
    label_text = subjects[label[0]]
    # 在检测到的脸部周围画一个矩形
    draw_rectangle(img, rect)
    # 标出预测的名字
    draw_text(img, label_text, rect[0], rect[1] - 5)
    #返回预测的图像
    return img
#加载测试图像
test_img1 = cv2.imread("test_data/test1.jpg")
test_img2 = cv2.imread("test_data/test2.jpg")
#执行预测
predicted_img1 = predict(test_img1)
predicted_img2 = predict(test_img2)
#显示两个图像
cv2.imshow(subjects[0], predicted_img1)
cv2.imshow(subjects[1], predicted_img2)
cv2.waitKey(0)
cv2.destroyAllWindows()
```
这个代码还要改写成输入从mjpg_streamer中提取，你试着改改看。
## 使用python和nodejs执行外部命令
操作系统的一个职责是对运行进程的调度和运行管理，有进程/子进程的划分。进程偶尔也需要进行通信，每个进程各自有不同的用户地址空间,任何一个进程的全局变量在另一个进程中都看不到，所以进程之间要交换数据必须通过内核,在内核中开辟一块缓冲区,进程A把数据从用户空间拷到内核缓冲区,进程B再从内核缓冲区把数据读走,内核提供的这种机制称为进程间通信。

而管道就是提供这份公共资源的形式的一种，进程启动时默认会提供输入、输出和报错三个管道。在运行命令时，可以使用“|”进行进程间管道通信的设置，也可以使用“>”或“>>”进行输出重定向，这些都是使用了管道概念的应用技巧。

在python中如需启动外部进程，通常有三种方式：
- os.system      : 独立运行外部程序，如成功则返回0，缺点读不到输出的信息
- os.popen       ：独立运行外部程序，读取所有输出信息
- subprocess.Open：独立运行子进程，可设定输入/输出/报错管道

除了subprocess.Open的时候，参数中可以设置stdin,stdout和stderr外，其他方法都没有设置的地方了，但通过命令行的变更操作，可以增加输出的管道（管道文件）stdout和stderr。格式如下：
```shell
# 将输出输出到/tmp/null，报错输出到/tmp/err_null
apt updat 1>/tmp/null 2>/tmp/err_null
# 将输出和报错都输出到/tmp/null
apt updat 1>/tmp/null 2>&1
# 添加key
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
```
在nodejs中，则是调用child_process模块执行外部命令，根据场景不同，也有两种方式：
- child_process.exec
- child_process.spawn
从实现原理来说，spawn是更底层的接口，exec对spawn进行了再次封装，提供了更简单的API接口。
- exec比spawn易于使用，当子进程返回的数据不超过200K时，exec比spawn更适合。
- 当子进程需要返回大量数据时，spawn更安全。
- spawn提供了更多的选项，可以对子进程进行更详细的设置。

大致了解后，其实就可以关注如何运行一个外部命令并获取返回值了。下面介绍两组代码，分别是python和nodejs运行外部命令，提起数据的例子：
```python
import os

for line in os.popen(cmd).read().strip().split("\n"):
    print(line)
```
```javascript
const child = require('child_process');
let cmd="ls -l /dev |grep spi";
child.exec(cmd, function(err, sto) {
    console.log(sto);//sto才是真正的输出，要不要打印到控制台，由你自己啊
})
```
以上运行的是列出所有spi设备，在虚拟机中运行基本是空的，因为虚机中没有连接类似设备，但在树莓派上运行则有返回结果，如下：
```shell
# 在虚机上运行
lipy-raspiOS:~ $ ls -l /dev |grep spi
pi@lipy-raspiOS:~ $ 

# 在树莓派上运行
pi@lipy-test-agent-01:~$ ls -l /dev |grep spi
crw-rw----  1 root spi     153,   0 Apr  8 09:31 spidev0.0
crw-rw----  1 root spi     153,   1 Apr  8 09:31 spidev0.1
```
也可以在脚本语言的命令行解释器运行看看：
```shell
root@lipy-test-agent-01:~# python
Python 2.7.13 (default, Feb  6 2022, 20:16:18)
[GCC 6.3.0 20170516] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import os
>>> cmd="ls -l /dev |grep spi"
>>> for line in os.popen(cmd).read().strip().split("\n"):print(line)
...
crw-rw----  1 root spi     153,   0 Apr  8 09:31 spidev0.0
crw-rw----  1 root spi     153,   1 Apr  8 09:31 spidev0.1
>>> exit()
root@lipy-test-agent-01:~# node
> const child = require('child_process');let cmd="ls -l /dev |grep spi";child.exec(cmd, function(err, sto){console.log(sto);})
> crw-rw----  1 root spi     153,   0 Apr  8 09:31 spidev0.0
rw-rw----  1 root spi     153,   1 Apr  8 09:31 spidev0.1
> .exit
root@lipy-test-agent-01:~#
```
接下来，就需要讨论需要什么执行命令，完成什么效果了。最后，看一下成果，先看一下python版本读取网络接口的操作[代码](https://gitee.com/gvsun/gsiot/blob/master/v3/net/__init__.py)，运行结果如下：
```shell
# 直接运行代码，带参数all，则打印所有网卡信息
pi@lipy-raspiOS:~/codes/gsiot $ python v3/net/__init__.py all
{
    "interfaces":["lo","docker0","eth0"],
    "adapters":{
        "lo":{
            "ip":"127.0.0.1",
            "iswireless":false,
            "islinked":true,
            "running":true,
            "mac":"",
            "dns":"",
            "device":"lo",
            "dhcp":true,
            "netmask":"255.0.0.0",
            "gateway":"",
            "flow":{
                "rx":"0",
                "tx":"0"
            }
        },
        "docker0":{
            "ip":"172.17.0.1",
            "iswireless":false,
            "islinked":true,
            "running":false,
            "mac":"02:42:4c:69:ef:a6",
            "dns":"",
            "device":"docker0",
            "dhcp":true,
            "netmask":"255.255.0.0",
            "gateway":"",
            "flow":{
                "rx":"0",
                "tx":"0"
            }
        },
        "eth0":{
            "ip":"192.168.133.132",
            "iswireless":false,
            "islinked":true,
            "running":true,
            "mac":"00:0c:29:07:ca:d1",
            "dns":"",
            "device":"eth0",
            "dhcp":true,
            "netmask":"255.255.255.0",
            "gateway":"192.168.133.2",
            "flow":{
                "rx":"89",
                "tx":"0"
            }
        }
    },
    "dns":["192.168.133.2"]
}
# 直接运行代码，不带参数，则打印当前默认上网的网卡的配置信息
pi@lipy-raspiOS:~/codes/gsiot $ python v3/net/__init__.py
{
    "ip":"192.168.133.132",
    "iswireless":false,
    "islinked":true,
    "running":true,
    "mac":"00:0c:29:07:ca:d1",
    "dns":"",
    "device":"eth0",
    "dhcp":true,
    "netmask":"255.255.255.0",
    "gateway":"192.168.133.2",
    "wifi":{
        "isinit":false,
        "access_point":"",
        "mode":"",
        "essid":"",
        "signallevel":0
    },
    "flow":{
        "rx":"143",
        "tx":"0"
    },
    "networking":true
}
# 直接运行代码，带参数(网络适配器名称)，则打印当前上网的网卡信息
pi@lipy-raspiOS:~/codes/gsiot $ python ./v3/net/__init__.py docker0
{
    "ip":"172.17.0.1",
    "iswireless":false,
    "islinked":true,
    "running":false,
    "mac":"02:42:4c:69:ef:a6",
    "dns":"",
    "device":"docker0",
    "dhcp":true,
    "netmask":"255.255.0.0",
    "gateway":"",
    "wifi":{
        "isinit":false,
        "access_point":"",
        "mode":"",
        "essid":"",
        "signallevel":0
    },
    "flow":{
        "rx":"0",
        "tx":"0"
    },
    "networking":false
}
```
当然，在代码里还包含了一个读取和配置无线网络连接无线ap的方法，大家可以试试。另外，在目录./bin/network-config，提供了一个nodejs的开源项目[network-config](https://gitee.com/gvsun/gsiot/tree/master/bin/network-config),其实现的主要方式就是执行外部命令，并解析返回结果，可以作为参考。
这次留的题目就是将python版本的对象Net和NetworkInterface使用nodejs重新实现一次。

## 使用opencv.js进行人脸识别
既然可以使用opencv模块进行人脸开发，那么使用opencv.js也可以。现在要解决的是第一个问题，视频从那里来。可以访问[这里](/opencv/02/)，这个页面从人脸图片提取样本，从mjpg-streamer中提取视频帧。访问该页面仅需要使用http就好，但如果访问本地摄像头，就需要使用https了，不过[nginx.conf](https://gitee.com/gvsun/gsiot/blob/master/bin/nginx/nginx.conf)已经配置好了，可以直接使用。在运行/setup/run.py的时候实际将nginx.conf链接到了/etc/nginx目录下了。
```shell
root@raspiOS-Work:/home/pi/codes/gsiot# ls /etc/nginx -l
总用量 68
drwxr-xr-x 2 root root 4096 5月  28  2021 conf.d
-rw-r--r-- 1 root root 1077 8月  24  2020 fastcgi.conf
-rw-r--r-- 1 root root 1007 8月  24  2020 fastcgi_params
-rw-r--r-- 1 root root 2837 8月  24  2020 koi-utf
-rw-r--r-- 1 root root 2223 8月  24  2020 koi-win
-rw-r--r-- 1 root root 3957 8月  24  2020 mime.types
drwxr-xr-x 2 root root 4096 5月  28  2021 modules-available
drwxr-xr-x 2 root root 4096 6月   1 15:01 modules-enabled
lrwxrwxrwx 1 root root   65 6月  16 09:44 nginx.conf -> /usr/local/lib/python2.7/dist-packages/gsiot/bin/nginx/nginx.conf
lrwxrwxrwx 1 root root   65 6月   1 15:43 nginx.old.conf -> /usr/local/lib/python2.7/dist-packages/gsiot/bin/nginx/nginx.conf
-rw-r--r-- 1 root root  180 8月  24  2020 proxy_params
-rw-r--r-- 1 root root  636 8月  24  2020 scgi_params
drwxr-xr-x 2 root root 4096 6月   1 15:01 sites-available
drwxr-xr-x 2 root root 4096 6月   1 15:01 sites-enabled
drwxr-xr-x 2 root root 4096 6月   1 15:01 snippets
-rw-r--r-- 1 root root  664 8月  24  2020 uwsgi_params
-rw-r--r-- 1 root root 3071 8月  24  2020 win-utf
root@raspiOS-Work:/home/pi/codes/gsiot# ls -l /usr/local/lib/python2.7/dist-packages/gsiot
lrwxrwxrwx 1 root staff 20 6月  16 09:40 /usr/local/lib/python2.7/dist-packages/gsiot -> /home/pi/codes/gsiot
```
**注意观察：**实际上通过两次链接完成的。先将```/home/pi/codes/gsiot```链接到```/usr/local/lib/python2.7/dist-packages```下，实现了在python中无需定义目录就可以直接import，然后再将```/usr/local/lib/python2.7/dist-packages/gsiot/bin/nginx/nginx.conf```链接到了```/etc/nginx```下。
执行好run.py,需要再执行一个命令重启nginx：```service nginx restart````。配置https所需要的证书已经放在了```/bin/nginx/目录下了，如需要换证书，仅需在nginx.conf文件中的相关位置修改一下即可。

完成以上操作后，可以在浏览器里访问https://raspiOS-Work/opencv/01/

------------


# 结束