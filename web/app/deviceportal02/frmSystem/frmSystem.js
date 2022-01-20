App.frmSystem = new Form("frmSystem"); frmSystem = App.frmSystem;
App.frmSystem.Form_Resize=function(w,h){}
App.frmSystem.load = function () {
	App.frmSystem.cfg=(App.rootpath+"api/getsystemfolder").LoadJson()
	App.frmSystem.cfgFile=new JsonFile(App.rootpath+"api/file/"+(App.frmSystem.cfg.rootpath+"/etc/conf/release.json").base64encode())
    App.frmSystem.binddata=this.cfgFile.data
	App.frmSystem.parent=App.controls.panWork;
	App.frmSystem.parent.CSS("color","#ffffff")
}
App.frmSystem.Form_Show = function () {
	console.log("wsc_receive:" + this.Name);
	App.wsc.event_receive = App.frmSystem.Form_Receive;
	App.frmSystem.parent.Clear().Text(JSON.stringify(App.frmSystem.binddata,null,2))
	// $$(".panLeftItem").css("background","rgba(0,0,0,0)");
	// $$("#itemSystem").css("background","rgba(0,0,0,0.9)");
}
App.frmSystem.Form_Receive = function (data) {
	console.log(this.Name + " receive:" + JSON.stringify(data))
}

