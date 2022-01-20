var App=new Form("frmMain")
App.wsc=null;
App.Form_Receive=function(data){ console.log(App.Name+" receive:"+JSON.stringify(data)); if(data.type=="sensor_dht11"){ $$("#humidity").Html(data.result.humidity); $$("#temperature").Html(data.result.temperature); } }
App.load=function(){
    App.frm=App;
    App.data.tmpl={
    	"frmMain":App.path+"/tmpl/"+App.tmplName+"/frmdesktop.txt",
    	"frmBrowser":App.path+"/tmpl/"+App.tmplName+"/frmbrowser.txt",
		"frmAttendance":App.path+"/tmpl/"+App.tmplName+"/frmAttendance.txt",
		"frmWork":App.path+"/tmpl/"+App.tmplName+"/case.txt",
		"frmOrder":App.path+"/tmpl/"+App.tmplName+"/order.txt"
    }
    App.data.api={
        "showlibrary":App.rootpath+"api/record/showlibrary/today",
        "release":App.rootpath+"api/config/release.json",
        "station":App.rootpath+"api/config/station.json",
        "list":App.path+"/tmpl/"+App.tmplName+"/list.txt",
        "attlog":"/api/log/attlog.txt",
        "uvccamer":App.rootpath+"api/device/uvccamera/url",
        "openuvccamer":App.rootpath+"api/openuvccamer"
    };
    App.data.Module={
    	"qrcode":App.path+"/script/qrcode.js",
    	"frmAttendanceURL":App.path+"/script/frmAttendance.js",
    	"frmBrowserURL":App.path+"/script/frmBrowser.js",
    	"frmOrderURL":App.path+"/script/frmOrder.js",
    	"frmWorkURL":App.path+"/script/frmWork.js"
    };
    App.data.cfg={
        sn:"",
        isface:"",
        ip:Document.Path().host,
        port:8131,
        release:App.data.api.release.LoadURL(),
        station:App.data.api.station.LoadURL()
    };
    Document.LoadCSS(App.path+"/css/global.css"); 
    Document.LoadJscript(App.data.Module.frmWorkURL);
    App.tmpl="".LoadURL(App.data.tmpl.frmMain); 
    if(App.wsc==null){ App.wsc=new webSockObject(App.data.cfg.release.device.sn); App.wsc.Connect(App.data.cfg.release.device.ip,App.data.cfg.port,App.websocket_Connect,App.websocket_DisConnect,App.frm.Form_Receive); }else{ App.wsc.event_receive=App.frm.Windows_Receive; } if(App.data.cfg.station.debug){ Document.LoadJscript(App.rootpath+"script/vconsole.min.js",function(url){ App.vConsole = new VConsole(); })  }
}
App.websocket_Connect=function(){ App.wsc.isOpen=true; console.log("websocket connected"); App.wsc.SendMessage({'cmd':'websocket.test'},this,function(self, result){ self.id=result.clientid; console.log("websocket.test.return:"+result.clientid); }); }
App.websocket_DisConnect=function(){App.wsc.isOpen=false;console.log("websocket closed");}
//App.cmdView_Click = function() { App.Show(); data = Document.LoadJson(App.data.api.showlibrary); data.PublicServation = App.data.cfg.station.PublicServation; strtmpl = "".LoadURL(App.data.api.list); $$("#panwork").Html(tmpl(strtmpl, data)); };
App.cmdView_Click = function() {
	App.Show();
	if(isLoadJS(App.data.Module.frmBrowserURL)==false){
		Document.LoadJscript(App.data.Module.frmBrowserURL,function(url) {
			App.frmBrowser.Show();
		});
	}else App.frmBrowser.Show();
}
App.cmdOrder_Click=function(){ if(isLoadJS(App.data.Module.frmOrderURL)==false){ Document.LoadJscript(App.data.Module.frmOrderURL,function(url) { App.frmOrder.Show(); }); }else App.frmOrder.Show();}
App.cmdAttendance_Click=function(){ if(isLoadJS(App.data.Module.frmdAttendanceURL)==false){ Document.LoadJscript(App.data.ModulefrmdAttendanceURL,function(url) { App.frmAttendance.Show(); }); }else App.frmAttendance.Show(); }
App.cmdRemoteAccess_Click=function(){}
