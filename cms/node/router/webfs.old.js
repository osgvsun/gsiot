var express = require('express')
var jwt = require("jsonwebtoken");
var request = require("request");
var fs = require('fs');
var path = require('path');
var url = require('url');
// var confDb = require('../db')

var isJson = function (obj) { return typeof (obj) == "object" && Object.prototype.toString.call(obj).toLowerCase() == "[object object]" && !obj.length; }
var webLocalFolder=function(path){
    /*
        path参数代表根目录，当前从根目录开始计算，没有根目录则默认是/,当前目录不支持删除，只能从之下
        建立起来的目录系统中，多了两个文件类型分别是lnk和ulnk
        - lnk是本地的文件目录链接
        - ulnk则是外链
        这两类文件都是使用json格式的载体内容，该两文件类型包含了权限定义，不包含监控
    */
    this.watch=this.parent=this.path=this.list=null;this.isEmpty=true;
    this.bind(path);
    this.bind=function(path){
        if(path){this.path=path;this.stats = fs.statSync(this.path);this.watch=fs.watch(this.path);}
    }
    // this.monitor=function(){
    //     if(!this.watch)this.watch=fs.watch(this.path);

    // };
    // this.subFSList=function(){
    //     if(this.stats && this.stats.isDirectory()){

    //     }
    // };
    // this.rename=function(newname){fs.renameSync(this.path,newname);this.path=newname}
    // this.delete=function(){fs.rmdirSync(this.path)}
    // this.mkdir=function(){}
}
var webLocalFile=function(file){

}
var webRedisFolder=function(path){

}
var router = function (app) {
    var ctrl = require('./control.js')
    var control = new ctrl(app)
    var webroot="/home/pi/codes/gsiot/cms/webroot"
    
    // var rootpath="/"
    //读文件或列目录
    control.get('/webfs/(*)', function(req, res) {
        path=(webroot+"/"+req.params[0]).replace("//","/");
        console.log(req.url)
        fs.stat(path,function(err,stats){
            if(err){res.send({code:500,msg:err})}
            else if(stats.isFile()){
                res.send({code:200,result:{file:path,data:fs.readFileSync(path, "utf-8")}})                
            }
            else if(stats.isDirectory()){
                path=(path+"/").replace("//","/");
                splitpath="/webfs"+path.replace(webroot,"");
                sublist=splitpath+fs.readdirSync(path).join(","+splitpath);
                res.send({code:200,result:{webroot:webroot,folder:path,list:sublist.split(",")}})
            }else{res.send({code:200,result:path})}
        })
    });
    // 写文件
    control.post('/webfs/(*)', function(req, res) {
        path=(webroot+"/"+req.params[0]).replace("//","/");
        console.log(req.params)
        fs.stat(path,function(err,stats){
            if(err){
                //文件不存在，新建
                if(req.body.type=="file"){
                    if (typeof (req.body.data) == "string") filedata=req.body.data;
                    else if(isJson(req.body.data)) filedata=JSON.stringify(req.body.data,null, 4);
                    fs.writeFileSync(path,filedata);   
                    res.send({code:200,method:"post",file:"/webfs/"+req.params[0]})  
                }else{
                    res.send({code:500,msg:err})}
                }
            else if(stats.isFile()){
                if (typeof (req.body.data) == "string") filedata=req.body.data;
		        else if(isJson(req.body.data))filedata=JSON.stringify(req.body.data,null, 4);
                fs.writeFileSync(path,filedata); 
                res.send({code:200,method:"post",file:"/webfs/"+req.params[0]})        
            }
            else{res.send({code:200,result:path})}
        })
        
    });
}

module.exports = router