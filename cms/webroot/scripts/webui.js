/*
	模块:element.js
	用途:使用OOP对页面容器的操作
	日期:2022-01-19
	作者:李品勇(lipy.sh@qq.com)
 */
window.OS = {
	isWindows: /windows/.test(navigator.userAgent.toLocaleLowerCase()),
	isIOS: /iphone|ipad|ipod/.test(navigator.userAgent.toLocaleLowerCase()),
	isAndroid: /android/.test(navigator.userAgent.toLocaleLowerCase())
};
window.browAgent = {
	isChrome: /chrome/.test(navigator.userAgent.toLocaleLowerCase()),
	isFirefox: /firefox/.test(navigator.userAgent.toLocaleLowerCase()),
	isEdg: /edg/.test(navigator.userAgent.toLocaleLowerCase())
};
window.AddEvent = function (objElement, ename, lpfn) {
	if (objElement.addEventListener) {
		objElement.addEventListener(ename, lpfn, true);
	} else if (objElement.attachEvent) {
		objElement.attachEvent("on" + ename, lpfn, true);
	}
};
window.RemoveEvent = function (objElement, ename, lpfn) {
	if (objElement.removeEventListener) {
		objElement.removeEventListener(ename, lpfn);
	} else if (objElement.detachEvent) {
		objElement.detachEvent("on" + ename, lpfn);
	}
};
window.getRequest = function () {
	if (window.XMLHttpRequest) return new XMLHttpRequest();
	else if (window.ActiveXObject) { return new ActiveXObject("Microsoft.XMLHTTP") };
}
window.online = navigator.onLine;
window.$$ = function (selector, parent) {
	if (parent == null) parent = document;
	if (typeof (selector) == "function") { selector() }
	else if (typeof (selector) == "string") {
		key = selector.substr(0, 1);
		if (key == ".") return parent.getElementsByClassName(selector.substr(1));
		else if (key == "#") return parent.getElementById(selector.substr(1));
		else if (key == "@") return parent.getElementsByName(selector.substr(1));
		else if (selector == "body") return document.body;
		else return parent.getElementsByTagName(selector)
	}
	else if (isHTMLElement(selector)) return selector;
	else if (isHTMLCollection(selector)) return selector;

}
window.tmpl = function (str, obj) { 
	// console.log(JSON.parse(obj));
	data=str.replace(/[\r\t\n]/g, " ")
	.split("<%").join("\t")
	.replace(/((^|%>)[^\t]*)'/g, "$1\r")
	.replace(/\t=(.*?)%>/g, "',$1,'")
	.split("\t").join("');")
	.split("%>").join("p.push('")
	.split("\r")

	try{
		code="var p=[],print=function(){p.push.apply(p,arguments);};" + "console.log(obj);with(obj){p.push('";
		code=code+data.join("\\'") + "');}return p.join('');";console.log(code);
		fn = new Function("obj", code);
	}catch(e){
		code="var p=[],print=function(){p.push.apply(p,arguments);};" + "with(obj){p.push('";
		code=code+data.join("\'") + "');}return p.join('');";console.log(code);
		fn = new Function("obj", code);
	}

	return fn(obj); 
};
window.msgbox = function (txt, time) {
	var self = this; this.txt = txt; this.time = time; this.Width = 300; this.Height = 150;
	this.topFormHeight = 100; this.butFormHeight = 50;
	this.backobj = createElement("div");
	this.backobj.Style.background = "rgba(0,0,0,.5)";
	this.body = createElement("div");
	this.body.Parent(this.backobj);
	this.body.BackColor("#d7d7d7");
	this.butForm = createElement("div");
	this.butForm.Parent(this.backobj);
	this.butForm.BackColor("#c3c3c3");
	this.closemsg = function () { document.body.removeChild(self.backobj.hWnd) };
	this.setTime = function (waittime) {
		if (waittime == null) waittime = this.time;
		if (waittime != null) setTimeout(this.closemsg, waittime * 1000)
	};
	this.Show = function (msg) {
		if (msg == null) msg = this.txt;
		console.log(msg);
		this.body.Html("<table width='100%' height='100%'><tr><td align='center' valign='center'>" + msg.replace("\n", "<br>") + "</td></tr><tr><td align='center' valign='center' id='readcar_qrcode'</td><td align='center' valign='center' id='readcar_qrcode1'</td></tr></table>")
	};
	this.Resize = function () {
		this.backobj.Move(0, 0, Document.Width(), Document.Height());
		this.body.Move((Document.Width() - this.Width) / 2, (Document.Height() - this.Height) / 2, this.Width, this.topFormHeight);
		this.butForm.Move((Document.Width() - this.Width) / 2, (Document.Height() - this.Height) / 2 + this.topFormHeight, this.Width, this.butFormHeight);
	};
	this.Show(); this.setTime(); this.Resize();
	System.AddEvent(window, "resize", this.Resize);
}
window.newmsgbox = function (txt, time) {
	var self = this; this.txt = txt; this.time = time; this.Width = 300; this.Height = 150;
	this.topFormHeight = 100; this.butFormHeight = 50;

	this.backobj = createElement("div");
	this.backobj.Style.background = "rgba(78,127,206,1.000)";
	//设置id
	this.backobj.ID('entirback');

	this.body = createElement("div");
	this.body.Parent(this.backobj);
	this.body.BackColor("#b3d3ea");

	this.closemsg = function () { document.body.removeChild(self.backobj.hWnd) };

	this.setTime = function (waittime) {
		if (waittime == null) waittime = this.time;
		if (waittime != null) setTimeout(this.closemsg, waittime * 1000)
	};

	this.Show = function (msg) {
		if (msg == null) msg = this.txt;
		console.log(msg);
		this.body.Html("<table id='orderid' width='100%' height='100%'><tr id='orderid'><td id='orderid' align='center' valign='center'>" +
			msg.replace("\n", "<br>") + "</td></tr><tr><td align='center' valign='center' id='readcar_qrcode'</td><td align='center' valign='center' id='readcar_qrcode1'</td></tr></table>")
	};

	this.Resize = function () {
		this.body.Move((Document.Width() - this.Width) / 2, 150, this.Width, this.topFormHeight);
		this.backobj.Move(0, 0, Document.Width(), Document.Height());
		this.body.Move((Document.Width() - this.Width) / 2, 150, this.Width, this.topFormHeight);
	};
	this.Show(); this.setTime(); this.Resize();
	System.AddEvent(window, "resize", this.Resize);
}
window.webFile = function (filepath,header) {
	this.url = filepath; this.isEmpty = true; this.data = null; this.request = getRequest();this.header=header;
	this.Write = function (data) {
		this.request.open("post", this.url, false);
		this.request.setRequestHeader('content-type', 'application/json');
		if(header){for(key in header){this.request.setRequestHeader(key,header[key]);}}
		if (typeof (data) == "string") filedata = { type: "file", data: data };
		else r = { type: "file", data: JSON.stringify(data) };
		console.log(JSON.stringify(filedata));
		this.request.send( JSON.stringify(filedata));
		if (this.request.status == 200) { return true }
		else { return false }
	}
	this.Read = function () { return this.data==null?"":this.data}
	this.Readfile = function () {
		if(this.url!=""&&this.url!=null){
			result = this.url.LoadJson();
			if (result.code == 200) {
				this.data = result.result.data; this.isEmpty = false;
			}
			else if (result.code == 500) { this.data = ""; this.isEmpty = true; }
		}
	}
	this.Savefile = function (data) { if(data)this.data=data;return this.Write(this.data); }
	this.Readfile();
}
window.markDownBrowser=function(e,f){
	var file=isObject(f,webFile)?f:new webFile(f);
	return {
		file:file,parent:e,
		Parse:function(){
			code=file.Read();
			this.parent.html(marked?marked.parse(code):"");
		}
	}
}
window.TreeView=function(e,json){
	this.parent=e;this.uid=null;this.data=json;
	this.Loading=function(e){};
	this.NodeDblClick=function(e){}
	this.Show=function(json){}
}