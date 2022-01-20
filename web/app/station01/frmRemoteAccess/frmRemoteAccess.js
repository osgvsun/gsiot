App.frmRemoteAccess=new Form("frmRemoteAccess");frmRemoteAccess=App.frmRemoteAccess;
App.frmRemoteAccess.load=function(){
    frmRemoteAccess.parent=new Element("#panwork");
    frmRemoteAccess.Url="http://"+App.data.cfg.release.device.ip+":"+App.data.cfg.release.services.port+App.path+"index.html?"+new Date().Format("yyyy-MM-dd hh:mm:ss").base64encode()
    frmRemoteAccess.tmpl=App.path+App.data.tmpl.frmRemoteAccess;
}
App.frmRemoteAccess.Form_Show=function(){ 
	console.log("wsc_receive:"+this.Name);
	App.wsc.event_receive=App.frmRemoteAccess.Form_Receive;
	Document.LoadJscript(App.path+App.data.Module.qrcode,function(url){	
		qrcode=new QRCode($$("#qrcode").hWnd, {width :180,height : 180}); 
		qrcode.makeCode(frmRemoteAccess.Url); 
	});
}
App.frmRemoteAccess.LoadCase=function(result){ frmWork.data=result; frmWork.Show(); }
App.frmRemoteAccess.Form_Receive = function(data) {
	console.log(frmRemoteAccess.Name + " receive:" + JSON.stringify(data))
	if(data.cmd == "show library id") {
		if(isLoadJS(App.data.Module.frmWorkURL) == false) {
			Document.LoadJscript(App.data.ModulefrmWorkURL, function(url) {
				App.frmRemoteAccess.LoadCase(data.result);
			});
		} else App.frmRemoteAccess.LoadCase(data.result);
	}
}