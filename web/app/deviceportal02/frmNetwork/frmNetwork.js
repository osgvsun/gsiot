App.frmNetwork = new Form("frmNetwork"); frmNetwork = App.frmNetwork;
App.frmNetwork.controls={}
App.frmNetwork.submit=false;
App.frmNetwork.Form_Resize=function(w,h){
	var start=100,height=50,listheight=150;
	for(key in App.frmNetwork.controls){
		// console.log(key+":"+App.frmNetwork.controls[key].css("display"))
		if(key.indexOf("_list")==-1){
			App.frmNetwork.controls[key].Position({"position": "absolute","left":30,"top":start,"width":w-60,"height":height})
			start+=height+1
		}else if(App.frmNetwork.controls[key].css("display")!="none"){
			App.frmNetwork.controls[key].Position({"position": "absolute","left":30,"top":start,"width":w-60,"height":listheight})
			start+=listheight+1
		}
		
	}
	// $$("#lan").Position({"position": "absolute","left":30,"top":100,"width":w-60,"height":50})
	// $$("#wlan").Position({"position": "absolute","left":30,"top":151,"width":w-60,"height":50})
}
App.frmNetwork.load = function () {App.frmNetwork.parent=App.controls.panWork;}
App.frmNetwork.Form_Show = function () {
	console.log("wsc_receive:" + this.Name);

	App.frm=App.frmNetwork;App.wsc.event_receive = App.frmNetwork.Form_Receive;
	App.frmNetwork.parent.Clear();result="/api/runtime/network".LoadJson();
	if(result){
		App.frmNetwork.controls["share"]=App.frmNetwork.parent.CreatesubElement().ID("share").BackColor("rgba(255,255,255,0.1)")//.Tmpl((App.path+"frmNetwork/dns.txt").LoadURL(),result);
		result.interfaces.sort().ForEach(function(adapter){
			if(adapter!="lo"){
				App.frmNetwork.controls[adapter]=App.frmNetwork.parent.CreatesubElement().ID(adapter);
				
				App.frmNetwork.controls[adapter].Text(tmpl((App.path+"frmNetwork/item.txt").LoadURL(),result.adapters[adapter]))
				.BackColor("rgba(255,255,255,0.1)").Position({"position": "absolute","left":30,"top":130,"height":30});
				rightItem=App.frmNetwork.controls[adapter].Item().align("left").TD(2);rightItem.Text("▼");
				
				console.log(App.frmNetwork.controls[adapter].hWnd)
				record=result.adapters[adapter]
				App.frmNetwork.controls[adapter+"_list"]=App.frmNetwork.parent.CreatesubElement().ID(adapter+"_list");
				App.frmNetwork.controls[adapter+"_list"].BackColor("rgba(255,255,255,0.1)").Hide();
				if(record.iswireless) App.frmNetwork.controls[adapter+"_list"].Tmpl((App.path+"frmNetwork/wlan.txt").LoadURL(),("/api/runtime/network/"+adapter).LoadJson());
				else App.frmNetwork.controls[adapter+"_list"].Tmpl((App.path+"frmNetwork/lan.txt").LoadURL(),("/api/runtime/network/"+adapter).LoadJson());

				App.frmNetwork.controls[adapter].Click(function(){
					if(App.frmNetwork.controls[this.id].Item().TD(2).Text()=="▼"){
						App.frmNetwork.controls[this.id].Item().TD(2).Text("▲");
						App.frmNetwork.controls[this.id+"_list"].Show();
					}else if(App.frmNetwork.controls[this.id].Item().TD(2).Text()=="▲"){
						App.frmNetwork.controls[this.id+"_list"].Hide();
						App.frmNetwork.controls[this.id].Item().TD(2).Text("▼");
					}
					App.frmNetwork.submit=true;App.frmNetwork.Form_Resize(App.controls.panWork.Width(),App.controls.panWork.Height());
				})

			}
		})
	}
	// .Text(JSON.stringify("/api/runtime/network/wlan0".LoadJson(),null,2))
	App.frmNetwork.parent.CSS({"color":"#ffffff"})
	// $$(".panLeftItem").css("background","rgba(0,0,0,0)");
	$$("#itemNetwork").css("background","rgba(0,0,0,0.9)");
	App.frmNetwork.Form_Resize(App.controls.panWork.Width(),App.controls.panWork.Height());

}
App.frmNetwork.Submit=function(adapter){
	ip=$$("#"+adapter+"_ipaddress").val(),netmask=$$("#"+adapter+"_netmask").val(),gw=$$("#"+adapter+"_gw").val();
	url=App.rootpath+"api/runtime/network/"+adapter+"/"+ip+"/"+netmask+"/"+gw
	result=url.LoadJson()
	if(result.result){
		msgbox("修改成功，点击保存按钮保存配置文件",3);record=result.cfg;App.frmNetwork.controls[adapter].Text(tmpl((App.path+"frmNetwork/item.txt").LoadURL(),record)).Item().align("left");
	}else msgbox("修改失败，"+result.msg,3);
}
App.frmNetwork.SaveNetworkConfig=function(){
	result=(App.rootpath+"api/runtime/network/save").LoadJson();
	if(result.result)msgbox("保存成功，已生成网络配置文件",3);
}
App.frmNetwork.Form_Receive = function (data) {
	console.log(this.Name + " receive:" + JSON.stringify(data))
}

