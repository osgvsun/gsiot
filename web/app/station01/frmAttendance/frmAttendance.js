App.frmAttendance = new Form("frmAttendance");
frmAttendance = App.frmAttendance;
App.frmAttendance.load = function() {
	App.frm = frmAttendance;
	frmAttendance.parent = new Element("#panwork");
	frmAttendance.tmpl = App.path + App.data.tmpl.frmAttendance;
	frmAttendance.dataurl = App.rootpath + App.data.api.attlog;
}
App.frmAttendance.Form_Show = function() {
	console.log("wsc_receive:" + this.Name);
	App.wsc.event_receive = App.frmAttendance.Form_Receive;

}
App.frmAttendance.Form_Receive = function(data) {
	console.log(frmAttendance.Name + " receive:" + JSON.stringify(data))
	if(data.type == "readcard_read") {
		result = "".LoadJson(App.rootpath + App.data.api.getcard + data.card);
		console.log(result)
		if(result.code == 200) {
			data = {};
			data.username = result.username;
			data.cname = result.cname;
			data.cardnumber = result.card;
			data.datetime = new Date().Format("yyyy-MM-dd hh:mm:ss");
			App.frmAttendance.binddata.result.push(data);
			App.frmAttendance.parent.Html(tmpl(App.frmAttendance.tmpldata, App.frmAttendance.binddata));
		} else if(result.code == 404) {
			Document.LoadJscript(App.path + App.data.Module.qrcode, function(url) {
				t = msgbox("卡号" + result.card + "查无此人", 30)
				url = "http://"+App.data.cfg.release.device.ip+":"+App.data.cfg.release.services.port+"/user/bindcard/" + result.card
				qrcode = new QRCode(document.getElementById("readcar_qrcode"), {
					width: 80,
					height: 80
				});
				qrcode.makeCode(url)
				url = "http://www.lubanlou.com/api/usercenter/share/addCardOrReplace?newCard=" + result.card
				qrcode = new QRCode(document.getElementById("readcar_qrcode1"), {
					width: 80,
					height: 80
				});
				qrcode.makeCode(url)
			});

		}
	}

}