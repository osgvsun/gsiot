/*
    模块:element.js
    用途:从函数编程角度定义对标签的操作
    日期:2022-01-19
    作者:李品勇(lipy.sh@qq.com)
*/

HTMLCollection.prototype.forEach=function(fn){for(var i=0;i<this.length;i++){if(fn(this[i],i)==false)break;}}
//基本操作接口，操作item、attributes和style
HTMLElement.prototype.item=HTMLCollection.prototype.item=function(item,value){
    var self=this;
    return ("length" in this?
        (function(){
            return value==null?
                (function(){
                    data=[];
                    self.forEach(function(e){data.Add(e.item(item))});
                    return (data.length==1?data[0]:data)
                })():
                (function(){
                    self.forEach(function(e){e.item(item,value)});return self;
                })();
        })():
        (function(){
            if((item in self) && ["string","number","boolean"].indexOf(typeof(self[item]))==0){
                if (value == null)return self[item];
                else self[item]=value;return self;
            }else if (isJson(item)){for(var key in item){self.item(key, item[key])}}
        })()
    )
}
HTMLElement.prototype.attr=HTMLCollection.prototype.attr=function(item,value){
    var self=this;
    return ("length" in this?
        (function(){
            return value==null?
                (function(){
                    data=[];
                    self.forEach(function(e){data.Add(e.attr(item))});
                    return (data.length==1?data[0]:data)
                })():
                (function(){
                    self.forEach(function(e){e.attr(item,value)});return self;
                })();
        })():
        (function(){
            if (value == null){if(item in self)return self[item];else return self.getAttribute(item);}
            else if (value=="")self.removeAttribute(item);
            else if (isJson(item)){for(var key in item){self.attr(key, item[key])}}
            else{if(item in self)self[item]=value;else self.setAttribute(item, value);} return self;
        })()
    )
}
HTMLElement.prototype.css=HTMLCollection.prototype.css=function(item,value){
    var self=this;
    if (item in self.style) { 
        return ("length" in self?
            (function(){
                return value==null?
                    (function(){
                        data=[];
                        self.forEach(function(e){data.Add(e.css(item))});
                        return (data.length==1?data[0]:data)
                    })():
                    (function(){
                        self.forEach(function(e){e.attr(item,value)});return self;
                    })();
            })():
            (function(){
                if (value == null)return self.style[item];
                else if (isJson(item)){for(var key in item){self.attr(key, item[key])}}
                else self.style[item]=value;return self;
            })()
        )
    };return self;
}
// HTMLElement.prototype.getElement=HTMLCollection.prototype.getElement=function(item){var self=this;return ("length" in this?(function(){})():(function(){})())}
HTMLElement.prototype.On=function (ename, lpfn) {if (this.addEventListener) {this.addEventListener(ename, lpfn, true);}else if (this.attachEvent) {this.attachEvent("on" + ename, lpfn, true);}return this;};
HTMLElement.prototype.addClass=HTMLCollection.prototype.addClass=function (value) {var data = this.attr("class") == null?[]:this.attr("class"); if(data.indexOf(value)==-1) this.attr("class",data.Add(value).join(" "));return this}
HTMLElement.prototype.removeClass=HTMLCollection.prototype.removeClass= function (value) {var data = this.attr("class") == null ? [] : this.className().split(" "); this.attr("class",data.Remove(value).join(" ").trim());return this}
HTMLElement.prototype.text=HTMLCollection.prototype.text=function(value){return this.item("innerText",value)}
HTMLElement.prototype.html=HTMLCollection.prototype.html=function(value){return this.item("innerHTML",value)}
HTMLElement.prototype.val=HTMLCollection.prototype.val=function(value){return this.attr("value",value)}
HTMLElement.prototype.show=HTMLCollection.prototype.show=function(){return this.css("display","block")}
HTMLElement.prototype.hide=HTMLCollection.prototype.hide=function(){return this.css("display","none")}
HTMLElement.prototype.color=HTMLCollection.prototype.color=function(value){return this.css("color",value)}
HTMLElement.prototype.append=HTMLCollection.prototype.append=function(html){var self=this;result=self.html();if(typeof(result)=="string"){self.html(result+html);}}
HTMLElement.prototype.Add=function(tagName){var self=this,node=document.createElement(tagName);self.appendChild(node);return node}
"AfterPrint,BeforepPrint,BeforeLoad,Blur,Error,Focus,HashChange".split(",").forEach((item)=>{HTMLElement.prototype[item]=HTMLCollection.prototype[item]=function(fn){"length" in this?(this.forEach(function(e){e.On(item.toLowerCase(), fn)})):this.On(item.toLowerCase(), fn);return this;}});
"Load,Message,Offline,Line,PageHide,PageShow,PopState,Redew,Resize,Storage,UNDew,UNLoad".split(",").forEach((item)=>{HTMLElement.prototype[item]=HTMLCollection.prototype[item]=function(fn){"length" in this?(this.forEach(function(e){e.On(item.toLowerCase(), fn)})):this.On(item.toLowerCase(), fn);return this;}});
"Change,ContextMenu,FormChange,FormInput,Input,Invalid,Reset,Select,Submit".split(",").forEach((item)=>{HTMLElement.prototype[item]=HTMLCollection.prototype[item]=function(fn){"length" in this?(this.forEach(function(e){e.On(item.toLowerCase(), fn)})):this.On(item.toLowerCase(), fn);return this;}});
"KeyDown,KeyUP,KeyPress".split(",").forEach((item)=>{HTMLElement.prototype[item]=HTMLCollection.prototype[item]=function(fn){"length" in this?(this.forEach(function(e){e.On(item.toLowerCase(), fn)})):this.On(item.toLowerCase(), fn);return this;}});
"Click,DblClick,Drag,Dragend,DragEnter,DragLeave,DragOver,DragStart,Drop,MouseDown,MouseMove,MouseOut,MouseOver,MouseUP,MouseWheel,Scroll".split(",").forEach((item)=>{HTMLElement.prototype[item]=HTMLCollection.prototype[item]=function(fn){"length" in this?(this.forEach(function(e){e.On(item.toLowerCase(), fn)})):this.On(item.toLowerCase(), fn);return this;}});
"Abort,CanPlay,CanPlayThrough,DuratiChange,Emptied,Ended,LoadEdData,LoadEdmetaData".split(",").forEach((item)=>{HTMLElement.prototype[item]=HTMLCollection.prototype[item]=function(fn){"length" in this?(this.forEach(function(e){e.On(item.toLowerCase(), fn)})):this.On(item.toLowerCase(), fn);return this;}});
"LoadStart,Pause,Play,Playing,Progress".split(",").forEach((item)=>{HTMLElement.prototype[item]=HTMLCollection.prototype[item]=function(fn){"length" in this?(this.forEach(function(e){e.On(item.toLowerCase(), fn)})):this.On(item.toLowerCase(), fn);return this;}});
"RateChange,ReadyStateChang,Seekd,Seeking,Stalled,Suspend,TimeUPdate,VolumeChange,Waiting".split(",").forEach((item)=>{HTMLElement.prototype[item]=HTMLCollection.prototype[item]=function(fn){"length" in this?(this.forEach(function(e){e.On(item.toLowerCase(), fn)})):this.On(item.toLowerCase(), fn);return this;}});
HTMLElement.prototype.tmpl = function (str, obj) { 
	data=str.replace(/[\r\t\n]/g, " ")
	.split("<%").join("\t")
	.replace(/((^|%>)[^\t]*)'/g, "$1\r")
	.replace(/\t=(.*?)%>/g, "',$1,'")
	.split("\t").join("');")
	.split("%>").join("p.push('")
	.split("\r");
	try{
		code="var p=[],print=function(){p.push.apply(p,arguments);};" + "with(obj){p.push('";
		code=code+data.join("\\'") + "');}return p.join('');";console.log(code);
		fn = new Function("obj", code);
	}catch(e){
		code="var p=[],print=function(){p.push.apply(p,arguments);};" + "with(obj){p.push('";
		code=code+data.join("\'") + "');}return p.join('');";console.log(code);
		fn = new Function("obj", code);
	}
    result=fn(obj);this.html(result);return result; 
};
HTMLElement.prototype.markDownBrowser=function(f){
	var file=isObject(f,webFile)?f:new webFile(f);
	return {
		file:file,parent:this,
		Parse:function(){
			code=file.Read();
			this.parent.html(marked?marked.parse(code):"");
		}
	}
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
Document.Path = function () {return new URL(window.location.href)}    
Document.SystemTime = function (id) { window.setInterval(function () { $$("#" + id).html(new Date().Format("hh:mm:ss")) }, 1000); }
Document.OnResize = function(value) {if (value != null) {window.AddEvent(window, "resize", value)}};