App.frmLogin=new Form("frmLogin");var frmLogin=App.frmLogin;
App.frmLogin.load=function(){
    App.frmLogin.parent=new Element("#panwork");
    App.frmLogin.tmpl=App.path+App.data.tmpl.frmLogin;
}
App.frmLogin.Form_Show=function(){ 
	$$("#raspicamera").src("http://"+App.data.cfg.release.device.ip+":1891/?action=streamer")
	App.wsc.event_receive=App.frmLogin.Form_Receive;
}
App.frmLogin.Form_Receive=function(data){
    console.log(frmLogin.Name+" receive:"+JSON.stringify(data))
	if(data.type=="event_auth" && data.result.code==200){
		App.data.policy=data.result.data;
		App.getPolicy(data.result.data.username);
		App.frmBrowser.CheckPolicy();
	}
}
App.frmLogin.cmdLogin=function(){
	phone=$$("#login_username").Val();pass=$$("#login_pass").Val();
	url=App.rootpath+App.data.api.login.replace("<phone>",phone).replace("<pass>",pass)
	result=url.LoadJson()
	console.log(result)
	if(result.code==200){
		App.data.policy.username=result.username;
		App.data.policy.cname=result.cname;
		console.log(result);
		App.getPolicy(result.username)
		App.frmBrowser.CheckPolicy();
	}else{
		msgbox(result.msg,3)
	}
}
