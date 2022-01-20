App.code.debug.frmLogin.code=function(name,app){
	var self = this;Form.call(this, name);this.app = app; this.parent = app.parent;this.Timer = null;
    this.data=null;this.tmpldata=null;this.tmpldata=null;this.Timer=null
	this.load=function(){
		this.tmpl=this.app.path+"/frmLogin/frmLogin.txt";
		Document.LoadCSS(this.app.apppath+"/global.css");
		Document.LoadCSS(this.app.rootpath+"/css/gvsun.webui.css");
	};
	this.Form_Show=function(){
		this.app.Forms.activeForm = this;
		this.app.wsc.SendMessage({"cmd":"start detect face"})
		console.log("frmLogin")
		console.log(self.app.policy)
		if(self.app.cfg.release.module.slots.indexOf("face")!=-1){
			$$("#raspicamera").src("http://"+Document.Paths.server+":1891/?action=streamer").css("width","240px").css("height","320px")
		}
		this.Form_Resize(Document.Width(),Document.Height());
		if (this.Timer==null) {this.Timer=setInterval(this.task,60000);};
	};
	this.Form_Resize=function(w,h){};
	this.Form_Receive = function (data) {
		console.log(data);
		console.log(this.Name + " receive:" + JSON.stringify(data))
		if(data.type=="event_auth" && data.result.code==200){
			this.app.policy=data.result.data;
			App.getPolicy(data.result.data.username);
			App.Forms.frmBrowser.CheckPolicy();
		}else if(data.type == "readcard_read" && data.status==false) {
			url=this.app.rootpath+this.app.api.getcard+data.card;
			this.getAttendance(url.LoadJson());
		}else if(data.type == "face_read" && data.score>70){
			//getuser获取的应该是用户名 username对应的是密码
			url=this.app.rootpath+this.app.api.getuser+data.username
			this.getAttendance(url.LoadJson());
		}
	};
	this.getAttendance=function(data){
		if(data.code==200){				
			console.log(data);
			this.app.policy.username=data.username;
			this.app.policy.cname=data.cname;
			this.app.getPolicy(data.username)
			this.app.Forms.frmBrowser.CheckPolicy();

		}else if(data.code=404){
			t=msgbox(data.msg,3)
			if("card" in data && data.card!=""){
				Document.LoadJscript( this.app.rootpath +  this.app.Module.qrcode, function(url) {
					// t=msgbox("卡号" + data.card + "查无此人", 3);
					url = "http://"+ self.app.cfg.release.device.ip+":"+ self.app.cfg.release.services.port+"/user/bindcard/" + data.card
					qrcode = new QRCode(document.getElementById("readcar_qrcode"), {width: 80,height: 80});qrcode.makeCode(url);
					url = "http://www.lubanlou.com/api/usercenter/share/addCardOrReplace?newCard=" + result.card
					qrcode = new QRCode(document.getElementById("readcar_qrcode1"), {width: 80,height: 80});qrcode.makeCode(url);
				});
			}
		}
	};
	this.task=function(){
		now=new Date().Format("yyyy-MM-dd hh:mm:ss");
		if(self.app.policy.end<now){
			if(self.Timer!=null){window.clearInterval(self.Timer);self.Timer=null;}
			self.app.Forms.frmBrowser.Show();
		}
	};
	this.cmdLogin=function(){
		if(this.Timer!=null){window.clearInterval(this.Timer);this.Timer=null;}
		phone=$$("#login_username").Val();pass=$$("#login_pass").Val();
		url=this.app.rootpath+this.app.api.login.replace("<user>",phone).replace("<pass>",pass)
		result=url.LoadJson()
		if(result.code==200){
			this.app.policy.username=result.username;
			this.app.policy.cname=result.cname;
			this.app.getPolicy(result.username)
			this.app.Forms.frmBrowser.CheckPolicy();
		}else{
			console.log(result)
			if(!("msg" in result))result.msg="登录不成功,原因：未知";
			msgbox(result.msg,3)
		}
	};
}
