App.frmSystem = new Form("frmSystem"); frmSystem = App.frmSystem;
App.frmSystem.Form_Resize=function(w,h){}
App.frmSystem.load = function () {
	App.frmSystem.parent=App.controls.panWork;
	App.frmSystem.parent.CSS("color","#ffffff")
}
App.frmSystem.Form_Show = function () {
	console.log("wsc_receive:" + this.Name);
	App.wsc.event_receive = App.frmSystem.Form_Receive;
	App.frmSystem.parent.Clear().Text(JSON.stringify(App.data.cfg.release,null,2))
	// $$(".panLeftItem").css("background","rgba(0,0,0,0)");
	// $$("#itemSystem").css("background","rgba(0,0,0,0.9)");
}
App.frmSystem.Form_Receive = function (data) {
	console.log(this.Name + " receive:" + JSON.stringify(data))
}

