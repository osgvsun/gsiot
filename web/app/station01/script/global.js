/*连接*/
$(".link_btn").click(
    function () {
        $(".shade_box").fadeIn();
        $(".outside_box_limit").addClass("blur");
        $(this).parents(".info_line").addClass("link");
        $(this).parents(".info_line").siblings(".info_line").removeClass("link");
        $(this).siblings(".break_btn").show();
    }
);
$(".break_btn").click(
    function () {
        $(this).parents(".info_line").removeClass("link");
        $(this).hide();
        $(this).siblings(".link_btn").show();
    }
);
$(".fill_close").click(
    function () {
        $(".shade_box").fadeOut();
        $(".outside_box_limit").removeClass("blur");
    }
);
$(".fill_footer input").click(
    function () {
        $(".shade_box").fadeOut();
        $(".outside_box_limit").removeClass("blur");
    }
);
//开启摄像头
function onCamera(a) {
    $(a).hide();
    $(a).siblings(".off_camera").css("display", "inline-block");
}
//关闭摄像头
function offCamera(a) {
    $(a).hide();
    $(a).siblings(".on_camera").css("display", "inline-block");
}
//开始录像
function onVideotape(a) {
    $(a).hide();
    $(a).siblings(".off_videotape").css("display", "inline-block");
    $(".videotape_control").show();
    $(".pause_videotape").css("display", "inline-block");
    $(".play_videotape").hide();
    $(".videotape_ing").addClass("beat");
    // 计时
    start_countdown_videoTimer(a);
}
function twoDigits(num) {
    if (`${num}`.toString().length === 1) {
        return `0${num}`
    }
    return num;
}
//定义变量 d,h,m,s分别保存天数，小时，分钟，秒
var d, h, m, s,endTime,Timer=null;
var hours = 0;
var mins = 0;
var seconds = 0;
var showDate = 0;
//开始录像计时
function start_videoTimer(a) {
    $("#cameraTime").html("0秒")
    Timer = setInterval(function () {
        showDate = ""
        seconds += 1;
        if (seconds >= 60) {
            seconds = 0;
            mins += 1;
            if (mins >= 60) {
                mins = 0;
                hours += 1;
                if (hours >= 24) {
                    clearInterval(timer)
                    alert("已录像24小时！")
                }
            }
        }
        if (hours != 0) {
            showDate += hours + "时 "
        }
        if (mins != 0) {
            showDate += mins + "分 "
        }
        if (seconds != 0) {
            showDate += seconds + "秒 "
        }
        $("#cameraTime").html(showDate)
    }, 1000);
}
//开始倒计时录像
function start_countdown_videoTimer(a) {
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
//停止录像
function offVideotape(a) {
    // if(Timer!=null){
        window.clearInterval(Timer);
        Timer=null;
    // }
    $(a).hide();
    $(a).siblings(".on_videotape").css("display", "inline-block");
    $(".videotape_control").hide();
}
function onNetworkVideo(a) {
    $(a).hide();
    $(".off_networkvideotape").show();
}
function offNetworkVideo(a) {
    $(a).hide();
    $(".on_networkvideotape").show();
}
//录像暂停
$(".pause_videotape").click(
    function () {
        $(this).hide();
        $(this).siblings(".play_videotape").css("display", "inline-block");
        $(".videotape_ing").removeClass("beat");
    }
);
//录像重新开始
$(".play_videotape").click(
    function () {
        $(this).hide();
        $(this).siblings(".pause_videotape").css("display", "inline-block");
        $(".videotape_ing").addClass("beat");
    }
);
//底部小图切换主摄像头
function sub_camera_box_a_click(_this) {
    var img = $(_this).attr("data-imgUrl");
    $("#showpic").css('display', 'inline-block');
    $("#showvideo").css('display', 'none');
    $("#showpic").attr({
        src: img
    });
    $(_this).addClass("sub_camera_select").siblings("a").removeClass("sub_camera_select");
    $(".on_live").removeClass("live_select");
    return false;
}
//底部小图切换主摄像头
function sub_camera_video_a_click(_this) {
    var img = $(_this).attr("data-imgUrl");
    $("#showpic").css('display', 'none');
    $("#showvideo").css('display', 'inline-block');
    $("#showvideo").attr({ src: img });
    $(_this).addClass("sub_camera_select").siblings("a").removeClass("sub_camera_select");
    $(".on_live").removeClass("live_select");
    return false;
}
