var frmWork={
	data:{},
	mode:"",
	t:null,
	parent:null,
	data_init:function(){return {"username":"","cname":"","StationId":"","LabId":"","CourseID":"","ExperimentID":"","handle":{}}},
	cmdAttendance_Click:function(e){
		this.mode="attendance"
		$ID("panwork").Clear();
		ret={};ret.data=eval("".LoadURL("/attendance/logs"))
		ret.data.reverse()
		strtmpl="".LoadURL(App.path+"/tmpl/attendance/list.txt").replace("<host>", this.parent.ip);
		$ID("panwork").Html(tmpl(strtmpl,ret));		
		this.cmdface_Attendance_Click()
		if(this.parent.ip=="127.0.0.1")$ID("video_attendance").Hide();
		else $ID("face_attendance_button").Hide();
	},
	cmdface_Attendance_Click:function(){
		if(this.parent.ip=="127.0.0.1" && this.parent.cfg.isface){console.log("打开人脸识别模块：","".LoadURL("/api/login/openface"));}
		$ID("face_attendance").Show()
		$ID("qcode_attendance").Hide()
	},
	cmdqrcode_Attendance_Click:function(){
		if(this.parent.ip=="127.0.0.1" && this.parent.cfg.isface)
			{console.log("关闭人脸识别模块：","".LoadURL("/api/login/closeface"));}
		$ID("face_attendance").Hide();
		$ID("qcode_attendance").Show();
		$ID("qcode_attendance").Clear();
		url="http://"+this.parent.servicersip+":9523/getAttendanceQrCode"
		qrcode=new QRCode(document.getElementById("qcode_attendance"), {width :200,height : 200});
		qrcode.makeCode(url)
	},
	cmdOrder_Click:function(e){
		this.mode="order"
		$ID("panwork").Clear();
		url="http://"+this.parent.cfg.release.device.ip+":9523/"+App.path+"/order.html"
		qrcode=new QRCode(document.getElementById("panwork"), {width :180,height : 180});
		qrcode.makeCode(url);
	},
	cmdRemoteAccess_Click:function(e){
		$ID("panwork").Clear();
		url="http://"+this.parent.cfg.release.device.ip+":9523/"+App.path+"/index.html"
		qrcode=new QRCode(document.getElementById("panwork"), {width :180,height : 180});
		qrcode.makeCode(url);
	},
	cmdView_Click:function(e){
		if(this.mode=="order"){
			this.parent.data.user.username=""
		}
		this.mode="station"
		$ID("panwork").Clear();
		value={};value.cmd="show library today";
		if(this.parent.cfg.isface){console.log("关闭人脸识别模块：","".LoadURL("/api/login/closeface"));}
		var value = {}; value.cmd = "mjpg-streamer start"; App.wsc.SendMessage(value); 
		showlibrary()
		function showlibrary(data){
			if(data==null){
				data=JSON.parse("".LoadURL("/api/record/showlibrary/today"))
				data.PublicServation=App.cfg.station.PublicServation
			}
			strtmpl="".LoadURL(App.path+"/tmpl/inspection/list.txt");
			$ID("panwork").Html(tmpl(strtmpl,data));
		}		
	},
	cmdExit_Click:function(){
		this.parent.data.user.username="";
		this.parent.data.user.cname="";
		this.parent.data.item.courseid="";
		this.parent.data.item.experimentid="";
		this.data=this.data_init();
		location.reload();
	},
	cmdLogin:function(){
		phone=$ID("login_username").Val();
		pass=$ID("login_pass").Val();
		msg="".LoadURL("/api/login/phone/"+phone+"/"+pass);
		console.log("phone:"+phone);
		console.log("pass:"+pass);
		data=JSON.parse(msg)
		console.log(data)
		if(data.code!=200){
			msgbox(data.msg,3);
		}else{
			this.parent.data.user.username=data.username;
			this.parent.data.user.cname=data.cname;
			this.checkPolicy(data.username)
		}
	},
	cmdtakePicture_Click:function(){
		value ={};
		value.cmd = "take picture";
		value.type=this.parent.cfg.release.version.sn+".recordmovice";
		value.username=this.parent.data.user.username;
		value.courseid=this.parent.data.item.courseid;
		value.experimentid=this.parent.data.item.experimentid;
		if(value.username=="")value.username=this.data.username;
		this.parent.wsc.SendMessage(value);
		// msg=this.parent.Load("/takepicture/"+username+"/"+courseid+"/"+experimentid)
		// console.log(msg)
		// data=JSON.parse(msg)
		// 
	},
	cmdStartNetworkMoive_Click:function(){
		value ={};
		value.cmd = "start network video record";
		value.type=this.parent.cfg.result.eth0.mac+".recordmovice";
		value.username=this.parent.data.user.username;
		value.courseid=this.parent.data.item.courseid;
		value.experimentid=this.parent.data.item.experimentid;
		if(value.OperatorUserName=="")value.OperatorUserName=this.data.username;
		this.parent.wsc.SendMessage(value);
	},
	cmdStopNetworkMoive_Click:function(){
		value ={};
		value.cmd = "end network video record";
		value.type=this.parent.cfg.result.eth0.mac+".recordmovice";
		value.username=this.parent.data.user.username;
		value.courseid=this.parent.data.item.courseid;
		value.experimentid=this.parent.data.item.experimentid;
		if(value.OperatorUserName=="")value.OperatorUserName=this.data.username;
		this.parent.wsc.SendMessage(value);
	},
	cmdStartMoive_Click:function(){
		url="/startrecord/usb/"+this.parent.data.user.username+"/"+this.parent.data.item.courseid+"/"+this.parent.data.item.experimentid;
		console.log("".LoadURL(url))
	},
    cmdStopMoive_Click:function(){
		value ={};
		value.cmd = "end record moive";
		value.type=this.parent.cfg.result.eth0.mac+".recordmovice";
		value.OperatorUserName=this.parent.data.user.username;
		value.courseid=this.parent.data.item.courseid;
		value.experimentid=this.parent.data.item.experimentid;
		if(value.OperatorUserName=="")value.OperatorUserName=this.data.username;
		this.parent.wsc.SendMessage(value);
	},
	opencase:function(){
		$ID("panwork").Clear();
		if(this.parent.cfg.isface){console.log("关闭人脸识别模块：","".LoadURL("/api/login/closeface"));}
		this.mode="";
		username=this.parent.data.user.username;
		courseid=this.parent.data.item.courseid;
		experimentid=this.parent.data.item.experimentid;
		value={};
		value.cmd="show library id";
		value.username=username;
		value.courseid=courseid;
		value.experimentid=experimentid;
		this.parent.wsc.SendMessage(value,this,function(self, result){
			console.log(result)
			strtmpl="".LoadURL(App.path+"/tmpl/inspection/case.txt").replace("<host>",self.parent.ip);
			$ID("panwork").Html(tmpl(strtmpl,result).replace("<uvccamera>","".LoadURL("/api/device/uvccamera/url").replace("<host>", self.parent.ip)));
			try{self.parent.data.handle.closemsg()}
			catch(e){}
		})
	},
	checkPolicy:function(username,cname){
		const now=new Date().Format("yyyy-MM-dd hh:mm:ss");
		devid=this.parent.StationId;
		courseid=this.parent.data.item.courseid;
		experimentid=this.parent.data.item.experimentid;
		// url="/api/policy/"+devid+"/"+courseid+"/"+experimentid+"/"+username;
		url="/api/getpolicy/user/"+username;
		console.log(url);msg="".LoadURL(url);
		try{
			data=JSON.parse(msg);
			console.log(courseid);
			console.log(experimentid);
			console.log(devid);
			for(var i=0;i<data.policy.length;i++){
				rs=data.policy[i]
				console.log("policy:"+JSON.stringify(rs));
				if(rs.devindex==devid || rs.devindex==devid+"_"+courseid+"_"+experimentid){
					start=rs.start;end=rs.end;
					console.log("devindex:"+rs.devindex);
					console.log("starttime:"+start);
					console.log("endtime:"+end);
					console.log("now:"+now);
					console.log("datetime:"+(start<now && now<end))
					if(start<now && now<end){
						this.parent.data.user.username=username;
						this.parent.data.user.cname=cname;
						this.opencase();
						break;
					}
				}
			}
		}catch(err){console.log(err);msgbox("查找权限失败，无法访问服务器",3)}
	},
	cmdInspection_Click:function(CourseID,ExperimentID,start,end){
		const now=new Date().Format("yyyy-MM-dd hh:mm:ss")
		console.log("starttime:"+start)
		console.log("endtime:"+end)	
		console.log("now:"+now)
		console.log("datetime:"+(start<now && now<end))
        if(CourseID==null){
			this.opencase()
		}else if(start<now && now<end){
			this.mode="login";
			console.log("CourseID:"+this.parent.data.item.courseid);console.log("ExperimentID:"+this.parent.data.item.experimentid)
			$ID("panwork").Clear()
			if(this.parent.data.user.username==""){
				this.parent.data.item.courseid=CourseID;
				this.parent.data.item.experimentid=ExperimentID;
				strtmpl=this.parent.Load(App.path+"/tmpl/inspection/login.txt").replace("<rpicamera>","".LoadURL("/api/device/picamera/url")).replace("<host>", this.parent.ip)
				$ID("panwork").Html(strtmpl)
				if(this.parent.cfg.isface){console.log("打开人脸识别模块：","".LoadURL("/api/login/openface"));}
				
			}else if(this.parent.data.item.courseid!=CourseID || this.parent.data.item.experimentid!=ExperimentID){
				this.parent.data.item.courseid=CourseID;
				this.parent.data.item.experimentid=ExperimentID;
				this.checkPolicy();
			}else if(this.parent.data.item.courseid==CourseID && this.parent.data.item.experimentid==ExperimentID){
				this.opencase();
			}
		}else{
			msgbox("当前时间不在有效时段",3)
		}
		
	},
	show:function(){this.data=this.data_init();strtmpl=this.parent.Load(App.path+"/tmpl/inspection/frmdesktop.txt");this.parent.Html(tmpl(strtmpl,this));this.cmdView_Click();Document.SystemTime("system_time");this.parent.cmdInit();},
	Form_Load:function(p){
		this.parent=p;
		this.data.handle={};
		this.show();
	},
	Form_Resize:function(w,h){},
	Form_Receive:function(obj){
		console.log("frm work recv:" + JSON.stringify(obj));
		//{"eventType":"readcard","cname":"李品勇","user":"20110032","card":"164887559"}
		if(obj.type=="auth"){
			console.log(obj)
			this.opencase(this,obj)
		}else if(obj.topic=="readcard_changereadcardmode"){
			console.log(obj.username);
			console.log(obj.cname.base64decode());
			this.cmdCard(obj)
		}else if(obj.topic=="nouser"){
			console.log("topic nouser")
			var strtmpl="抱歉，用户名或密码错误";
            var data={};
            data.username=obj.username;
            var o=msgbox(tmpl(strtmpl,data),3)
		}else if(obj.type=="login"){
			if(this.frm.mode=="login")self.opencase(this.frm,obj)
		}else if(obj.eventType=="readcard" && this.mode=="station"){
			if(obj.user==""){
				msgbox("卡号"+obj.card+"查无此人",3)
			}	
			else{console.log(obj.user);this.checkPolicy(obj.user,obj.cname)}
		}else if(obj.eventType=="readcard" ){
			try{this.t.closemsg();}
			catch(e){}
			if(this.mode=="login"){console.log(obj.user);this.checkPolicy(obj.user,obj.cname);}
			else if(this.mode=="attendance"){
				if(obj.user=="" && obj.card!=""){
					this.t=msgbox("卡号"+obj.card+"查无此人",30)
					url="http://"+this.parent.servicersip+":9523/user/bindcard/"+obj.card
					console.log(url)
					qrcode=new QRCode(document.getElementById("readcar_qrcode"), {width :80,height : 80});
					qrcode.makeCode(url)
					url="http://www.lubanlou.com/api/usercenter/share/addCardOrReplace?newCard="+obj.card
					qrcode=new QRCode(document.getElementById("readcar_qrcode1"), {width :80,height : 80});
					qrcode.makeCode(url)
				}
				else{
					msgbox("卡号："+obj.card+"工号："+obj.user+"\n姓名："+obj.cname+"\n考勤成功",3);
					if(this.parent.ip=="127.0.0.1"){
						msg="/attendance/log/"
						msg=msg+"%7Ccname%7C_%7C"+obj.cname.base64encode()+"%7C="
						msg=msg+"%7Cusername%7C_%7C"+obj.user+"%7C="
						msg=msg+"%7Ccardnumber%7C_%7C"+obj.card+"%7C"
						console.log("".LoadURL(msg))
					}
					this.cmdAttendance_Click()
				}
			}
			
			
		}else if(obj.eventType=="face"){
			if(this.mode=="login"){console.log(obj.user);this.checkPolicy(obj.user,obj.cname);}
			else if(this.mode=="attendance"){
				msgbox("工号："+obj.user+"姓名："+obj.cname+"\n考勤成功",3);
				if(this.parent.ip=="127.0.0.1"){
					msg="/attendance/log/"
					msg=msg+"%7Ccname%7C_%7C"+obj.cname.base64encode()+"%7C="
					msg=msg+"%7Cusername%7C_%7C"+obj.user+"%7C"
					console.log("".LoadURL(msg))
				}
				this.cmdAttendance_Click()
			}
			
		}else if(obj.cmd=="start network video record"){
			if(obj.code==500){
				msgbox(obj.msg,3)
				$(".on_networkvideotape").show();
				$(".off_networkvideotape").hide();
			}
		}else if(obj.cmd=="show library id"){
			data=obj.result
			var value = {}; value.cmd = "mjpg-streamer start"; App.wsc.SendMessage(value); 
			this.parent.data.user.username=data.username;
			this.parent.data.item.courseid=data.courseid;
			this.parent.data.item.experimentid=data.experimentid;
			strtmpl="".LoadURL(App.path+"/tmpl/inspection/case.txt").replace("<host>",this.parent.ip);
			$ID("panwork").Html(tmpl(strtmpl,data).replace("<uvccamera>","".LoadURL("/api/device/uvccamera/url").replace("<host>", this.parent.ip)));
		}else if(obj.eventType=="broadcast"){
			data=obj.result
			console.log("frm work recv broadcast result:" + JSON.stringify(data));
			if (data.type=="sensor_dht11"){
				document.getElementById("humidity").innerHTML=obj.result.humidity;
				document.getElementById("temperature").innerHTML=obj.result.temperature;
			}else if(data.cmd=="take picture"){
				list=new Element("library");
				strtmpl=list.Html()
				strtmpl=strtmpl+"<a href='javascript:void(0)' data-imgUrl='"+data.url+"' onclick='sub_camera_box_a_click(this);' class='switch_camera_sub  sub_camera_select'>"
				strtmpl=strtmpl+"<img class='switch_camera_sub' src='"+data.url+"'>"
				strtmpl=strtmpl+"</a>"
				list.Html(strtmpl)
			}else if(data.cmd=="end record moive"){
				if(data.url==""){
					list=new Element("library");
					strtmpl=list.Html()
					strtmpl=strtmpl+"<a href='javascript:void(0)' id='"+data.filename.replace(".","_")+"' onclick='sub_camera_video_a_click(this);' class='switch_camera_sub  sub_camera_select'>"
					strtmpl=strtmpl+"正在生成中...";
					strtmpl=strtmpl+"</a>"
					list.Html(strtmpl)
				}else{
					e=new Element(data.filename.replace(".","_"))
					e.Html("<video class='switch_camera_sub' src='"+data.url+"'></video>")
					e.attribute("data-imgUrl",data.url)
				}
			}
		}			
	}
}
var App={
	data:{item:{courseid:"",experimentid:""},user:{username:"",cname:""},handle:null},
	Width:0,
	Height:0,
	frm:frmWork,
	handle:null,
	rootpath:"",
	user:null,
	path:"",
	cfg:{
		sn:"",
		isface:"",
		release:Document.LoadJson("/api/config/release.json"),
		station:Document.LoadJson("/api/config/station.json")
	},
	wsc:null,
	ip:Document.Path().host,
	servicersip:'',
	port:8131,
	StationId:"",
	LabId:"",
	Tmpl:function(strurl,data){strtmpl=this.handle.Load(strurl);this.handle.Html(tmpl(strtmpl,data))},
	Windows_Load:function(){
		console.log(this.cfg.release);
		if("device" in this.cfg.release){
			this.StationId=this.cfg.release.device.labid;this.LabId=this.cfg.release.device.labid;this.cfg.sn=this.cfg.release.version.sn;this.servicesip=Document.LoadJson("/api/runtime/network/"+this.cfg.release.device.network).ip;
			this.cfg.isface=this.cfg.release.module.slots.indexOf("face")==true;
		}
		console.log(this.cfg.station);
		if ("debug" in this.cfg.station){
			if(this.cfg.station.debug == true) { window.vConsole = new VConsole(); }
		}	
		
		if(this.wsc==null){
			this.wsc=new webSockObject(this.cfg.sn)
			this.wsc.Connect(this.ip,this.port,
				function(){
					App.wsc.isOpen=true;
					console.log("websocket connected");
					App.wsc.SendMessage({'cmd':'websocket.test'},this,function(self, result){
						self.id=result.clientid;
						console.log("websocket.test.return:"+result.clientid);
					});
					},
				function(){App.wsc.isOpen=false;console.log("websocket closed");},
				function(obj){
					console.log("app receive:"+JSON.stringify(obj));
					console.log(obj.type=="sensor_dht11")
					if(obj.type=="sensor_dht11"){
						document.getElementById("humidity").innerHTML=obj.result.humidity;
						document.getElementById("temperature").innerHTML=obj.result.temperature;
					}
					else if(App.frm!=null) App.frm.Form_Receive(obj);
				}
			)
		}
		if(this.frm!=null){App.frm.Form_Load(App)};
	},
	Windows_Resize:function(w,h){
		console.log("resize....");
		if(w!=this.Width){console.log("width:"+w);this.Width=w;}
		if(h!=this.Height){console.log("height:"+h);this.Height=h;}
		if(this.frm!=null){this.frm.Form_Resize(w,h)}
        //Zoom();
	},
	Load:function(value){if(this.handle!=null)return this.handle.Load(value)},
	Html:function(value){if(this.handle!=null)this.handle.Html(value)},
	Clear:function(){if(this.handle!=null)this.handle.Html("")},
	cmdInit:function(){
		$class("button").ForEach(function(i,item){
			item.BindEvent("mouseover",function(){this.style.cursor="pointer";});
			item.BindEvent("mouseout",function(){this.style.cursor="auto";});
			item.BindEvent("mousedown",function(){this.style.background="rgba(255, 255, 255, 0.6)"});
			item.BindEvent("mouseup",function(){this.style.background=""});
		})
	}
	// ws:new webSockObject("127.0.0.1")
}
