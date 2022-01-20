var App=new Form("frmMain");App.wsc=null;
App.controls={panLeftwidth:20};App.frm=null;
App.Form_Resize=function(w,h){
    App.controls.panLeftwidth=w/2
    if("panLeft" in App.controls) {
        App.controls.panLeft.Position({position:"absolute",left: 0,height:h+10,width:App.controls.panLeftwidth});
        App.controls.panLeft.Children(0).css("height","50px")
        App.controls.panLeft.Children(1).css({"height":(h-50)+"px","overflow":"auto"})
    }
    if("panWork" in App.controls) {
        App.controls.panWork.Position({position:"absolute",left:App.controls.panLeftwidth,top:0,width:w-App.controls.panLeftwidth,height:h+10});   
        App.controls.panWork.Children(0).css("height","50px")
        App.controls.panWork.Children(1).css({"height":(h-50)+"px","overflow":"auto"})
    }
}
App.Form_Receive=function(data){ console.log(App.Name+" receive:"+JSON.stringify(data));}
App.load=function(){
    App.parent=new Element("#work");
    // Document.LoadCSS(App.path+"frmMain/global.css");
    Document.LoadCSS(App.rootpath+"css/gvsun.webui.css");
    App.data=(App.path+"config.json").LoadJson();
    App.controls.panLeftwidth=App.data.config.panLeftwidth;
    App.data.cfg={
        ip:Document.Path().host,
        port:8131,
        release:(App.rootpath+App.data.api.release).LoadJson(),
        station:(App.rootpath+App.data.api.station).LoadJson()
    };
	if(App.wsc==null){ App.wsc=new webSockObject(App.data.cfg.release.device.sn); App.wsc.Connect(App.data.cfg.release.device.ip,App.data.cfg.port,App.websocket_Connect,App.websocket_DisConnect,App.Form_Receive);}else{ App.wsc.event_receive=App.Windows_Receive; } 
    if(App.data.cfg.station.debug){ Document.LoadJscript(App.rootpath+"script/vconsole.min.js",function(url){ App.vConsole = new VConsole(); })  }
    for(var key in App.data.tmpl){App.controls[key]=App.parent.CreatesubElement();for(var itemkey in App.data.tmpl[key]){App.controls[key][itemkey](App.data.tmpl[key][itemkey])}}
    App.controls.panLeft.Tmpl("/app/filetransfer/frmMain/list.txt".LoadURL())
    App.controls.panWork.Tmpl("/app/filetransfer/frmMain/list.txt".LoadURL())
}
App.Form_Show=function(){App.Form_Resize(Document.Width(),Document.Height());}
App.websocket_Connect=function(){ App.wsc.isOpen=true; console.log("websocket connected"); 
App.wsc.SendMessage({'cmd':'websocket.test'},this,function(self, result){ self.id=result.clientid; console.log("websocket.test.return:"+result.clientid); }); }
App.websocket_DisConnect=function(){App.wsc.isOpen=false;console.log("websocket closed");}
