App.frmBrowser = new Form("frmBrowser"); frmBrowser = App.frmBrowser;
App.frmBrowser.load = function () {
	frmBrowser.parent = new Element("#panwork");
	frmBrowser.dataurl = App.rootpath + App.data.api.showlibrary;
	frmBrowser.PublicServation = App.data.config.PublicServation;
	frmBrowser.tmpl = App.path + App.data.tmpl.frmBrowser;
	if(App.frmBrowser.PublicServation){
		file=new JsonFile("/data/inspection/share/record.json")
		var now = new Date().Format("yyyy-MM-dd hh:mm:ss")
		if(file.isEmpty || file.data.InspectionRecord[0].datetime.endtime<now){
			console.log("/api/makeshare".LoadJson());
			file.Readfile();
		}
	}
}
App.frmBrowser.Form_Show = function () {
	console.log("wsc_receive:" + this.Name);
	App.wsc.event_receive = App.frmBrowser.Form_Receive;
}
App.frmBrowser.Form_Receive = function (data) {
	console.log(this.Name + " receive:" + JSON.stringify(data))
	if (data.cmd == "show library id") {

	} else if (data.type == "event_auth") {
		if (data.code = 200) {
			App.data.policy.username = data.data.username;
			App.data.policy.cname = data.data.cname;
		}
	}
}
App.frmBrowser.cmdInspection_Click = function (CourseID, ExperimentID, start, end) {
	if(CourseID==null || CourseID=="share"){
		// result="/data/inspection/share/record.json".LoadJson()
		App.frmWork.data = { 
			"courseid": "share", 
			"experimentid": "01",
			"InspectionRecord": file.data.InspectionRecord[0]
		}
		App.frmWork.binddata = {"data":App.frmWork.data}
		// App.frmWork.binddata ={"data":result}
		App.frmWork.Show();
	}else{
		console.log("policy:" + JSON.stringify(App.data.policy))
		var now = new Date().Format("yyyy-MM-dd hh:mm:ss")
		if(start < now && now < end){
			if (App.data.policy.username == "") {
				App.frmWork.binddata = { "courseid": CourseID, "experimentid": ExperimentID, "start": start, "end": end }
				console.log(App.frmWork.binddata);
				Document.LoadJscript(App.path + App.data.Module.frmLoginURL, function (url) {
					App.frmLogin.Show();
				});
			} else App.frmBrowser.CheckPolicy();
		}else if(start > now){
			msgbox("预约时间为\n"+start+"\n至\n"+end+"\n,该预约没有开始",3)
		}else if(end< now){
			msgbox("预约时间为\n"+start+"\n至\n"+end+"\n,预约已结束",3)
		}
	}
}
App.frmBrowser.CheckPolicy = function () {
	var start = App.frmWork.binddata.start, 
	end = App.frmWork.binddata.end,
	devindex = App.data.cfg.release.device.id + "_" 
			+ App.frmWork.binddata.courseid + "_" 
			+ App.frmWork.binddata.experimentid;
	console.log("starttime:" + start)
	console.log("endtime:" + end)
	console.log("CourseID:" + App.frmWork.data.CourseID)
	console.log("ExperimentID:" + App.frmWork.data.ExperimentID)
	console.log("devindex:" +devindex)
	
	App.data.policy.data.ForEach(function (policy, index) {
		if (policy.devindex == App.data.cfg.release.device.id || policy.devindex == devindex) {
			url = App.rootpath + "api/showlibraryid/<username>/<course>/<experiment>"
				.replace("<username>", App.data.policy.username)
				.replace("<course>", App.frmWork.binddata.courseid)
				.replace("<experiment>", App.frmWork.binddata.experimentid)
			result = url.LoadJson();
			App.frmWork.binddata = {"data":result}
			App.frmWork.Show();
		} else {console.log(policy.devindex);}
	})
}
