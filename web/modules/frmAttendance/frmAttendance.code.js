var self = this;Form.call(this,name);this.app = app; this.parent = app.parent; this.tabBody=null;
this.load=function(){self = this.app.Forms[this.Name];Document.LoadCSS(this.app.rootpath+"/css/gvsun.webui.css");this.tmpl = this.app.path + "/frmAttendance/frmAttendance.txt";this.dataurl = this.app.rootpath + this.app.api.attlog;};
this.Form_Show=function(){self.app.Forms.activeForm=this;console.log("wsc_receive:" + this.Name);tabTitle=this.parent.FindElement("table").Index(0);this.tabBody=new webui.Grid("tabBody").Parent($$("#divBody"));tabTitle.Cell(0,0).Width(50);tabTitle.Cell(0,1).Width(150);tabTitle.Cell(0,2).Width(150);tabTitle.Cell(0,3).Width(150);tabTitle.Cell(0,4).Width(260);this.ShowData();this.Form_Resize();};
this.ShowData=function(){data=this.binddata;if(data!=null){this.tabBody.binddata(["#","cname","username","cardnumber","datetime"],data.result,true).Resize();this.tabBody.FindElement(".row00").css("width","50px");this.tabBody.FindElement(".row01").css("width","149px");this.tabBody.FindElement(".row02").css("width","149px");this.tabBody.FindElement(".row03").css("width","148px");this.tabBody.FindElement(".row04").css("width","260px");}};
this.Form_Resize=function(w,h){this.tabBody.css("height",(this.parent.Height()-85)+"px")};
this.Form_Receive = function (data) {
    console.log(this.Name + " receive:" + JSON.stringify(data));
    if(data.type == "readcard_read" && data.status==false) {
        result = "".LoadJson(this.app.rootpath +  this.app.api.getcard + data.card);console.log(result);
        if(result.code == 200) {data = {};data.username = result.username;data.cname = result.cname;data.cardnumber = result.card;data.datetime = new Date().Format("yyyy-MM-dd hh:mm:ss");this.binddata.result.push(data);this.ShowData();
        } else if(result.code == 404) {
            Document.LoadJscript( this.app.rootpath +  this.app.Module.qrcode, function(url) {
                t = msgbox("卡号" + result.card + "查无此人", 30);
                url = "http://"+ self.app.cfg.release.device.ip+":"+ self.app.cfg.release.services.port+"/user/bindcard/" + result.card
                qrcode = new QRCode(document.getElementById("readcar_qrcode"), {width: 80,height: 80});qrcode.makeCode(url);
                url = "http://www.lubanlou.com/api/usercenter/share/addCardOrReplace?newCard=" + result.card
                qrcode = new QRCode(document.getElementById("readcar_qrcode1"), {width: 80,height: 80});qrcode.makeCode(url);
            });
        }
    }
};
