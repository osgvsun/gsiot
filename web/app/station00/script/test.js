var frmLogin=new Application("frmLogin")
frmLogin.load=function(){
    App.frm=frmLogin;
    frmLogin.parent=new Element("panwork");
    // frmLogin.tmpl="".LoadURL(App.data.api.case).replace("<uvccamera>","".LoadURL(App.data.api.uvccamer).replace("<host>", App.data.cfg.ip)).replace("<host>",App.data.cfg.ip)
    // frmLogin.Show();
    // $ID("showpic").Error(frmLogin.OpenUsbCamera)
    App.wsc.event_receive=App.frm.Windows_Receive
}
frmLogin.Windows_Receive=function(data){
    console.log(frmLogin.Name+" receive:"+JSON.stringify(data))
}
var frmAttendance=new Application("frmAttendance")
frmAttendance.load=function(){
    App.frm=frmAttendance;
    frmAttendance.parent=new Element("panwork");
    // frmAttendance.tmpl="".LoadURL(App.data.api.case).replace("<uvccamera>","".LoadURL(App.data.api.uvccamer).replace("<host>", App.data.cfg.ip)).replace("<host>",App.data.cfg.ip)
    // frmAttendance.Show();
    // $ID("showpic").Error(frmAttendance.OpenUsbCamera)
    App.wsc.event_receive=App.frm.Windows_Receive
}
frmAttendance.Windows_Receive=function(data){
    console.log(frmAttendance.Name+" receive:"+JSON.stringify(data))
}
var frmWork=new Application("frmWork")
frmWork.load=function(){
    App.frm=frmWork;
    frmWork.parent=new Element("panwork");
    frmWork.tmpl="".LoadURL(App.data.api.case).replace("<uvccamera>","".LoadURL(App.data.api.uvccamer).replace("<host>", App.data.cfg.ip)).replace("<host>",App.data.cfg.ip)
    frmWork.Show();
    $("#showpic").Error(frmWork.OpenUsbCamera)
    App.wsc.event_receive=App.frm.Windows_Receive
}
frmWork.Windows_Receive=function(data){
    console.log(frmWork.Name+" receive:"+JSON.stringify(data))
}
frmWork.OpenUsbCamera=function(){
    $ID("showpic").RemoveEvent("error",this);
    frmWork.msgbox=new msgbox("加载usb摄像头视频失败，正在重启");
    result="".LoadURL(App.data.api.openuvccamer);
    if(JSON.parse(result).result){
        frmWork.msgbox.Show("重新加载usb摄像头成功，请点击直播刷新界面");
        frmWork.msgbox.setTime(5);
    }
}
frmWork.onVideotape=function(a) {
    $(a).hide();
    $(a).siblings(".off_videotape").css("display", "inline-block");
    $(".videotape_control").show();
    $(".pause_videotape").css("display", "inline-block");
    $(".play_videotape").hide();
    $(".videotape_ing").addClass("beat");
    // 计时
    frmWork.start_countdown_videoTimer(a);
}
frmWork.offVideotape=function(a) {
    window.clearInterval(Timer);
    Timer=null;
    $(a).hide();
    $(a).siblings(".on_videotape").css("display", "inline-block");
    $(".videotape_control").hide();
}
frmWork.start_countdown_videoTimer=function(a) {
    endTime= 600000;
    //设置截止时间
    var date = new Date();
    var start= date.getTime();
    var endDate = new Date(start + endTime);
    var end = endDate.getTime();
    // if(Timer==null){
        Timer=window.setInterval(function(){
            //获取当前时间
            date = new Date();
            start= date.getTime();
            //获取截止时间和当前时间的时间差
            var leftTime = end - start;
            // console.log(leftTime)            
            //判断剩余天数，时，分，秒
            if (leftTime >= 0) {
                d = Math.floor(leftTime / 1000 / 60 / 60 / 24);
                h = Math.floor(leftTime / 1000 / 60 / 60 % 24);
                m = Math.floor(leftTime / 1000 / 60 % 60);
                s = Math.floor(leftTime / 1000 % 60);
            }
            d = twoDigits(d)
            h = twoDigits(h)
            m = twoDigits(m)
            s = twoDigits(s)
            //判断时间
            //let showTime = `${d}天 ${h}时 ${m}分 ${s}秒`
            let showTime = `${h}:${m}:${s}`
            $("#cameraTime").html("<b>"+showTime+"</b>")
            d = Number(d)
            h = Number(h)
            m = Number(m)
            s = Number(s)
            if (d === 0 && h === 0 && m === 0 && s === 0) {
                console.log("倒计时结束")
                $("#cameraTime").html("<b>00:00:00</b>")
                $(".off_videotape").click()
            }
        }, 1000); 
    // }    
}
frmWork.onNetworkVideo=function(a) {
    $(a).hide();
    $(".off_networkvideotape").show();
    frmWork.cmdStartNetworkMoive_Click()
}
frmWork.offNetworkVideo=function(a) {
    $(a).hide();
    $(".on_networkvideotape").show();
    frmWork.cmdStopNetworkMoive_Click()
}
frmWork.cmdStartMoive_Click=function(){}
frmWork.cmdStopMoive_Click=function(){}
frmWork.cmdStartNetworkMoive_Click=function(){}
frmWork.cmdStopNetworkMoive_Click=function(){}
frmWork.cmdtakePicture_Click=function(){}
var frmOrder=new Application("frmOrder")
frmOrder.load=function(){
    App.frm=frmOrder;
    frmOrder.parent=new Element("panwork");
    frmOrder.Url="http://"+App.data.cfg.release.device.ip+":"+App.data.cfg.release.services.port+App.rootpath+"api/order/"+new Date().Format("yyyy-MM-dd hh:mm:ss").base64encode()
    Document.LoadJscript(App.data.api.qrcode,function(url){
        frmOrder.tmpl="".LoadURL(App.data.api.tmplorder);frmOrder.Show();
        qrcode=new QRCode(document.getElementById("qrcode"), {width :180,height : 180});
        qrcode.makeCode(frmOrder.Url);
    })
    App.wsc.event_receive=App.frm.Windows_Receive
}
frmOrder.Windows_Receive=function(data){
    console.log(frmOrder.Name+" receive:"+JSON.stringify(data))
    if(data.cmd=="show library id"){
        frmWork.data=data.result;
        frmWork.Windows_Load();
    }
}
var App=new Application()
App.wsc=null;
App.Windows_Receive=function(data){
    console.log(App.Name+" receive:"+JSON.stringify(data))
    if(data.type=="sensor_dht11"){
        $ID("humidity").Html(data.result.humidity);
        $ID("temperature").Html(data.result.temperature);
    }
}
App.load=function(){
    App.frm=App;
    App.data.api={
        "showlibrary":App.rootpath+"api/record/showlibrary/today",
        "release":App.rootpath+"api/config/release.json",
        "station":App.rootpath+"api/config/station.json",
        "list":App.path+"/tmpl/"+App.Name+"/list.txt",
        "tmpl":App.path+"/tmpl/"+App.Name+"/frmdesktop.txt",
        "tmplorder":App.path+"/tmpl/"+App.Name+"/order.txt",
        "qrcode":App.path+"/script/qrcode.js",
        "case":App.path+"/tmpl/"+App.Name+"/case.txt",
        "uvccamer":App.rootpath+"api/device/uvccamera/url",
        "openuvccamer":App.rootpath+"api/openuvccamer"
    };
     App.data.cfg={
        sn:"",
        isface:"",
        ip:Document.Path().host,
        port:8131,
        release:Document.LoadJson(App.data.api.release),
        station:Document.LoadJson(App.data.api.station)
    };
    Document.LoadCSS(App.path+"/css/global.css")
    App.tmpl="".LoadURL(App.data.api.tmpl)
    App.Show();
    if(App.wsc==null){
        App.wsc=new webSockObject(App.data.cfg.release.device.sn)
        App.wsc.Connect(App.data.cfg.ip,App.data.cfg.port,App.websocket_Connect,App.websocket_DisConnect,App.frm.Windows_Receive)
    }else{
        App.wsc.event_receive=App.frm.Windows_Receive
    }
    
}
App.websocket_Connect=function(){
    App.wsc.isOpen=true;
    console.log("websocket connected");
    App.wsc.SendMessage({'cmd':'websocket.test'},this,function(self, result){
        self.id=result.clientid;
        console.log("websocket.test.return:"+result.clientid);
    });
}
App.websocket_DisConnect=function(){App.wsc.isOpen=false;console.log("websocket closed");}
App.cmdView_Click=function(){
    data=JSON.parse("".LoadURL(App.data.api.showlibrary))
    data.PublicServation=App.data.cfg.station.PublicServation;
    strtmpl="".LoadURL(App.data.api.list);
    
    $ID("panwork").Html(tmpl(strtmpl,data));
}
App.cmdOrder_Click=function(){frmOrder.Windows_Load();}
App.cmdAttendance_Click=function(){

}
App.cmdRemoteAccess_Click=function(){

}
App.cmdInspection_Click=function(CourseID,ExperimentID,start,end){
    const now=new Date().Format("yyyy-MM-dd hh:mm:ss")
	console.log("starttime:"+start)
	console.log("endtime:"+end)	
	console.log("now:"+now)
	console.log("datetime:"+(start<now && now<end))
}
