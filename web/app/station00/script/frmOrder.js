App.frmOrder=new Form("frmOrder");frmOrder=App.frmOrder;
App.frmOrder.load=function(){
    App.frm=frmOrder;
    frmOrder.parent=new Element("panwork");
    frmOrder.Url="http://"+App.data.cfg.release.device.ip+":"+App.data.cfg.release.services.port+App.rootpath+"api/order/"+new Date().Format("yyyy-MM-dd hh:mm:ss").base64encode()
    App.wsc.event_receive=App.frmOrder.Form_Receive;
    frmOrder.tmpl="".LoadURL(App.data.tmpl.frmOrder);
    frmOrder.parent.Html(tmpl(App.frmOrder.tmpl, App.frmOrder));
    Document.LoadJscript(App.data.Module.qrcode,function(url){frmOrder.Form_Show()});
    frmOrder.isshow=true;
}
App.frmOrder.Form_Show=function(){ qrcode=new QRCode(document.getElementById("qrcode"), {width :180,height : 180}); qrcode.makeCode(frmOrder.Url); }
App.frmOrder.LoadCase=function(result){ frmWork.data=result; frmWork.Show(); }
App.frmOrder.Form_Receive = function(data) {
	console.log(frmOrder.Name + " receive:" + JSON.stringify(data))
	if(data.cmd == "show library id") {
		if(isLoadJS(App.data.Module.frmWorkURL) == false) {
			Document.LoadJscript(App.data.ModulefrmWorkURL, function(url) {
				App.frmOrder.LoadCase(data.result);
			});
		} else App.frmOrder.LoadCase(data.result);
	}
}