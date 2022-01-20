var App=new Form("frmMain")
App.wsc=null;
App.Form_Resize=function(w,h){}
App.Form_Receive=function(data){ 
    console.log(App.Name+" receive:"+JSON.stringify(data)); 
    if(data.type=="sensor_dht11"){ 
        $$("#humidity").Html(data.result.humidity); 
        $$("#temperature").Html(data.result.temperature); } }
App.load=function(){
	App.parent=new Element("#work");
    App.data=(App.path+"config.json").LoadURL();
    App.data.cfg={
        sn:"",
        isface:"",
        ip:Document.Path().host,
        port:8131,
        release:(App.rootpath+App.data.api.release).LoadURL(),
        station:(App.rootpath+App.data.api.station).LoadURL()
    };
    App.data.policy={"username":"","cname":"","CourseID":"","ExperimentID":""}
    App.data.Record={"CourseID":"","ExperimentID":"","start":"","end":""}
    Document.LoadCSS(App.path+"frmMain/global.css");
    Document.LoadJscript(App.path+App.data.Module.frmWorkURL);
    App.tmpl=App.path+App.data.tmpl.frmMain;

    if(App.wsc==null){ App.wsc=new webSockObject(App.data.cfg.release.device.sn); 
        App.wsc.Connect(Document.Paths.server,App.data.cfg.port,App.websocket_Connect,App.websocket_DisConnect,App.frm.Form_Receive); }
    else{ App.wsc.event_receive=App.Windows_Receive; } 
    if(App.data.cfg.station.debug){ Document.LoadJscript(App.rootpath+"script/vconsole.min.js",function(url){ App.vConsole = new VConsole(); })  }
}

App.Form_Show=function(){
    App.data.policy={"username":"","cname":"","CourseID":"","ExperimentID":""};
    App.data.Record={"CourseID":"","ExperimentID":"","start":"","end":""};
    App.cmdView_Click();}
App.websocket_Connect=function(){ App.wsc.isOpen=true; console.log("websocket connected"); 
App.wsc.SendMessage({'cmd':'websocket.test'},this,function(self, result){ self.id=result.clientid; console.log("websocket.test.return:"+result.clientid); }); }
App.websocket_DisConnect=function(){App.wsc.isOpen=false;console.log("websocket closed");}
App.cmdView_Click = function() { Document.LoadJscript(App.path+App.data.Module.frmBrowserURL, function(url) { App.frmBrowser.Show(); });  }
App.cmdOrder_Click = function() { Document.LoadJscript(App.path+App.data.Module.frmOrderURL, function(url) { App.frmOrder.Show(); }); }
App.cmdAttendance_Click = function() { Document.LoadJscript(App.path+App.data.Module.frmAttendanceURL, function(url) { App.frmAttendance.Show(); }); }
App.cmdRemoteAccess_Click=function(){
	Document.LoadJscript(App.path+App.data.Module.frmRemoteAccessURL, function(url) { App.frmRemoteAccess.Show(); }); 
}
App.cmdExit_Click=function(){
    console.log(App.frmWork.binddata.data.courseid)
    if(App.frmWork.binddata.data.courseid=="share"){
        file=new JsonFile("/api/data/inspection/share")
        file.data.InspectionRecord[0].Record=[]
        file.data.InspectionRecord[0].Upload=[]
        // file.Savefile()
    }
	App.Show()
}
App.getPolicy=function(username){
	url = App.rootpath + "api/getpolicy/user/<username>".replace("<username>", username);
	App.data.policy.data=[];
	url.LoadJson().policy.ForEach(function (policy, index) {
		App.data.policy.data.Add({"starttime":policy.starttime,"endtime":policy.endtime,"devindex":policy.devindex})
	})
}
App.cmdExplorer=function(){
    window.open(App.rootpath+'app/filetransfer/index.html','filetransfer')
}


