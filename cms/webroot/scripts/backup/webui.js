var System = new function() {
	var idnumber = 0,
		objidnumber = 0;
	this.Width = function() {
		if(window.innerWidth) return window.innerWidth - 2;
		else if((document.body) && (document.body.clientWidth)) return document.body.clientWidth;
	};
	this.Height = function() {
		if(window.innerHeight) return window.innerHeight - 2;
		else if((document.body) && (document.body.clientHeight)) return document.body.clientHeight;
	};
	this.AddEvent = function(objElement, ename, lpfn) {
		if(objElement.addEventListener) {
			objElement.addEventListener(ename, lpfn, true);
		} else if(objElement.attachEvent) {
			objElement.attachEvent("on" + ename, lpfn, true);
		}
	};
	this.RemoveEvent = function(objElement, ename, lpfn) {
		if(objElement.removeEventListener) {
			objElement.removeEventListener(ename, lpfn);
		} else if(objElement.detachEvent) {
			objElement.detachEvent("on" + ename, lpfn);
		}
	};
	this.OnReady = function() { try {Window_Load(); window_resize(); }catch (err) {}};
	this.OnResize = function(value) {if (value != null) {this.AddEvent(window, "resize", value)}};
	this.getid = function() { idnumber++; return "gvsun_client_" + idnumber; };
	this.getobjid = function() { objidnumber++; return objidnumber; };
	this.path = function() {
		var ret = new edict(),
			url = window.location.href.replace("http://", "").replace("file:///", "").split("/"),
			host = url[0],
			find = url[0].indexOf(":");
		if(find > 0) {
			ret.host = url[0].substr(0, find);
			ret.port = url[0].substr(find + 1);
		} else {
			ret.host = url[0];
			ret.port = 80;
		};
		var f = url.pop();
		if(f.indexOf("?") != -1) {
			ret.file = f.split("?")[0];
			if(f.split("?")[1].indexOf("&") != -1) {
				ret.option = new edict();
				f.split("?")[1].split("&").ForEach(function(e) {
					eval("ret.option." + e);
				})
			}
		} else {
			ret.file = f;
		};
		url.shift();
		ret.path = "/" + url.join("/");
		return ret;
	}
}
function Application(name,parent,stmpl,load,receive,resize){
	var self=this;this.isshow=false;this.Form_Show=null;this.isload=false;this.Name=name;this.frm=this;this.parent=parent;this.tmpl=stmpl;this.data={};this.load=load;this.receive=receive;this.resize=resize;
    this.Show = function() {
    	if(this.isload == false) {
    		this.load()
    	}
    	if(this.isshow==false){
	    	if(this.tmpl != null && this.parent != null) {
	    		this.parent.Html(tmpl(this.tmpl, this));
	    	}
	    	if(this.Form_Show!=null)this.Form_Show();
    	}
    	this.isshow=false;
    	console.log(this.Name + "刷新完成");
    }
    this.Window_Load = function() { if(this.load != null) this.load(); this.isload == true; }
    this.Window_Resize=function(w,h){if(this.resize!=null)this.resize(w,h)}
    this.Window_Receive=function(data){console.log(this.receive);if(this.receive!=null)this.receive(data);}
}
//基于web ocx
var webui=function(id,parent){
	Element.call(this)
	if(id!=null)this.ID(id);
	if(parent!=null)this.Parent(parent);
	else this.Parent(document.body);
	this.Resize=function(w,h){return this;}
}
webui.Grid=function(id,value){
	webui.call(this,id);
	if (!(isJson(value))){value={"cols":1,"rows":1,"data":null,"fields":[]}}
	this.cols=value.cols;
	this.rows=value.rows;
	this.cellWidth=100;
	this.cellHeight=50;
	this.hasField=false;
	this.fields=[]
	this.collength=3
	this.Resize();self=this;
	this.sethasField=function(value){this.hasField=value;return this;}
	this.setField=function(value){this.rows=value.length;this.fields=value;return this;}
	this.makecell=function(i,data){
		r=self.CreatesubElement("div").className("col"+i.NDigits(this.collength))
		for(var j=0;j<self.rows;j++){
			o=r.CreatesubElement("div").className("row"+j.NDigits(this.collength)).ID("col"+i.NDigits(this.collength)+"row"+j.NDigits(this.collength))
			.css({"position":"inherit","display":"table-cell","vertical-align":"middle","text-align":"center"});
			if(this.hasField && i==0)o.addClass("up").hWnd.innerText=data[this.fields[j]];
			else if(this.fields[j]=="#")o.addClass("up").hWnd.innerText=i+1;
			else o.addClass("cellflat").css("background","#ffffff");
			if(this.fields[j] in data)o.hWnd.innerText=data[this.fields[j]];
		}
		return this
	}
	this.Init=function(){
		for(var i=0;i<this.cols;i++){
			r=this.CreatesubElement("div").className("col"+i.NDigits(this.collength))
			for(var j=0;j<this.rows;j++){
				o=r.CreatesubElement("div").className("row"+j.NDigits(this.collength))
				.css("position","inherit").css("display","inline-block");
				if(j==0)o.addClass("up");
				else o.addClass("cellflat").css("background","#ffffff");		
			}
		};
		return this;
	}
	this.Move=function(value){
		this.Position(value);
		this.Resize();
	}
	this.cells=function(row,col){return $$("#col"+col.NDigits(this.collength)+"row"+row.NDigits(this.collength))}
	this.Resize=function(){
		var w=this.Width(),h=this.Height();
		// console.log((this.cellWidth+2)*this.cols)
		for(var i=0;i<this.cols;i++){this.FindElement(".col"+i.NDigits(this.collength)).css({"height":this.cellHeight+"px"});}
		for(var i=0;i<this.rows;i++){this.FindElement(".row"+i.NDigits(this.collength)).css({"width":this.cellWidth+"px","height":this.cellHeight+"px"});}
		return this;
	}
	this.binddata=function(fields,data,reverse){
		console.log(data)
		value.fields=fields;value.data=data;
		if(reverse==null)reverse=false;
		this.fields=fields
		this.rows=fields.length;this.cols=data.length;this.Clear()
		if(reverse){for(var i=this.cols-1;i>=0;i--){this.makecell(i,value.data[i]);};}
		else{for(var i=0;i<this.cols;i++){this.makecell(i,value.data[i]);};}
		return this;
	}
	this.AddLineData=function(data){
		this.cols+=1;
		this.makecell(this.cols,value.data);
		return this;
	}
}
webui.Grid.Flex=function(id,value){

}
webui.mjpgStreamerPlay=function(url,options){
	var self=this;
	if(!options) {
		options = {};
		options.Parent=document.body;
		options.IntervalTime=200;
		options.Width=320;
		options.Height=240;
	}
	options.Url=url;
	options.isonload=false;
	options.t=null;
	options.status=false;
	if(!(canvas in options)){
		options.canvas=document.createElement("canvas");
		options.Parent.appendChild(options.canvas);
	}else if(typeof(options.canvas)=="string"){
		options.canvas=document.getElementById(options.canvas);
	}
	options.canvas.setAttribute("width",options.Width);
	options.canvas.setAttribute("height",options.Height);
	// options.canvas.setAttribute("class","mirrorRotateLevel");
	
	options.canvas.addEventListener("click", function() {if(options.status) {self.stop();} else {self.start();}}, false);
	options.img=new Image();
	options.img.setAttribute("class","mirrorRotateLevel");
	options.img.onerror=function(){console.log("img error");}
	this.addtime=function(){ options.hWnd.beginPath(); options.hWnd.fillStyle="white"; options.hWnd.font = '20px serif'; options.hWnd.fillText(new Date().toLocaleString(),20,options.Height-60); options.hWnd.closePath(); }
	this.setURL=function(url){options.img.src=url;options.img.onload=function(){options.hWnd.drawImage(options.img,0,0,options.Width,options.Height);}}
	this.load=function(url){options.hWnd=options.canvas.getContext("2d");this.setURL(url); }
	this.start=function(){
		console.log("start");options.status=true;this.setURL(url);
		options.t=window.setInterval(function(){
			options.hWnd.translate(options.hWnd.width, 0);
     		options.hWnd.scale(-1, 1);
			options.hWnd.drawImage(options.img,0-options.Width, 0,options.Width,options.Height);
			options.hWnd.translate(options.hWnd.width, 0);
     		options.hWnd.scale(-1, 1);
			self.addtime();},options.IntervalTime); }
	this.stop=function(){console.log("stop");options.status=false;clearInterval(options.t); options.t=null; }
	this.load(options.Url);
}
webui.Msgbox=function(e){
	webui.call(this,document.body)
	this.Eject=function(left,top,width,height){}
}
webui.webSocket=function(addr){
	window.webSockObject.call(this,addr)
}