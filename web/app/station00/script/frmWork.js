App.frmWork=new Form("frmWork");var frmWork=App.frmWork;
App.frmWork.load=function(){
    App.frm=frmWork;
    frmWork.parent=new Element("panwork");
    frmWork.tmpl="".LoadURL(App.data.tmpl.frmWork)
    frmWork.tmpl=frmWork.tmpl.replace("<uvccamera>","".LoadURL(App.data.api.uvccamer).replace("<host>", App.data.cfg.ip)).replace("<host>",App.data.cfg.ip)
    $$("#showpic").Error(frmWork.OpenUsbCamera)
    App.wsc.event_receive=frmWork.Form_Receive
}
App.frmWork.Form_Receive=function(data){
    console.log(frmWork.Name+" receive:"+JSON.stringify(data))
}
App.frmWork.OpenUsbCamera=function(){
    $ID("showpic").RemoveEvent("error",this);
    frmWork.msgbox=new msgbox("加载usb摄像头视频失败，正在重启");
    result="".LoadURL(App.data.api.openuvccamer);
    if(JSON.parse(result).result){
        frmWork.msgbox.Show("重新加载usb摄像头成功，请点击直播刷新界面");
        frmWork.msgbox.setTime(5);
    }
}
App.frmWork.onVideotape=function(a) {
    $(a).hide();
    $(a).siblings(".off_videotape").css("display", "inline-block");
    $(".videotape_control").show();
    $(".pause_videotape").css("display", "inline-block");
    $(".play_videotape").hide();
    $(".videotape_ing").addClass("beat");
    // 计时
    frmWork.start_countdown_videoTimer(a);
}
App.frmWork.offVideotape=function(a) {
    window.clearInterval(Timer);
    Timer=null;
    $(a).hide();
    $(a).siblings(".on_videotape").css("display", "inline-block");
    $(".videotape_control").hide();
}
App.frmWork.start_countdown_videoTimer=function(a) {
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
App.frmWork.onNetworkVideo=function(a) {
    $(a).hide();
    $(".off_networkvideotape").show();
    frmWork.cmdStartNetworkMoive_Click()
}
App.frmWork.offNetworkVideo=function(a) {
    $(a).hide();
    $(".on_networkvideotape").show();
    frmWork.cmdStopNetworkMoive_Click()
}
App.frmWork.cmdStartMoive_Click=function(){}
App.frmWork.cmdStopMoive_Click=function(){}
App.frmWork.cmdStartNetworkMoive_Click=function(){}
App.frmWork.cmdStopNetworkMoive_Click=function(){}
App.frmWork.cmdtakePicture_Click=function(){}