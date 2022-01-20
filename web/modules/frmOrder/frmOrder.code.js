var self = this;Form.call(this, name);this.app = app; this.parent = app.parent;this.Timer = null;
this.load=function(){
	this.Url="http://"+this.app.cfg.release.device.ip+":"+this.app.cfg.release.services.port
	this.Url+=self.app.apppath+"/order.html?"+new Date().Format("yyyy-MM-dd hh:mm:ss").base64encode()
	this.tmpl=this.app.path+"/frmOrder/frmOrder.txt";
};
this.Form_Show=function(){
	App.Forms.activeForm = this;
	Document.LoadJscript(this.app.rootpath+this.app.Module.qrcode,function(url){	
		qrcode=new QRCode($$("#qrcode").hWnd, {width :180,height : 180}); 
		qrcode.makeCode(self.Url); 
	});
	this.Form_Resize(Document.Width(),Document.Height());
};
this.Form_Resize=function(w,h){}   
this.LoadCase=function(result){ 
	this.app.policy={
		"username":result.username,
		"cname":result.cname,
		"courseid":result.courseid,
		"experimentid":result.experimentid,
		"InspectionRecord":result.InspectionRecord,
		"start":result.InspectionRecord.datetime.starttime,
		"end":result.InspectionRecord.datetime.endtime
	}
	if(this.app.Forms.frmInspection!=null){
		this.app.getPolicy(result.username);
		this.app.Forms.frmInspection.binddata=this.app.policy
		this.app.Forms.frmInspection.Show(); 
		this.app.Forms.frmBrowser.data=null;
	}else if(this.app.Forms.frmBrowser!=null){
		this.app.Forms.frmBrowser.data=null;
		this.app.Forms.frmBrowser.Show();}
};
this.Form_Receive = function(data) {
	console.log(this.Name + " receive:" + JSON.stringify(data));
	if(data.cmd == "show library id") {this.LoadCase(data.result);}
};