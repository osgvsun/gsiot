App.code.debug.frmAttendance.code=function(name,app){
	var self = this;Form.call(this,name);this.app = app; this.parent = app.parent; this.tabBody=null;
    this.load=function(){self = this.app.Forms[this.Name];Document.LoadCSS(this.app.rootpath+"/css/gvsun.webui.css");this.tmpl = this.app.path + "/frmAttendance/frmAttendance.txt";this.dataurl = this.app.rootpath + this.app.api.attlog;};
    
	this.Form_Show=function(){
		this.app.Forms.activeForm = this;

		//开启人脸识别
		this.app.wsc.SendMessage({"cmd":"start detect face"})
		console.log("wsc_receive:" + this.Name);
		if(self.app.cfg.release.module.slots.indexOf("face")!=-1){
			$$("#raspicamera")
			.src("http://"+Document.Paths.server+":1891/?action=streamer")
		}
		tabTitle=this.parent.FindElement("table").Index(0);
        this.tabBody=new webui.Grid("tabBody").Parent($$("#divBody"));
		tabTitle.Cell(0,0).Width(50);
		tabTitle.Cell(0,1).Width(150);
		tabTitle.Cell(0,2).Width(150);
		tabTitle.Cell(0,3).Width(150);
		tabTitle.Cell(0,4).Width(260);
		this.ShowData();
		this.Form_Resize();
	};
	
	this.ShowData=function(){
		data=this.binddata;
		if(data!=null){
			this.tabBody.binddata(["#","cname","username","cardnumber","datetime"],data.result,true).Resize();
			this.tabBody.FindElement(".row00").css("width","50px");
			this.tabBody.FindElement(".row01").css("width","149px");
			this.tabBody.FindElement(".row02").css("width","149px");
			this.tabBody.FindElement(".row03").css("width","148px");
			this.tabBody.FindElement(".row04").css("width","260px");
		}
	};


    this.Form_Resize=function(w,h){this.tabBody.css("height",(this.parent.Height()-85)+"px")};
	
    this.Form_Receive = function (data) {
        console.log(this.Name + " receive:" + JSON.stringify(data));
		if(data.type == "readcard_read" && data.status==false) {
			url=this.app.rootpath+this.app.api.getcard+data.card;
			this.getAttendance(url.LoadJson());
		}else if(data.type == "face_read" && data.score>70){
			url=this.app.rootpath+this.app.api.getuser+data.username
			this.getAttendance(url.LoadJson());
		}
    };
	this.getAttendance=function(data){
		if(data.code==200){
			value={};
			value.username = data.username;
			value.cname = data.cname;
			value.cardnumber = data.card;
			value.datetime = new Date().Format("yyyy-MM-dd hh:mm:ss");
			this.binddata.result.Add(value);
			this.ShowData();
			msg="考勤成功"
			if(data.card!="")msg+="("+data.card+")"
			msg+="\n工号:"+data.username+"\n姓名:"+data.cname
			t=msgbox(msg,3)
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
	}
	this.makeAttendanceXLS=function(){
		result=(App.rootpath+"/api/setAttendance").LoadJson();
		if(result.result==true){
			msgbox("导出成功",3)
		}
	};
}