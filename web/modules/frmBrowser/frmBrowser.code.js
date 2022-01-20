var self = this;Form.call(this, name);this.app = app; this.parent = app.parent;this.Timer = null;
this.data=null;this.tmpldata=null;this.tmpldata=null;
this.load = function () {
    self = this.app.Forms[this.Name];
    this.tmpl = this.app.path + "/frmBrowser/frmBrowser.txt";
    this.PublicServation = this.app.station.PublicServation;
    this.dataurl = this.app.rootpath + this.app.api.showlibrary;
    if (this.PublicServation) {
        file = new JsonFile(this.app.rootpath + this.app.api.share_record)
        var now = new Date().Format("yyyy-MM-dd hh:mm:ss")
        if (file.isEmpty || file.data.InspectionRecord[0].datetime.endtime < now) {
            console.log(this.app.api.makeshare.LoadJson());
            file.Readfile();
        }
    }
};
this.Show=function(){
    this.app.Forms.activeForm = this;
    this.app.wsc.SendMessage({"cmd":"stop detect face"})
    if(this.isload==false){this.load();this.isload=true;};
    if(this.tmpl!=null){
        if(this.tmpldata==null)this.tmpldata=this.tmpl.LoadURL();
        if(this.data==null && this.dataurl!=null)this.data=this.dataurl.LoadJson();
        if(this.data==null)this.data=this;
        else{data=[];this.data.result.ForEach(function(item,index){if(item.InspectionRecord.length!=0)data.Add(item);});this.data.result=data;};
        this.parent.Tmpl(this.tmpldata,this.data);
    };
    if (this.Timer==null) {this.Timer=setInterval(this.task,60000);};
};
this.Form_Resize = function (w, h) { };
this.Form_Receive = function (data) {
    console.log(this.Name + " receive:" + JSON.stringify(data))
    if (data.cmd == "show library id") {this.data=this.dataurl.LoadJson();this.Show();
    } else if (data.type == "event_auth") {
        if (data.code = 200) {
            this.app.cfg.policy.username = data.data.username;
            this.app.cfg.policy.cname = data.data.cname;
        }
    }
};
this.task=function(){
    var flag=false;
    if(self.data!=null){
        self.data.result.ForEach(
            function(item,index){if(item!=null){
                item.InspectionRecord.ForEach(
                    function(record){
                        record.datetime.now=new Date().Format("yyyy-MM-dd hh:mm:ss");
                        if(record.datetime.endtime<record.datetime.now) flag=true;
                    })};return !flag;})};
    if(self.app.Forms.activeForm.Name==self.Name){
        if(flag){console.log("刷新页面："+new Date().Format("hh:mm:ss"));self.data=null;self.Show();}
    }else if(self.Timer!=null){window.clearInterval(self.Timer);self.Timer=null;}

};
this.cmdInspection_Click = function (CourseID, ExperimentID, starttime, endtime) {
    if (CourseID == null || CourseID == "share") {
        file = new JsonFile(this.app.rootpath + this.app.api.share_record)
        with (this.app.policy) { 
            courseid = "share"; 
            experimentid = "01"; 
            start=new Date().Format("yyyy-MM-dd")+" 00:00:00";
            end=new Date().Format("yyyy-MM-dd")+" 23:59:59";
            InspectionRecord = file.data.InspectionRecord[0] }
        if(this.app.Forms.frmInspection!=null)this.app.Forms.frmInspection.Show();
    } else {
        console.log("policy:" + JSON.stringify(self.app.policy))
        var now = new Date().Format("yyyy-MM-dd hh:mm:ss");
        console.log(now);console.log(starttime < now);console.log(now < endtime);
        if (starttime < now && now < endtime) {
            if (this.app.policy.username == "") {
                with (this.app.policy) { 
                    courseid = CourseID; 
                    experimentid = ExperimentID; 
                    start = starttime; end = endtime; }
                if(this.app.Forms.frmLogin!=null)this.app.Forms.frmLogin.Show();
            } else this.CheckPolicy();
        } else if (starttime > now) {
            msgbox("预约时间为\n" + starttime + "\n至\n" + endtime + "\n,该预约没有开始", 3)
        } else if (endtime < now) {
            msgbox("预约时间为\n" + starttime + "\n至\n" + endtime + "\n,预约已结束", 3)
        }
    }
};
this.CheckPolicy = function () {
    var start = this.app.policy.start,
        end = this.app.policy.end,
        devindex = this.app.cfg.release.device.id + "_"
            + this.app.policy.courseid + "_"
            + this.app.policy.experimentid;

    this.app.policy.data.ForEach(function (policy, index) {
        if (policy.devindex == App.cfg.release.device.id || policy.devindex == devindex) {
            url = self.app.rootpath + "/api/showlibraryid/<username>/<course>/<experiment>"
                .replace("<username>", self.app.policy.username)
                .replace("<course>", self.app.policy.courseid)
                .replace("<experiment>", self.app.policy.experimentid)
            result = url.LoadJson();
            if(result.code==200){
                self.app.policy.InspectionRecord=result.InspectionRecord;
                if(self.app.Forms.frmInspection!=null)self.app.Forms.frmInspection.Show();
            }
        } else { console.log(policy.devindex); }
    })
};