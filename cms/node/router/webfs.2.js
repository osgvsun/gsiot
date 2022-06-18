//创建一个路由就要先实例化express下创建路由的方法
const express=require('express');
var child = require('child_process');
const router=express.Router();//注意这里的router是方法，需要括号
const jwt = require("jsonwebtoken");
const request = require("request");
var requestSync = require('sync-request');
const fs = require('fs');
const paths = require('path');
const url = require('url');
const config=require("../config.js")
let webroot=config.webfs.webroot;
let exts=['.lnk','.ulnk']
let ulinkPath=[]
child.exec('find '+config.webfs.webroot+' -name conn.ulnk', function(err, sto) {sto.split("\n").forEach(function(item){if(item!="")ulinkPath.Add(paths.dirname(item));});/*console.log(ulinkPath);*/})
var httpClient=function(url,header,params){
    var options = {};if(header)options.headers=header;if(params)options.form=params;
    // console.log(url,header)
    return requestSync('GET',url,options).getBody('utf-8').toString();
}
var listpath=function(path,baseurl){
    var subfile=[],subfolder=[];
    path=(path+"/").replace("//","/");
    splitpath=baseurl+path.replace(webroot,"");
    fs.readdirSync(path).forEach((name,index)=>{
        var ext=fs.statSync(path+name).isFile()?(paths.extname(name)==""?"file":paths.extname(name)):"dir";
        data={name:splitpath+name,ext:ext};
        if(ext=="dir"){
            data.name+="/"
            subfolder.Add(data)
        }else{
            data.access=(path.replace(webroot,"")+name)
            if(ext==".md"){
                data.edit="/edit/markdown/edit.html?file="+splitpath+name;
                data.show="/edit/markdown/show.html?file="+splitpath+name;
            }else if([".txt",".log",".json",".html",".htm",".js",".css"]){
                data.edit="/edit/notepad.html?file="+splitpath+name;
            }
            subfile.Add(data);
        }
    })
    return {code:200,result:{webroot:webroot,folder:path,subfolder:subfolder,subfile:subfile}}
}
router.get('(*)', (req, res) =>{
    let path=webroot+req.params[0]
    let stats=err=connFile=resData=rURL=null;
    let ext=paths.extname(path)
    // console.log(path)
    if(fs.existsSync(path)){
        stats=fs.statSync(path)
        // console.log(path,stats.isDirectory())
        if(stats.isFile()){resData={code:200,result:{file:path,data:fs.readFileSync(path, "utf-8")}}}
        else if(stats.isDirectory()){resData=listpath(path,"/webfs")}
    }else{
        //查找当前目录下有conn.ulnk,如果没有则查找已有的列表中是否有匹配的
        if(fs.existsSync(paths.dirname(path)+"/conn.ulnk")==0){
            ulinkPath.reverse().ForEach((item,index)=>{
                if(paths.dirname(path).indexOf(item)!=-1){
                    if(!connFile){
                        connFile=item+"/conn.ulnk";rURL=path.replace(item,"")
                        return true; //中断
                    }
                }
            })
        }else connFile=paths.dirname(path)+"/conn.ulnk";
        if(connFile!=null){
            conndata=JSON.parse(fs.readFileSync(connFile, "utf-8"));
            if("httpconntion" in conndata){    
                curl=conndata.httpconntion+rURL
                upam=""
                if(req.query!={}){for(key in req.query){upam+=key+"="+encodeURI(req.query[key])+"&"}}
                if(upam,upam!="")curl+="?"+upam
                
                resData=httpClient(curl,conndata.header);
            }else if("lnk" in conndata){
                // console.log(path)
                // console.log((conndata.lnk+rURL).replace("//","/"))
                resData=listpath(rURL)

            }
        }
        else resData={code:500,msg:"文件不存在"}
    }
    if(resData)res.send(resData)
});
router.post('(*)', (req, res)=> {
    let path=webroot+req.params[0]
    let stats=err=connFile=resData=null;
    let ext=paths.extname(path)
    if(fs.existsSync(path)){
        stats=fs.statSync(path)
        if(stats.isFile()){
        }else if(stats.isDirectory()){
        }
    }else{
    }
    if(resData)res.send(resData)
});
//路由写完了，现在可以把该数据库返回到操作层了
module.exports=router;