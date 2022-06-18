/*
    模块:data.js
    用途:改造现有对象使其满足使用要求
    日期:2022-01-19
    作者:李品勇(lipy.sh@qq.com)
*/
Array.prototype.Add = function(value) {this.push(value);return this;};
Array.prototype.Del = function(n) {if(n < 0) return this;else return this.slice(0, n).concat(this.slice(n + 1, this.length));}
Array.prototype.Remove = function(val) {return this.Del(this.indexOf(val))};
Date.prototype.Format = function (fmt) { var o = { "M+": this.getMonth() + 1, "d+": this.getDate(), "h+": this.getHours(), "m+": this.getMinutes(), "s+": this.getSeconds(), "q+": Math.floor((this.getMonth() + 3) / 3), "S": this.getMilliseconds() }; if (/(y+)/.test(fmt)){fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));} for (var k in o){ 　　　　if (new RegExp("(" + k + ")").test(fmt)){ 　　　　　　fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));}} return fmt; };
String.prototype.LoadURL = function(url) { 
    var request; if(url == null) url = this; 
    if(window.XMLHttpRequest) request = new XMLHttpRequest(); 
    else if(window.ActiveXObject) { request = new ActiveXObject("Microsoft.XMLHTTP") }; 
    request.open("get", url, false); request.send(null); 
    while(true) { 
        if(request.readyState == 4) break; }; 
        if(request.status == 200) { 
            type = request.getResponseHeader("Content-Type"); 
            if(type.indexOf("application/json")!=-1) return JSON.parse(request.responseText); 
            return request.responseText; } 
        else return ""; 
    };
String.prototype.LoadURLfromDomain = function(url) { var request;if(url == null) url = this;if(url.indexOf("?")==-1)url=url+"?domain=g";else url=url+"&domain=gvsun"; if(window.XMLHttpRequest) request = new XMLHttpRequest();else if(window.ActiveXObject) request = new ActiveXObject("Microsoft.XMLHTTP"); request.open("get", url, false);request.send(null);while(true) {if(request.readyState == 4) break;}; if(request.status == 200) { type=request.getResponseHeader('Content-Type'); data=request.responseText;data=data.substr(2,data.length-3); if(type.indexOf("application/json")!=-1) return JSON.parse(data); return data; } else return ""; };
String.prototype.LoadJson = function(url) {if(url == null) url = this;__data__ = this.LoadURL(url);if(__data__.constructor == String){if(__data__=="")return {};else return JSON.parse(__data__);} else return __data__;}
String.prototype.base64encode=function(){_keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";_utf8_encode = function (string) {string = string.replace(/\r\n/g,"\n");var utftext = "";for (var n = 0; n < string.length; n++) {var c = string.charCodeAt(n);if (c < 128) {utftext += String.fromCharCode(c);} else if((c > 127) && (c < 2048)) {utftext += String.fromCharCode((c >> 6) | 192);utftext += String.fromCharCode((c & 63) | 128);} else {utftext += String.fromCharCode((c >> 12) | 224);utftext += String.fromCharCode(((c >> 6) & 63) | 128);utftext += String.fromCharCode((c & 63) | 128);}}return utftext;};var output = "";var chr1, chr2, chr3, enc1, enc2, enc3, enc4;var i = 0;input = _utf8_encode(this);while (i < input.length) {chr1 = input.charCodeAt(i++);chr2 = input.charCodeAt(i++);chr3 = input.charCodeAt(i++);enc1 = chr1 >> 2;enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);enc4 = chr3 & 63;if (isNaN(chr2)) {enc3 = enc4 = 64;} else if (isNaN(chr3)) {enc4 = 64;}output = output +_keyStr.charAt(enc1) + _keyStr.charAt(enc2) +_keyStr.charAt(enc3) + _keyStr.charAt(enc4);}return output;}
String.prototype.base64decode=function(){_keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";_utf8_decode = function (utftext) {var string = "";var i = 0;var c = c1 = c2 = 0;while ( i < utftext.length ) {c = utftext.charCodeAt(i);if (c < 128) {string += String.fromCharCode(c);i++;} else if((c > 191) && (c < 224)) {c2 = utftext.charCodeAt(i+1);string += String.fromCharCode(((c & 31) << 6) | (c2 & 63));i += 2;} else {c2 = utftext.charCodeAt(i+1);c3 = utftext.charCodeAt(i+2);string += String.fromCharCode(((c & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));i += 3;}}return string;};var output = "";var chr1, chr2, chr3;var enc1, enc2, enc3, enc4;var i = 0;input = this.replace(/[^A-Za-z0-9\+\/\=]/g, "");while (i < input.length) {enc1 = _keyStr.indexOf(input.charAt(i++));enc2 = _keyStr.indexOf(input.charAt(i++));enc3 = _keyStr.indexOf(input.charAt(i++));enc4 = _keyStr.indexOf(input.charAt(i++));chr1 = (enc1 << 2) | (enc2 >> 4);chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);chr3 = ((enc3 & 3) << 6) | enc4;output = output + String.fromCharCode(chr1);if (enc3 != 64) {output = output + String.fromCharCode(chr2);}if (enc4 != 64) {output = output + String.fromCharCode(chr3);}}return _utf8_decode(output);}
/* 基于标准base64编解码时容易产生字符串“/”，会和rest API冲突，所以将其替换成了字符“_”*/
String.prototype.b64encode=function(){_keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+_=";_utf8_encode = function (string) {string = string.replace(/\r\n/g,"\n");var utftext = "";for (var n = 0; n < string.length; n++) {var c = string.charCodeAt(n);if (c < 128) {utftext += String.fromCharCode(c);} else if((c > 127) && (c < 2048)) {utftext += String.fromCharCode((c >> 6) | 192);utftext += String.fromCharCode((c & 63) | 128);} else {utftext += String.fromCharCode((c >> 12) | 224);utftext += String.fromCharCode(((c >> 6) & 63) | 128);utftext += String.fromCharCode((c & 63) | 128);}}return utftext;};var output = "";var chr1, chr2, chr3, enc1, enc2, enc3, enc4;var i = 0;input = _utf8_encode(this);while (i < input.length) {chr1 = input.charCodeAt(i++);chr2 = input.charCodeAt(i++);chr3 = input.charCodeAt(i++);enc1 = chr1 >> 2;enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);enc4 = chr3 & 63;if (isNaN(chr2)) {enc3 = enc4 = 64;} else if (isNaN(chr3)) {enc4 = 64;}output = output +_keyStr.charAt(enc1) + _keyStr.charAt(enc2) +_keyStr.charAt(enc3) + _keyStr.charAt(enc4);}return output.replace("/","_");}
String.prototype.b64decode=function(){_keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+_=";_utf8_decode = function (utftext) {var string = "";var i = 0;var c = c1 = c2 = 0;while ( i < utftext.length ) {c = utftext.charCodeAt(i);if (c < 128) {string += String.fromCharCode(c);i++;} else if((c > 191) && (c < 224)) {c2 = utftext.charCodeAt(i+1);string += String.fromCharCode(((c & 31) << 6) | (c2 & 63));i += 2;} else {c2 = utftext.charCodeAt(i+1);c3 = utftext.charCodeAt(i+2);string += String.fromCharCode(((c & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));i += 3;}}return string;};var output = "";var chr1, chr2, chr3;var enc1, enc2, enc3, enc4;var i = 0;input = this.replace(/[^A-Za-z0-9\+\/\=]/g, "");while (i < input.length) {enc1 = _keyStr.indexOf(input.charAt(i++));enc2 = _keyStr.indexOf(input.charAt(i++));enc3 = _keyStr.indexOf(input.charAt(i++));enc4 = _keyStr.indexOf(input.charAt(i++));chr1 = (enc1 << 2) | (enc2 >> 4);chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);chr3 = ((enc3 & 3) << 6) | enc4;output = output + String.fromCharCode(chr1);if (enc3 != 64) {output = output + String.fromCharCode(chr2);}if (enc4 != 64) {output = output + String.fromCharCode(chr3);}}return _utf8_decode(output.replace("_","/"));}
String.prototype.Left=function(length){return this.substr(0,length)}
String.prototype.Right=function(length){return this.substr(this.length-length,length)}
String.prototype.ForEach=function(fn){for(i=0;i<this.length;i++){fn(this.substr(i,1))}}
String.prototype.rjust=function(length,char){return (Array(length-this.length+1).join(char || 0) + this).slice(-length-this.length)}
String.prototype.ljust=function(length,char){return (this+Array(length-this.length+1).join(char || 0)).slice(-length-this.length)}
String.prototype.isChinese=function(){return /.*[\u4e00-\u9fa5]+.*$/.test(this)}
Number.prototype.NDigits=function(length){var num=this;return num.toString().rjust(length)}
Number.prototype.twoDigits=function(){return this.NDigits(2)}
HTMLCollection.prototype.forEach=function(fn){for(var i=0;i<this.length;i++){if(fn(this[i],i)==false)break;}}
window.isArray=function (arr) {return Array.isArray(arr)}
window.isJson = function (obj) { return typeof (obj) == "object" && Object.prototype.toString.call(obj).toLowerCase() == "[object object]" && !obj.length; }
window.isLoadJS = function (url) { var flag = false; $$("script").toArray().ForEach(function (e) { if (e.src() == url) { flag = true; } }); return flag; }
window.isLoadCSS = function (url) { var flag = false; $$("link").toArray().ForEach(function (e) { if (e.href() == url) { flag = true; } }); return flag; }
window.isObject=function(e,obj){return (obj?obj:Object).prototype.isPrototypeOf(e)}
window.isHTMLElement = function (e) { return isObject(e,HTMLElement) }
window.isHTMLCollection = function (e) { return isObject(e,HTMLCollection)}
window.merge =function (target, ...arg) {
    return arg.reduce((acc, cur) => {
        return Object.keys(cur).reduce((subAcc, key) => {
            const srcVal = cur[key];
            if (isObject(srcVal)) {
                subAcc[key] = merge(subAcc[key] ? subAcc[key] : {}, srcVal);
                } else if (isArray(srcVal)) {
                // series: []，下层数组直接赋值
                subAcc[key] = srcVal.map((item, idx) => {
                    if (isObject(item)) {
                        const curAccVal = subAcc[key] ? subAcc[key] : [];
                        return merge(curAccVal[idx] ? curAccVal[idx] : {}, item);
                    } else {return item}
                })
            } else {subAcc[key] = srcVal}
            return subAcc
        }, acc)
    }, target)
}
