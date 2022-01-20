var self = this;Form.call(this, name);this.app = app; this.parent = app.parent;this.Timer = null;
this.load = function () {
    self = this.app.Forms[this.Name];
    this.tmpl = this.app.path + "/frmInspection/frmInspection.txt";
    Document.LoadJscript(self.app.rootpath+self.app.Module.jquery);
};
this.Form_Show=function(){
    self.app.Forms.activeForm = this;
    console.log("wsc_receive:"+this.Name);
    $$("#userhead").src(self.app.rootpath+self.app.img.userhead)
    e=document.getElementById("showpic")
    if(e==null)this.cmdLive_Click($$("#cmdLive").hWnd)
    //else {$$(e).src("http://"+this.app.cfg.release.device.ip+":"+this.app.cfg.server.webservice.uvccamera.port+"/"+this.app.cfg.server.webservice.uvccamera.streamer)}
    else {$$("#showpic").src("/mjpgstreamer/picamera")}
    this.Form_Resize(Document.Width(),Document.Height());
};
this.Form_Resize=function(w,h){};
this.Form_Receive = function (data) {
    console.log(this.Name + " receive:" + JSON.stringify(data))
    if(data.eventType=="broadcast"){
        result=data.result;
        if(result.type=="take picture"){
            value=$$("#filelist").Html();
            file="/data/inspection/"+result.courseid+"/"+result.experimentid+"/"+result.File;
            value+="<a href='javascript:void(0)' data-itemtype='image' data-imgUrl='"
            value+=file+"' onclick='App.Forms.activeForm.sub_camera_box_a_click(this);'"
            value+="  class='switch_camera_sub  sub_camera_select'>"
            value+="<img class='switch_camera_sub' src='"+file+"' /></a>";
            $$("#filelist").Html(value);
        }
    }
};
this.sub_camera_box_a_click=function(e){
    var recordtype=$$(e).attr("data-itemtype");
    $(e).addClass("sub_camera_select").siblings("a").removeClass("sub_camera_select");
    $(".on_live").removeClass("live_select");
    $$("#preview").Clear();
    if(recordtype=="image") node=$$("#preview").CreatesubElement("img").ID("showpic");
    else if(recordtype=="video") node=$$("#preview").CreatesubElement("video").ID("showvideo").attr("controls","controls");
    node.className("switch_camera_main").src($$(e).attr("data-imgUrl"))
}
this.OpenUsbCamera=function(){
    $$("#showpic").RemoveEvent("error",this);
    this.msgbox=new msgbox("加载usb摄像头视频失败，正在重启",10);
    result="".LoadURL(this.app.rootpath+this.app.api.openuvccamer);
    console.log(result)
    if(result.result){
        this.msgbox.Show("重新加载usb摄像头成功，请点击直播刷新界面");
        this.msgbox.setTime(5);
    }
};
this.start_countdown_videoTimer=function(a) {
    var d,h,m,s,leftTime,endTime=null;
    endTime= 600000;
    //设置截止时间
    var date = new Date();
    var start= date.getTime();console.log("截止时间："+start)
    var endDate = new Date(start + endTime);
    var end = endDate.getTime();
    
    this.Timer=window.setInterval(function(){
        //获取当前时间
        date = new Date();
        start= date.getTime();
        //获取截止时间和当前时间的时间差
        leftTime = end - start;
        // console.log(leftTime)            
        //判断剩余天数，时，分，秒
        if (leftTime >= 0) {
            d = Math.floor(leftTime / 1000 / 60 / 60 / 24).twoDigits();
            h = Math.floor(leftTime / 1000 / 60 / 60 % 24).twoDigits();
            m = Math.floor(leftTime / 1000 / 60 % 60).twoDigits();
            s = Math.floor(leftTime / 1000 % 60).twoDigits();
        }
        //判断时间
        //let showTime = `${d}天 ${h}时 ${m}分 ${s}秒`
        let showTime = `${h}:${m}:${s}`
        a.html("<b>"+showTime+"</b>")
        d = Number(d)
        h = Number(h)
        m = Number(m)
        s = Number(s)
        if (d === 0 && h === 0 && m === 0 && s === 0) {
            console.log("倒计时结束")
            a.html("<b>00:00:00</b>")
            $(".off_videotape").click()
        }
    }, 1000);   
};
this.cmdLive_Click=function(e){
    $$("#preview").Clear();
    img=$$("#preview").CreatesubElement("img").ID("showpic").className("switch_camera_main")
    // img.Error(this.OpenUsbCamera)
    url=(this.app.rootpath+this.app.api.uvccamer).LoadURL().replace("<host>",Document.Path().host)
    img.src(url)
    // new mjpgStreamerPlay(url,{"Parent":$$("#preview").hWnd,"Width":320,"Height":240,"IntervalTime":100}).start()
    $$(e).addClass("live_select");
    $$("#cmdQRCode").removeClass("live_select");
};
this.cmdStartMoive_Click=function(a){
    $$(a).hide();
    $(a).siblings(".off_videotape").css("display", "inline-block");
    $$(".videotape_control").show();
    $$(".pause_videotape").css("display", "inline-block");
    $$(".play_videotape").hide();
    $$(".videotape_ing").addClass("beat");
    this.start_countdown_videoTimer($$("#cameraTime"));
    this.app.wsc.SendMessage({
        "cmd":"start record moive",
        "courseid":"share",
        "experimentid":"01",
        "OperatorUserName":"20110032"
    });
};
this.cmdStopMoive_Click=function(e){
    window.clearInterval(this.Timer);
    this.Timer=null;
    $$(e).hide();
    $(e).siblings(".on_videotape").css("display", "inline-block");
    $$(".videotape_control").hide();
    this.app.wsc.SendMessage({
        "cmd":"end record moive",
        "courseid":"share",
        "experimentid":"01",
        "OperatorUserName":"20110032"
    },this,function(self, result){
        console.log(JSON.stringify(result))
        value=$$("#filelist").Html();
        file=result.url;//"/data/inspection/"+result.courseid+"/"+result.experimentid+"/"+result.File;
        value+="<a href='javascript:void(0)' data-itemtype='video' data-imgUrl='"
        value+=file+"' onclick='App.Forms.activeForm.sub_camera_box_a_click(this);'"
        value+="  class='switch_camera_sub  sub_camera_select'>"
        value+="<video class='switch_camera_sub' src='"+file+"' /></a>";
        $$("#filelist").Html(value);
    });
};
this.cmdStartNetworkMoive_Click=function(a){
    if(this.app.cfg.station.webcam!=""){
        $(a).hide();
        $(".off_networkvideotape").show();
        this.app.wsc.SendMessage({
            "cmd":"start network video record",
            "courseid":"share",
            "experimentid":"01",
            "OperatorUserName":"20110032"
        });
    }else{
        msgbox("没有配置网络摄像头",3)
    }
};
this.cmdStopNetworkMoive_Click=function(a){
    $(a).hide();
    $(".on_networkvideotape").show();
    this.app.wsc.SendMessage({
        "cmd":"end network video record",
        "courseid":"share",
        "experimentid":"01",
        "OperatorUserName":"20110032"
    },this,function(self, result){
        console.log(JSON.stringify(result))
    });
};
this.cmdtakePicture_Click=function(){
    url="/api/takepicture/<username>/<courseid>/<id>"
    .replace("<username>",this.app.policy.username)
    .replace("<courseid>",this.app.policy.courseid)
    .replace("<id>",this.app.policy.experimentid)
    console.log(url)
    console.log(url.LoadJson())
};
this.cmdQRCode_Click=function(e){
    $$(e).addClass("live_select");
    $$(".on_live").removeClass("live_select");
    $$("#preview").Clear();
    div=$$("#preview").CreatesubElement("div").ID("showwork")
    Document.LoadJscript(this.app.path+this.app.Module.qrcode,function(url){	
        url="http://"+this.app.cfg.release.device.ip+":"+this.app.cfg.release.services.port+this.app.rootpath+"showlibrary.html?courseid=share&experimentid=01";
        qrcode=new QRCode(div.hWnd, {width :300,height : 300}); 
        qrcode.makeCode(url); 
        font=div.CreatesubElement("p").CreatesubElement("font")
        font.attr("size",3);
        font.Text("请确保扫码设备和工位仪在同一局域网内时扫码")
    })
};
