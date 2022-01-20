App.code.debug.frmNetwork.code=function(name,app){
    var self = this;Form.call(this, name);this.app = app;this.workparent=this.app.parent;this.parent = app.parent;this.Timer = null;
	this.controls={};this.submit=false;
    this.Form_Show=function(){
		self = this.app.Forms[this.Name];
        this.app.Forms.activeForm = this;
		this.app.wsc.SendMessage({"cmd":"stop detect face"})
		this.workparent.Html("<div class=\"content\"><div id=\"contentWork\" class=\"scrollbar\"></div></div>")
		this.parent=$$("#contentWork");
		result="/api/runtime/network".LoadJson();
		if(result){
			this.controls["share"]=this.parent.CreatesubElement().ID("share").BackColor("rgba(255,255,255,0.1)")//.Tmpl((App.path+"frmNetwork/dns.txt").LoadURL(),result);
			result.interfaces.sort().ForEach(function(adapter){
				if(adapter!="lo"){
					self.controls[adapter]=self.parent.CreatesubElement().ID(adapter);
					
					self.controls[adapter].Text(tmpl((self.app.path+"/frmNetwork/item.txt").LoadURL(),result.adapters[adapter]))
					.BackColor("rgba(255,255,255,0.5)").css("color","#0078a7").Position({"position": "absolute","left":30,"top":130,"height":30});
					rightItem=self.controls[adapter].Item().align("left").TD(2);rightItem.Text("▼");

					record=result.adapters[adapter]
					self.controls[adapter+"_list"]=self.parent.CreatesubElement().ID(adapter+"_list");
					self.controls[adapter+"_list"].BackColor("rgba(255,255,255,0.5)").Hide();
					if(record.iswireless) self.controls[adapter+"_list"].Tmpl((self.app.path+"/frmNetwork/wlan.txt").LoadURL(),(self.app.rootpath+"/api/runtime/network/"+adapter).LoadJson());
					else self.controls[adapter+"_list"].Tmpl(
						(self.app.path+"/frmNetwork/lan.txt").LoadURL(),
						(self.app.rootpath+"/api/runtime/network/"+adapter).LoadJson());

					self.controls[adapter].Click(function(){
						if(self.controls[this.id].Item().TD(2).Text()=="▼"){
							self.controls[this.id].Item().TD(2).Text("▲");
							self.controls[this.id+"_list"].Show();
						}else if(self.controls[this.id].Item().TD(2).Text()=="▲"){
							self.controls[this.id+"_list"].Hide();
							self.controls[this.id].Item().TD(2).Text("▼");
						}
						self.submit=true;self.Form_Resize();
					})

				}
			})
		}
		this.parent.CSS({"color":"#ffffff"})
		$$("#itemNetwork").css("background","rgba(0,0,0,0.9)");
        this.Form_Resize();
    };
    this.Form_Resize=function(w,h){
		if(w==null)w=this.parent.Width();
		if(h==null)h=this.parent.Height();
		var start=this.app.station.frmNetwork_starttop,height=50,listheight=150;
		for(key in this.controls){
			// console.log(key+":"+this.controls[key].css("display"))
			if(key.indexOf("_list")==-1){
				this.controls[key].Position({"position": "absolute","left":30,"top":start,"width":w-60,"height":height})
				start+=height+1
			}else if(this.controls[key].css("display")!="none"){
				this.controls[key].Position({"position": "absolute","left":30,"top":start,"width":w-60,"height":listheight})
				start+=listheight+1
			}
			
		}
	};
    this.Form_Receive = function (data) {
        console.log(this.Name + " receive:" + JSON.stringify(data))
    };
	this.BindNetwork=function(adapter){
		adapter=adapter.replace(":","_")
		console.log((App.rootpath+"/api/runtime/bindnetwork/"+adapter).LoadJson());
		window.location.reload();
	};
	this.OpenDHCP=function(adapter){
		$$("#"+adapter+"_list").FindElement("input").attr("disabled","true");
		$$("#"+adapter+"_list").FindElement("button").attr("disabled","true");
		$$("#"+adapter+"_list").FindElement("button").Index(0).attr("disabled","");
		$$("#"+adapter+"_list").FindElement("button").Index(1).attr("disabled","");

	}
	this.CloseDHCP=function(adapter){
		$$("#"+adapter+"_list").FindElement("input").attr("disabled","");
		$$("#"+adapter+"_list").FindElement("button").attr("disabled","");
		$$("#"+adapter+"_list").FindElement("button").Index(0).css("display","none");
		$$("#"+adapter+"_list").FindElement("button").Index(1).css("display","");
	};
	this.setDHCP=function(e){
		obj=$$(e);adapter=obj.attr("data-interface");
		if(obj.Text()=="关闭"){
			$$("#"+adapter+"_list").FindElement("input").attr("disabled","");
			$$("#"+adapter+"_list").FindElement("button").attr("disabled","");
			obj.Text("开启");
		}else if(obj.Text()=="开启"){
			$$("#"+adapter+"_list").FindElement("input").attr("disabled","true");
			$$("#"+adapter+"_list").FindElement("button").attr("disabled","true");
			$$("#"+adapter+"_list").FindElement("button").Index(0).attr("disabled","");
			obj.Text("关闭");
		}
	};
	this.Submit=function(adapter){
		ip=$$("#"+adapter+"_ipaddress").val(),netmask=$$("#"+adapter+"_netmask").val(),gw=$$("#"+adapter+"_gw").val();
		url=this.app.rootpath+"/api/runtime/network/"+adapter+"/"+ip+"/"+netmask+"/"+gw
		result=url.LoadJson()
		if(result.result){
			msgbox("修改成功，点击保存按钮保存配置文件",3);record=result.cfg;this.controls[adapter].Text(tmpl((this.app.path+"/frmNetwork/item.txt").LoadURL(),record)).Item().align("left");
		}else msgbox("修改失败，"+result.msg,3);
	};
	this.SaveNetworkConfig=function(){
		result=(this.app.rootpath+"/api/runtime/network/save").LoadJson();
		if(result.result)msgbox("保存成功，已生成网络配置文件",3);
	};
	this.Form_Receive = function (data) {
		console.log(this.Name + " receive:" + JSON.stringify(data))
	};
}