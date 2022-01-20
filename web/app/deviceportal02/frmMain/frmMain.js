var App=new Form("frmMain");App.wsc=null;
App.controls={panLeftwidth:20};App.frm=null;
App.Form_Resize=function(w,h){
    if("panLeft" in App.controls) App.controls.panLeft.Position({position:"absolute",left: 0,height:h+10,width:App.controls.panLeftwidth});
    if("panWork" in App.controls) App.controls.panWork.Position({position:"absolute",left:App.controls.panLeftwidth,top:0,width:w-App.controls.panLeftwidth,height:h+10});   
    if(App.frm!=null)App.frm.Form_Resize(App.controls.panWork.Width(),App.controls.panWork.Height());
}
App.Form_Receive=function(data){ console.log(App.Name+" receive:"+JSON.stringify(data));}
App.load=function(){
    App.parent=new Element("#work");
    App.data=(App.path+"config.json").LoadJson();
    App.controls.panLeftwidth=App.data.config.panLeftwidth;
    App.data.cfg={
        ip:Document.Paths.server,
        port:8131,
        release:(App.rootpath+App.data.api.release).LoadJson(),
        station:(App.rootpath+App.data.api.station).LoadJson()
    };
	Document.LoadCSS(App.path+"frmMain/global.css");
    if(App.wsc==null){ App.wsc=new webSockObject(App.data.cfg.release.device.sn); 
        App.wsc.Connect(Document.Paths.server,App.data.cfg.port,App.websocket_Connect,App.websocket_DisConnect,App.Form_Receive); }
    else{ App.wsc.event_receive=App.Windows_Receive; } 
    if(App.data.cfg.station.debug){ Document.LoadJscript(App.rootpath+"script/vconsole.min.js",function(url){ App.vConsole = new VConsole(); })  }
    for(var key in App.data.tmpl){
        App.controls[key]=App.parent.CreatesubElement();
        for(var itemkey in App.data.tmpl[key]){
            if(itemkey!="Children")App.controls[key][itemkey](App.data.tmpl[key][itemkey])
        }
        if(key=="panLeft"){
            App.data.tmpl.panLeft.Children.list.ForEach(function(key){
                App.controls[key]=App.controls.panLeft.CreatesubElement().ID(key);
                item=App.controls[key]
                item.Text( App.data.tmpl.panLeft.Children[key].Text).Item().align("left").td.Index(2).Text("▶")
                for(var itemkey in App.data.tmpl.panLeft.Children[key]){
                    if(itemkey in item){
                        item[itemkey](App.data.tmpl.panLeft.Children[key][itemkey]);item.Width(App.controls.panLeftwidth);
                        frmKey=App.data.tmpl.panLeft.Children[key].bindfrm;
                        url=App.path+App.data.Module[frmKey];
                        Document.LoadJscript(url);
                        item.className("panLeftItem").attr("onclick","App.panLeft_Click(this.id)")                        
                    }
                }    
            })
        }else if(key=="panWork"){
            App.controls.panWork.css("overflow","auto")
        }
    }
}
App.panLeft_Click=function(e){
    for(key in App.controls){
        if(key.indexOf("item")!=-1){
           App.controls[key].Item().td.Index(0).attr("bgcolor","")
           App.controls[key].css("background","rgba(0,0,0,0)");
        }
    }
    $$("#"+e).css("background","rgba(0,0,0,0.9)");
    App.controls[e].Item().td.Index(0).attr("bgcolor","green")
    App[e.replace("item","frm")].Show()
}
App.Form_Show=function(){App.Form_Resize(Document.Width(),Document.Height());}
App.websocket_Connect=function(){ App.wsc.isOpen=true; console.log("websocket connected"); 
App.wsc.SendMessage({'cmd':'websocket.test'},this,function(self, result){ self.id=result.clientid; console.log("websocket.test.return:"+result.clientid); }); }
App.websocket_DisConnect=function(){App.wsc.isOpen=false;console.log("websocket closed");}
