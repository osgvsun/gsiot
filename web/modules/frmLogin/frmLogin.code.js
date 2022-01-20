var self = this;Form.call(this, name);this.app = app; this.parent = app.parent;this.Timer = null;
this.data=null;this.tmpldata=null;this.tmpldata=null;this.Timer=null
this.load=function(){
	this.tmpl=this.app.path+"/frmLogin/frmLogin.txt";
	Document.LoadCSS(this.app.apppath+"/global.css");
	Document.LoadCSS(this.app.rootpath+"/css/gvsun.webui.css");
};
this.Form_Show=function(){
	this.app.Forms.activeForm = this;
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
	console.log(this.Name + " receive:" + JSON.stringify(data))
	if(data.type=="event_auth" && data.result.code==200){
		this.app.policy=data.result.data;
		App.getPolicy(data.result.data.username);
		App.Forms.frmBrowser.CheckPolicy();
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
	console.log(url)
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
