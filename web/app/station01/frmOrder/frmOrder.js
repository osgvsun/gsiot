App.frmOrder=new Form("frmOrder");frmOrder=App.frmOrder;
App.frmOrder.load=function(){
    frmOrder.parent=new Element("#panwork");
    frmOrder.Url="http://"+Document.Paths.server+":"+App.data.cfg.release.services.port+App.rootpath+"api/order/"+new Date().Format("yyyy-MM-dd hh:mm:ss").base64encode()
    frmOrder.tmpl=App.path+App.data.tmpl.frmOrder;
}
App.frmOrder.Form_Show=function(){ 
	console.log("wsc_receive:"+this.Name);
	App.wsc.event_receive=App.frmOrder.Form_Receive;
	Document.LoadJscript(App.path+App.data.Module.qrcode,function(url){	
		qrcode=new QRCode($$("#qrcode").hWnd, {width :180,height : 180}); 
		qrcode.makeCode(frmOrder.Url); 
	});
}
App.frmOrder.LoadCase=function(result){ 
	App.data.policy={"username":result.username,"cname":result.cname}
	App.getPolicy(result.username);
	App.frmWork.binddata={
		"CourseID":result.courseid,
		"ExperimentID":result.experimentid,
		"start":result.InspectionRecord.datetime.starttime,
		"end":result.InspectionRecord.datetime.endtime,
		"data":result.result.InspectionRecord
	}
    App.frmWork.Show(); 

}
App.frmOrder.Form_Receive = function(data) {
	console.log(frmOrder.Name + " receive:" + JSON.stringify(data));
	if(data.cmd == "show library id") {App.frmOrder.LoadCase(data.result.result);}
}