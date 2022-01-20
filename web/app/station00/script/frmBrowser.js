App.frmBrowser=new Form("frmBrowser");frmBrowser=App.frmBrowser;
App.frmBrowser.load=function(){
    App.frm=frmBrowser;
    frmBrowser.parent=new Element("panwork");
    App.wsc.event_receive=App.frmBrowser.Form_Receive;
    frmBrowser.cfg = Document.LoadJson(App.data.api.showlibrary);
	frmBrowser.cfg.PublicServation = App.data.cfg.station.PublicServation;
    frmBrowser.tmpl="".LoadURL(App.data.tmpl.frmBrowser);    
}
App.frmBrowser.Form_Receive=function(data){
    console.log(frmOrder.Name+" receive:"+JSON.stringify(data))
    if(data.cmd=="show library id"){
        frmWork.data=data.result;
        frmWork.Form_Load();
    }
}
App.frmBrowser.cmdInspection_Click=function(CourseID,ExperimentID,start,end){
    const now=new Date().Format("yyyy-MM-dd hh:mm:ss")
	console.log("starttime:"+start)
	console.log("endtime:"+end)	
	console.log("now:"+now)
	console.log("datetime:"+(start<now && now<end))
}