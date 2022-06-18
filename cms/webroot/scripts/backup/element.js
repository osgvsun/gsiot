var Element = function (e) {
	var rotate = 0, rotatex = 0, rotatey = 0,txtItem=null,self=this
	if (e == null) this.hWnd = document.createElement("div");
	else if (typeof (e) == "string") { 
		key = e.substr(0, 1); 
		if (key == "#") this.hWnd=document.getElementById(e.substr(1)); 
		else this.hWnd=document.createElement(e);
	}
	else if (isHTMLElement(e)) this.hWnd = e; else if (isElement(e)) this.hWnd = e.hWnd;
	else if (isObject(e,PointerEvent)) this.hWnd=e.target||e.srcElement;
	if (this.hWnd != null) {
		this.Style = this.hWnd.style;
		this.tagName = this.hWnd.tagName.toLowerCase();
		this.attribute = function (item, value) { 
			if (value == null) return this.hWnd.getAttribute(item); 
			else if (isJson(item)) {
				for (var key in item){
					this.hWnd.setAttribute(key, item[key])}
				console.log(this.hWnd.getAttribute("width"))
			}
			else if(value=="")this.hWnd.removeAttribute(item); 
			else this.hWnd.setAttribute(item, value); 
			return this;
		}
		this.className = function (value) { if (value == null) { return this.hWnd.className; } else { this.hWnd.className = value.trim(); return this;} }
		this.addClass = function (value) { var data = this.className() == null ? [] : this.className().split(" "); if(data.indexOf(value)==-1) this.className(data.Add(value).join(" "));return this; }
		this.removeClass= function (value) { var data = this.className() == null ? [] : this.className().split(" "); data.splice(data.indexOf("live_select"),1);this.className(data.join(" ").trim()); return this; }
		this.CSS = function (item, value) {if (item in this.hWnd.style) { if (value == null) return this.hWnd.style[item]; else this.hWnd.style[item] = value; } else if (isJson(item)) { for (var key in item) this.hWnd.style[key] = item[key]; } return this;};
		this.Color=function(value){if(value==null)return this.CSS("color");else this.CSS("color",value);return this;}
		this.ID = function (value) { if (value == null) return this.hWnd.id; else {this.hWnd.id = value;return this;} }
		//this.guimode = function () { this.hWnd.style.position = "absolute"; }
		this.Hide = function () { this.Visible(false);return this; }
		this.Show = function () { this.Visible(true);return this; }
		this.Visible = function (value) { if (value != null) { if (value == true) { this.hWnd.style.display = "block"; } else { this.hWnd.style.display = "none"; } } else { if (this.hWnd.style.display = "block") return true; else return false; }; }
		this.Html = function (value) { if (value == null) return this.hWnd.innerHTML; else { this.hWnd.innerHTML = value; return this;} }
		this.Text = function (value) { if (value == null && txtItem==null) return this.hWnd.innerText;else if(value==null && txtItem!=null) return txtItem.Text();else if(txtItem==null) {txtItem=new Element.Item(this);txtItem.Text(value);}else txtItem.Text(value);return this;}
		this.Item=function(){return txtItem}
		this.Clear = function () { this.Html("");txtItem=null;return this;}
		this.Tmpl=function(strtmpl,data){if(strtmpl!=null && data==null){this.Html(strtmpl);}else if(strtmpl!=null && data!=null){this.Html(tmpl(strtmpl,data));}}
		//this.Rotate = function (value) { if (value == null) return rotate; else { rotate = value; this.hWnd.style.transform = 'rotate(' + value + 'deg) rotateX(' + rotatex + 'deg) rotateY(' + rotatey + 'deg)'; } };
		//this.RotateX = function (value) { if (value == null) return rotatex; else { rotatex = value; this.hWnd.style.transform = 'rotate(' + rotate + 'deg) rotateX(' + value + 'deg) rotateY(' + rotatey + 'deg)'; } };
		//this.RotateY = function (value) { if (value == null) return rotatey; else { rotatey = value; this.hWnd.style.transform = 'rotate(' + rotate + 'deg) rotateX(' + rotatex + 'deg) rotateY(' + value + 'deg)'; } };
		this.Left = function (value) { if (value == null) {if(this.hWnd.style.position=="") return this.hWnd.offsetLeft;else if(this.hWnd.style.left=="") return this.hWnd.offsetLeft;else return this.hWnd.style.left;}else if(this.hWnd.style.position=="") this.hWnd.offsetLeft = value;else if(this.hWnd.style.position=="absolute") this.hWnd.style.left=value+'px';else if(this.hWnd.style.position=="relative") this.hWnd.style.left=value+'px';return this };
		this.Top = function (value) { if (value == null) {if(this.hWnd.style.position=="") return this.hWnd.offsetTop; else if(this.hWnd.style.top=="") return this.hWnd.offsetTop;else return this.hWnd.style.top;}else if(this.hWnd.style.position=="") this.hWnd.offsetTop = value ;else if(this.hWnd.style.position=="absolute") this.hWnd.style.top=value+'px';else if(this.hWnd.style.position=="relative") this.hWnd.style.top=value+'px';return this };
		this.Width = function (value) { if (value == null) {if(this.hWnd.style.position=="") return this.hWnd.offsetWidth; else if(this.hWnd.style.position=="absolute") return parseInt(this.hWnd.style.width);else return this.hWnd.width;}else if(this.hWnd.style.position=="") this.hWnd.width = value;else if(this.hWnd.style.position=="absolute") this.hWnd.style.width=value+'px';	else if(this.hWnd.style.position=="relative") this.hWnd.style.width=value+'px';return this };
		this.Height = function (value) { if (value == null) {if(this.hWnd.style.position=="") return this.hWnd.offsetHeight; else if(this.hWnd.style.position=="absolute") return parseInt(this.hWnd.style.height);	else return this.hWnd.height;}else if(this.hWnd.style.position=="") this.hWnd.height = value;else if(this.hWnd.style.position=="absolute") this.hWnd.style.height=value+'px';else if(this.hWnd.style.position=="relative") this.hWnd.style.height=value+'px';return this };
		this.Position=function(value){if(value==null) return {"left":this.Left(),"top":this.Top(),"width":this.Width(),"height":this.Height()};else{if ("position" in value) this.hWnd.style.position = value.position;if ("left"     in value && value.left    !=null) this.Left(value.left); if ("top"      in value && value.top     !=null) this.Top(value.top); if ("width"    in value && value.width   !=null) this.Width(value.width); if ("height"   in value && value.height  !=null) this.Height(value.height); }return this;}
		this.Move = function (left, top, width, height) {this.Position({position:"absolute","left":left,"top":top,"width":width,"height":height});return this;};
		this.BackColor = function (value) { if (value == null) return this.hWnd.style.background; else this.hWnd.style.background = value; return this;};
		this.Click = function (fn) { 
			if (fn != null)  { this.fnclick = fn; this.BindEvent("click", fn);} 
			else if (this.fnclick != null) return this.fnclick(self); 
		}
		this.Error = function (fn) { if (fn != null)  { this.fnerror = fn; this.BindEvent("error", fn);} else if (this.fnclick != null) return this.fnerror(); }
		this.BindEvent = function (eventname, fn) { 
			var args=[];
			this.hWnd.addEventListener(eventname, fn) 
		}
		this.RemoveEvent = function (eventname, fn) { this.hWnd.removeEventListener(eventname, fn); if (eventname == "click") { this.fnclick = null; } else if (eventname == "error") { this.fnerror = null; } }
		this.Children = function (value) { if(value==null)return new Elements(this.hWnd.children);else return new Element(this.hWnd.children[value]) }
		this.FindElement=function(value){return $$(value,this.hWnd);}
		this.Parent = function (value) {
			if (value == null) return new Element(this.hWnd.parentNode);
			else { newparent = value;if (value instanceof Element) newparent = value.hWnd;
				if (newparent != this.hWnd.parentNode) {if (this.hWnd.parentNode != null) this.hWnd.parentNode.removeChild(this.hWnd);newparent.appendChild(this.hWnd);}return this;}}
		this.CreatesubElement = function (tagname) {if(tagname==null)tagname="div";var e=new Element(tagname);this.hWnd.appendChild(e.hWnd);return e; }
		if (this.tagName == "input") {
			if (this.attribute("type") == "radio" || this.attribute("type") == "checkbox") {
				this.checked = function (value) { if (value == null) return this.hWnd.checked; else this.hWnd.checked = value; return this;}
			}
			this.Val = function (value) { if (value == null) return this.hWnd.value; else this.hWnd.value = value;return this; };
			this.val = this.Val;
		}
		else if(["title", "button"].indexOf(this.tagName) != -1){
			this.Text=function(value){if(value==null)return this.hWnd.innerText;else this.hWnd.innerText=value;return this}
		}
		else if (["img", "script","video"].indexOf(this.tagName) != -1) {
			this.src = function (value) { return this.attribute("src", value) }
		}
		else if (["a", "script", "link"].indexOf(this.tagName) != -1) {
			this.href = function (value) { return this.attribute("href", value) }
		}
		else if (this.tagName == "table") {
			this.columnLength = function () { return this.hWnd.rows[0].cells.length }
			this.LineLength = function () { return this.hWnd.rows.length }
			this.AddLine = function (rowindex, column) { var row = this.hWnd.insertRow(rowindex); if (column == null) column = this.columnLength(); for (i = 0; i < column; i++) { row.insertCell(i) } }
			this.AppendLine = function () { this.AddLine(this.LineLength()) }
			this.AddFirstLine = function () { this.AddLine(0) }
			this.RemoveLine = function (index) { this.hWnd.deleteRow(index) }
			this.Text = function (r, c, value) { if (r != null && c != null) { if (value == null) return this.hWnd.rows[r].cells[c].innerHTML; else this.hWnd.rows[r].cells[c].innerHTML = value; } else return this.hWnd.innerText; }
			this.Cell = function (r, c) { return new Element(this.hWnd.rows[r].cells[c]) }
		}
		/*兼容jq的一些接口*/
		this.position=this.Position;this.html=this.Html;this.show = this.Show; this.hide = this.Hide; this.on = this.BindEvent; this.attr = this.attribute; this.css = this.CSS
		/*未实现的jq接口*/
		this.siblings = function () { }
	}
}
Element.Item=function(p){
	this.image=this.text=null;
	Element.call(this,"table");
	this.tr=this.CreatesubElement("tr");
	this.tr.CreatesubElement("td")
	.Parent().CreatesubElement("td")
	.Parent().CreatesubElement("td");
	this.td=this.tr.FindElement("td");
	this.td.Index(0).attr("width",5);
	this.td.Index(2).attr("width",5);

	this.attr("width","100%").attr("height","100%")
	if(p!=null)this.Parent(p.hWnd);
	this.TD=function(index){return this.td.Index(index);}
	this.align=function(value){
		if(value==null) return this.td.Index(1).attr("align");
		else this.td.Index(1).attr("align",value)
		return this;
	}
	this.valign=function(value){
		if(value==null) return this.td.Index(1).attr("valign");
		else this.td.Index(1).attr("valign",value)
		return this;
	}
	this.Show=function(){
		if(this.text!=null && this.image==null ){
			this.td.Index(1).Html(this.text)
			this.align("center").valign("middle")
		}
	}
	
	this.Text=function(value){if(value==null)return this.text;else{this.text=value;this.Show();}}
}
var Elements = function (e) {
	var es = [];
	if (isElement(e)) es.push(e);
	else if (isHTMLElement(e)) es.push(new Element(e));
	else if (isElements(e)) es = e.toArray();
	else if (isHTMLCollection(e)) { for (var o of e) { es.push(new Element(o)) } }
	else if (typeof (e) == "string") { document.querySelectorAll(e).forEach(function(o){es.push(new Element(o))})}
	this.Add=function(val){es.Add(val);return this};
	this.toArray = function () { return es; }
	this.size = function () { return es.length; }
	this.Index = function (index) { return es[index] }
	this.ForEach = function (fn) { for (var e of es) { fn(e) };return this;}
	this.show = function () { this.ForEach(function (node) { node.Show() });return this; }
	this.hide = function () { this.ForEach(function (node) { node.Hide() });return this; }
	this.on = function (name, fn) { this.ForEach(function (node) { node.BindEvent(name, fn) });return this; }
	this.attr = function (name, value) { this.ForEach(function (node) { node.attribute(name, value) });return this; }
	this.css = function (name, value) { this.ForEach(function (node) { node.CSS(name, value) });return this; }
	this.src = function (value) { this.ForEach(function (node) { node.src(value) });return this; }
	this.href = function (value) { this.ForEach(function (node) { node.href(value) });return this; }
	this.val = function (value) { this.ForEach(function (node) { node.val(value) });return this; }
	this.addClass = function (value) { this.ForEach(function (node) { node.addClass(value) });return this; }
	this.removeClass = function (value) { this.ForEach(function (node) { node.removeClass(value) });return this; }
}
var Document = document.head || document.getElementsByTagName("head")[0];
Document.Title = document.getElementsByTagName("title")[0] || (function () { t = document.createElement("title"); t.text = "未命名"; Document.appendChild(t); return t; })()
Document.Caption = function (value) { if (value == null) return Document.Title.text; else Document.Title.text = value; }
Document.LoadJscript = function (url, callback) { if (isLoadJS(url) == false) { var script = document.createElement('script'); var fn = callback || function () { }; script.type = 'text/javascript'; script.src = url; Document.appendChild(script); if (script.readyState) { script.onreadystatechange = function () { if (script.readyState == 'loaded' || script.readyState == 'complete') script.onreadystatechange = null; fn(url); } } else { script.onload = function () { fn(url) } } } else if (callback != null) callback(url); }
Document.LoadCSS = function (url) { if (isLoadCSS(url) == false) { var style = document.createElement("link"); style.rel = "stylesheet"; style.type = "text/css"; style.href = url; Document.appendChild(style); } };
Document.LoadJson = function (url) { result = "".LoadURL(url); if (result != "" && result.constructor == String) { return JSON.parse(result); }; if (result == "") return {}; if (isJson(result)) return result; };
Document.Width = function () { if (window.innerWidth) return window.innerWidth - 5; else if ((document.body) && (document.body.clientWidth)) return document.body.clientWidth - 5; };
Document.Height = function () { if (window.innerHeight) return window.innerHeight - 8; else if ((document.body) && (document.body.clientHeight)) return document.body.clientHeight - 8; };
Document.AddEvent = function (objElement, ename, lpfn) { if (objElement.addEventListener) { objElement.addEventListener(ename, lpfn, true); } else if (objElement.attachEvent) { objElement.attachEvent("on" + ename, lpfn, true); } };
Document.RemoveEvent = function (objElement, ename, lpfn) { if (objElement.removeEventListener) { objElement.removeEventListener(ename, lpfn); } else if (objElement.detachEvent) { objElement.detachEvent("on" + ename, lpfn); } };
Document.Path = function () { var ret = {}, url = window.location.href.replace("http://", "").replace("file:///", "").split("/"), host = url[0], find = url[0].indexOf(":"); if (find > 0) { ret.host = url[0].substr(0, find); ret.port = url[0].substr(find + 1); } else { ret.host = url[0]; ret.port = 80; }; var f = url.pop(); if (f.indexOf("?") != -1) { ret.file = f.split("?")[0]; param = f.split("?")[1].split("&"); ret.option = {}; for (i = 0; i < param.length; i++) { eval(("ret.option." + param[i] + "';").replace("=", "='")); } } return ret; }
Document.SystemTime = function (id) { window.setInterval(function () { $$("#" + id).Html(new Date().Format("hh:mm:ss")) }, 1000); }
Document.OnResize = function(value) {if (value != null) {window.AddEvent(window, "resize", value)}};
window.AddEvent = function(objElement, ename, lpfn) {
	if(objElement.addEventListener) {
		objElement.addEventListener(ename, lpfn, true);
	} else if(objElement.attachEvent) {
		objElement.attachEvent("on" + ename, lpfn, true);
	}
};
window.RemoveEvent = function(objElement, ename, lpfn) {
	if(objElement.removeEventListener) {
		objElement.removeEventListener(ename, lpfn);
	} else if(objElement.detachEvent) {
		objElement.detachEvent("on" + ename, lpfn);
	}
};
window.OS={};window.browAgent={};
window.OS.isWindows=/windows/.test(navigator.userAgent.toLocaleLowerCase());
window.OS.isIOS = /iphone|ipad|ipod/.test(navigator.userAgent.toLocaleLowerCase());
window.OS.isAndroid = /android/.test(navigator.userAgent.toLocaleLowerCase());
window.browAgent.isChrome=/chrome/.test(navigator.userAgent.toLocaleLowerCase());
window.browAgent.isFirefox=/firefox/.test(navigator.userAgent.toLocaleLowerCase());
window.browAgent.isEdg=/edg/.test(navigator.userAgent.toLocaleLowerCase())
window.getRequest=function(){
	if(window.XMLHttpRequest) return new XMLHttpRequest(); 
	else if(window.ActiveXObject) { return new ActiveXObject("Microsoft.XMLHTTP") };
}
window.online=navigator.OnLine;
window.$$ = function (selector,parent) { 
	if(parent==null)parent=document;
	if (typeof (selector) == "string") { 
		key = selector.substr(0, 1); 
		if (key == ".")return new Elements(parent.getElementsByClassName(selector.substr(1))); 
		else if (key == "#") return new Element(parent.getElementById(selector.substr(1))); 
		else return new Elements(parent.getElementsByTagName(selector)) } 
	else if (isHTMLElement(selector)) return new Element(selector); 
	else if (isObject(selector,PointerEvent)) return new Element(selector)
	else if (isHTMLCollection(selector)) return new Elements(selector);
}
window.createElement = function (tag) { var e = document.createElement(tag); document.body.appendChild(e); return new Element(e); };
window.tmpl = function (str, obj) { 
	var fn=null,data=str.replace(/[\r\t\n]/g, " ")
	.split("<%").join("\t")
	.replace(/((^|%>)[^\t]*)'/g, "$1\r")
	.replace(/\t=(.*?)%>/g, "',$1,'")
	.split("\t").join("');")
	.split("%>").join("p.push('")
	.split("\r")

	try{
		code="var p=[],print=function(){p.push.apply(p,arguments);};" + "with(obj){p.push('";
		code=code+data.join("\\'") + "');}return p.join('');";fn = new Function("obj", code);
	}catch(e){
		code="var p=[],print=function(){p.push.apply(p,arguments);};" + "with(obj){p.push('";
		code=code+data.join("\'") + "');}return p.join('');";fn = new Function("obj", code);
	}
	console.log(code)
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
		if (waittime != null) setTimeout(this.closemsg, waittime * 1000) }; 
	this.Show = function (msg) { if (msg == null) msg = this.txt; 
		console.log(msg); 
		this.body.Html("<table width='100%' height='100%'><tr><td align='center' valign='center'>" + msg.replace("\n", "<br>") + "</td></tr><tr><td align='center' valign='center' id='readcar_qrcode'</td><td align='center' valign='center' id='readcar_qrcode1'</td></tr></table>") 
	};
	this.Resize = function () { 
		this.backobj.Move(0, 0, Document.Width(), Document.Height()); 
		this.body.Move((Document.Width() - this.Width) / 2, (Document.Height() - this.Height) / 2, this.Width, this.topFormHeight); 
		this.butForm.Move((Document.Width() - this.Width) / 2, (Document.Height() - this.Height) / 2 + this.topFormHeight, this.Width, this.butFormHeight); }; 
	this.Show(); this.setTime(); this.Resize(); 
	System.AddEvent(window, "resize", this.Resize); 
}
window.newmsgbox = function (txt, time) { 
	var self = this; this.txt = txt; this.time = time; this.Width = 300; this.Height = 150; 
	this.topFormHeight =100 ; this.butFormHeight = 50; 

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
		if (waittime != null) setTimeout(this.closemsg, waittime * 1000) }; 

	this.Show = function (msg) { if (msg == null) msg = this.txt; 
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
window.isJson = function (obj) { return typeof (obj) == "object" && Object.prototype.toString.call(obj).toLowerCase() == "[object object]" && !obj.length; }
window.isLoadJS = function (url) { var flag = false; $$("script").toArray().ForEach(function (e) { if (e.src() == url) { flag = true; } }); return flag; }
window.isLoadCSS = function (url) { var flag = false; $$("link").toArray().ForEach(function (e) { if (e.href() == url) { flag = true; } }); return flag; }
window.isObject=function(e,obj){return obj.prototype.isPrototypeOf(e)}
window.isHTMLElement = function (e) { return isObject(e,HTMLElement) }
window.isHTMLCollection = function (e) { return isObject(e,HTMLCollection) }
window.isElement = function (e) { return isObject(e,Elements)}
window.isElements = function (e) { return isObject(e,Elements)}
window.eventHandler=function () { };
window.eventHandler.prototype = {
	registerEvent : function(element, eventType, handler) {
		if(element.attachEvent) { //2级DOM的事件处理
			element.attachEvent('on'+ eventType, handler);
		}else if (element.addEventListener) {
			element.addEventListener(eventType, handler, false);
		} else { //0级DOM的事件处理
			element['on'+ eventType] = handler;
		}
	},
	bind: function(obj, handler) {
		obj = obj || window;var args = [];
		for(var i =2; i < arguments.length; i++){args.push(arguments[i]);}
		return function() { handler.apply(obj, args) };
	}
}
window.Form = function (name, parent, stmpl, load, receive, resize) {
	this.binddata = this; this.tmpldata = null; this.dataurl = null; this.isshow = false; this.Form_Show = null; this.isload = false; this.Name = name; this.frm = this; this.parent = parent; this.tmpl = stmpl; this.data = {}; this.load = load; this.receive = receive; this.resize = resize;
	this.Show = function () { if (this.isload == false) { this.Form_Load() } if (this.tmpl != null && this.parent != null) { if (this.tmpldata == null) this.tmpldata = this.tmpl.LoadURL(); if (this.dataurl != null) this.binddata = this.dataurl.LoadJson(); this.parent.Html(tmpl(this.tmpldata, this.binddata));  } if (this.Form_Show != null) return this.Form_Show(); console.log(this.Name + "刷新完成"); return this;}
	this.Form_Load = function () { if (this.load != null) this.load(); this.isload = true; }
	this.Form_Resize = function (w, h) { if (this.resize != null) this.resize(w, h) }
	this.Form_Receive = function (data) { if (this.receive != null) this.receive(data); }
}
window.webSockObject = function (addr) {
	var webSockObj = this;
	webSockObj.isOpen = false;
	webSockObj.address = addr;
	webSockObj.route = {};
	webSockObj.event_open = null;webSockObj.event_close = null;webSockObj.event_receive = null;webSockObj.dev = null;webSockObj.id = null;webSockObj.t=0;
	webSockObj.SendMessage = function (value, obj, fn) {
		if (this.isOpen == true) {
			data = {};
			data.sour = this.address;
			data.datetime = new Date().Format("yyyy-MM-dd hh:mm:ss");
			data.cmd = value.cmd;
			data.result = value;
			console.log("send:" + JSON.stringify(data));
			if (fn != null) {
				if (value.type == undefined) { value.type = new Date().Format("yyyyMMddhhmmss"); }
				this.route[value.type] = {
					"fun": fn,
					"param": obj
				}
			}
			this.dev.send(JSON.stringify(data));
			//console.log(JSON.stringify(this.route))
		}
	};
	webSockObj.Connect = function (ip, port, fn_open, fn_close, fn_receive) {
		if (ip != null) webSockObj.ip = ip;
		if (port != null) webSockObj.port = port;
		if (fn_open != null) webSockObj.event_open = fn_open;
		if (fn_close != null) webSockObj.event_close = fn_close;
		if (fn_receive != null) webSockObj.event_receive = fn_receive;
		webSockObj.clientid = 0;
		webSockObj.dev = new WebSocket("ws://" + webSockObj.ip + ":" + webSockObj.port);
		webSockObj.dev.onopen = function () {
			if (webSockObj.event_open != null) webSockObj.event_open();
			if (webSockObj.t != 0) {
				clearInterval(webSockObj.t);
				self.t = 0;
			}
		};
		webSockObj.dev.onclose = function () {
			if (webSockObj.event_close != null) webSockObj.event_close();
			if (webSockObj.t == 0) {
				console.log("5 secs triggered");
				webSockObj.t = setInterval(webSockObj.Connect, 5000);
			}
		};
		webSockObj.dev.onmessage = function (evt) {
			console.log("recv:" + evt.data);
			var frame = JSON.parse(evt.data);
			var value = frame.result;
			value.id = frame.id;
			this.id = value.id;
			if (value.type in webSockObj.route) {
				webSockObj.route[value.type].fun(webSockObj.route[value.type].param, value);
				if (value.type.indexOf(".") == -1) {
					delete webSockObj.route[value.type]
				}
			} else webSockObj.event_receive(value);
		};
	};
}
window.JsonFile=function(filepath){
	this.url=this.api="/api/file/";this.approot="/api/getsystemfolder".LoadJson().rootpath;this.isEmpty=true;this.data=null;this.filepath=filepath.replace(this.api+"?pathfile=","")
	if(this.filepath.isChinese())this.url=this.api+this.filepath.base64encode();
	else if(filepath.indexOf(this.approot)!=-1) this.url=this.api+"?pathfile="+this.filepath;
	else this.url=this.filepath;this.request=getRequest();
	this.Write=function(data){
		if(this.url.indexOf(this.api)!=-1){
			this.request.open("post", this.url, false);
			this.request.setRequestHeader('content-type', 'application/json');
			if (typeof(data) == "string")this.request.send(data);
			else this.request.send(JSON.stringify(data));
			while(true) { if(this.request.readyState == 4) {console.log(this.request.status);break;} }
			if(this.request.status == 200){return true}
			else{return false}
		}
		return false;
	}
	this.Readfile=function(){this.data=(this.url).LoadJson();for(var x in this.data){this.isEmpty=false};return this.data;}
	this.Savefile=function(){return this.Write(this.data);}
	this.Readfile();
}
window.requestAnimFrame = (function () {
	return window.requestAnimationFrame ||
		window.webkitRequestAnimationFrame ||
		window.mozRequestAnimationFrame ||
		function (callback) {
			window.setTimeout(callback, 1000 / 60);
		};
})();
window.mjpgStreamerPlay=function(url,options){

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
	if(!("canvas" in options)){
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
	this.addtime=function(){ options.hWnd.beginPath(); options.hWnd.fillStyle="white"; options.hWnd.font = '20px serif'; options.hWnd.fillText(new Date().Format("yyyy-MM-dd hh:mm:ss"),20,options.Height-60); options.hWnd.closePath(); }
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
window.import=function(){}
window.require=function(){}
Element.treeview=function(){};
Document.Paths=(function(url){var ret={};ret.data=url;protocol=ret.data.split("//");ret.protocol=protocol[0];ret.url=protocol[1];if(ret.protocol=="file")ret.url=protocol[1].Right(protocol[1].length-1);servers=ret.url.split("/",1)[0];if(servers.indexOf(":")==-1){ret.server=servers;ret.port=80;}else {ret.server=servers.split(":")[0];ret.port=parseInt(servers.split(":")[1]);}param=ret.url.split("?")[1];ret.url=ret.url.replace(ret.server,"").replace(":"+ret.port,"");if(param!=null){ret.url=ret.url.replace("?"+param,"");ret.param={};param.split("&").ForEach(function(item){key=item.split("=")[0],value=null;if(item.indexOf("=")!=-1)value=item.split("=")[1];if(!(key in ret.param))ret.param[key]=value;else if(Array.prototype.isPrototypeOf(ret.param[key])){ret.param[key].Add(value)}else {tmp=ret.param[key];ret.param[key]=new Array();ret.param[key].Add(tmp);ret.param[key].Add(value)}})}return ret;})(window.location.href);
